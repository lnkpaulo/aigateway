# libs/token_operations.py
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
        user_list = ["Available users and their API KEYs name:"]
        for user, api_name in users:
            user_list.append(f"User: {user}, API KEY Name: {api_name}")
        return "\n".join(user_list)
    else:
        return "No users found."

def delete_token(user, api_name):
    try:
        token_manager.revoke_token(user, api_name)
        return f"Deleted token for {user} with API {api_name}."
    except ValueError as e:
        return str(e)
