# AI Gateway

This project is a FastAPI application that acts as a gateway to the Ollama AI API, forwarding requests to endpoints like `/api/generate` and `/api/chat`. It supports multiple users with unique authentication tokens and handles both streaming and non-streaming responses.

## Features

- **Multiple Endpoints**: Supports `/generate` and `/chat` endpoints.
- **Authentication**: Uses the `Authorization` header with the `Bearer` token scheme.
- **Multiple Users**: Supports different authentication tokens for different users via a local token store.
- **Streaming Responses**: Handles both streaming and non-streaming responses from the Ollama API.
- **Configuration**: Reads configuration from a `.env` file and manages user tokens via `tokens.json`.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Setup Instructions](#setup-instructions)
- [Running the Application](#running-the-application)
- [Testing the Endpoints](#testing-the-endpoints)
  - [Generate Endpoint](#generate-endpoint)
  - [Chat Endpoint](#chat-endpoint)
- [Examples](#examples)
  - [Generate Text](#generate-text)
  - [Chat Conversation](#chat-conversation)
- [Token Management](#token-management)
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

   **Note:** If `requirements.txt` doesn't exist, install the necessary packages manually:

   ```bash
   pip install fastapi uvicorn httpx pydantic pydantic-settings
   ```

4. **Create a `.env` File**

   Create a `.env` file in the project root directory with the following content:

   ```dotenv
   # .env
   OLLAMA_BASE_URL=http://localhost:11434
   ```

   Adjust the `OLLAMA_BASE_URL` if your Ollama API is running on a different host or port.

5. **Create a `tokens.json` File**

   Create a `tokens.json` file in the project root directory to store user tokens:

   ```json
   {
     "user1": "token_for_user1",
     "user2": "token_for_user2",
     "user3": "token_for_user3"
   }
   ```

   Replace the tokens with secure, unique tokens for each user.

6. **Update `.gitignore`**

   Ensure that sensitive files are not committed to version control by adding them to your `.gitignore`:

   ```gitignore
   # .gitignore
   .env
   tokens.json
   ```

## Running the Application

Start the FastAPI application using Uvicorn:

```bash
uvicorn main:app --reload
```

- **`main`**: The name of your Python file without the `.py` extension (e.g., `main.py`).
- **`--reload`**: Enables auto-reload on code changes (useful during development).

The application will be accessible at `http://localhost:8000`.

## Testing the Endpoints

### Generate Endpoint

- **URL**: `http://localhost:8000/generate`
- **Method**: `POST`
- **Authentication**: Required (`Authorization: Bearer <token>`)

### Chat Endpoint

- **URL**: `http://localhost:8000/chat`
- **Method**: `POST`
- **Authentication**: Required (`Authorization: Bearer <token>`)

## Examples

### Generate Text

#### Non-Streaming Request

```bash
curl -X POST 'http://localhost:8000/generate' \
  -H 'Authorization: Bearer token_for_user1' \
  -H 'Content-Type: application/json' \
  -d '{
        "model": "llama3.1",
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
curl -X POST 'http://localhost:8000/generate' \
  -H 'Authorization: Bearer token_for_user1' \
  -H 'Content-Type: application/json' \
  -d '{
        "model": "llama3.1",
        "prompt": "Why is the sky blue?"
      }'
```

**Note:** By omitting `"stream": false`, the request defaults to streaming mode.

**Expected Behavior:**

- The response is streamed back to the client incrementally.

### Chat Conversation

#### Non-Streaming Chat

```bash
curl -X POST 'http://localhost:8000/chat' \
  -H 'Authorization: Bearer token_for_user1' \
  -H 'Content-Type: application/json' \
  -d '{
        "model": "llama3.1",
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
curl -X POST 'http://localhost:8000/chat' \
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

**Expected Behavior:**

- The assistant's reply is streamed back to the client.

## Token Management

- **Adding Users**: Update the `tokens.json` file with new users and tokens.
- **Removing Users**: Remove the user's entry from the `tokens.json` file.
- **Token Validation**: Tokens are validated against the entries in `tokens.json`.

**Note:** Remember to restart the application after modifying `tokens.json` or implement a token reload mechanism if tokens change frequently.

## Security Considerations

- **Protect Sensitive Files**: Ensure that `.env` and `tokens.json` are not committed to version control or exposed publicly.
- **Use Secure Tokens**: Generate strong, unique tokens for each user.
- **HTTPS**: Consider running the application over HTTPS in production environments.
- **Authentication**: All endpoints require authentication using the `Authorization` header with the `Bearer` scheme.

## Future Enhancements

- **Database Integration**: Replace `tokens.json` with a database for better scalability and security.
- **Additional Endpoints**: Support more Ollama API endpoints like `/embed`.
- **User Management**: Implement user registration, token generation, and revocation endpoints.
- **Error Handling**: Enhance error messages and logging for better diagnostics.
- **Rate Limiting**: Add rate limiting per user to prevent abuse.

## License

This project is licensed under the [MIT License](LICENSE).
