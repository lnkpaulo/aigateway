import logging
import json
import os
import httpx
from fastapi import FastAPI, HTTPException, Depends, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from pydantic_settings import BaseSettings
from typing import Dict, Any, Optional
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
    FORWARD_URL: str

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

# Request model
class GenerateRequest(BaseModel):
    model: str
    prompt: str
    stream: Optional[bool] = False
    extra_params: Dict[str, Any] = {}

    class Config:
        extra = "allow"

@app.post("/generate")
async def generate(
    request_data: GenerateRequest, api_key: str = Depends(get_api_key)
):
    logging.debug(f"Received request with data: {request_data}")

    # Optional: Get the username associated with the token
    username = token_manager.get_user_by_token(api_key)
    logging.debug(f"Request made by user: {username}")

    # Prepare payload for forwarding
    payload = request_data.dict(exclude_unset=True)
    payload.update(request_data.extra_params)

    logging.debug(f"Payload to forward: {payload}")

    try:
        if request_data.stream:
            logging.debug("Streaming response enabled.")

            async def stream_response():
                async with httpx.AsyncClient(timeout=None) as client:
                    async with client.stream(
                        "POST", settings.FORWARD_URL, json=payload
                    ) as response:
                        if response.status_code != 200:
                            logging.error(
                                f"Failed to fetch streaming data: {response.status_code}"
                            )
                            raise HTTPException(
                                status_code=response.status_code, detail=response.text
                            )

                        async for chunk in response.aiter_bytes():
                            yield chunk

            return StreamingResponse(
                stream_response(), media_type="application/json"
            )

        else:
            async with httpx.AsyncClient(timeout=None) as client:
                response = await client.post(settings.FORWARD_URL, json=payload)
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
