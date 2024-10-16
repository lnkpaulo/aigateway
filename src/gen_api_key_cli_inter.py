# gen_api_key_cli_inter.py
import sys
from InquirerPy import prompt
from InquirerPy.utils import color_print
from libs.token_operations import generate_token, list_users, delete_token

def generate_token_interactive():
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
    
    result = generate_token(user, api_name)
    color_print([("fg:green" if "Generated" in result else "fg:red", result)])

def list_users_interactive():
    result = list_users()
    color_print([("fg:yellow" if "Available" in result else "fg:red", result)])

def delete_token_interactive():
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

    result = delete_token(user, api_name)
    color_print([("fg:green" if "Deleted" in result else "fg:red", result)])

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
            generate_token_interactive()
        elif answer == "list":
            list_users_interactive()
        elif answer == "delete":
            delete_token_interactive()
        elif answer == "exit":
            color_print([("fg:green", "Exiting...")])
            sys.exit(0)

if __name__ == "__main__":
    main_menu()
