# gen_api_key_cli.py
import sys
from libs.token_operations import generate_token, list_users, delete_token

def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python gen_api_key.py -g <user> <api_key_name>     # Generate token")
        print("  python gen_api_key.py -l                           # List users")
        print("  python gen_api_key.py -d <user> <api_key_name>     # Delete token")
        sys.exit(1)

    if sys.argv[1] == '-g' and len(sys.argv) == 4:
        user = sys.argv[2]
        api_name = sys.argv[3]
        print(generate_token(user, api_name))
    elif sys.argv[1] == '-l':
        print(list_users())
    elif sys.argv[1] == '-d' and len(sys.argv) == 4:
        user = sys.argv[2]
        api_name = sys.argv[3]
        print(delete_token(user, api_name))
    else:
        print("Invalid command or arguments.")
        sys.exit(1)

if __name__ == "__main__":
    main()
