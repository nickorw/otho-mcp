import dotenv
import os
from src.utils.excel_processor import get_story_by_id
from src.prompts.prompt_manager import PromptManager
from src.utils.file_handler import save_text_file
from src.reviewers.reviewer import OopsPitfallReviewer, RDFSyntaxReviewer
from src.models.requirement_models import Story
from src.models.requirement_models import CompetencyQuestion
from google import genai
import langgraph
from langgraph.graph import StateGraph, END
from typing import Dict, Any, List, TypedDict

dotenv.load_dotenv()
llm = genai.Client()
def call_gemini(prompt: str) -> str:
    response = llm.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )
    return response.text
prompt_manager = PromptManager(prompts_file_path="src/prompts/prompts.yaml")

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

# --- Node functions ---
def get_story_node(state: OntoAgentState) -> OntoAgentState:
    story_id = state["story_id"]
    story = get_story_by_id(story_id)
    return {
        **state,
        "story_object": story,
        "unprocessed_cqs": list(story.competency_questions),
        "processed_owls": [],
    }

def generate_owl_node(state: OntoAgentState) -> OntoAgentState:
    error_message = state.get("error_message", "")
    invalid_owl = state.get("invalid_owl", "")
    print(f"Generating OWL for CQ ID: {state['unprocessed_cqs'][0].id}")
    if error_message:
        print(f"Previous validation error: {error_message}")
        # Optionally, include error_message and invalid_owl in the prompt for the LLM
        prompt = (
            prompt_manager.get_structured_prompt("otho_memless_cq_by_cq")["task"].format(
                story=state["story_object"].context,
                CQ=state["unprocessed_cqs"][0].question
            )
            + f"\n\nPrevious error: {error_message}\nInvalid OWL:\n{invalid_owl}\nPlease fix and regenerate."
        )
    else:
        prompt = prompt_manager.get_structured_prompt("otho_memless_cq_by_cq")["task"].format(
            story=state["story_object"].context,
            CQ=state["unprocessed_cqs"][0].question
        )
    llm_response = call_gemini(prompt)
    owl_code = llm_response.text if hasattr(llm_response, 'text') else llm_response
    # Determine a unique filename to avoid overwriting
    base_path = f"data/output/{state['story_id']}_{state['unprocessed_cqs'][0].id}_pre_validation"
    ext = ".owl"
    file_path = base_path + ext
    counter = 2
    while os.path.exists(file_path):
        file_path = f"{base_path}_{counter}{ext}"
        counter += 1
    save_text_file(file_path, owl_code)
    return {
        **state,
        "current_cq": state["unprocessed_cqs"][0],
        "current_owl": owl_code,
        "error_message": "",  # Clear error after new attempt
        "invalid_owl": "",
    }

def validate_owl_node(state: OntoAgentState) -> OntoAgentState:
    reviewer = RDFSyntaxReviewer()
    print("Validating CQ ID:", state["current_cq"].id)
    try:
        validation_result = reviewer.review_owl_content(state["current_owl"])
        validation_successful = validation_result == "OK"
        if not validation_successful:
            print("Validation error for", state["current_cq"].id, ":", validation_result)
        else:
            print("Validation successful: ", validation_successful)
        return {
            **state,
            "current_validation": validation_result,
            "validation_ok": validation_successful,
            "error_message": validation_result if not validation_successful else "",
            "invalid_owl": state["current_owl"] if not validation_successful else "",
        }
    except Exception as e:
        print(f"Exception during RDF validation for {state['current_cq'].id}: {e}")
        return {
            **state,
            "current_validation": str(e),
            "validation_ok": False,
            "error_message": str(e),
            "invalid_owl": state["current_owl"],
        }
  
def store_owl_node(state: OntoAgentState) -> OntoAgentState:
    story_id = state["story_id"]
    cq = state["current_cq"]
    owl_code = state["current_owl"]
    processed_owls = state["processed_owls"] + [(cq.id, owl_code)]
    print("Storing CQ ID:", cq.id)
    save_text_file(f"data/output/{story_id}_{cq.id}.owl", owl_code)
    unprocessed_cqs = state["unprocessed_cqs"][1:]
    return {
        **state,
        "processed_owls": processed_owls,
        "unprocessed_cqs": unprocessed_cqs
    }

def combine_owls_node(state: OntoAgentState) -> OntoAgentState:
    print("Combining OWLs for Story ID:", state["story_id"])
    story_id = state["story_id"]
    concatenated_owl = "\n".join([owl for _, owl in state["processed_owls"]])
    save_text_file(f"data/output/{story_id}_concat.owl", concatenated_owl)

    structured_prompt = prompt_manager.get_structured_prompt("combine_owl_codes")
    combination_prompt = structured_prompt['user_template'].format(
        story_id="FestS",
        story="",
        snippets=concatenated_owl,
    
    )
    output_path = f"data/output/prompt_{story_id}_agent_combined_OWL2.txt"
    save_text_file(output_path, combination_prompt)
    combined_owl = call_gemini(combination_prompt)

    return {
        **state,
        "combined_owl": combined_owl
    }

def validate_combined_owl_node(state: OntoAgentState) -> OntoAgentState:
    reviewer = OopsPitfallReviewer()
    try:
        print("Validating combined OWL for Story ID:", state["story_id"])            
        validation_result = reviewer.review_owl_content(state["combined_owl"])
        save_text_file(f"data/output/{state['story_id']}_combined_oops_result.xml", validation_result)
        return {
            **state,
            "combined_validation": validation_result,
            "combined_validation_ok": True
        }
    except Exception as e:
        return {
            **state,
            "combined_validation": str(e),
            "combined_validation_ok": False
        }

def end_node(state: OntoAgentState) -> OntoAgentState:
    print(f"Workflow complete for story {state['story_id']}")
    return state

def validate_owl_branch(state: OntoAgentState) -> str:
    return 'store_owl' if state["validation_ok"] else 'generate_owl'

def store_owl_branch(state: OntoAgentState) -> str:
    return 'generate_owl' if len(state["unprocessed_cqs"]) > 0 else 'combine_owls'

def validate_combined_owl_branch(state: OntoAgentState) -> str:
    return 'end' if state["combined_validation_ok"] else 'combine_owls'

# --- Graph definition ---
graph = StateGraph(state_schema=OntoAgentState)
graph.add_node('get_story', get_story_node)
graph.add_node('generate_owl', generate_owl_node)
graph.add_node('validate_owl', validate_owl_node)
graph.add_node('store_owl', store_owl_node)
graph.add_node('combine_owls', combine_owls_node)
graph.add_node('validate_combined_owl', validate_combined_owl_node)
graph.add_node('end', end_node)

graph.set_entry_point('get_story')

graph.add_edge('get_story', 'generate_owl')
graph.add_edge('generate_owl', 'validate_owl')
graph.add_conditional_edges('validate_owl', validate_owl_branch)
graph.add_conditional_edges('store_owl', store_owl_branch)
graph.add_edge('combine_owls', 'validate_combined_owl')
graph.add_conditional_edges('validate_combined_owl', validate_combined_owl_branch)

graph.set_finish_point('end')
# --- Run the workflow ---
if __name__ == "__main__":
    # Prod Code requesting input from user
    # story_id = input("Please enter the Story ID to process (e.g., FestS, MusicS or HospitalS): ")

    # Test code to speed up testing
    story_id = "FestS"  # Example story ID for testing

    print(f"Starting ontology workflow for Story ID: {story_id}\n")
    initial_state: OntoAgentState = {"story_id": story_id}
    app = graph.compile()
   
    app.invoke(initial_state, config={"recursion_limit": 125})
