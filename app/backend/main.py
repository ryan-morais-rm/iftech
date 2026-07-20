import time

from fastapi import FastAPI, Request

from logging_config import get_logger, setup_logging
from routers import classifier, llm

setup_logging()
logger = get_logger("http")

app = FastAPI(title="IFTech 2026 - Deploy de Modelos Classicos vs LLMs")

app.include_router(classifier.router)
app.include_router(llm.router)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    start = time.perf_counter()
    response = await call_next(request)
    elapsed_ms = (time.perf_counter() - start) * 1000

    logger.info(
        f"{request.method} {request.url.path} -> {response.status_code} ({elapsed_ms:.0f}ms)"
    )
    return response


@app.get("/health")
def health():
    return {"status": "ok"}
