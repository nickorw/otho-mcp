"""
StateGraph node implementations for Otho agent workflow.

This module contains all node functions for the self-validating React agent
workflow, including the main ontology generation agent and validation nodes.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, TypedDict

from langchain.tools import tool
from langchain_core.messages import HumanMessage
from langgraph.prebuilt import create_react_agent

from src.agents.tools import check_pitfalls_tool, validate_syntax_tool
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
from src.utils.llm_manager import get_gaih_openai_llm
from src.utils.oops_parser import parse_oops_response

# Initialize prompt manager
prompt_manager = PromptManager(prompts_file_path=Path("src/prompts/prompts.yaml"))


# Type alias for state (will match OntoAgentState from otho.py)
StateDict = Dict[str, Any]


def get_story_node(state: StateDict) -> StateDict:
    """
    Load story object and initialize workspace.

    This is the entry point of the workflow. It loads the story from the
    Excel dataset and creates a fresh AgentWorkspace for the agent to use.

    Args:
        state: Current workflow state containing story_id

    Returns:
        Updated state with story_object and initialized workspace
    """
    story_id = state.get("story_id", "")
    print(f"\n{'=' * 60}")
    print(f"Loading Story: {story_id}")
    print(f"{'=' * 60}\n")

    story = get_story_by_id(story_id)

    # Create new AgentWorkspace instance
    workspace = AgentWorkspace()

    print(f"✓ Story loaded: {story.context[:100]}...")
    print(f"✓ Competency questions: {len(story.competency_questions or [])}")
    print(f"✓ Workspace initialized\n")

    return {
        **state,
        "story_object": story,
        "workspace": [workspace],  # Wrap in list for state mutability pattern
        "iteration_count": 0,
        "validation_history": [],
    }


def create_agent_tools(workspace: AgentWorkspace) -> List:
    """
    Create tool instances with access to shared workspace.

    Tools modify the workspace object which is shared between the node and agent.
    This pattern allows mutation while respecting LangGraph's immutable state.

    Args:
        workspace: AgentWorkspace instance that tools will modify

    Returns:
        List of tool instances for the React agent
    """

    @tool
    def update_scratchpad(key: str, value: Any) -> Dict[str, bool]:
        """
        Update agent's persistent working memory (scratchpad).

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
        Read from agent's persistent working memory (scratchpad).

        Use this to review your previous plans, decisions, and drafts.

        Args:
            key: The scratchpad key to read

        Returns:
            The value stored at that key, or None if not found

        Example:
            plan = read_scratchpad("plan")
            previous_iterations = read_scratchpad("iterations")
        """
        return workspace.get_scratchpad(key)

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

    # Return all 5 tools
    return [
        update_scratchpad,
        read_scratchpad,
        validate_syntax_tool,
        check_pitfalls_tool,
        save_final_ontology,
    ]


def ontology_generation_agent(state: StateDict) -> StateDict:
    """
    React agent generates and self-validates ontology.

    The agent will:
    1. Plan the ontology structure (using update_scratchpad)
    2. Verify CQ coverage (using update_scratchpad)
    3. Generate OWL code directly (not via tool)
    4. Validate syntax (using validate_syntax_tool)
    5. Check pitfalls (using check_pitfalls_tool)
    6. Iterate and fix issues until validation passes
    7. Save final ontology (using save_ontology_draft tool)

    Maximum 10 iterations to prevent infinite loops.

    Args:
        state: Current workflow state with story_object and workspace

    Returns:
        Updated state with agent results
    """
    story_object = state.get("story_object")
    story_id = story_object.id if story_object else ""

    print(f"\n{'=' * 60}")
    print(f"Starting React Agent for Story ID: {story_id}")
    print(f"{'=' * 60}\n")

    # Extract story context and competency questions
    story_context = story_object.context if story_object else ""
    competency_questions = (
        story_object.competency_questions if story_object else None
    ) or []

    # Format competency questions as text
    cq_list = "\n".join(
        [f"{i + 1}. {cq.question}" for i, cq in enumerate(competency_questions)]
    )

    print(f"Story context length: {len(story_context)} characters")
    print(f"Number of CQs: {len(competency_questions)}\n")

    # Get the base prompt from PromptManager
    prompt = prompt_manager.format_prompt(
        "generate_ontology", story_text=story_context, cq_list=cq_list
    )

    # Get workspace reference
    workspace = state["workspace"][0]

    # Create tools with workspace reference
    tools = create_agent_tools(workspace)

    tool_names = [tool.name for tool in tools]
    print(f"Created {len(tools)} tools for agent:")
    for tool_name in tool_names:
        print(f"  - {tool_name}")
    print()

    # Initialize comprehensive logger
    agent_logger = AgentLogger(story_id=story_id, log_dir="logs")
    agent_logger.log_agent_start(
        prompt_length=len(prompt), num_tools=len(tools), tool_names=tool_names
    )

    # Get LLM for React agent
    llm = get_gaih_openai_llm(model="gpt-4.1")

    # Create React agent
    agent_logger.logger.info("Creating React agent with tools...")
    agent_executor = create_react_agent(llm, tools)

    # Configure recursion limit
    config = {"recursion_limit": 100}

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
    print(f"\n{'=' * 60}")
    print("AGENT EXECUTION SUMMARY")
    print(f"{'=' * 60}")
    print(f"✓ Tool calls made: {len(agent_logger.json_data['tool_calls'])}")
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

    print(f"\n{'=' * 60}")
    print(f"FINAL VALIDATION AND SAVE TO DISK FOR {story_id}")
    print(f"{'=' * 60}\n")

    # Final syntax check
    print("Running final syntax validation...")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
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
    import time

    start_time = time.time()
    syntax_result = RDFSyntaxReviewer().review_owl_content(generated_owl)
    syntax_time_ms = int((time.time() - start_time) * 1000)
    syntax_valid = syntax_result == "OK"

    validation_results["syntax"] = {
        "valid": syntax_valid,
        "execution_time_ms": syntax_time_ms,
        "error": None if syntax_valid else syntax_result,
    }

    if syntax_valid:
        print(f"✓ Syntax validation PASSED ({syntax_time_ms}ms)\n")
    else:
        print(f"✗ Syntax validation FAILED ({syntax_time_ms}ms)")
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
    pitfall_result = pitfall_reviewer.review_owl_content(
        owl_content=generated_owl, pitfalls=pitfalls, output_format="XML"
    )
    oops_time_ms = int((time.time() - start_time) * 1000)

    pitfall_data = parse_oops_response(pitfall_result)
    has_pitfalls = pitfall_data.get("has_pitfalls", False)
    pitfall_count = pitfall_data.get("pitfall_count", 0)

    validation_results["oops"] = {
        "has_pitfalls": has_pitfalls,
        "pitfall_count": pitfall_count,
        "execution_time_ms": oops_time_ms,
        "pitfalls": pitfall_data.get("pitfalls", []),
    }

    if not has_pitfalls:
        print(f"✓ Pitfall check PASSED - No pitfalls detected ({oops_time_ms}ms)\n")
    else:
        print(f"⚠ Pitfall check: Found {pitfall_count} pitfall(s) ({oops_time_ms}ms)")
        pitfall_codes = [p.get("code", "") for p in pitfall_data.get("pitfalls", [])]
        print(f"  Pitfalls: {', '.join(pitfall_codes)}\n")

    # ============================================================
    # PILLAR 3: REASONING CONSISTENCY
    # ============================================================
    print("3️⃣  Reasoning Consistency")
    print("-" * 60)

    # 3a. Hermit Reasoner (reads RDF/XML file created by OOPS)
    print("  → Hermit Reasoner...")
    hermit_validator = HermitReasonerValidator()
    hermit_result = hermit_validator.validate()

    validation_results["hermit"] = hermit_result

    if hermit_result["is_consistent"]:
        print(
            f"    ✓ PASSED - Ontology is consistent ({hermit_result['execution_time_ms']}ms)"
        )
    else:
        print(
            f"    ✗ FAILED - Inconsistencies detected ({hermit_result['execution_time_ms']}ms)"
        )
        if hermit_result.get("inconsistent_classes"):
            print(f"    Inconsistent classes: {hermit_result['inconsistent_classes']}")
        if hermit_result.get("error"):
            print(f"    Error: {hermit_result['error']}")

    # 3b. Pellet Reasoner (reads RDF/XML file created by OOPS)
    print("\n  → Pellet Reasoner...")
    pellet_validator = PelletReasonerValidator()
    pellet_result = pellet_validator.validate()

    validation_results["pellet"] = pellet_result

    if pellet_result["is_consistent"]:
        print(
            f"    ✓ PASSED - Ontology is consistent ({pellet_result['execution_time_ms']}ms)\n"
        )
    else:
        print(
            f"    ✗ FAILED - Inconsistencies detected ({pellet_result['execution_time_ms']}ms)"
        )
        if pellet_result.get("inconsistent_classes"):
            print(f"    Inconsistent classes: {pellet_result['inconsistent_classes']}")
        if pellet_result.get("error"):
            print(f"    Error: {pellet_result['error']}\n")

    # ============================================================
    # AGGREGATE RESULTS
    # ============================================================
    total_time_ms = (
        syntax_time_ms
        + oops_time_ms
        + hermit_result["execution_time_ms"]
        + pellet_result["execution_time_ms"]
    )

    all_passed = (
        syntax_valid
        and not has_pitfalls
        and hermit_result["is_consistent"]
        and pellet_result["is_consistent"]
    )

    validation_results["aggregate"] = {
        "all_validators_passed": all_passed,
        "total_execution_time_ms": total_time_ms,
    }

    # ============================================================
    # SAVE OUTPUTS
    # ============================================================
    print("=" * 60)
    print("SAVING OUTPUTS")
    print("=" * 60)

    # Save ontology
    final_path = f"data/output/{story_id}_ontology_{timestamp}.owl"
    save_text_file(final_path, generated_owl)
    print(f"✓ Ontology saved to: {final_path}")

    # Save OOPS XML results
    validation_path = f"data/output/{story_id}_validation_{timestamp}.xml"
    save_text_file(validation_path, pitfall_result)
    print(f"✓ OOPS results: {validation_path}")

    # Save comprehensive validation results as JSON
    validation_json_path = f"data/output/{story_id}_validation_{timestamp}.json"
    with open(validation_json_path, "w") as f:
        json.dump(validation_results, f, indent=2)
    print(f"✓ Validation metrics: {validation_json_path}")

    # Save scratchpad
    scratchpad_path = f"data/output/{story_id}_scratchpad_{timestamp}.json"
    with open(scratchpad_path, "w") as f:
        json.dump(scratchpad, f, indent=2)
    print(f"✓ Scratchpad: {scratchpad_path}")

    # ============================================================
    # FINAL REPORT
    # ============================================================
    print(f"\n{'=' * 60}")
    print("VALIDATION SUMMARY")
    print(f"{'=' * 60}")
    print(
        f"1. Syntax:    {'✓ PASSED' if syntax_valid else '✗ FAILED'} ({syntax_time_ms}ms)"
    )
    print(
        f"2. OOPS:      {'✓ PASSED' if not has_pitfalls else f'⚠ {pitfall_count} pitfalls'} ({oops_time_ms}ms)"
    )
    print(
        f"3. Hermit:    {'✓ PASSED' if hermit_result['is_consistent'] else '✗ FAILED'} ({hermit_result['execution_time_ms']}ms)"
    )
    print(
        f"4. Pellet:    {'✓ PASSED' if pellet_result['is_consistent'] else '✗ FAILED'} ({pellet_result['execution_time_ms']}ms)"
    )
    print("-" * 60)
    print(f"Overall:      {'✅ ALL PASSED' if all_passed else '❌ VALIDATION FAILED'}")
    print(f"Total time:   {total_time_ms}ms ({total_time_ms / 1000:.2f}s)")
    print(f"Iterations:   {state.get('iteration_count', 0)}")
    print(f"{'=' * 60}\n")

    return {
        **state,
        "validation_history": state.get("validation_history", [])
        + [validation_results],
    }


def end_node(state: StateDict) -> StateDict:
    """
    Workflow termination.

    Args:
        state: Final workflow state

    Returns:
        Unchanged state
    """
    print(f"\n✓ Workflow complete for story {state.get('story_id', '')}\n")
    return state
