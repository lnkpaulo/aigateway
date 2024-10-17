# # main.py
# import logging
# import json
# import os
# import httpx
# from fastapi import FastAPI, HTTPException, Depends, Security, Response, APIRouter
# from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
# from pydantic import BaseModel
# from pydantic_settings import BaseSettings
# from typing import Dict, Any, Optional, List
# from fastapi.responses import JSONResponse, StreamingResponse
# from models import Settings

# # Import TokenManager
# from libs.token_manager import TokenManager

# # Configure logging
# logging.basicConfig(level=logging.DEBUG)

# app = FastAPI()

# # Initialize TokenManager
# token_manager = TokenManager()
# settings = Settings()

# # Create an APIRouter
# router = APIRouter(prefix=settings.BASE_PATH)


# # Define the HTTPBearer security scheme
# security_scheme = HTTPBearer(auto_error=False)

# # HELPERS #####################################################################################

# # Authentication Dependency
# async def get_api_key(credentials: HTTPAuthorizationCredentials = Security(security_scheme)):
#     logging.debug(f"get_api_key() called with credentials: {credentials}")

#     if credentials and credentials.scheme == "Bearer":
#         if token_manager.validate_token(credentials.credentials):
#             return credentials.credentials
#     raise HTTPException(status_code=401, detail="Invalid or missing token")

# # Request models
# class BaseRequest(BaseModel):
#     model: str
#     stream: Optional[bool] = True  # Default to True to match Ollama's default behavior
#     extra_params: Dict[str, Any] = {}

#     class Config:
#         extra = "allow"

# class GenerateRequest(BaseRequest):
#     prompt: str

# class ChatRequest(BaseRequest):
#     system: Optional[str] = None
#     messages: List[Dict[str, str]]

# # Helper function to forward requests
# async def forward_request(
#     endpoint: str,
#     payload: Dict[str, Any],
#     stream: bool,
# ) -> Response:
#     url = f"{settings.OLLAMA_BASE_URL}{endpoint}"
#     logging.debug(f"Forwarding request to {url} with payload: {payload}")

#     try:
#         if stream:
#             logging.debug("Streaming response enabled.")

#             async def stream_response():
#                 async with httpx.AsyncClient(timeout=None) as client:
#                     async with client.stream("POST", url, json=payload) as response:
#                         if response.status_code != 200:
#                             logging.error(
#                                 f"Failed to fetch streaming data: {response.status_code}"
#                             )
#                             raise HTTPException(
#                                 status_code=response.status_code,
#                                 detail=response.text,
#                             )

#                         async for chunk in response.aiter_bytes():
#                             yield chunk

#             return StreamingResponse(
#                 stream_response(), media_type="application/json"
#             )
#         else:
#             # Non-streaming response
#             async with httpx.AsyncClient(timeout=None) as client:
#                 response = await client.post(url, json=payload)
#                 response.raise_for_status()
#                 logging.debug(f"Response from Ollama: {response.status_code}")

#                 content = await response.aread()
#                 content_text = content.decode("utf-8")
#                 logging.debug(f"Response content from Ollama: {content_text}")

#                 # Parse the JSON content
#                 try:
#                     json_obj = json.loads(content_text)
#                 except json.JSONDecodeError as e:
#                     logging.error(f"JSON decoding error: {e}")
#                     raise HTTPException(
#                         status_code=500,
#                         detail="Invalid JSON response from Ollama",
#                     )
                
#                 # Return the parsed JSON as a JSONResponse
#                 return JSONResponse(content=json_obj, status_code=response.status_code)
            
#     except httpx.HTTPStatusError as exc:
#         logging.error(
#             f"Error response {exc.response.status_code} from Ollama: {exc.response.text}"
#         )
#         raise HTTPException(
#             status_code=exc.response.status_code, detail=exc.response.text
#         )
#     except httpx.RequestError as exc:
#         logging.error(f"Request forwarding failed: {exc}")
#         raise HTTPException(
#             status_code=500, detail=f"Request forwarding failed: {exc}"
#         )
#     except Exception as e:
#         logging.error(f"Unhandled exception: {e}")
#         raise HTTPException(status_code=500, detail="Request forwarding failed")

# # Helper function to forward GET requests
# async def forward_get_request(endpoint: str) -> Response:
#     url = f"{settings.OLLAMA_BASE_URL}{endpoint}"
#     logging.debug(f"Forwarding GET request to {url}")

#     try:
#         async with httpx.AsyncClient(timeout=None) as client:
#             response = await client.get(url)
#             response.raise_for_status()
#             content = await response.aread()
#             return Response(
#                 content=content,
#                 status_code=response.status_code,
#                 media_type=response.headers.get('Content-Type', 'application/json')
#             )
#     except httpx.HTTPStatusError as exc:
#         logging.error(
#             f"Error response {exc.response.status_code} from Ollama: {exc.response.text}"
#         )
#         raise HTTPException(
#             status_code=exc.response.status_code, detail=exc.response.text
#         )
#     except httpx.RequestError as exc:
#         logging.error(f"Request forwarding failed: {exc}")
#         raise HTTPException(
#             status_code=500, detail=f"Request forwarding failed: {exc}"
#         )
#     except Exception as e:
#         logging.error(f"Unhandled exception: {e}")
#         raise HTTPException(status_code=500, detail="Request forwarding failed")
    
# # APIs #####################################################################################

# # Route handlers
# @router.post("/generate")
# async def generate(
#     request_data: GenerateRequest, api_key: str = Security(get_api_key)
# ):
#     username = token_manager.get_user_by_token(api_key)
#     logging.debug(f"Generate request made by user: {username}")

#     # Prepare payload for forwarding
#     payload = request_data.model_dump(exclude_unset=True)
#     payload.update(request_data.extra_params)

#     return await forward_request(
#         endpoint="/api/generate",
#         payload=payload,
#         stream=request_data.stream,
#     )

# @router.post("/chat")
# async def chat(
#     request_data: ChatRequest, api_key: str = Security(get_api_key)
# ):
#     username = token_manager.get_user_by_token(api_key)
#     logging.debug(f"Chat request made by user: {username}")

#     # Prepare payload for forwarding
#     payload = request_data.model_dump(exclude_unset=True)
#     payload.update(request_data.extra_params)

#     return await forward_request(
#         endpoint="/api/chat",
#         payload=payload,
#         stream=request_data.stream,
#     )

# # Request model for embedding
# class EmbedRequest(BaseRequest):
#     input: str

# # Embed endpoint
# @router.post("/embed")
# async def embed(
#     request_data: EmbedRequest, api_key: str = Security(get_api_key)
# ):
#     username = token_manager.get_user_by_token(api_key)
#     logging.debug(f"Embeddings request made by user: {username}")

#     # Prepare payload for forwarding
#     payload = request_data.model_dump(exclude_unset=True)
#     payload.update(request_data.extra_params)

#     return await forward_request(
#         endpoint="/api/embed",
#         payload=payload,
#         stream=request_data.stream,
#     )


# # GET /api/tags endpoint
# @router.get("/tags")
# async def get_tags(api_key: str = Security(get_api_key)):
#     username = token_manager.get_user_by_token(api_key)
#     logging.debug(f"Tags request made by user: {username}")

#     return await forward_get_request(endpoint="/api/tags")

# app.include_router(router)

import logging
from fastapi import FastAPI
from models import Settings
from libs.token_manager import TokenManager
from routes import router  # Import the router from routes.py

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Initialize FastAPI app
app = FastAPI()

# Initialize TokenManager and Settings
token_manager = TokenManager()
settings = Settings()

# Include the router with the prefix defined in settings
app.include_router(router, prefix=settings.BASE_PATH)
