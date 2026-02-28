import argparse
import os
import sys
import time
import json
from pathlib import Path
from typing import Any, Dict, List, TypedDict
from datetime import datetime

import dotenv
import langgraph
from langgraph.graph import END, StateGraph
from rdflib import Graph

from src.models.requirement_models import CompetencyQuestion, Story
from src.prompts.prompt_manager import PromptManager
from src.reviewers.reviewer import OopsPitfallReviewer, RDFSyntaxReviewer
from src.reviewers.reasoner_validator import HermitReasonerValidator, PelletReasonerValidator
from src.utils.excel_processor import get_story_by_id
from src.utils.file_handler import load_existing_owl_files, save_text_file
from src.utils.llm_manager import call_llm
from src.utils.oops_parser import format_pitfalls_for_feedback, parse_oops_response
from src.utils.validation_logger import ValidationLogger
from src.utils.timing import format_duration

###########################################
########### Foundational Setup ############
###########################################

########### Load environment variables ###########
dotenv.load_dotenv()

########### LLM Configuration ###########
llm_type = "openai"


########### Prompt Manager Initialization ###########
prompt_manager = PromptManager(prompts_file_path=Path("src/prompts/prompts.yaml"))


########### Langgraph Workflow State ###########
class OntoAgentState(TypedDict, total=False):
    story_id: str
    story_object: Story
    unprocessed_cqs: List[CompetencyQuestion]
    processed_owls: List[Any]
    generated_owl: str
    combined_owl: str
    error_message: str
    is_valid: bool
    final_result: Any
    tool_calls: List[Any]
    current_cq: CompetencyQuestion
    current_owl: str
    current_validation: str
    validation_ok: bool
    combined_validation: Any
    combined_validation_ok: bool
    invalid_owl: str  # Added for error handling
    pitfall_feedback: str  # Formatted pitfall feedback for LLM
    retry_count: int  # Track correction attempts
    log_timestamp: str  # Shared timestamp for logs
    story_start_time: float  # Timing for benchmarking
    story_duration_seconds: float  # Total duration
    story_duration_formatted: str  # Formatted duration
    syntax_time_seconds: float  # Syntax validation timing
    oops_time_seconds: float  # OOPS validation timing


#############################
########### Nodes ###########
#############################


##### Node to load story object into state
def get_story_node(state: OntoAgentState) -> OntoAgentState:
    story_id = state.get("story_id", "")

    # Add timestamp and timing
    log_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    story_start_time = time.time()

    print(f"\n{'=' * 60}")
    print(f"Loading Story: {story_id}")
    print(f"Run Timestamp: {log_timestamp}")
    print(f"{'=' * 60}\n")

    story = get_story_by_id(story_id)
    cqs = (
        list(story.competency_questions) if story and story.competency_questions else []
    )
    return {
        **state,
        "story_object": story,
        "unprocessed_cqs": cqs,
        "processed_owls": [],
        "log_timestamp": log_timestamp,
        "story_start_time": story_start_time,
    }


##### Node to generate OWL code for each CQ
def generate_owl_node(state: OntoAgentState) -> OntoAgentState:
    error_message = state.get("error_message", "")
    invalid_owl = state.get("invalid_owl", "")
    unprocessed_cqs = state.get("unprocessed_cqs") or []
    story_object = state.get("story_object")
    if not unprocessed_cqs or not story_object:
        return {**state, "error_message": "No unprocessed CQs or story object."}
    print(f"Generating OWL for CQ ID: {unprocessed_cqs[0].id}")
    if error_message:
        print(f"Previous validation error: {error_message}")
        prompt = (
            prompt_manager.get_structured_prompt("otho_memless_cq_by_cq")[
                "task"
            ].format(story=story_object.context, CQ=unprocessed_cqs[0].question)
            + f"\n\nPrevious error: {error_message}\nInvalid OWL:\n{invalid_owl}\nPlease fix and regenerate."
        )
    else:
        prompt = prompt_manager.get_structured_prompt("otho_memless_cq_by_cq")[
            "task"
        ].format(story=story_object.context, CQ=unprocessed_cqs[0].question)
    llm_response = call_llm(llm_type, prompt)
    owl_code = getattr(llm_response, "text", llm_response)
    # Determine a unique filename to avoid overwriting
    story_id = state.get("story_id", "")
    base_path = f"data/output/{story_id}_{unprocessed_cqs[0].id}_pre_validation"
    ext = ".owl"
    file_path = base_path + ext
    counter = 2
    while os.path.exists(file_path):
        file_path = f"{base_path}_{counter}{ext}"
        counter += 1
    save_text_file(file_path, owl_code)
    return {
        **state,
        "current_cq": unprocessed_cqs[0],
        "current_owl": owl_code,
        "error_message": "",  # Clear error after new attempt
        "invalid_owl": "",
    }


##### Node to validate each OWL code produced and store(in State and Output files for auditing), if valid
def validate_and_store_owl_node(state: OntoAgentState) -> OntoAgentState:
    reviewer = RDFSyntaxReviewer()
    cq = state.get("current_cq")
    owl_code = state.get("current_owl") or ""
    if cq is None:
        print("No current CQ to validate.")
        return {
            **state,
            "current_validation": "No current CQ to validate.",
            "validation_ok": False,
        }
    print("Validating CQ ID:", cq.id)

    try:
        validation_result = reviewer.review_owl_content(owl_code)
        validation_successful = validation_result == "OK"
        if not validation_successful:
            # print("Validation error for", cq.id, ":", validation_result)
            return {
                **state,
                "current_validation": validation_result,
                "validation_ok": False,
                "error_message": validation_result,
                "invalid_owl": owl_code,
            }
        else:
            print("Validation successful: ", validation_successful)
            # Store OWL if valid
            story_id = state.get("story_id", "")
            processed_owls = (state.get("processed_owls") or []) + [(cq.id, owl_code)]
            print("Storing CQ ID:", cq.id)
            save_text_file(f"data/output/{story_id}_{cq.id}.owl", owl_code)
            unprocessed_cqs = (state.get("unprocessed_cqs") or [])[1:]
            return {
                **state,
                "current_validation": validation_result,
                "validation_ok": True,
                "error_message": "",
                "invalid_owl": "",
                "processed_owls": processed_owls,
                "unprocessed_cqs": unprocessed_cqs,
            }
    except Exception as e:
        print(f"Exception during RDF validation for {cq.id}: {e}")
        return {
            **state,
            "current_validation": str(e),
            "validation_ok": False,
            "error_message": str(e),
            "invalid_owl": owl_code or "",
        }


##### Node to combine all valid OWL codes into a single OWL for the entire story
def combine_owls_node(state: OntoAgentState) -> OntoAgentState:
    print("Combining OWLs for Story ID:", state.get("story_id", ""))
    story_id = state.get("story_id", "")
    processed_owls = state.get("processed_owls") or []
    concatenated_owl = "\n".join([owl for _, owl in processed_owls])
    save_text_file(f"data/output/{story_id}_concat.owl", concatenated_owl)

    structured_prompt = prompt_manager.get_structured_prompt("combine_owl_codes")
    combination_prompt = structured_prompt["user_template"].format(
        story_id="FestS",
        story="",
        snippets=concatenated_owl,
    )
    print("Combining OWLs")
    combined_owl = call_llm(llm_type, combination_prompt)

    print("Combined, saving OWLs file")
    save_text_file(f"data/output/{story_id}_combined_turtle.owl", combined_owl)
    return {**state, "combined_owl": combined_owl}


##### Node to validate the combined OWL for the story
def validate_combined_owl_node(state: OntoAgentState) -> OntoAgentState:
    pitfall_reviewer = OopsPitfallReviewer()
    syntax_reviewer = RDFSyntaxReviewer()
    story_id = state.get("story_id", "")

    # Initialize validation logger
    combined_owl = state.get("combined_owl", "")
    timestamp = state.get("log_timestamp") or datetime.now().strftime("%Y%m%d_%H%M%S")
    validation_logger = ValidationLogger(
        story_id=story_id,
        log_dir="logs",
        timestamp=timestamp
    )
    validation_logger.log_start(ontology_size=len(combined_owl))

    try:
        print("Validating combined OWL for Story ID:", story_id)

        # Syntax validation with timing
        syntax_start_time = time.time()
        syntax_validation_result = syntax_reviewer.review_owl_content(combined_owl)
        syntax_time_seconds = time.time() - syntax_start_time
        print("Syntax Validation Result:", syntax_validation_result)

        syntax_valid = syntax_validation_result == "OK"
        validation_logger.log_syntax_validation(
            is_valid=syntax_valid,
            execution_time_seconds=syntax_time_seconds,
            error=None if syntax_valid else syntax_validation_result,
        )

        if syntax_validation_result != "OK":
            print("Syntax validation failed!")
            return {
                **state,
                "combined_validation": f"Syntax Error: {syntax_validation_result}",
                "combined_validation_ok": False,
                "pitfall_feedback": f"Syntax Error: {syntax_validation_result}",
            }

        # Validate Pitfalls using turtle file with timing
        oops_start_time = time.time()
        owl_file_path = os.path.join(
            "data", "output", f"{story_id}_combined_turtle.owl"
        )
        pitfalls = [
            "2,3, 4, 5, 6, 7, 8, 10, 11, 12, 13, 19, 20, 21, 22, 24, 25, 25, 26, 27, 28, 29"
        ]
        pitfall_validation_result = pitfall_reviewer.review_owl_file(
            owl_file_path=owl_file_path,
            pitfalls=pitfalls,
            output_format="XML",
        )
        oops_time_seconds = time.time() - oops_start_time

        # Parse OOPS response
        pitfall_data = parse_oops_response(pitfall_validation_result)
        has_pitfalls = pitfall_data.get("has_pitfalls", False)
        pitfall_count = pitfall_data.get("pitfall_count", 0)
        pitfalls_list = pitfall_data.get("pitfalls", [])

        validation_logger.log_pitfall_detection(
            has_pitfalls=has_pitfalls,
            pitfall_count=pitfall_count,
            execution_time_seconds=oops_time_seconds,
            pitfalls=pitfalls_list,
        )

        # Format pitfall feedback for potential correction
        pitfall_feedback = format_pitfalls_for_feedback(pitfall_data)

        # Determine if validation passed
        validation_ok = not has_pitfalls

        if has_pitfalls:
            print(f"\nFound {pitfall_data['pitfall_count']} pitfall(s)")
            print(pitfall_feedback)
        else:
            print("\n✓ No pitfalls detected!")

        # Full validation result for auditing
        validation_result = f"Syntax Check: {syntax_validation_result}\nPitfall Check: {pitfall_validation_result}"
        print("Combined OWL validation result:", validation_result)

        # Validation result save for auditing with incremental numbering
        retry_count = state.get("retry_count", 0)
        if retry_count == 0:
            # Initial validation (no corrections yet)
            oops_result_file = f"data/output/{story_id}_combined_oops_result.xml"
        else:
            # After correction attempts
            oops_result_file = (
                f"data/output/{story_id}_combined_oops_result_{retry_count}.xml"
            )

        save_text_file(oops_result_file, validation_result)
        print(f"Saved validation results to: {oops_result_file}")

        # Note: ValidationLogger will be completed and saved by final_reasoner_validation_node

        return {
            **state,
            "combined_validation": validation_result,
            "combined_validation_ok": validation_ok,
            "pitfall_feedback": pitfall_feedback if has_pitfalls else "",
            "syntax_time_seconds": syntax_time_seconds,
            "oops_time_seconds": oops_time_seconds,
        }

    except Exception as e:
        print("Combined OWL validation exception:", str(e))
        return {
            **state,
            "combined_validation": str(e),
            "combined_validation_ok": False,
            "pitfall_feedback": f"Validation exception: {str(e)}",
        }


##### Node for final reasoner validation (Hermit + Pellet)
def final_reasoner_validation_node(state: OntoAgentState) -> OntoAgentState:
    """Add reasoner validation (Hermit + Pellet) as Pillar 3."""
    story_id = state.get("story_id", "")
    combined_owl = state.get("combined_owl", "")

    if not combined_owl:
        print("\n⚠ No ontology to validate")
        return state

    timestamp = state.get("log_timestamp") or datetime.now().strftime("%Y%m%d_%H%M%S")

    print(f"\n{'=' * 60}")
    print(f"FINAL REASONER VALIDATION FOR {story_id}")
    print(f"{'=' * 60}\n")

    # Load existing validation log to append reasoners
    log_json_path = f"logs/{story_id}_validation_{timestamp}.json"

    try:
        if os.path.exists(log_json_path):
            with open(log_json_path, "r") as f:
                existing_log = json.load(f)
                validation_results = existing_log.get("validation_results", {})
                if not validation_results:
                    validation_results = {
                        "timestamp": timestamp,
                        "story_id": story_id,
                        "ontology_size_chars": len(combined_owl),
                    }
        else:
            validation_results = {
                "timestamp": timestamp,
                "story_id": story_id,
                "ontology_size_chars": len(combined_owl),
            }
    except Exception as e:
        print(f"Warning: Could not load existing log: {e}")
        validation_results = {
            "timestamp": timestamp,
            "story_id": story_id,
            "ontology_size_chars": len(combined_owl),
        }

    # Get RDF/XML
    rdfxml_path = "data/output/xml_combined_owl.xml"
    if not os.path.exists(rdfxml_path):
        print(f"⚠ RDF/XML not found - skipping reasoners")
        return state

    # Add syntax and OOPS results to validation_results (from state)
    syntax_time = state.get("syntax_time_seconds", 0)
    oops_time = state.get("oops_time_seconds", 0)

    validation_results["syntax"] = {
        "valid": validation_results.get("syntax", {}).get("valid", True),
        "execution_time_seconds": syntax_time,
        "error": None,
    }

    validation_results["oops"] = {
        "has_pitfalls": validation_results.get("oops", {}).get("has_pitfalls", False),
        "pitfall_count": validation_results.get("oops", {}).get("pitfall_count", 0),
        "execution_time_seconds": oops_time,
        "pitfalls": validation_results.get("oops", {}).get("pitfalls", []),
    }

    print("3️⃣  Reasoning Consistency")
    print("-" * 60)

    # Hermit
    print("  🧠 Hermit reasoner...")
    hermit_validator = HermitReasonerValidator(rdfxml_path=rdfxml_path)
    hermit_result = hermit_validator.validate()
    validation_results["hermit"] = hermit_result

    if hermit_result["is_consistent"]:
        print(f"    ✓ PASSED ({hermit_result['execution_time_seconds']:.3f}s)")
    else:
        print(f"    ✗ FAILED ({hermit_result['execution_time_seconds']:.3f}s)")

    # Pellet
    print("  🧠 Pellet reasoner...")
    pellet_validator = PelletReasonerValidator(rdfxml_path=rdfxml_path)
    pellet_result = pellet_validator.validate()
    validation_results["pellet"] = pellet_result

    if pellet_result["is_consistent"]:
        print(f"    ✓ PASSED ({pellet_result['execution_time_seconds']:.3f}s)\n")
    else:
        print(f"    ✗ FAILED ({pellet_result['execution_time_seconds']:.3f}s)\n")

    # Aggregate
    reasoners_passed = (
        hermit_result["is_consistent"] and pellet_result["is_consistent"]
    )
    total_time = (
        hermit_result["execution_time_seconds"] +
        pellet_result["execution_time_seconds"]
    )

    syntax_valid = validation_results.get("syntax", {}).get("valid", True)
    has_pitfalls = validation_results.get("oops", {}).get("has_pitfalls", False)
    pitfall_count = validation_results.get("oops", {}).get("pitfall_count", 0)

    all_passed = syntax_valid and not has_pitfalls and reasoners_passed

    validation_results["aggregate"] = {
        "all_validators_passed": all_passed,
        "total_execution_time_seconds": round(total_time, 3),
    }

    # Save JSON
    os.makedirs("data/output/validations", exist_ok=True)
    val_json = f"data/output/validations/{story_id}_validation_{timestamp}.json"
    with open(val_json, "w") as f:
        json.dump(validation_results, f, indent=2)
    print(f"✓ Validation JSON: {val_json}")

    # Re-create logger and save complete logs
    validation_logger = ValidationLogger(
        story_id=story_id,
        log_dir="logs",
        timestamp=timestamp
    )
    validation_logger.log_start(ontology_size=len(combined_owl))

    # Re-log syntax and OOPS
    if "syntax" in validation_results:
        validation_logger.log_syntax_validation(
            is_valid=validation_results["syntax"].get("valid", False),
            execution_time_seconds=validation_results["syntax"].get("execution_time_seconds", 0),
            error=validation_results["syntax"].get("error"),
        )

    if "oops" in validation_results:
        validation_logger.log_pitfall_detection(
            has_pitfalls=validation_results["oops"].get("has_pitfalls", False),
            pitfall_count=validation_results["oops"].get("pitfall_count", 0),
            execution_time_seconds=validation_results["oops"].get("execution_time_seconds", 0),
            pitfalls=validation_results["oops"].get("pitfalls", []),
        )

    # Log reasoners
    validation_logger.log_reasoning_start()
    validation_logger.log_reasoner_validation("Hermit", hermit_result)
    validation_logger.log_reasoner_validation("Pellet", pellet_result)

    # Get individual timing values for log_summary
    syntax_time = state.get("syntax_time_seconds", 0)
    oops_time = state.get("oops_time_seconds", 0)
    hermit_time = hermit_result["execution_time_seconds"]
    pellet_time = pellet_result["execution_time_seconds"]

    validation_logger.log_summary(
        syntax_valid=syntax_valid,
        has_pitfalls=has_pitfalls,
        pitfall_count=pitfall_count,
        hermit_consistent=hermit_result["is_consistent"],
        pellet_consistent=pellet_result["is_consistent"],
        syntax_time_seconds=syntax_time,
        oops_time_seconds=oops_time,
        hermit_time_seconds=hermit_time,
        pellet_time_seconds=pellet_time,
        iteration_count=0,  # Main branch has no iterations
    )
    validation_logger.save_json_log()

    print(f"✓ Complete logs: {validation_logger.get_log_paths()['text_log']}")
    print(f"{'=' * 60}\n")

    return {
        **state,
        "reasoner_validation": validation_results,
        "reasoners_passed": reasoners_passed,
    }


##### Node to correct OWL based on pitfall feedback
def correct_owl_pitfalls_node(state: OntoAgentState) -> OntoAgentState:
    print("Correcting OWL pitfalls...")
    story_id = state.get("story_id", "")
    combined_owl = state.get("combined_owl", "")
    pitfall_feedback = state.get("pitfall_feedback", "")
    retry_count = state.get("retry_count", 0)

    if not pitfall_feedback:
        print("No pitfall feedback to address")
        return state

    print(f"Attempting correction (attempt {retry_count + 1})...")
    print("Pitfalls to address:")
    print(pitfall_feedback)

    # Use prompt manager for correction prompt
    structured_prompt = prompt_manager.get_structured_prompt("correct_owl_pitfalls")
    correction_prompt = structured_prompt["user_template"].format(
        pitfall_feedback=pitfall_feedback,
        combined_owl=combined_owl,
    )

    # Call LLM to fix the OWL
    corrected_owl = call_llm(llm_type, correction_prompt)

    # Save the corrected version
    correction_file = (
        f"data/output/{story_id}_combined_turtle_correction_{retry_count + 1}.owl"
    )
    save_text_file(correction_file, corrected_owl)
    print(f"Saved correction attempt to: {correction_file}")

    # Also update the main combined file
    save_text_file(f"data/output/{story_id}_combined_turtle.owl", corrected_owl)

    return {
        **state,
        "combined_owl": corrected_owl,
        "retry_count": retry_count + 1,
    }


def create_generator_log_node(state: OntoAgentState) -> OntoAgentState:
    """Create minimal generator log for analyze_logs.py."""
    story_id = state.get("story_id", "")
    timestamp = state.get("log_timestamp") or datetime.now().strftime("%Y%m%d_%H%M%S")

    story_start_time = state.get("story_start_time")
    if story_start_time:
        duration_seconds = time.time() - story_start_time
        duration_formatted = format_duration(duration_seconds)
    else:
        duration_seconds = 0
        duration_formatted = "0s"

    combined_owl = state.get("combined_owl", "")

    generator_log = {
        "story_id": story_id,
        "timestamp": timestamp,
        "duration_seconds": duration_seconds,
        "duration_formatted": duration_formatted,
        "ontology_saved": len(combined_owl) > 0,
        "ontology_size_chars": len(combined_owl),
        "workflow_type": "main_branch_sequential",
        "iterations": [],
    }

    log_path = f"logs/{story_id}_generator_{timestamp}.json"
    with open(log_path, "w") as f:
        json.dump(generator_log, f, indent=2)

    print(f"✓ Generator log: {log_path}")
    return state


def end_node(state: OntoAgentState) -> OntoAgentState:
    story_id = state.get("story_id", "")

    story_start_time = state.get("story_start_time")
    if story_start_time:
        duration = time.time() - story_start_time
        duration_fmt = format_duration(duration)

        print(f"\n{'=' * 60}")
        print(f"WORKFLOW COMPLETE FOR {story_id}")
        print(f"Duration: {duration_fmt}")
        print(f"{'=' * 60}\n")

        return {
            **state,
            "story_duration_seconds": duration,
            "story_duration_formatted": duration_fmt,
        }

    return state


########### Branches ###########


def validate_and_store_owl_branch(state: OntoAgentState) -> str:
    unprocessed_cqs = state.get("unprocessed_cqs", [])
    return "generate_owl" if len(unprocessed_cqs) > 0 else "combine_owls"


def validate_combined_owl_branch(state: OntoAgentState) -> str:
    """Branch logic after combined OWL validation"""
    if state.get("combined_validation_ok", False):
        # Validation passed - proceed to reasoner validation
        return "final_reasoner_validation"
    else:
        # Validation failed - check retry count
        retry_count = state.get("retry_count", 0)
        max_retries = 5
        if retry_count >= max_retries:
            print(f"Max retries ({max_retries}) reached. Proceeding to reasoner validation.")
            return "final_reasoner_validation"
        # Still have retries left - correct the OWL
        return "correct_owl_pitfalls"


###################################
########### Graph Nodes ###########
###################################

graph = StateGraph(state_schema=OntoAgentState)
graph.add_node("get_story", get_story_node)
graph.add_node("generate_owl", generate_owl_node)
graph.add_node("validate_and_store_owl", validate_and_store_owl_node)
graph.add_node("combine_owls", combine_owls_node)
graph.add_node("validate_combined_owl", validate_combined_owl_node)
graph.add_node("correct_owl_pitfalls", correct_owl_pitfalls_node)
graph.add_node("final_reasoner_validation", final_reasoner_validation_node)
graph.add_node("create_generator_log", create_generator_log_node)
graph.add_node("end", end_node)

######################################
########### Graph workflow ###########
######################################

graph.set_entry_point("get_story")
graph.add_edge("get_story", "generate_owl")
graph.add_edge("generate_owl", "validate_and_store_owl")
graph.add_conditional_edges("validate_and_store_owl", validate_and_store_owl_branch)
graph.add_edge("combine_owls", "validate_combined_owl")
graph.add_conditional_edges("validate_combined_owl", validate_combined_owl_branch)
graph.add_edge("correct_owl_pitfalls", "validate_combined_owl")
graph.add_edge("final_reasoner_validation", "create_generator_log")
graph.add_edge("create_generator_log", "end")

graph.set_finish_point("end")

########################################
########### Run the workflow ###########
########################################

if __name__ == "__main__":
    # Parse command-line arguments
    parser = argparse.ArgumentParser(
        description="Otho - Ontology generation workflow with competency questions"
    )
    parser.add_argument(
        "--story-id",
        type=str,
        default="MusicS",
        help="Story ID to process (e.g., FestS, MusicS, HospitalS). Default: MusicS",
    )
    parser.add_argument(
        "--skip-to-combine",
        action="store_true",
        help="Skip CQ generation and jump directly to combination phase. Loads existing OWL files.",
    )
    parser.add_argument(
        "--repeat",
        type=int,
        metavar="N",
        help="Run the specified story N times without sharing context between runs.",
    )

    args = parser.parse_args()
    story_id = args.story_id

    print(f"Starting ontology workflow for Story ID: {story_id}")
    print(f"Mode: {'Skip-to-Combine' if args.skip_to_combine else 'Full Workflow'}\n")

    # Compile the workflow graph
    app = graph.compile()

    # Repeat mode: run single story N times without sharing context
    if args.repeat:
        print(
            f"REPEAT MODE: Running story '{story_id}' {args.repeat} time(s) without shared context\n"
        )

        for iteration in range(1, args.repeat + 1):
            print(
                f"\n{'=' * 60}\nSINGLE STORY RUN {iteration}/{args.repeat} - {story_id}\n{'=' * 60}"
            )

            # Each invocation gets a fresh state with no shared context
            initial_state: OntoAgentState = {"story_id": story_id}
            app.invoke(initial_state, config={"recursion_limit": 125})

    elif args.skip_to_combine:
        # Skip-to-combine mode: Load existing OWL files and start at combine_owls
        try:
            print("Loading existing OWL files...")
            processed_owls = load_existing_owl_files(story_id)

            if not processed_owls:
                print(f"ERROR: No OWL files found for story '{story_id}'")
                print("Please run the full workflow first to generate OWL files.")
                sys.exit(1)

            print(
                f"\nStarting combination phase with {len(processed_owls)} OWL files...\n"
            )

            # Create initial state with pre-loaded OWL files
            initial_state: OntoAgentState = {
                "story_id": story_id,
                "processed_owls": processed_owls,
                "unprocessed_cqs": [],  # Empty to skip generation
            }

            # Manually execute nodes starting from combine_owls
            print("Executing combine_owls node...")
            state = combine_owls_node(initial_state)

            print("\nExecuting validate_combined_owl node...")
            state = validate_combined_owl_node(state)

            # Correction loop - attempt to fix pitfalls up to max_retries
            max_retries = 5
            while (
                not state.get("combined_validation_ok", False)
                and state.get("retry_count", 0) < max_retries
            ):
                print(f"\nExecuting correct_owl_pitfalls node...")
                state = correct_owl_pitfalls_node(state)

                print("\nRe-validating corrected OWL...")
                state = validate_combined_owl_node(state)

            print("\nExecuting end node...")
            state = end_node(state)

            if state.get("combined_validation_ok", False):
                print("\n✓ Workflow completed successfully!")
            else:
                print(
                    f"\n✗ Workflow completed but validation failed after {max_retries} retries."
                )

        except FileNotFoundError as e:
            print(f"ERROR: {e}")
            print(
                "\nPlease ensure you have run the full workflow first to generate OWL files."
            )
            print(f"Expected files: data/output/{story_id}_{{CQ_ID}}.owl")
            sys.exit(1)
        except Exception as e:
            print(f"ERROR: An unexpected error occurred: {e}")
            sys.exit(1)

    else:
        # Normal mode: Full workflow from the beginning
        initial_state: OntoAgentState = {"story_id": story_id}
        app.invoke(initial_state, config={"recursion_limit": 125})
