# gen_api_key.py
import sys
from libs.token_manager import TokenManager
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

# Initialize the token manager
token_manager = TokenManager()

def generate_token(user, api_name):
    try:
        token = token_manager.generate_token(user, api_name)
        print(Fore.GREEN + f"Generated token for {user} with API {api_name}: {token}")
    except ValueError as e:
        print(Fore.RED + str(e))

def list_users():
    users = token_manager.list_users()
    if users:
        print(Fore.YELLOW + "Available users and their API KEYs name:")
        for user, api_name in users:
            print(Fore.CYAN + f"User: {user}, API KEY Name: {api_name}")
    else:
        print(Fore.RED + "No users found.")

def delete_token(user, api_name):
    try:
        token_manager.revoke_token(user, api_name)
        print(Fore.GREEN + f"Deleted token for {user} with API {api_name}.")
    except ValueError as e:
        print(Fore.RED + str(e))

def main():
    if len(sys.argv) < 2:
        print(Fore.YELLOW + "Usage:")
        print(Fore.YELLOW + "  python gen_api_key.py -g <user> <api_key_name>     # Generate token")
        print(Fore.YELLOW + "  python gen_api_key.py -l                           # List users")
        print(Fore.YELLOW + "  python gen_api_key.py -d <user> <api_key_name>     # Delete token")
        sys.exit(1)

    if sys.argv[1] == '-g' and len(sys.argv) == 4:
        user = sys.argv[2]
        api_name = sys.argv[3]
        generate_token(user, api_name)
    elif sys.argv[1] == '-l':
        list_users()
    elif sys.argv[1] == '-d' and len(sys.argv) == 4:
        user = sys.argv[2]
        api_name = sys.argv[3]
        delete_token(user, api_name)
    else:
        print(Fore.RED + "Invalid command or arguments.")
        sys.exit(1)

if __name__ == "__main__":
    main()

