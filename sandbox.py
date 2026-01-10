########################################################################################
############ Sandbox for testing various functionalities in the Otho project - NOTHING HERE IS TO BE USED BY AI ASSISTANTS(Copilot, Cline, others)###########
########################################################################################

import os
import traceback
from pathlib import Path

import dotenv
from google import genai
from google.genai import types

from src.prompts.prompt_manager import PromptManager
from src.reviewers.reviewer import OopsPitfallReviewer, RDFSyntaxReviewer
from src.utils.excel_processor import get_story_by_id
from src.utils.file_handler import save_text_file

dotenv.load_dotenv()

# Initialize Gemini client with API key from environment variable
gemini_client = genai.Client()

prompt_manager = PromptManager(prompts_file_path=Path("src/prompts/prompts.yaml"))


def call_gemini(prompt: str) -> str:
    response = gemini_client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )

    return response.text or ""


if __name__ == "__main__":
    # Get story by ID, populating into Story object
    story_id = "FestS"
    story = get_story_by_id(story_id)

    # # Print story & cqs
    # print(f"Story ID: {story.id}")
    # print(f"Story Text: {story.context}")
    # if story.competency_questions:
    #     for cq in story.competency_questions:
    #         print(f"{cq.id}: {cq.question}")

    #################################### Prompt manager test
    # if story.competency_questions:

    #     structured_prompt = prompt_manager.get_structured_prompt("otho_memless_cq_by_cq")
    #     # Use the 'task' field as the main prompt template
    #     prompt = structured_prompt['task'].format(
    #         story=story.context,
    #         CQ=story.competency_questions[0].question
    #     )
    #     print("\nPrompt sent to Gemini (otho_memless_cq_by_cq):\n", prompt)
    #     llm_response = call_gemini(prompt)
    #     print("\nGemini response:\n", llm_response)
    #     # Save LLM response to a text file in data/output
    #     output_path = f"data/output/{story_id}_llm_response.txt"
    #     save_text_file(output_path, llm_response)
    #     print(f"LLM response saved to {output_path}")

    ####################################  Path to the OWL file to validate
    # owl_file_path = "data/output/FestS_combined.owl"

    # with open(owl_file_path, "r", encoding="utf-8") as f:
    #     owl_content = f.read()

    #################################### OWL Syntax Validator instantiation
    reviewer = RDFSyntaxReviewer(
        format="turtle"
    )  # Use "xml" for RDF/XML, "turtle" for Turtle, etc.

    #################################### OWL Syntax Validation Test
    # try:
    #     result = reviewer.review_owl_content(owl_content)
    #     print(f"RDF Syntax Valid: {result == 'OK'}")
    # except Exception as e:
    #     print("RDF Syntax Error:", e)
    #     print("Full exception details:")
    #     traceback.print_exc()

    #################################### Combination Prompt Test
    # structured_prompt = prompt_manager.get_structured_prompt("combine_owl_codes")
    # prompt = structured_prompt['user_template'].format(
    #     story_id="FestS",
    #     story="",
    #     snippets=owl_content,

    # )
    # output_path = f"data/output/prompt_{story_id}_agent_combined_OWL2.txt"
    # save_text_file(output_path, prompt)
    # llm_response = call_gemini(prompt)
    # # Save LLM response to a text file in data/output
    # output_path = f"data/output/{story_id}_agent_combined_OWL2.txt"
    # save_text_file(output_path, llm_response)

    #################################### Syntax Check File #################################
    # reviewer = RDFSyntaxReviewer()
    # try:
    #     syntax_review_result = reviewer.review_owl_content(owl_content)
    #     validation_successful = syntax_review_result == "OK"
    #     print("Validation successful: ", validation_successful)

    # except Exception as e:
    #     print(f"Exception during RDF validation: {e}")


############## Node test for validation of OWL
def validate_combined_owl_node():
    reviewer = OopsPitfallReviewer()
    try:
        with open(
            "data/output/backup/FestS_combined_turtle.owl", "r", encoding="utf-8"
        ) as f:
            combined_owl = f.read()
        validation_result = reviewer.review_owl_content(combined_owl)
        save_text_file(
            f"data/output/debug_FestS_combined_oops_result.xml", validation_result
        )
        print("Combined OWL validation result:", validation_result)
        print("Combined OWL validation ran successfully")

    except Exception as e:
        print("Validation failed, result: ", str(e))


validate_combined_owl_node()
