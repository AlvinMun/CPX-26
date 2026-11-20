import os
from typing import Optional

import httpx
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

load_dotenv()

app = FastAPI(title="CrossPointX 2026 API", version="0.1.0")

frontend_origin = os.getenv("FRONTEND_ORIGIN", "http://localhost:5173")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[frontend_origin],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=8000)
    conversation_id: Optional[str] = None


class ChatResponse(BaseModel):
    reply: str
    conversation_id: Optional[str] = None
    provider: str


@app.get("/")
async def root():
    return {"name": "CrossPointX 2026 API", "status": "running"}


@app.get("/health")
async def health():
    return {"ok": True}


async def ask_dify(message: str, conversation_id: Optional[str]):
    api_key = os.getenv("DIFY_API_KEY")
    base_url = os.getenv("DIFY_BASE_URL", "https://api.dify.ai/v1").rstrip("/")
    if not api_key:
        raise HTTPException(status_code=503, detail="DIFY_API_KEY is not configured.")

    payload = {
        "inputs": {},
        "query": message,
        "response_mode": "blocking",
        "user": "crosspointx-demo-user",
    }
    if conversation_id:
        payload["conversation_id"] = conversation_id

    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(
            f"{base_url}/chat-messages",
            headers={"Authorization": f"Bearer {api_key}"},
            json=payload,
        )

    if response.is_error:
        raise HTTPException(
            status_code=502,
            detail=f"Dify request failed ({response.status_code}). Check your Dify app and API settings.",
        )
    data = response.json()
    return data.get("answer", "The AI service returned no answer."), data.get("conversation_id")


async def ask_openai_compatible(message: str):
    api_key = os.getenv("AIHUBMIX_API_KEY")
    base_url = os.getenv("AIHUBMIX_BASE_URL", "").rstrip("/")
    model = os.getenv("AIHUBMIX_MODEL", "")
    if not (api_key and base_url and model):
        raise HTTPException(
            status_code=503,
            detail="Set AIHUBMIX_API_KEY, AIHUBMIX_BASE_URL and AIHUBMIX_MODEL in backend/.env.",
        )

    # The supplied base URL should be the API base expected by the provider.
    # If the organiser's instructions specify a different endpoint format, follow those instructions.
    endpoint = base_url if base_url.endswith("/chat/completions") else f"{base_url}/chat/completions"

    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(
            endpoint,
            headers={"Authorization": f"Bearer {api_key}"},
            json={
                "model": model,
                "messages": [{"role": "user", "content": message}],
                "temperature": 0.5,
            },
        )

    if response.is_error:
        raise HTTPException(
            status_code=502,
            detail=f"Model provider request failed ({response.status_code}). Check the event-provided endpoint and model name.",
        )
    data = response.json()
    try:
        reply = data["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError):
        raise HTTPException(status_code=502, detail="The model provider returned an unexpected response format.")
    return reply


@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    provider = os.getenv("AI_PROVIDER", "mock").lower()

    if provider == "mock":
        return ChatResponse(
            reply=f"Demo mode is working. You sent: {request.message}",
            conversation_id=request.conversation_id,
            provider="mock",
        )

    if provider == "dify":
        reply, new_conversation_id = await ask_dify(request.message, request.conversation_id)
        return ChatResponse(reply=reply, conversation_id=new_conversation_id, provider="dify")

    if provider == "openai_compatible":
        reply = await ask_openai_compatible(request.message)
        return ChatResponse(reply=reply, conversation_id=None, provider="openai_compatible")

    raise HTTPException(status_code=500, detail="Unknown AI_PROVIDER. Use mock, dify, or openai_compatible.")
