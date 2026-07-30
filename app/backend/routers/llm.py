import os
import time

import httpx
from fastapi import APIRouter, HTTPException
from google import genai
from google.genai import errors as genai_errors
from pydantic import BaseModel

from logging_config import get_logger

router = APIRouter(prefix="/llm", tags=["Chat LLM"])
logger = get_logger("llm")

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://ollama:11434")
LLM_MODEL = os.getenv("LLM_MODEL", "llama3.2")

GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.6-flash")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
gemini_client = genai.Client(api_key=GEMINI_API_KEY) if GEMINI_API_KEY else None


class ChatRequest(BaseModel):
    prompt: str


class ChatResponse(BaseModel):
    response: str


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    payload = {
        "model": LLM_MODEL,
        "prompt": request.prompt,
        "stream": False,
    }

    logger.info(f'Prompt recebido: "{request.prompt}"')
    logger.info(f"Encaminhando para Ollama ({OLLAMA_URL}) usando modelo '{LLM_MODEL}'")

    start = time.perf_counter()
    try:
        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(f"{OLLAMA_URL}/api/generate", json=payload)
            response.raise_for_status()
    except httpx.HTTPError as exc:
        logger.error(f"Falha ao falar com o Ollama: {exc}")
        raise HTTPException(status_code=502, detail=f"Erro ao comunicar com o Ollama: {exc}")

    elapsed_s = time.perf_counter() - start
    text = response.json()["response"]

    logger.info(f"Resposta gerada em {elapsed_s:.2f}s ({len(text)} caracteres)")
    logger.info(f'Preview: "{text[:120]}{"..." if len(text) > 120 else ""}"')

    return ChatResponse(response=text)


@router.post("/chat/api", response_model=ChatResponse)
async def chat_api(request: ChatRequest):
    if gemini_client is None:
        raise HTTPException(status_code=500, detail="GEMINI_API_KEY nao configurada no .env")

    logger.info(f'Prompt recebido (API): "{request.prompt}"')
    logger.info(f"Encaminhando para a API do Gemini usando modelo '{GEMINI_MODEL}'")

    start = time.perf_counter()
    try:
        result = await gemini_client.aio.models.generate_content(
            model=GEMINI_MODEL,
            contents=request.prompt,
        )
    except genai_errors.APIError as exc:
        if exc.code == 429:
            logger.warning(f"Limite de taxa do Gemini atingido: {exc}")
            raise HTTPException(
                status_code=429,
                detail="Muita gente usando o chat agora. Aguarde alguns segundos e tente de novo.",
            )
        logger.error(f"Falha ao falar com a API do Gemini: {exc}")
        raise HTTPException(status_code=502, detail=f"Erro ao comunicar com a API do Gemini: {exc}")

    text = result.text
    elapsed_s = time.perf_counter() - start

    logger.info(f"Resposta gerada em {elapsed_s:.2f}s ({len(text)} caracteres)")
    logger.info(f'Preview: "{text[:120]}{"..." if len(text) > 120 else ""}"')

    return ChatResponse(response=text)
