"""
LLM Manager Module

This module handles all LLM initialization and calling logic for the Otho project.
It supports multiple LLM providers including Gemini (direct and via GenAIHub),
OpenAI (via GenAIHub), and Anthropic (via GenAIHub).
"""

import os
from typing import Optional

import dotenv
from gen_ai_hub.proxy.core import get_proxy_client
from gen_ai_hub.proxy.langchain import init_llm
from gen_ai_hub.proxy.langchain.openai import ChatOpenAI
from gen_ai_hub.proxy.native.google_vertexai.clients import GenerativeModel
from google import genai

###########################################
########### LLM Initialization ############
###########################################

# Load environment variables
dotenv.load_dotenv()

# Initialize LLM clients
llm_gemini = genai.Client()
proxy_client = get_proxy_client("gen-ai-hub")


###########################################
########### LLM Call Functions ############
###########################################


def call_gemini(prompt: str) -> str:
    """
    Call Gemini directly using the Google GenAI SDK.

    Args:
        prompt: The prompt text to send to the model

    Returns:
        The model's response as a string
    """
    response = llm_gemini.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )
    return str(response.text)


def call_gen_ai_hub(model: str, prompt: str) -> str:
    """
    Call a model via GenAIHub using the native Google Vertex AI client.

    Args:
        model: The model name to use
        prompt: The prompt text to send to the model

    Returns:
        The model's raw response as a string
    """
    kwargs = dict({"model_name": model})
    llm = GenerativeModel(proxy_client=proxy_client, **kwargs)
    content = [{"role": "user", "parts": [{"text": prompt}]}]
    return str(llm.generate_content(content)._raw_response)


def call_gaih_google(model: str, prompt: str) -> str:
    """
    Call a Google model via GenAIHub.

    Args:
        model: The model name to use
        prompt: The prompt text to send to the model

    Returns:
        The model's raw response as a string
    """
    kwargs = dict({"model_name": model})
    llm = GenerativeModel(proxy_client=proxy_client, **kwargs)
    content = [{"role": "user", "parts": [{"text": prompt}]}]
    llm_call = llm.generate_content(content)._raw_response
    response = llm_call.candidates[0].content.parts[0].text
    return str(response)


def call_gaih_openai(model: str, prompt: str) -> str:
    """
    Call an OpenAI model via GenAIHub.

    Uses init_llm for older models (gpt-4o, gpt-4o-mini, o1) and ChatOpenAI for newer models (gpt-4.1+).

    Args:
        model: The model name to use
        prompt: The prompt text to send to the model

    Returns:
        The model's response content as a string
    """
    # Models that require init_llm instead of ChatOpenAI
    legacy_models = ["gpt-4o", "gpt-4o-mini", "o1", "o1-mini", "o1-preview"]

    if model in legacy_models:
        # Use init_llm for older OpenAI models
        llm_openai = init_llm(model, max_tokens=4096)
        response = llm_openai.invoke(prompt).content
        return str(response)
    else:
        # Use ChatOpenAI for newer models (gpt-4.1 and later)
        llm_openai = ChatOpenAI(
            proxy_model_name=model, proxy_client=proxy_client, temperature=0.5
        )
        response = llm_openai.invoke(prompt).content
        return str(response)


def call_llm(llm_type: str, prompt: str, model: Optional[str] = None) -> str:
    """
    Main dispatcher function to call the appropriate LLM based on type.

    Args:
        llm_type: The type of LLM to use ('gemini-direct', 'gemini', 'openai', 'anthropic')
        prompt: The prompt text to send to the model
        model: Optional model name (used for some providers)

    Returns:
        The model's response as a string
    """
    if llm_type == "gemini-direct":
        ## Flash model due to cost constraints
        return str(call_gemini(prompt))
    elif llm_type == "google":
        return str(call_gaih_google(model or "gemini-2.5-flash", prompt))
    elif llm_type == "openai":
        return str(call_gaih_openai(model or "gpt-4.1", prompt))
    elif llm_type == "anthropic":
        return str(call_gen_ai_hub(model or "anthropic--claude-4.5-sonnet", prompt))
    else:
        # Default to Gemini direct if type is not recognized
        print(
            f"LLM type '{llm_type}' not recognized. Defaulting to Gemini direct(2.5 Flash)."
        )
        return str(call_gemini(prompt))
