"""
StateGraph node implementations for Otho agent workflow.

This module contains all node functions for the self-validating React agent
workflow, including the main ontology generation agent and validation nodes.
"""

import json
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, TypedDict

from langchain.tools import tool
from langchain_core.messages import HumanMessage
from langgraph.prebuilt import create_react_agent

from src.agents.tools import validate_syntax_tool
from src.agents.workspace import AgentWorkspace
from src.prompts.prompt_manager import PromptManager
from src.reviewers.reasoner_validator import (
    HermitReasonerValidator,
    PelletReasonerValidator,
)
from src.reviewers.reviewer import OopsPitfallReviewer, RDFSyntaxReviewer
from src.utils.agent_logger import AgentLogger
from src.utils.excel_processor import get_story_by_id
from src.utils.file_handler import save_text_file
from src.utils.llm_manager import (
    get_gaih_anthropic_llm,
    get_gaih_google_llm,
    get_gaih_openai_llm,
)
from src.utils.oops_parser import parse_oops_response
from src.utils.timing import format_duration
from src.utils.validation_logger import ValidationLogger

# Initialize prompt manager
prompt_manager = PromptManager(prompts_file_path=Path("src/prompts/prompts.yaml"))


# Type alias for state (will match OntoAgentState from otho.py)
StateDict = Dict[str, Any]


def set_output_directories():
    """
    Ensure organized output directory structure exists.

    Creates subdirectories for different output types:
    - data/output/ontologies/ - OWL ontology files
    - data/output/reviews/ - Review reports
    - data/output/scratchpads/ - Agent scratchpad files
    - data/output/validations/ - Validation result files (XML and JSON)
    """
    base_dir = Path("data/output")
    subdirs = ["ontologies", "reviews", "scratchpads", "validations"]

    for subdir in subdirs:
        (base_dir / subdir).mkdir(parents=True, exist_ok=True)


def get_story_node(state: StateDict) -> StateDict:
    """
    Load story object and initialize workspace.

    This is the entry point of the workflow. It loads the story from the
    Excel dataset and creates a fresh AgentWorkspace for the agent to use.
    Also creates a shared timestamp for all logs in this run and starts timing.

    Args:
        state: Current workflow state containing story_id

    Returns:
        Updated state with story_object, initialized workspace, and shared log_timestamp
    """
    story_id = state.get("story_id", "")

    # Create shared timestamp for all logs in this run
    log_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Start story timing
    story_start_time = time.time()

    print(f"\n{'=' * 60}")
    print(f"Loading Story: {story_id}")
    print(f"Run Timestamp: {log_timestamp}")
    print(f"{'=' * 60}\n")

    story = get_story_by_id(story_id)

    # Create new AgentWorkspace instance
    workspace = AgentWorkspace()

    print(f"✓ Story loaded: {story.context[:100]}...")
    print(f"✓ Competency questions: {len(story.competency_questions or [])}")
    print(f"✓ Workspace initialized")
    print(f"✓ Log timestamp: {log_timestamp}\n")

    return {
        **state,
        "story_object": story,
        "workspace": [workspace],  # Wrap in list for state mutability pattern
        "iteration_count": 0,
        "validation_history": [],
        "log_timestamp": log_timestamp,  # Shared timestamp for generator and validator logs
        "generator_iteration": 0,  # Track which iteration of the generator we're on
        "story_start_time": story_start_time,  # For timing calculation
    }


def create_agent_tools(
    workspace: AgentWorkspace, story_id: str, timestamp: str
) -> List:
    """
    Create tool instances with access to shared workspace.

    Tools modify the workspace object which is shared between the node and agent.
    This pattern allows mutation while respecting LangGraph's immutable state.

    Args:
        workspace: AgentWorkspace instance that tools will modify
        story_id: Story identifier for unique file naming (prevents race conditions)
        timestamp: Timestamp for unique file naming (prevents race conditions)

    Returns:
        List of tool instances for the React agent
    """

    @tool
    def update_scratchpad(key: str, value: Any) -> Dict[str, bool]:
        """
        Update agent's persistent working memory (scratchpad) with a key-value pair.

        Use this to track your planning, progress, and decisions.
        Recommended keys:
        - 'plan': Your ontology structure plan
        - 'cq_coverage': Mapping of CQs to ontology elements
        - 'iterations': List of validation attempts and fixes
        - 'current_owl_draft': Working version of ontology
        - 'notes': Your reasoning and observations

        Args:
            key: The scratchpad key to update
            value: The value to store (can be dict, list, string, etc.)

        Returns:
            {"success": True, "key": key}

        Example:
            update_scratchpad("plan", {
                "classes": ["User", "Resource"],
                "properties": [{"name": "uses", "type": "ObjectProperty"}]
            })
        """
        workspace.update_scratchpad(key, value)
        return {"success": True}

    @tool
    def read_scratchpad(key: str) -> Any:
        """
        Read a single key from the scratchpad.

        Args:
            key: The scratchpad key to read

        Returns:
            The value stored at that key, or None if not found
        """
        return workspace.get_scratchpad(key)

    @tool
    def read_full_context() -> Dict[str, Any]:
        """
        Read ALL scratchpad entries in one call. Use at the start of refinement
        to restore your previous design context (plan, cq_coverage, iterations, notes).

        Returns:
            Dictionary with all stored scratchpad entries
        """
        return workspace.scratchpad

    @tool
    def save_final_ontology(
        owl_content: str, label: str = "final_validated"
    ) -> Dict[str, Any]:
        """
        Save the final validated ontology to complete the task.

        This tool marks task completion. Call this ONLY when you have a complete,
        validated ontology ready. This writes to the workspace's 'generated_owl' field,
        signaling that you have successfully completed the ontology generation task.

        CRITICAL: Only call this after BOTH syntax and pitfall validation have passed!
        Calling this tool signals you are done with the task.

        Args:
            owl_content: Complete OWL ontology in Turtle syntax
            label: Description (default: "final_validated")

        Returns:
            {
                "saved": True,
                "label": label,
                "length": character_count,
                "message": "Final ontology saved - task complete"
            }

        Example:
            # After both validations pass
            result = save_final_ontology(my_owl_code, "final_validated")
            # Task is now complete!
        """
        workspace.save_ontology(owl_content)
        return {
            "saved": True,
            "label": label,
            "length": len(owl_content),
            "message": "Final ontology saved - task complete",
        }

    @tool
    def check_pitfalls_tool(owl_content: str) -> Dict[str, Any]:
        """
        Check for OOPS ontology modeling pitfalls.

        Use this tool to validate your ontology against common modeling pitfalls
        using the OOPS (OntOlogy Pitfall Scanner) web service. The tool checks
        for 22 different types of pitfalls including missing annotations, unconnected
        classes, and other modeling issues.

        Args:
            owl_content: OWL ontology code in Turtle syntax

        Returns:
            Dictionary with pitfall analysis:
            - has_pitfalls (bool): True if pitfalls were detected
            - pitfall_count (int): Number of pitfalls found
            - pitfalls (list): List of pitfall details, each containing:
                - code (str): Pitfall code (e.g., "P04", "P08")
                - name (str): Pitfall name
                - description (str): Description of the issue
                - affected_elements (list): List of ontology elements with this pitfall
        """
        import os
        import tempfile

        # Save to temporary file for OOPS validation
        with tempfile.NamedTemporaryFile(mode="w", suffix=".owl", delete=False) as f:
            f.write(owl_content)
            temp_path = f.name

        try:
            reviewer = OopsPitfallReviewer()

            # Check for common pitfalls
            pitfalls_to_check = [
                "2",
                "3",
                "4",
                "5",
                "6",
                "7",
                "8",
                "10",
                "11",
                "12",
                "13",
                "19",
                "20",
                "21",
                "22",
                "24",
                "25",
                "26",
                "27",
                "28",
                "29",
            ]

            # Use story_id and timestamp captured from create_agent_tools parameters
            # This ensures unique file naming to prevent race conditions
            result = reviewer.review_owl_file(
                temp_path,
                pitfalls=pitfalls_to_check,
                output_format="XML",
                story_id=story_id,
                timestamp=timestamp,
            )

            pitfall_data = parse_oops_response(result)

            return {
                "has_pitfalls": pitfall_data.get("has_pitfalls", False),
                "pitfall_count": pitfall_data.get("pitfall_count", 0),
                "pitfalls": pitfall_data.get("pitfalls", []),
            }
        except Exception as e:
            return {
                "has_pitfalls": True,
                "pitfall_count": 1,
                "pitfalls": [
                    {
                        "code": "ERROR",
                        "name": "Validation Exception",
                        "description": str(e),
                        "affected_elements": [],
                    }
                ],
            }
        finally:
            # Clean up temporary file
            if os.path.exists(temp_path):
                os.unlink(temp_path)

    # Return all 6 tools
    return [
        update_scratchpad,
        read_scratchpad,
        read_full_context,
        validate_syntax_tool,
        check_pitfalls_tool,
        save_final_ontology,
    ]


def ontology_generation_agent(state: StateDict) -> StateDict:
    """
    React agent generates and self-validates ontology (or refines based on review).

    MODE 1 - Initial Generation:
    The agent will:
    1. Plan the ontology structure (using update_scratchpad)
    2. Verify CQ coverage (using update_scratchpad)
    3. Generate OWL code directly (not via tool)
    4. Validate syntax (using validate_syntax_tool)
    5. Check pitfalls (using check_pitfalls_tool)
    6. Iterate and fix issues until validation passes
    7. Save final ontology (using save_final_ontology tool)

    MODE 2 - Refinement (if latest_review exists):
    The agent will:
    1. Analyze review feedback
    2. Identify high-priority improvements
    3. Refine the ontology to address feedback
    4. Validate syntax and pitfalls
    5. Save refined version

    Maximum 10 iterations to prevent infinite loops.

    Args:
        state: Current workflow state with story_object and workspace

    Returns:
        Updated state with agent results
    """
    story_object = state.get("story_object")
    story_id = story_object.id if story_object else ""

    # Check if this is refinement mode
    latest_review = state.get("latest_review")
    review_iteration = state.get("review_iteration_count", 0)
    workspace = state["workspace"][0]

    # Extract story context and competency questions
    story_context = story_object.context if story_object else ""
    competency_questions = (
        story_object.competency_questions if story_object else None
    ) or []

    # Format competency questions as text
    cq_list = "\n".join(
        [f"{i + 1}. {cq.question}" for i, cq in enumerate(competency_questions)]
    )

    # Determine mode and build appropriate prompt
    if latest_review and review_iteration > 0:
        # REFINEMENT MODE
        print(f"\n{'=' * 60}")
        print(f"REFINEMENT MODE - React Agent (Iteration {review_iteration})")
        print(f"{'=' * 60}\n")

        current_owl = workspace.generated_owl

        # Extract key review metrics for display
        cq_coverage_score = latest_review.get("cq_coverage", {}).get(
            "coverage_score", "N/A"
        )
        quality_score = latest_review.get("quality_metrics", {}).get(
            "overall_score", "N/A"
        )
        suggestions_count = len(latest_review.get("improvement_suggestions", []))

        print(f"Previous CQ Coverage: {cq_coverage_score}")
        print(f"Previous Quality Score: {quality_score}")
        print(f"Improvement Suggestions: {suggestions_count}\n")

        prompt = prompt_manager.format_prompt(
            "refine_ontology",
            story_text=story_context,
            cq_list=cq_list,
            current_ontology=current_owl,
            review_feedback=json.dumps(latest_review, indent=2),
            iteration=review_iteration,
        )
    else:
        # INITIAL GENERATION MODE
        print(f"\n{'=' * 60}")
        print(f"INITIAL GENERATION - React Agent for Story ID: {story_id}")
        print(f"{'=' * 60}\n")

        print(f"Story context length: {len(story_context)} characters")
        print(f"Number of CQs: {len(competency_questions)}\n")

        prompt = prompt_manager.format_prompt(
            "generate_ontology", story_text=story_context, cq_list=cq_list
        )

    # Get workspace reference
    workspace = state["workspace"][0]

    # Get shared timestamp and increment generator iteration
    log_timestamp = state.get("log_timestamp")
    generator_iteration = state.get("generator_iteration", 0) + 1

    # Create tools with workspace, story_id, and timestamp for unique file naming
    # The timestamp is the same shared log_timestamp used for all logs in this run
    tools = create_agent_tools(workspace, story_id=story_id, timestamp=log_timestamp)

    tool_names = [tool.name for tool in tools]
    print(f"Created {len(tools)} tools for agent:")
    for tool_name in tool_names:
        print(f"  - {tool_name}")
    print()

    # Initialize comprehensive logger with shared timestamp and iteration tracking
    agent_logger = AgentLogger(
        story_id=story_id,
        log_dir="logs",
        timestamp=log_timestamp,
        iteration=generator_iteration,
    )
    agent_logger.log_agent_start(
        prompt_length=len(prompt), num_tools=len(tools), tool_names=tool_names
    )

    # Get LLM for React agent
    generator_model = "anthropic--claude-4.5-opus"
    llm = get_gaih_anthropic_llm(model=generator_model)

    # generator_model = "gpt-4.1"
    # llm = get_gaih_openai_llm(model=generator_model)

    # generator_model = "gemini-2.5-flash"
    # llm = get_gaih_google_llm(model=generator_model)

    agent_logger.log_llm_model(generator_model)

    # Create React agent
    agent_logger.logger.info("Creating React agent with tools...")
    agent_executor = create_react_agent(llm, tools)

    # Configure recursion limit (175 to accommodate review loop with 3 agent runs)
    config = {"recursion_limit": 400}

    # Invoke agent
    agent_logger.logger.info("Invoking React agent (this may take several minutes)...")

    try:
        agent_response = agent_executor.invoke(
            {"messages": [HumanMessage(content=prompt)]}, config=config
        )

        # Log all messages from the conversation
        messages = agent_response.get("messages", [])
        for i, msg in enumerate(messages):
            agent_logger.log_message(i, msg)

        # Log completion
        agent_logger.log_agent_complete(
            message_count=len(messages), workspace_state=workspace.to_dict()
        )

    except Exception as e:
        agent_logger.log_error(e)
        agent_logger.save_json_log()
        return {**state, "error_message": f"Agent execution failed: {str(e)}"}

    # Save JSON log
    agent_logger.save_json_log()

    # Extract results from workspace (agent updated via tools)
    generated_owl = workspace.generated_owl
    scratchpad = workspace.scratchpad
    iteration_count = workspace.get_iteration_count()

    # Report results
    log_paths = agent_logger.get_log_paths()
    tool_call_count = len(agent_logger._current_iteration.get("tool_calls", []))
    print(f"\n{'=' * 60}")
    print("AGENT EXECUTION SUMMARY")
    print(f"{'=' * 60}")
    print(f"✓ Tool calls made: {tool_call_count}")
    print(f"✓ Iterations: {iteration_count}")
    print(f"✓ Generated OWL length: {len(generated_owl)} characters")
    print(f"✓ Text log: {log_paths['text_log']}")
    print(f"✓ JSON log: {log_paths['json_log']}")

    if not generated_owl:
        print(f"\n⚠ WARNING: Agent did not save ontology to workspace!")
        print("Check the log files for details on what the agent did.")

    print(f"{'=' * 60}\n")

    return {
        **state,
        "workspace": [workspace],  # Pass workspace reference forward
        "iteration_count": iteration_count,
        "generator_iteration": generator_iteration,  # Track generator iteration for logging
        "error_message": "",
    }


def validate_and_save_node(state: StateDict) -> StateDict:
    """
    Final validation and save to disk in a multi-dimensional, 3-pillar, approach.

    Validates ontology across three complementary dimensions:
    1. Structural: RDF/Turtle syntax validation
    2. Pitfalls: OOPS modeling anti-pattern detection
    3. Logical: Reasoning consistency with Hermit and Pellet

    Each validator runs in isolation with proper cleanup to prevent
    state contamination. Results are aggregated and saved with timing metrics.

    Args:
        state: Current workflow state with workspace

    Returns:
        Updated state with comprehensive validation results
    """
    story_id = state.get("story_id", "")

    # Extract from workspace
    workspace = state["workspace"][0]
    generated_owl = workspace.generated_owl
    scratchpad = workspace.scratchpad

    if not generated_owl:
        print(f"\n✗ ERROR: No ontology generated by agent!")
        return {**state, "error_message": "Agent did not produce ontology"}

    # Get shared timestamp from state (same as generator logs)
    log_timestamp = state.get("log_timestamp")

    # Initialize validation logger with shared timestamp
    validation_logger = ValidationLogger(
        story_id=story_id, log_dir="logs", timestamp=log_timestamp
    )
    validation_logger.log_start(ontology_size=len(generated_owl))

    # Use shared timestamp for output files too
    timestamp = log_timestamp or datetime.now().strftime("%Y%m%d_%H%M%S")
    validation_results = {
        "timestamp": timestamp,
        "story_id": story_id,
        "ontology_size_chars": len(generated_owl),
    }

    # ============================================================
    # PILLAR 1: SYNTAX VALIDATION
    # ============================================================
    print("1️⃣  Syntax Validation (RDFLib)")
    print("-" * 60)

    start_time = time.time()
    syntax_result = RDFSyntaxReviewer().review_owl_content(generated_owl)
    syntax_time_seconds = time.time() - start_time
    syntax_valid = syntax_result == "OK"

    validation_results["syntax"] = {
        "valid": syntax_valid,
        "execution_time_seconds": round(syntax_time_seconds, 3),
        "error": None if syntax_valid else syntax_result,
    }

    # Log to file with detailed info
    validation_logger.log_syntax_validation(
        is_valid=syntax_valid,
        execution_time_seconds=syntax_time_seconds,
        error=None if syntax_valid else syntax_result,
    )

    # Also print summary to console
    if syntax_valid:
        print(f"✓ Syntax validation PASSED ({syntax_time_seconds:.3f}s)\n")
    else:
        print(f"✗ Syntax validation FAILED ({syntax_time_seconds:.3f}s)")
        print(f"  Error: {syntax_result}\n")

    # ============================================================
    # PILLAR 2: PITFALL DETECTION
    # ============================================================
    print("2️⃣  Pitfall Detection (OOPS)")
    print("-" * 60)
    pitfall_reviewer = OopsPitfallReviewer()
    pitfalls = [
        "2",
        "3",
        "4",
        "5",
        "6",
        "7",
        "8",
        "10",
        "11",
        "12",
        "13",
        "19",
        "20",
        "21",
        "22",
        "24",
        "25",
        "26",
        "27",
        "28",
        "29",
    ]

    start_time = time.time()
    # Pass story_id and timestamp for unique file naming to prevent race conditions
    # when running multiple Otho instances concurrently
    pitfall_result = pitfall_reviewer.review_owl_content(
        owl_content=generated_owl,
        pitfalls=pitfalls,
        output_format="XML",
        story_id=story_id,
        timestamp=timestamp,
    )
    oops_time_seconds = time.time() - start_time

    # Get the path to the RDF/XML file created by OOPS for use by reasoners
    rdfxml_path = pitfall_reviewer.last_rdfxml_path

    pitfall_data = parse_oops_response(pitfall_result)
    has_pitfalls = pitfall_data.get("has_pitfalls", False)
    pitfall_count = pitfall_data.get("pitfall_count", 0)

    validation_results["oops"] = {
        "has_pitfalls": has_pitfalls,
        "pitfall_count": pitfall_count,
        "execution_time_seconds": round(oops_time_seconds, 3),
        "pitfalls": pitfall_data.get("pitfalls", []),
    }

    # Log to file with complete pitfall details
    pitfalls_list = pitfall_data.get("pitfalls", [])
    validation_logger.log_pitfall_detection(
        has_pitfalls=has_pitfalls,
        pitfall_count=pitfall_count,
        execution_time_seconds=oops_time_seconds,
        pitfalls=pitfalls_list,
    )

    # Also print summary to console

    # ============================================================
    # PILLAR 3: REASONING CONSISTENCY
    # ============================================================
    print("3️⃣  Reasoning Consistency")
    print("-" * 60)

    # Log reasoning start to file
    validation_logger.log_reasoning_start()

    # 3a. Hermit Reasoner (reads RDF/XML file created by OOPS)
    # Pass the unique rdfxml_path to prevent race conditions with concurrent runs
    hermit_validator = HermitReasonerValidator(rdfxml_path=rdfxml_path)
    hermit_result = hermit_validator.validate()
    validation_results["hermit"] = hermit_result

    # Log to file with detailed info
    validation_logger.log_reasoner_validation("Hermit", hermit_result)

    # Also print summary to console

    # 3b. Pellet Reasoner (reads RDF/XML file created by OOPS)
    # Pass the unique rdfxml_path to prevent race conditions with concurrent runs
    pellet_validator = PelletReasonerValidator(rdfxml_path=rdfxml_path)
    pellet_result = pellet_validator.validate()
    validation_results["pellet"] = pellet_result

    # Log to file with detailed info
    validation_logger.log_reasoner_validation("Pellet", pellet_result)

    # Also print summary to console

    # ============================================================
    # AGGREGATE RESULTS
    # ============================================================
    total_time_seconds = (
        syntax_time_seconds
        + oops_time_seconds
        + hermit_result["execution_time_seconds"]
        + pellet_result["execution_time_seconds"]
    )

    all_passed = (
        syntax_valid
        and not has_pitfalls
        and hermit_result["is_consistent"]
        and pellet_result["is_consistent"]
    )

    validation_results["aggregate"] = {
        "all_validators_passed": all_passed,
        "total_execution_time_seconds": round(total_time_seconds, 3),
    }

    # ============================================================
    # SAVE OUTPUTS
    # ============================================================
    print("=" * 60)
    print("SAVING OUTPUTS")
    print("=" * 60)

    # Ensure output directories exist
    set_output_directories()

    # Save ontology to ontologies folder
    final_path = f"data/output/ontologies/{story_id}_ontology_{timestamp}.owl"
    save_text_file(final_path, generated_owl)
    validation_logger.log_file_saved(final_path, "Ontology")
    print(f"✓ Ontology: {final_path}")

    # Save OOPS XML results to validations folder
    validation_xml_path = (
        f"data/output/validations/{story_id}_validation_{timestamp}.xml"
    )
    save_text_file(validation_xml_path, pitfall_result)
    validation_logger.log_file_saved(validation_xml_path, "OOPS XML results")
    print(f"✓ OOPS XML: {validation_xml_path}")

    # Save comprehensive validation results as JSON to validations folder
    validation_json_path = (
        f"data/output/validations/{story_id}_validation_{timestamp}.json"
    )
    with open(validation_json_path, "w") as f:
        json.dump(validation_results, f, indent=2)
    validation_logger.log_file_saved(validation_json_path, "Validation metrics JSON")
    print(f"✓ Validation JSON: {validation_json_path}")

    # Save scratchpad to scratchpads folder
    scratchpad_path = f"data/output/scratchpads/{story_id}_scratchpad_{timestamp}.json"
    with open(scratchpad_path, "w") as f:
        json.dump(scratchpad, f, indent=2)
    validation_logger.log_file_saved(scratchpad_path, "Agent scratchpad")
    print(f"✓ Scratchpad: {scratchpad_path}")

    # ============================================================
    # FINAL SUMMARY AND SAVE LOGS
    # ============================================================
    iteration_count = state.get("iteration_count", 0)

    # Log comprehensive summary to file
    validation_logger.log_summary(
        syntax_valid=syntax_valid,
        has_pitfalls=has_pitfalls,
        pitfall_count=pitfall_count,
        hermit_consistent=hermit_result["is_consistent"],
        pellet_consistent=pellet_result["is_consistent"],
        syntax_time_seconds=syntax_time_seconds,
        oops_time_seconds=oops_time_seconds,
        hermit_time_seconds=hermit_result["execution_time_seconds"],
        pellet_time_seconds=pellet_result["execution_time_seconds"],
        iteration_count=iteration_count,
    )

    # Save validation JSON log
    validation_logger.save_json_log()

    # Also print summary to console
    print(f"\n{'=' * 60}")
    print("VALIDATION SUMMARY")
    print(f"{'=' * 60}")
    print(
        f"1. Syntax:    {'✓ PASSED' if syntax_valid else '✗ FAILED'} ({syntax_time_seconds:.3f}s)"
    )
    print(
        f"2. OOPS:      {'✓ PASSED' if not has_pitfalls else f'⚠ {pitfall_count} pitfalls'} ({oops_time_seconds:.3f}s)"
    )
    print(
        f"3. Hermit:    {'✓ PASSED' if hermit_result['is_consistent'] else '✗ FAILED'} ({hermit_result['execution_time_seconds']:.3f}s)"
    )
    print(
        f"4. Pellet:    {'✓ PASSED' if pellet_result['is_consistent'] else '✗ FAILED'} ({pellet_result['execution_time_seconds']:.3f}s)"
    )
    print("-" * 60)
    print(f"Overall:      {'✅ ALL PASSED' if all_passed else '❌ VALIDATION FAILED'}")
    print(f"Total time:   {total_time_seconds:.3f}s")
    print(f"Iterations:   {iteration_count}")

    # Report log file locations
    log_paths = validation_logger.get_log_paths()
    print(f"\nValidation logs saved:")
    print(f"  Text log: {log_paths['text_log']}")
    print(f"  JSON log: {log_paths['json_log']}")
    print(f"{'=' * 60}\n")

    return {
        **state,
        "validation_history": state.get("validation_history", [])
        + [validation_results],
    }


def advisory_review_node(state: StateDict) -> StateDict:
    """
    Comprehensive advisory review of generated ontology.

    Reviews:
    - CQ coverage completeness
    - Constraint adherence (reification, OWL 2, etc.)
    - Quality and depth
    - Previous review suggestions (if this is iteration 2+)

    Args:
        state: Current workflow state with workspace and optional review history

    Returns:
        Updated state with review results added to review_history
    """
    story_object = state.get("story_object")
    workspace = state["workspace"][0]
    generated_owl = workspace.generated_owl
    review_history = state.get("review_history", [])
    review_iteration = state.get("review_iteration_count", 0) + 1

    print(f"\n{'=' * 60}")
    print(f"ADVISORY REVIEW - Iteration {review_iteration}")
    print(f"{'=' * 60}\n")

    if not generated_owl:
        print(f"✗ ERROR: No ontology to review!")
        return {**state, "error_message": "No ontology available for review"}

    # Build review context
    story_context = story_object.context if story_object else ""
    competency_questions = (
        story_object.competency_questions if story_object else None
    ) or []
    cq_list = "\n".join(
        [f"{i + 1}. {cq.question}" for i, cq in enumerate(competency_questions)]
    )

    # Load OWL 2 Datatype Map for reference
    owl2_datatype_map = ""
    try:
        with open("src/prompts/owl2_datatype_map.txt", "r") as f:
            owl2_datatype_map = f.read()
    except Exception as e:
        print(f"⚠ Warning: Could not load OWL 2 Datatype Map: {e}")

    context = {
        "story_text": story_context,
        "cq_list": cq_list,
        "ontology": generated_owl,
        "review_iteration": review_iteration,
        "owl2_datatype_map": owl2_datatype_map,
    }

    # Add previous review section if this is iteration 2+
    if review_history:
        prev_review = review_history[-1]
        previous_review_section = f"""
### PREVIOUS REVIEW (Iteration {review_iteration - 1})
This is refinement iteration {review_iteration}. A previous review was provided:

{json.dumps(prev_review, indent=2)}

**CRITICAL:** Evaluate whether the suggestions from the previous review were addressed:
- Which suggestions were successfully implemented?
- Which suggestions were ignored or poorly implemented?
- Did the quality and coverage scores improve?
- Were new issues introduced?
"""
        context["previous_review_section"] = previous_review_section
    else:
        context["previous_review_section"] = ""

    # Get review prompt
    review_prompt = prompt_manager.format_prompt("advisory_review", **context)

    # Single LLM call for review
    generator_model = "anthropic--claude-4.5-opus"
    llm = get_gaih_anthropic_llm(model=generator_model)

    # generator_model = "gemini-2.5-flash"
    # llm = get_gaih_google_llm(model=generator_model)

    # llm = get_gaih_openai_llm(model="gpt-4.1")

    print(f"Invoking reviewer LLM (iteration {review_iteration})...")
    review_response = llm.invoke(review_prompt)

    # Parse structured review from JSON
    try:
        # Extract JSON from response (may be wrapped in markdown)
        content = review_response.content
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0].strip()
        elif "```" in content:
            content = content.split("```")[1].split("```")[0].strip()

        review_report = json.loads(content)
        review_report["iteration"] = review_iteration
        review_report["timestamp"] = datetime.now().isoformat()

    except Exception as e:
        print(f"⚠ Warning: Could not parse review as JSON: {e}")
        review_report = {
            "iteration": review_iteration,
            "timestamp": datetime.now().isoformat(),
            "raw_review": review_response.content,
            "parse_error": str(e),
        }

    # Save review to reviews folder
    set_output_directories()  # Ensure directories exist
    # Use shared log_timestamp from state to ensure all files from this run share the same timestamp
    timestamp = state.get("log_timestamp")
    story_id = story_object.id if story_object else "unknown"
    review_path = (
        f"data/output/reviews/{story_id}_review_iter{review_iteration}_{timestamp}.json"
    )
    with open(review_path, "w") as f:
        json.dump(review_report, f, indent=2)

    print(f"✓ Review complete - Iteration {review_iteration}")
    if "cq_coverage" in review_report:
        print(
            f"  CQ Coverage Score: {review_report.get('cq_coverage', {}).get('coverage_score', 'N/A')}"
        )
    if "quality_metrics" in review_report:
        print(
            f"  Quality Score: {review_report.get('quality_metrics', {}).get('overall_score', 'N/A')}"
        )
    print(f"  Saved to: {review_path}\n")

    return {
        **state,
        "review_history": review_history + [review_report],
        "review_iteration_count": review_iteration,
        "latest_review": review_report,
    }


def review_routing_node(state: StateDict) -> StateDict:
    """
    Route workflow based on review iteration count.

    This is a pass-through node that doesn't modify state.
    The actual routing decision is made by the conditional_edges function.

    Args:
        state: Current workflow state

    Returns:
        Unchanged state
    """
    # Just return state unchanged - routing is handled by conditional_edges
    return state


def _review_routing_decision(state: StateDict) -> str:
    """
    Helper function for conditional routing decision.

    Args:
        state: Current workflow state

    Returns:
        "refine" if review_iteration_count < 2
        "validate" if review_iteration_count >= 2
    """
    review_iteration = state.get("review_iteration_count", 0)

    if review_iteration < 2:
        print(f"\n→ Routing to refinement (iteration {review_iteration}/2)\n")
        return "refine"
    else:
        print(f"\n→ Review cycle complete (2 iterations). Proceeding to validation.\n")
        return "validate"


def end_node(state: StateDict) -> StateDict:
    """
    Workflow termination with timing summary.

    Logs story duration to validation JSON log file.

    Args:
        state: Final workflow state

    Returns:
        State with story duration added
    """
    story_id = state.get("story_id", "")
    story_start_time = state.get("story_start_time")
    log_timestamp = state.get("log_timestamp")

    # Calculate story duration
    story_duration = 0.0
    if story_start_time:
        story_duration = time.time() - story_start_time

    # Log story timing to validation JSON file
    if log_timestamp:
        validation_json_path = (
            Path("logs") / f"{story_id}_validation_{log_timestamp}.json"
        )
        if validation_json_path.exists():
            try:
                with open(validation_json_path, "r", encoding="utf-8") as f:
                    validation_data = json.load(f)

                validation_data["story_timing"] = {
                    "duration_seconds": round(story_duration, 2),
                    "duration_formatted": format_duration(story_duration),
                }

                with open(validation_json_path, "w", encoding="utf-8") as f:
                    json.dump(validation_data, f, indent=2, ensure_ascii=False)
            except Exception as e:
                print(
                    f"⚠ Warning: Could not update validation log with story timing: {e}"
                )

    print(f"\n{'=' * 60}")
    print(f"✓ Workflow complete for story: {story_id}")
    print(
        f"⏱  Story duration: {story_duration:.2f}s ({format_duration(story_duration)})"
    )
    print(f"{'=' * 60}\n")

    return {
        **state,
        "story_duration_seconds": round(story_duration, 2),
        "story_duration_formatted": format_duration(story_duration),
    }
