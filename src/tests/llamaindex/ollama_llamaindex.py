# ollama_llamaindex.py
import httpx
from llama_index.llms.ollama import Ollama
from llama_index.core.llms import ChatMessage

# Your API key/token
API_KEY = "token_for_user1"


# Initialize the Ollama instance and pass the API key via **kwargs
llm = Ollama(
    # base_url="http://localhost:8000",
    model="llama3.2",
    request_timeout=60.0,
)

# Set the Authorization header on the internal client
# llm.client._client.headers.update({
#     "Authorization": f"Bearer {API_KEY}"
# })

#Chat
# messages = [
#     ChatMessage(
#         role="system", content="You are a pirate with a colorful personality"
#     ),
#     ChatMessage(role="user", content="What is your name"),
# ]
# response = llm.chat(messages)

#Completion
# response = llm.complete("What is the capital of France?")

# print(response)


response = llm.stream_complete("Who is Paul Graham?")
for r in response:
    print(r.delta, end="")


