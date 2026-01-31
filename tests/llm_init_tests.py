import dotenv
from gen_ai_hub.proxy.core import get_proxy_client
from gen_ai_hub.proxy.langchain import init_llm
from gen_ai_hub.proxy.langchain.openai import ChatOpenAI
from gen_ai_hub.proxy.native.google_vertexai.clients import GenerativeModel

dotenv.load_dotenv()

proxy_client = get_proxy_client("gen-ai-hub")

########### GenAIHub OpenAI LLM Initialization ###########
# llmGPT = ChatOpenAI(proxy_model_name="o1", proxy_client=proxy_client, temperature=0.5)
# print(llmGPT.invoke("Hello, Otho!"))

########## GenAIHub Google LLM Initialization ###########
kwargs = dict({"model_name": "gemini-2.5-flash-lite"})
model = GenerativeModel(proxy_client=proxy_client, **kwargs)
content = [{"role": "user", "parts": [{"text": "Hi, what is your name?"}]}]
model_response = model.generate_content(content)
print(model_response.text)


# ########### Direct Google LLM Initialization ###########
# llm = genai.Client()

# llm = init_llm("gpt-4.1x", max_tokens=4096)
# # print(llm.invoke("Hello, Otho!"))  # Test call to ensure LLM is initialized correctly

# llm = init_llm("gpt-4.1", max_tokens=4096)
# print(llm.invoke("Hello, Otho!"))  # Test call to ensure LLM
