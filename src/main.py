import logging
from fastapi import FastAPI, HTTPException, Depends, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from pydantic_settings import BaseSettings
from typing import Dict, Any, Optional
import httpx
from fastapi.responses import JSONResponse, StreamingResponse
import json

# Configure logging
logging.basicConfig(level=logging.DEBUG)

app = FastAPI()

# Settings class
class Settings(BaseSettings):
    AUTH_TOKEN: str
    FORWARD_URL: str

    class Config:
        env_file = ".env"

settings = Settings()

# Define the HTTPBearer security scheme
security_scheme = HTTPBearer(auto_error=False)

# Authentication Dependency
async def get_api_key(credentials: HTTPAuthorizationCredentials = Security(security_scheme)):
    if credentials and credentials.scheme == "Bearer" and credentials.credentials == settings.AUTH_TOKEN:
        return credentials.credentials
    else:
        raise HTTPException(status_code=401, detail="Invalid or missing token")
    
class GenerateRequest(BaseModel):
    model: str
    prompt: str
    stream: Optional[bool] = False
    extra_params: Dict[str, Any] = {}

    class Config:
        extra = "allow"

@app.post("/generate")
async def generate(request_data: GenerateRequest, api_key: str = Depends(get_api_key)):
    logging.debug(f"Received request with data: {request_data}")
    # Token has been validated; proceed with the logic

    # Prepare payload for forwarding
    payload = request_data.dict(exclude_unset=True)
    payload.update(request_data.extra_params)

    logging.debug(f"Payload to forward: {payload}")

    try:
        # Handle streaming response if stream: true is set
        if request_data.stream:
            logging.debug("Streaming response enabled.")

            # Function to yield data from Ollama stream
            async def stream_response():
                async with httpx.AsyncClient(timeout=None) as client:
                    async with client.stream("POST", settings.FORWARD_URL, json=payload) as response:
                        if response.status_code != 200:
                            logging.error(f"Failed to fetch streaming data: {response.status_code}")
                            raise HTTPException(status_code=response.status_code, detail=response.text)

                        async for chunk in response.aiter_bytes():
                            yield chunk

            # Return the streamed response
            return StreamingResponse(stream_response(), media_type="application/json")

        # If stream is False or not set, handle regular request
        else:
            async with httpx.AsyncClient(timeout=None) as client:
                response = await client.post(settings.FORWARD_URL, json=payload)
                response.raise_for_status()  # Raise an error for non-2xx responses
                logging.debug(f"Response from Ollama: {response.status_code}")

                # Read the entire response content
                content = await response.aread()
                content_text = content.decode('utf-8')

                # Split the content into individual JSON objects
                json_objects = []
                for line in content_text.strip().split('\n'):
                    if line.strip():
                        try:
                            json_obj = json.loads(line)
                            json_objects.append(json_obj)
                        except json.JSONDecodeError as e:
                            logging.error(f"JSON decoding error: {e}")
                            raise HTTPException(status_code=500, detail="Invalid JSON response from Ollama")

                # Aggregate or process the JSON objects
                # For example, you might want to collect all 'response' fields
                responses = ''.join(obj.get('response', '') for obj in json_objects)
                # Return the aggregated response
                return JSONResponse(content={"response": responses}, status_code=response.status_code)

    except httpx.HTTPStatusError as exc:
        logging.error(f"Error response {exc.response.status_code} from Ollama: {exc.response.text}")
        raise HTTPException(status_code=exc.response.status_code, detail=exc.response.text)
    except httpx.RequestError as exc:
        logging.error(f"Request forwarding failed: {exc}")
        raise HTTPException(status_code=500, detail=f"Request forwarding failed: {exc}")
    except Exception as e:
        logging.error(f"Unhandled exception: {e}")
        raise HTTPException(status_code=500, detail="Request forwarding failed")
