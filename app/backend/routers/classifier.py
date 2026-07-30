import json
import re
import time
from pathlib import Path

import torch
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from logging_config import get_logger, section

router = APIRouter(prefix="/classifier", tags=["Classificador IMDB"])
logger = get_logger("classificador")

MODEL_DIR = Path(__file__).resolve().parent.parent / "ml" / "model"

TEMPERATURE = 8.0

model = None
vocab = None
max_len = None
model_version = None


class ReviewRequest(BaseModel):
    text: str


class SentimentResponse(BaseModel):
    sentiment: str
    confidence: float


def preprocess_text(text):
    text = re.sub(r"[^\w\s]", "", text)
    return text.lower()


def text_to_sequence(text, vocab_map):
    return [vocab_map.get(word, 0) for word in text.split()]


def pad_sequence(sequence, length):
    if len(sequence) >= length:
        return sequence[:length]
    return sequence + [0] * (length - len(sequence))


@router.on_event("startup")
def load_model():
    global model, vocab, max_len, model_version
    section("TextCNN Congelado (IMDB)", color="\033[36m")

    frozen_path = MODEL_DIR / "model_frozen.pt"
    vocab_path = MODEL_DIR / "vocab.json"
    metadata_path = MODEL_DIR / "metadata.json"

    if not frozen_path.exists() or not vocab_path.exists():
        logger.error(f"Artefato nao encontrado em {MODEL_DIR}. Rode ml/model/train.ipynb antes.")
        return

    logger.info(f"Carregando modelo congelado (TorchScript) de {frozen_path}")
    model = torch.jit.load(str(frozen_path))
    model.eval()

    vocab = json.loads(vocab_path.read_text())

    if metadata_path.exists():
        metadata = json.loads(metadata_path.read_text())
        model_version = metadata.get("version", "desconhecida")
        max_len = metadata.get("max_len", 200)
        test_accuracy = metadata.get("test_accuracy")
        accuracy_info = f"{test_accuracy:.2%}" if test_accuracy is not None else "nao calculada"
        logger.info(f"Modelo versao '{model_version}' carregado (acuracia de teste: {accuracy_info})")
    else:
        max_len = 200
        logger.info("Modelo carregado (sem metadata.json)")


@router.post("/predict", response_model=SentimentResponse)
def predict(request: ReviewRequest):
    if model is None:
        raise HTTPException(status_code=503, detail="Modelo não carregado")

    start = time.perf_counter()

    sequence = pad_sequence(text_to_sequence(preprocess_text(request.text), vocab), max_len)
    input_tensor = torch.tensor(sequence, dtype=torch.long).unsqueeze(0)

    with torch.no_grad():
        logits = model(input_tensor)
        print(logits, flush=True)
        probabilities = torch.softmax(logits / TEMPERATURE, dim=1)[0]
        print(probabilities, flush=True)


    predicted_class = int(probabilities.argmax())
    sentiment = "Positivo" if predicted_class == 1 else "Negativo"
    confidence = round(float(probabilities[predicted_class]), 2)

    elapsed_ms = (time.perf_counter() - start) * 1000

    logger.info(f'Texto recebido: "{request.text}"')
    logger.info(f"Decisao: {sentiment} (confianca {confidence:.0%}) em {elapsed_ms:.1f}ms [modelo {model_version}]")

    return SentimentResponse(sentiment=sentiment, confidence=confidence)
