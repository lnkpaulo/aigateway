# gen_api_key_interactive.py
import sys
from libs.token_manager import TokenManager
from InquirerPy import prompt
from InquirerPy.utils import color_print

# Initialize the token manager
token_manager = TokenManager()

def generate_token():
    questions = [
        {
            "type": "input",
            "name": "user",
            "message": "Enter the username:",
        },
        {
            "type": "input",
            "name": "api_name",
            "message": "Enter the API key name:",
        }
    ]
    answers = prompt(questions)
    user = answers["user"]
    api_name = answers["api_name"]
    
    try:
        token = token_manager.generate_token(user, api_name)
        color_print([("fg:green", f"Generated token for {user} with API {api_name}: {token}")])
    except ValueError as e:
        color_print([("fg:red", str(e))])

def list_users():
    users = token_manager.list_users()
    if users:
        color_print([("fg:yellow", "Available users and their API KEYs name:")])
        for user, api_name in users:
            color_print([("fg:cyan", f"User: {user}, API KEY Name: {api_name}")])
    else:
        color_print([("fg:red", "No users found.")])

def delete_token():
    questions = [
        {
            "type": "input",
            "name": "user",
            "message": "Enter the username to delete:",
        },
        {
            "type": "input",
            "name": "api_name",
            "message": "Enter the API key name to delete:",
        }
    ]
    answers = prompt(questions)
    user = answers["user"]
    api_name = answers["api_name"]

    try:
        token_manager.revoke_token(user, api_name)
        color_print([("fg:green", f"Deleted token for {user} with API {api_name}.")])
    except ValueError as e:
        color_print([("fg:red", str(e))])

def main_menu():
    while True:
        questions = [
            {
                "type": "list",
                "name": "action",
                "message": "What do you want to do?",
                "choices": [
                    {"name": "Generate a token", "value": "generate"},
                    {"name": "List all users", "value": "list"},
                    {"name": "Delete a token", "value": "delete"},
                    {"name": "Exit", "value": "exit"}
                ]
            }
        ]

        answer = prompt(questions)["action"]

        if answer == "generate":
            generate_token()
        elif answer == "list":
            list_users()
        elif answer == "delete":
            delete_token()
        elif answer == "exit":
            color_print([("fg:green", "Exiting...")])
            sys.exit(0)

if __name__ == "__main__":
    main_menu()
