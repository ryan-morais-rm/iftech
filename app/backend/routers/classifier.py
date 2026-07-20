import time
from pathlib import Path

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from logging_config import get_logger, section

router = APIRouter(prefix="/classifier", tags=["Classificador IMDB"])
logger = get_logger("classificador")

MODEL_DIR = Path(__file__).resolve().parent.parent / "ml" / "model"

model = None


class ReviewRequest(BaseModel):
    text: str


class SentimentResponse(BaseModel):
    sentiment: str
    confidence: float


@router.on_event("startup")
def load_model():
    global model
    section("Modelo Classico (IMDB)", color="\033[36m")
    logger.info(f"Carregando artefato de {MODEL_DIR}")
    time.sleep(1)
    model = "imdb-sentiment-mock-v1"
    logger.info(f"Modelo '{model}' carregado e pronto em memoria")


@router.post("/predict", response_model=SentimentResponse)
def predict(request: ReviewRequest):
    if model is None:
        raise HTTPException(status_code=503, detail="Modelo não carregado")

    start = time.perf_counter()

    positive_words = {"good", "great", "excellent", "amazing", "love", "best", "wonderful"}
    negative_words = {"bad", "terrible", "awful", "worst", "boring", "hate", "poor"}

    words = set(request.text.lower().split())
    positives = len(words & positive_words)
    negatives = len(words & negative_words)

    if positives >= negatives:
        sentiment = "Positivo"
    else:
        sentiment = "Negativo"

    total = positives + negatives
    confidence = 0.5 if total == 0 else round(max(positives, negatives) / total, 2)

    elapsed_ms = (time.perf_counter() - start) * 1000

    logger.info(f'Texto recebido: "{request.text}"')
    logger.info(f"Palavras positivas encontradas: {positives} | negativas: {negatives}")
    logger.info(f"Decisao: {sentiment} (confianca {confidence:.0%}) em {elapsed_ms:.1f}ms")

    return SentimentResponse(sentiment=sentiment, confidence=confidence)
