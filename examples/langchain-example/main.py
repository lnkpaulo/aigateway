# tests/llamaindex/example.py
""" 
How to use? From project root, run:
$ python -m examples.langchain-example.main
"""
from langchain_ollama import ChatOllama
from langchain_core.messages import AIMessage

from ollama import Client
from src.models import Settings


settings = Settings()

# API key/token
API_KEY = settings.CLI_API_KEY_Test

llm = ChatOllama( 
    base_url="http://localhost:8000",
    client_kwargs={
        "headers": {
            'Authorization': f'Bearer {API_KEY}',
            'Content-Type': 'application/json',
        },
    },
    model="llama3.2",
)

#Invocation
messages = [
    (
        "system",
        "You are a helpful assistant that translates English to French. Translate the user sentence.",
    ),
    ("human", "I love programming."),
]

ai_msg = llm.invoke(messages)
print(ai_msg)
