# gen_api_key_cli.py
import sys
from libs.token_operations import generate_token, list_users, delete_token, export_users
from tabulate import tabulate  # Import tabulate for table formatting

def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python gen_api_key.py -g <user> <api_key_name>     # Generate token")
        print("  python gen_api_key.py -l                           # List users")
        print("  python gen_api_key.py -d <user> <api_key_name>     # Delete token")
        print("  python gen_api_key.py -e <filename>                # Export users to file")
        sys.exit(1)

    if sys.argv[1] == '-g' and len(sys.argv) == 4:
        user = sys.argv[2]
        api_name = sys.argv[3]
        print(generate_token(user, api_name))
    elif sys.argv[1] == '-l':
        users = list_users()
        if users:
            headers = ["User ID", "User", "API KEY Name", "Created At", "Expires At"]
            print(tabulate(users, headers, tablefmt="pretty"))  # Display as a pretty table
        else:
            print("No users found.")
    elif sys.argv[1] == '-d' and len(sys.argv) == 4:
        user = sys.argv[2]
        api_name = sys.argv[3]
        print(delete_token(user, api_name))
    elif sys.argv[1] == '-e' and len(sys.argv) == 3:
        filename = sys.argv[2]
        result = export_users(filename)
        print(result)
    else:
        print("Invalid command or arguments.")
        sys.exit(1)

if __name__ == "__main__":
    main()
