import argparse
import os
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, TypedDict

import dotenv
import langgraph
from langchain_core.messages import HumanMessage
from langchain_core.runnables import RunnableConfig
from langgraph.graph import END, StateGraph
from langgraph.prebuilt import create_react_agent
from rdflib import Graph

from src.agents.nodes import (
    _review_routing_decision,
    advisory_review_node,
    end_node,
    get_story_node,
    ontology_generation_agent,
    review_routing_node,
    validate_and_save_node,
)
from src.agents.workspace import AgentWorkspace
from src.models.requirement_models import Story
from src.utils.file_handler import load_story_owl
from src.utils.timing import format_duration

###########################################
########### Foundational Setup ############
###########################################

########### Load environment variables ###########
dotenv.load_dotenv()


########### Langgraph Workflow State ###########
class OntoAgentState(TypedDict, total=False):
    # Input
    story_id: str
    story_object: Story

    # Shared mutable workspace (class instance wrapped in list)
    workspace: List[AgentWorkspace]  # [workspace_instance]

    # Metadata
    validation_history: List[Dict]  # Track all validation attempts
    iteration_count: int  # How many times agent validated internally
    error_message: str  # For catastrophic failures

    # Review-refinement loop metadata
    review_iteration_count: int  # Number of review-refinement cycles
    review_history: List[Dict]  # All review reports
    latest_review: Dict[str, Any]  # Most recent review for refinement context

    # Logging and timing - shared across workflow nodes
    log_timestamp: str  # Shared timestamp for all logs in this run
    generator_iteration: int  # Track generator iteration for logging
    story_start_time: float  # Start time for duration calculation
    story_duration_seconds: float  # Final story duration
    story_duration_formatted: str  # Human-readable duration


# Nodes are now imported from src.agents.nodes


###################################
########### Graph Nodes ###########
###################################

graph = StateGraph(state_schema=OntoAgentState)
graph.add_node("get_story", get_story_node)
graph.add_node("ontology_generation_agent", ontology_generation_agent)
graph.add_node("advisory_review", advisory_review_node)
graph.add_node("review_routing", review_routing_node)
graph.add_node("validate_and_save", validate_and_save_node)
graph.add_node("end", end_node)

######################################
########### Graph workflow ###########
######################################

# Linear start: load story → initial generation
graph.set_entry_point("get_story")
graph.add_edge("get_story", "ontology_generation_agent")

# Review-refinement loop (2 iterations)
graph.add_edge("ontology_generation_agent", "advisory_review")
graph.add_edge("advisory_review", "review_routing")

# Conditional routing based on iteration count
graph.add_conditional_edges(
    "review_routing",
    _review_routing_decision,  # Helper function returns string for routing
    {
        "refine": "ontology_generation_agent",  # Loop back for refinement
        "validate": "validate_and_save",  # Proceed to final validation
    },
)

# Final validation and termination
graph.add_edge("validate_and_save", "end")
graph.add_edge("end", END)

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
        "--benchmark",
        type=int,
        metavar="N",
        help="Run all stories (MusicS, HospitalS, FestS) N times for benchmarking.",
    )
    parser.add_argument(
        "--repeat",
        type=int,
        metavar="N",
        help="Run the specified story N times without sharing context between runs.",
    )

    args = parser.parse_args()

    # Compile the workflow graph
    app = graph.compile()
    app_config: RunnableConfig = {"recursion_limit": 200}

    # Benchmark mode: run all stories N times
    if args.benchmark:
        stories = ["MusicS", "HospitalS", "FestS"]
        print(f"BENCHMARK MODE: Running all stories {args.benchmark} time(s)\n")

        benchmark_start = time.time()
        iteration_times = []

        for iteration in range(1, args.benchmark + 1):
            iteration_start = time.time()
            print(
                f"\n{'/\\' * 60}\nBENCHMARK ITERATION {iteration}/{args.benchmark}\n{'\\/' * 60}"
            )

            for story_id in stories:
                print(f"\nProcessing: {story_id}")
                initial_state: OntoAgentState = {"story_id": story_id}
                app.invoke(initial_state, config=app_config)

            iteration_duration = time.time() - iteration_start
            iteration_times.append(iteration_duration)
            print(
                f"\n⏱  Iteration {iteration} completed in {format_duration(iteration_duration)}"
            )

        # Print benchmark summary
        total_duration = time.time() - benchmark_start
        avg_iteration = (
            sum(iteration_times) / len(iteration_times) if iteration_times else 0
        )
        print(f"\n{'#' * 60}")
        print(f"BENCHMARK COMPLETE")
        print(f"{'#' * 60}")
        print(f"Total time: {format_duration(total_duration)}")
        print(f"Iterations: {args.benchmark}")
        print(f"Avg per iteration: {format_duration(avg_iteration)}")
        print(f"{'#' * 60}\n")

    # Repeat mode: run single story N times without sharing context
    elif args.repeat:
        story_id = args.story_id
        print(
            f"REPEAT MODE: Running story '{story_id}' {args.repeat} time(s) without shared context\n"
        )

        for iteration in range(1, args.repeat + 1):
            print(
                f"\n{'=' * 60}\nSINGLE STORY RUN {iteration}/{args.repeat} - {story_id}\n{'=' * 60}"
            )

            # Each invocation gets a fresh state with no shared context
            initial_state: OntoAgentState = {"story_id": story_id}
            app.invoke(initial_state, config=app_config)

    # Single story mode
    else:
        story_id = args.story_id
        print(f"Starting ontology workflow for Story ID: {story_id}\n")

        initial_state: OntoAgentState = {"story_id": story_id}
        app.invoke(initial_state, config=app_config)
