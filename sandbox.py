########################################################################################
############ Sandbox for testing various functionalities in the Otho project ###########
########################################################################################

import dotenv
from gen_ai_hub.proxy.langchain import init_llm
from gen_ai_hub.proxy.langchain.amazon import (
    init_chat_converse_model as amazon_init_converse_model,
)
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent

dotenv.load_dotenv()

# Initialize Claude LLM
model_name_amazon = "anthropic--claude-4.5-sonnet"
model_id_amazon = "anthropic.claude-4.5-sonnet-v1:0"

llm_claude = init_llm(
    model_name=model_name_amazon,
    model_id=model_id_amazon,
    init_func=amazon_init_converse_model,
    temperature=0.5,
    top_p=None,  # Explicitly set to None to avoid conflict
)


# Define a simple tool
@tool
def multiply(a: int, b: int) -> int:
    """Multiply two numbers."""
    return a * b


# Create the simplest ReAct agent using LangGraph's built-in function
tools = [multiply]
agent = create_react_agent(llm_claude, tools)

# Test the agent
if __name__ == "__main__":
    print("=" * 80)
    print("LangGraph Native ReAct Agent with Claude (Simplest Form)")
    print("=" * 80)

    # Test 1: Simple question
    print("\n[Test 1] Simple question:")
    result = agent.invoke({"messages": [("user", "Hello! What can you do?")]})
    print(result["messages"][-1].content)

    # Test 2: Using multiply tool
    print("\n[Test 2] Using multiply tool:")
    result = agent.invoke({"messages": [("user", "What is 123 times 456?")]})
    print(result["messages"][-1].content)

    print("\n" + "=" * 80)
    print("Agent tests completed!")
    print("=" * 80)
