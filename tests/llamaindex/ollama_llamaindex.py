# tests/llamaindex/ollama_llamaindex.py
from llama_index.llms.ollama import Ollama
from llama_index.core.llms import ChatMessage
from ollama import Client
# from ...src.models import Settings
from src.models import Settings


settings = Settings()

# API key/token
API_KEY = settings.CLI_API_KEY_Test


# Create an Ollama Client instance with the headers set
client = Client(
    host="http://localhost:8000",
    headers={
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json',
    },
    timeout=60.0,  # Adjust timeout if needed
)

llm = Ollama(
    client=client,
    model="llama3.2",
)

#Chat
# messages = [
#     ChatMessage(
#         role="system", content="You are a pirate with a colorful personality"
#     ),
#     ChatMessage(role="user", content="What is your name"),
# ]
# response = llm.chat(messages)

# Completion
# response = llm.complete("What is the capital of France?")

# print(response)


response = llm.stream_complete("Who is Paul Graham?")
for r in response:
    print(r.delta, end="")


