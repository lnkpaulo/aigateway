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
    url = f"{settings.OLLAMA_BASE_URL}{endpoint}"
    logging.debug(f"Forwarding request to {url} with payload: {payload}")

    try:
        client = httpx.AsyncClient(timeout=None)  # Keep client open for streaming
        if stream:
            logging.debug("Streaming response enabled.")

            async def stream_response():
                try:
                    async with client.stream("POST", url, json=payload) as response:
                        response.raise_for_status()
                        if response.status_code != 200:
                            logging.error(
                                f"Failed to fetch streaming data: {response.status_code}"
                            )
                            error_content = await response.aread()
                            raise HTTPException(
                                status_code=response.status_code,
                                detail=error_content.decode(),
                            )
                        # Stream the content directly to the client
                        async for chunk in response.aiter_bytes():
                            yield chunk
                finally:
                    await client.aclose()  # Close the client after streaming is done

            return StreamingResponse(
                stream_response(),
                media_type="application/json",
            )
        else:
            # Non-streaming response
            async with client:
                response = await client.post(url, json=payload)
                response.raise_for_status()
                logging.debug(f"Response from Ollama: {response.status_code}")
                # Return the response content directly
                return Response(
                    content=response.content,
                    status_code=response.status_code,
                    # headers=response.headers,  # Include headers from Ollama
                    media_type=response.headers.get("Content-Type", "application/json"),
                )
    except httpx.HTTPStatusError as exc:
        error_content = await exc.response.aread()
        logging.error(
            f"Error response {exc.response.status_code} from Ollama: {error_content.decode()}"
        )
        raise HTTPException(
            status_code=exc.response.status_code, detail=error_content.decode()
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
