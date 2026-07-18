import time
from pathlib import Path

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/classifier", tags=["Classificador IMDB"])

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
    print(f"Carregando modelo de {MODEL_DIR}")
    time.sleep(1)
    model = "imdb-sentiment-mock-v1"
    print("Modelo Carregado")


@router.post("/predict", response_model=SentimentResponse)
def predict(request: ReviewRequest):
    if model is None:
        raise HTTPException(status_code=503, detail="Modelo não carregado")

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

    return SentimentResponse(sentiment=sentiment, confidence=confidence)
