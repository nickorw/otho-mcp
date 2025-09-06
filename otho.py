import os
from pathlib import Path
from typing import Any, Dict, List, TypedDict

import dotenv
import langgraph
from google import genai
from langgraph.graph import END, StateGraph
from rdflib import Graph

from src.models.requirement_models import CompetencyQuestion, Story
from src.prompts.prompt_manager import PromptManager
from src.reviewers.reviewer import OopsPitfallReviewer, RDFSyntaxReviewer
from src.utils.excel_processor import get_story_by_id
from src.utils.file_handler import save_text_file

###########################################
########### Foundational Setup ############
###########################################

########### Load environment variables ###########
dotenv.load_dotenv()

########### LLM Initialization ###########
llm = genai.Client()


########### LLM Call Function ###########
def call_gemini(prompt: str) -> str:
    response = llm.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )
    return response.text or ""


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


#############################
########### Nodes ###########
#############################


##### Node to load story object into state
def get_story_node(state: OntoAgentState) -> OntoAgentState:
    story_id = state.get("story_id", "")
    story = get_story_by_id(story_id)
    cqs = (
        list(story.competency_questions) if story and story.competency_questions else []
    )
    return {
        **state,
        "story_object": story,
        "unprocessed_cqs": cqs,
        "processed_owls": [],
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
    llm_response = call_gemini(prompt)
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
    combined_owl = call_gemini(combination_prompt)

    print("Combined, saving OWLs file")
    save_text_file(f"data/output/{story_id}_combined_turtle.owl", combined_owl)
    return {**state, "combined_owl": combined_owl}


##### Node to validate the combined OWL for the story
def validate_combined_owl_node(state: OntoAgentState) -> OntoAgentState:
    pitfall_reviewer = OopsPitfallReviewer()
    syntax_reviewer = RDFSyntaxReviewer()

    try:
        print("Validating combined OWL for Story ID:", state.get("story_id", ""))

        combined_owl = state.get("combined_owl", "")

        ## Print for troubleshooting
        # print("First 5 lines of combined OWL:")
        # for line in combined_owl.splitlines()[:5]:
        #     print(line)

        ## File save for troubleshooting
        # story_id = state.get("story_id", "")
        # save_text_file(f"data/output/{story_id}_combined_turtle.owl", combined_owl)

        syntax_validation_result = syntax_reviewer.review_owl_content(combined_owl)

        
        print("Syntax Validation Result:", syntax_validation_result)
        
        
        # Convert Turtle to RDF/XML to use in Oops! (Usually insider reviewer.py, but here while Oops! API issues are being resolved)
        try:
            print("Converting OWL content to RDF/XML format for OOPs! API.")
            g = Graph()
            g.parse(data=combined_owl, format="turtle")
            owl_content_xml = g.serialize(format="xml")
            

        except Exception as e:
            raise ValueError(f"Failed to convert Turtle to RDF/XML: {e}")

        print("Saving XML OWL")
        save_text_file("data/output/xml_combined_owl.xml", owl_content_xml)

        # Validate Pitfalls using XML file
        owl_file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data", "output", "xml_combined_owl.xml")
        pitfall_validation_result = pitfall_reviewer.review_owl_file(
            owl_file_path="data/output/xml_combined_owl.xml",
            output_format="XML",
        )
        print("Pitfall Validation Result:", pitfall_validation_result)

        # Commented while troubleshooting Oops! API issues with XML formatting
      

        validation_result = f"Syntax Check: {syntax_validation_result}\nPitfall Check: {pitfall_validation_result}"
        print("Combined OWL validation result:", validation_result)
        
        # Validation result save for auditing
        save_text_file(
            f"data/output/{story_id}_combined_oops_result.xml", validation_result
        )
        return {
            **state,
            "combined_validation": validation_result,
            "combined_validation_ok": True,
        }

    except Exception as e:
        print("Combined OWL validation exception:",str(e))
        return {**state, "combined_validation": str(e), "combined_validation_ok": False}


def end_node(state: OntoAgentState) -> OntoAgentState:
    print(f"Workflow complete for story {state.get('story_id', '')}")
    return state

########### Branches ###########

def validate_and_store_owl_branch(state: OntoAgentState) -> str:
    unprocessed_cqs = state.get("unprocessed_cqs", [])
    return "generate_owl" if len(unprocessed_cqs) > 0 else "combine_owls"


def validate_combined_owl_branch(state: OntoAgentState) -> str:
    return "end" if state.get("combined_validation_ok", False) else "combine_owls"


###################################
########### Graph Nodes ###########
###################################

graph = StateGraph(state_schema=OntoAgentState)
graph.add_node("get_story", get_story_node)
graph.add_node("generate_owl", generate_owl_node)
graph.add_node("validate_and_store_owl", validate_and_store_owl_node)
graph.add_node("combine_owls", combine_owls_node)
graph.add_node("validate_combined_owl", validate_combined_owl_node)
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

graph.set_finish_point("end")

########################################
########### Run the workflow ###########
########################################

if __name__ == "__main__":
    # Requesting which Story to process from user
    # story_id = input(
    #     "Please enter the Story ID to process (e.g., FestS, MusicS or HospitalS): "
    # )

    # Test code to speed up testing
    story_id = "MusicS"  # Example story ID for testing

    print(f"Starting ontology workflow for Story ID: {story_id}\n")
    initial_state: OntoAgentState = {"story_id": story_id}
    app = graph.compile()


    
    # Alternate startup with recursion limit. TODO: Streamline workflow to reduce recursions.
    app.invoke(initial_state, config={"recursion_limit": 125})
