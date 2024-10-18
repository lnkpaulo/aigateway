# AI Gateway

This project is a FastAPI application that acts as a gateway to the Ollama API, forwarding requests to endpoints like `/api/generate`, `/api/chat`, `/api/embed`, and `/api/tags`. It supports multiple users with unique authentication tokens and handles both streaming and non-streaming responses.

This project was only possible due to the excellent work done by [Ollama](https://ollama.com/) team, whose work has been shared with the community. Thank you!

**Note: This is a work in progress, and due to limited time, I'm not able to maintain this repository. Feel free to fork it and make your own changes.**

## Features

- **Multiple Endpoints**: Supports `/generate`, `/chat`, `/embed`, and `/tags` endpoints.
- **Authentication**: Uses the `Authorization` header with the `Bearer` token scheme.
- **Multiple Users**: Supports different authentication tokens for different users via a local token store.
- **Streaming Responses**: Handles both streaming and non-streaming responses from the Ollama API.
- **Configuration**: Reads configuration from a `.env` file and manages user tokens via a SQLite database (`tokens.db`).
- **Token Management CLI**: Provides command-line and interactive interfaces for managing API tokens.

## Table of Contents

- [AI Gateway](#ai-gateway)
  - [Features](#features)
  - [Table of Contents](#table-of-contents)
  - [Prerequisites](#prerequisites)
  - [Setup Instructions](#setup-instructions)
  - [Running the Application](#running-the-application)
  - [Endpoints](#endpoints)
    - [Generate Endpoint](#generate-endpoint)
    - [Chat Endpoint](#chat-endpoint)
    - [Embed Endpoint](#embed-endpoint)
    - [Tags Endpoint](#tags-endpoint)
  - [Examples](#examples)
    - [Generate Text](#generate-text)
      - [Non-Streaming Request](#non-streaming-request)
      - [Streaming Request](#streaming-request)
    - [Chat Conversation](#chat-conversation)
      - [Non-Streaming Chat](#non-streaming-chat)
      - [Streaming Chat](#streaming-chat)
    - [Get Model Tags](#get-model-tags)
  - [Token Management](#token-management)
    - [Command-Line Interface (CLI)](#command-line-interface-cli)
    - [Interactive CLI](#interactive-cli)
  - [Configuration](#configuration)
  - [Security Considerations](#security-considerations)
  - [Future Enhancements](#future-enhancements)
  - [License](#license)

## Prerequisites

- **Python 3.8+**
- **pip** (Python package manager)
- **Ollama AI API** running locally or accessible via network

## Setup Instructions

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/aigateway.git
   cd aigateway
   ```

2. **Create a Virtual Environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use 'venv\Scripts\activate'
   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Create a `.env` File**

   Create a `.env` file in the project root directory with the following content:

   ```dotenv
   # .env
   LOG_LEVEL=DEBUG
   LOG_FILE_LEVEL=DEBUG
   BASE_PATH="/api"  # If BASE_PATH is not set, the default "/api" will be used
   OLLAMA_BASE_URL=http://localhost:11434
   TOKEN_DB_PATH=tokens.db
   CLI_API_KEY_Test=""
   ```

   **Configuration Options:**

   - `LOG_LEVEL`: Sets the logging level for the application (e.g., DEBUG, INFO, WARNING).
   - `LOG_FILE_LEVEL`: Sets the logging level for the log file.
   - `BASE_PATH`: The base path for the API endpoints. Defaults to `/api` if not set.
   - `OLLAMA_BASE_URL`: The base URL where the Ollama AI API is accessible.
   - `TOKEN_DB_PATH`: The path to the SQLite database file for storing tokens.
   - `CLI_API_KEY_Test`: Placeholder for future CLI API key configurations.

5. **Initialize the Token Database**

   The application uses a SQLite database (`tokens.db`) to manage user tokens. The database is initialize when the application starts up. If you want to reset the token database, delete the `tokens.db` file in the project root directory and restart the application.


## Running the Application

Start the FastAPI application using `run.sh`:

```bash
./run.sh
```

The application will be accessible at `http://localhost:8000`.

The API documentation will be accessible at `http://localhost:8000/docs`.

## Endpoints

### Generate Endpoint

- **URL**: `http://localhost:8000/api/generate`
- **Method**: `POST`
- **Authentication**: Required (`Authorization: Bearer <token>`)

### Chat Endpoint

- **URL**: `http://localhost:8000/api/chat`
- **Method**: `POST`
- **Authentication**: Required (`Authorization: Bearer <token>`)

### Embed Endpoint

- **URL**: `http://localhost:8000/api/embed`
- **Method**: `POST`
- **Authentication**: Required (`Authorization: Bearer <token>`)

### Tags Endpoint

- **URL**: `http://localhost:8000/api/tags`
- **Method**: `GET`
- **Authentication**: Required (`Authorization: Bearer <token>`)

## Examples

### Generate Text

#### Non-Streaming Request

```bash
curl -X POST 'http://localhost:8000/api/generate' \
  -H 'Authorization: Bearer token_for_user1' \
  -H 'Content-Type: application/json' \
  -d '{
        "model": "llama3.2",
        "prompt": "Why is the sky blue?",
        "stream": false
      }'
```

**Expected Response:**

```json
{
  "response": "The sky appears blue because molecules in the Earth's atmosphere scatter sunlight in all directions..."
}
```

#### Streaming Request

```bash
curl -X POST 'http://localhost:8000/api/generate' \
  -H 'Authorization: Bearer token_for_user1' \
  -H 'Content-Type: application/json' \
  -d '{
        "model": "llama3.2",
        "prompt": "Why is the sky blue?"
      }'
```

**Note:** By omitting `"stream": false`, the request defaults to streaming mode.

**Expected Behavior**:

- The response is streamed back to the client incrementally.

### Chat Conversation

#### Non-Streaming Chat

```bash
curl -X POST 'http://localhost:8000/api/chat' \
  -H 'Authorization: Bearer token_for_user1' \
  -H 'Content-Type: application/json' \
  -d '{
        "model": "llama3.2",
        "messages": [
          {
            "role": "user",
            "content": "Tell me a joke."
          }
        ],
        "stream": false
      }'
```

**Expected Response:**

```json
{
  "response": "Why don't scientists trust atoms? Because they make up everything!"
}
```

#### Streaming Chat

```bash
curl -X POST 'http://localhost:8000/api/chat' \
  -H 'Authorization: Bearer token_for_user1' \
  -H 'Content-Type: application/json' \
  -d '{
        "model": "llama3.1",
        "messages": [
          {
            "role": "user",
            "content": "Tell me a joke."
          }
        ]
      }'
```

**Expected Behavior**:

- The assistant's reply is streamed back to the client.

### Get Model Tags

```bash
curl -X GET 'http://localhost:8000/api/tags' \
  -H 'Authorization: Bearer token_for_user1'
```

**Expected Response:**

```json
{
  "models": [
    {
      "name": "codellama:13b",
      "modified_at": "2023-11-04T14:56:49.277302595-07:00",
      "size": 7365960935,
      "digest": "9f438cb9cd581fc025612d27f7c1a6669ff83a8bb0ed86c94fcf4c5440555697",
      "details": {
        "format": "gguf",
        "family": "llama",
        "families": null,
        "parameter_size": "13B",
        "quantization_level": "Q4_0"
      }
    },
    {
      "name": "llama3:latest",
      "modified_at": "2023-12-07T09:32:18.757212583-08:00",
      "size": 3825819519,
      "digest": "fe938a131f40e6f6d40083c9f0f430a515233eb2edaa6d72eb85c50d64f2300e",
      "details": {
        "format": "gguf",
        "family": "llama",
        "families": null,
        "parameter_size": "7B",
        "quantization_level": "Q4_0"
      }
    }
  ]
}
```

## Token Management

The application uses a SQLite database (`tokens.db`) to manage user tokens. Two interfaces are provided for managing tokens: a Command-Line Interface (CLI) and an Interactive CLI.

### Command-Line Interface (CLI)

Use `gen_api_key_cli.py` to manage API tokens via command-line arguments.

**Usage:**

```bash
python gen_api_key_cli.py [options]
```

**Options:**

- **Generate Token**

  ```bash
  python gen_api_key_cli.py -g <user> <api_key_name>
  ```

  *Generates a new token for the specified user with the given API key name.*

- **List Users**

  ```bash
  python gen_api_key_cli.py -l
  ```

  *Lists all users and their tokens in a tabulated format.*

- **Delete Token**

  ```bash
  python gen_api_key_cli.py -d <user> <api_key_name>
  ```

  *Deletes the specified API token for the given user.*

- **Export Users**

  ```bash
  python gen_api_key_cli.py -e <filename>
  ```

  *Exports all users and their tokens to the specified file.*

**Examples:**

- **Generate a Token for User1:**

  ```bash
  python gen_api_key_cli.py -g user1 my_api_key
  ```

- **List All Users:**

  ```bash
  python gen_api_key_cli.py -l
  ```

- **Delete a Token:**

  ```bash
  python gen_api_key_cli.py -d user1 my_api_key
  ```

- **Export Users to CSV:**

  ```bash
  python gen_api_key_cli.py -e users_export.csv
  ```

### Interactive CLI

Use `gen_api_key_cli_inter.py` for an interactive token management experience with prompts and menus.

**Usage:**

```bash
python gen_api_key_cli_inter.py
```

**Features:**

- **Generate a Token**: Prompts for username and API key name to generate a new token.
- **List All Users**: Displays all users and their tokens in a formatted table.
- **Delete a Token**: Prompts for username and API key name to delete a specific token.
- **Export Users to File**: Prompts for a filename to export all users and tokens.
- **Exit**: Exits the interactive menu.

**Example Workflow:**

1. **Start Interactive CLI:**

   ```bash
   python gen_api_key_cli_inter.py
   ```

2. **Main Menu:**

   ```
   What do you want to do?
   1. Generate a token
   2. List all users
   3. Delete a token
   4. Export users to file
   5. Exit
   ```

3. **Select an Action:** Choose an option by navigating with arrow keys and pressing Enter.

4. **Follow Prompts:** Depending on the selected action, follow the on-screen prompts to complete the task.

## Security Considerations

- **Use Secure Tokens**: Generate strong, unique tokens for each user to prevent unauthorized access.
- **HTTPS**: It is highly recommended to run the application over HTTPS in production environments to secure data in transit.
- **Authentication**: All endpoints require authentication using the `Authorization` header with the `Bearer` scheme.
- **Database Security**: Ensure that the `tokens.db` file is stored securely and access is restricted to authorized personnel only.

## Future Enhancements

- [ ] **Source Code Optimization**: Improve performance and maintainability of the source code.
- [x] **Database Integration**: Enhance database functionalities for better scalability and security.
- [ ] **Additional Endpoints**: Support more Ollama AI API endpoints.
- [ ] **User Management**: Implement user registration, token generation, and revocation endpoints via the API.
- [ ] **Error Handling**: Enhance error messages and logging for better diagnostics.
- [ ] **Rate Limiting**: Add rate limiting per user to prevent abuse and ensure fair usage.
- [ ] **Dockerization**: Containerize the application for easier deployment and scalability.
- [ ] **Unit Tests**: Implement comprehensive unit tests to ensure code reliability and facilitate future changes.

## License

This project is licensed under the [MIT License](LICENSE).

# Additional Notes

- **Scripts Execution Permissions**: Make sure that `run.sh` and any other shell scripts have the appropriate execution permissions:

  ```bash
  chmod +x run.sh
  ```