# libs/token_operations.py
import csv  # Import csv module to handle CSV file writing
from libs.token_manager import TokenManager

# Initialize the token manager
token_manager = TokenManager()

def generate_token(user, api_name):
    try:
        token = token_manager.generate_token(user, api_name)
        return f"Generated token for {user} with API {api_name}: {token}"
    except ValueError as e:
        return str(e)

def list_users():
    users = token_manager.list_users()
    if users:
        return users  # Return the list of tuples directly
    else:
        return []

def delete_token(user, api_name):
    try:
        token_manager.revoke_token(user, api_name)
        return f"Deleted token for {user} with API {api_name}."
    except ValueError as e:
        return str(e)

def export_users(filename):
    users = list_users()
    if users:
        headers = ["User ID", "User", "API KEY Name", "Created At", "Expires At"]
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(headers)  # Write the headers
            writer.writerows(users)   # Write the user data
        return f"Users exported successfully to {filename}"
    else:
        return "No users found to export."
