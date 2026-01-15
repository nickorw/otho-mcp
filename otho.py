import argparse
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, TypedDict

import dotenv
import langgraph
from langchain_core.messages import HumanMessage
from langgraph.graph import END, StateGraph
from langgraph.prebuilt import create_react_agent
from rdflib import Graph

from src.agents.nodes import (
    end_node,
    get_story_node,
    ontology_generation_agent,
    validate_and_save_node,
)
from src.agents.workspace import AgentWorkspace
from src.models.requirement_models import Story
from src.utils.file_handler import load_story_owl

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


# Nodes are now imported from src.agents.nodes


###################################
########### Graph Nodes ###########
###################################

graph = StateGraph(state_schema=OntoAgentState)
graph.add_node("get_story", get_story_node)
graph.add_node("ontology_generation_agent", ontology_generation_agent)
graph.add_node("validate_and_save", validate_and_save_node)
graph.add_node("end", end_node)

######################################
########### Graph workflow ###########
######################################

graph.set_entry_point("get_story")
graph.add_edge("get_story", "ontology_generation_agent")
graph.add_edge("ontology_generation_agent", "validate_and_save")
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

    args = parser.parse_args()

    # Compile the workflow graph
    app = graph.compile()

    # Benchmark mode: run all stories N times
    if args.benchmark:
        stories = ["MusicS", "HospitalS", "FestS"]
        print(f"BENCHMARK MODE: Running all stories {args.benchmark} time(s)\n")

        for iteration in range(1, args.benchmark + 1):
            print(f"\n{'=' * 60}\nITERATION {iteration}/{args.benchmark}\n{'=' * 60}")

            for story_id in stories:
                print(f"\nProcessing: {story_id}")
                initial_state: OntoAgentState = {"story_id": story_id}
                app.invoke(initial_state)

    # Single story mode
    else:
        story_id = args.story_id
        print(f"Starting ontology workflow for Story ID: {story_id}\n")

        initial_state: OntoAgentState = {"story_id": story_id}
        app.invoke(initial_state)
