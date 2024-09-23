import logging
import json
import os
import httpx
from fastapi import FastAPI, HTTPException, Depends, Security, Response
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from pydantic_settings import BaseSettings
from typing import Dict, Any, Optional, List
from fastapi.responses import JSONResponse, StreamingResponse

# Import TokenManager
from token_manager import TokenManager

# Configure logging
logging.basicConfig(level=logging.DEBUG)

app = FastAPI()

# Initialize TokenManager
token_manager = TokenManager()

# Settings class
class Settings(BaseSettings):
    OLLAMA_BASE_URL: str

    class Config:
        env_file = ".env"

settings = Settings()

# Define the HTTPBearer security scheme
security_scheme = HTTPBearer(auto_error=False)

# Authentication Dependency
async def get_api_key(credentials: HTTPAuthorizationCredentials = Security(security_scheme)):
    if credentials and credentials.scheme == "Bearer":
        if token_manager.validate_token(credentials.credentials):
            return credentials.credentials
    raise HTTPException(status_code=401, detail="Invalid or missing token")

# Request models
class BaseRequest(BaseModel):
    model: str
    stream: Optional[bool] = True  # Default to True to match Ollama's default behavior
    extra_params: Dict[str, Any] = {}

    class Config:
        extra = "allow"

class GenerateRequest(BaseRequest):
    prompt: str

class ChatRequest(BaseRequest):
    system: Optional[str] = None
    messages: List[Dict[str, str]]

# Helper function to forward requests
async def forward_request(
    endpoint: str,
    payload: Dict[str, Any],
    stream: bool,
) -> Response:
    """
    Forward the request to the specified Ollama endpoint.

    Args:
        endpoint (str): The Ollama API endpoint to forward to (e.g., "/api/generate", "/api/chat").
        payload (Dict[str, Any]): The JSON payload to send in the request.
        stream (bool): Whether to handle streaming responses.

    Returns:
        Response: The FastAPI Response object to return to the client.
    """
    # Construct the full URL for the Ollama endpoint
    url = f"{settings.OLLAMA_BASE_URL}{endpoint}"

    logging.debug(f"Forwarding request to {url} with payload: {payload}")

    try:
        if stream:
            logging.debug("Streaming response enabled.")

            async def stream_response():
                async with httpx.AsyncClient(timeout=None) as client:
                    async with client.stream("POST", url, json=payload) as response:
                        if response.status_code != 200:
                            logging.error(
                                f"Failed to fetch streaming data: {response.status_code}"
                            )
                            raise HTTPException(
                                status_code=response.status_code,
                                detail=response.text,
                            )

                        async for chunk in response.aiter_bytes():
                            yield chunk

            return StreamingResponse(
                stream_response(), media_type="application/json"
            )
        else:
            async with httpx.AsyncClient(timeout=None) as client:
                response = await client.post(url, json=payload)
                response.raise_for_status()
                logging.debug(f"Response from Ollama: {response.status_code}")

                content = await response.aread()
                content_text = content.decode("utf-8")

                json_objects = []
                for line in content_text.strip().split("\n"):
                    if line.strip():
                        try:
                            json_obj = json.loads(line)
                            json_objects.append(json_obj)
                        except json.JSONDecodeError as e:
                            logging.error(f"JSON decoding error: {e}")
                            raise HTTPException(
                                status_code=500,
                                detail="Invalid JSON response from Ollama",
                            )

                # Aggregate the 'response' fields
                responses = "".join(obj.get("response", "") for obj in json_objects)
                return JSONResponse(
                    content={"response": responses}, status_code=response.status_code
                )
    except httpx.HTTPStatusError as exc:
        logging.error(
            f"Error response {exc.response.status_code} from Ollama: {exc.response.text}"
        )
        raise HTTPException(
            status_code=exc.response.status_code, detail=exc.response.text
        )
    except httpx.RequestError as exc:
        logging.error(f"Request forwarding failed: {exc}")
        raise HTTPException(
            status_code=500, detail=f"Request forwarding failed: {exc}"
        )
    except Exception as e:
        logging.error(f"Unhandled exception: {e}")
        raise HTTPException(status_code=500, detail="Request forwarding failed")

# Route handlers
@app.post("/generate")
async def generate(
    request_data: GenerateRequest, api_key: str = Depends(get_api_key)
):
    username = token_manager.get_user_by_token(api_key)
    logging.debug(f"Generate request made by user: {username}")

    # Prepare payload for forwarding
    payload = request_data.dict(exclude_unset=True)
    payload.update(request_data.extra_params)

    return await forward_request(
        endpoint="/api/generate",
        payload=payload,
        stream=request_data.stream,
    )

@app.post("/chat")
async def chat(
    request_data: ChatRequest, api_key: str = Depends(get_api_key)
):
    username = token_manager.get_user_by_token(api_key)
    logging.debug(f"Chat request made by user: {username}")

    # Prepare payload for forwarding
    payload = request_data.dict(exclude_unset=True)
    payload.update(request_data.extra_params)

    return await forward_request(
        endpoint="/api/chat",
        payload=payload,
        stream=request_data.stream,
    )
