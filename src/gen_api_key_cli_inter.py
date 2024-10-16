# gen_api_key_cli_inter.py
import sys
from InquirerPy import prompt
from InquirerPy.utils import color_print
from libs.token_operations import generate_token, list_users, delete_token, export_users
from tabulate import tabulate  # Import tabulate for table formatting

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
    users = list_users()
    if users:
        headers = ["User ID", "User", "API KEY Name", "Created At", "Expires At"]
        table = tabulate(users, headers=headers, tablefmt="pretty")
        color_print([("fg:yellow", table)])
    else:
        color_print([("fg:red", "No users found.")])

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

def export_users_interactive():
    questions = [
        {
            "type": "input",
            "name": "filename",
            "message": "Enter the filename to export users to:",
            "default": "users.csv"
        }
    ]
    answers = prompt(questions)
    filename = answers["filename"]

    result = export_users(filename)
    color_print([("fg:green" if "successfully" in result else "fg:red", result)])

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
                    {"name": "Export users to file", "value": "export"},
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
        elif answer == "export":
            export_users_interactive()
        elif answer == "exit":
            color_print([("fg:green", "Exiting...")])
            sys.exit(0)

if __name__ == "__main__":
    main_menu()
