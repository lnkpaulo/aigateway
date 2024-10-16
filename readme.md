# AI Gateway

This project is a FastAPI application that acts as a gateway to the Ollama AI API, forwarding requests to endpoints like `/api/generate`, `/api/chat`, `/api/embed`, and `/api/tags`. It supports multiple users with unique authentication tokens and handles both streaming and non-streaming responses.

## Features

- **Multiple Endpoints**: Supports `/generate`, `/chat`, `/embed`, and `/tags` endpoints.
- **Authentication**: Uses the `Authorization` header with the `Bearer` token scheme.
- **Multiple Users**: Supports different authentication tokens for different users via a local token store.
- **Streaming Responses**: Handles both streaming and non-streaming responses from the Ollama API.
- **Dynamic HTTP Methods**: Supports both `POST` and `GET` requests depending on the endpoint.
- **Configuration**: Reads configuration from a `.env` file and manages user tokens via `tokens.json`.

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


## Running the Application

Start the FastAPI application using run.sh:

```bash
./run.sh
```

The application will be accessible at `http://localhost:8000`.
The application api documentation will be accessible at `http://localhost:8000/docs`.

## Endpoints

### Generate Endpoint

- **URL**: `http://localhost:8000/generate`
- **Method**: `POST`
- **Authentication**: Required (`Authorization: Bearer <token>`)

### Chat Endpoint

- **URL**: `http://localhost:8000/chat`
- **Method**: `POST`
- **Authentication**: Required (`Authorization: Bearer <token>`)

### Embed Endpoint

- **URL**: `http://localhost:8000/embed`
- **Method**: `POST`
- **Authentication**: Required (`Authorization: Bearer <token>`)

### Tags Endpoint

- **URL**: `http://localhost:8000/tags`
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

- **Adding Users**: Update the `tokens.json` file with new users and tokens.
- **Removing Users**: Remove the user's entry from the `tokens.json` file.
- **Token Validation**: Tokens are validated against the entries in `tokens.json`.

**Note:** The application reloads the token each time an api is called. No need to restart the application after modifying `tokens.json`

## Security Considerations

- **Use Secure Tokens**: Generate strong, unique tokens for each user.
- **HTTPS**: Consider running the application over HTTPS in production environments.
- **Authentication**: All endpoints require authentication using the `Authorization` header with the `Bearer` scheme.

## Future Enhancements

- **Source Code**: Optimize source code to improve performance and maintenance. 
- **Database Integration**: Replace `tokens.json` with a database for betcurl -X GET 'http://localhost:8000/api/tags' \
  -H 'Authorization: Bearer token_for_user1'ter scalability and security.
- **Additional Endpoints**: Support more Ollama API endpoints.
- **User Management**: Implement user registration, token generation, and revocation endpoints.
- **Error Handling**: Enhance error messages and logging for better diagnostics.
- **Rate Limiting**: Add rate limiting per user to prevent abuse.

## License

This project is licensed under the [MIT License](LICENSE).