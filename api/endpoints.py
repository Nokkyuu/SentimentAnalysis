from fastapi import APIRouter, Query
from nlp import SentimentAnalyser
from .models import TextRequest, BulkTextRequest

import logging

logger = logging.getLogger("backend")

router = APIRouter()

@router.get("/")
def read_root():
    return {"API": "Running"}


@router.post("/analyse")
def analyze_text(
    type: str = Query("full", description="Analysis type: 'full' or 'sentence'"),
    body: TextRequest = TextRequest(text=""),
):
    text = body.text
    analyser = SentimentAnalyser()
    if type == "full":
        result = analyser.analyse_text_full(text)
    elif type == "sentence":
        result = analyser.analyse_text_per_sentence(text)
    else:
        logger.error(f"Invalid type: {type}")
        return {"error": "Invalid type. Use 'full' or 'sentence'."}
    confidence = analyser.sentiment_confidence_score(text)
    return {"type": type, "result": result, "confidence": confidence}

@router.post("/analyse/bulk")
def analyze_text_bulk(
    body: BulkTextRequest = BulkTextRequest(texts=[]),
):
    texts = body.texts
    analyser = SentimentAnalyser()
    results = []
    for text in texts:
        result = analyser.analyse_text_full(text)
        confidence = analyser.sentiment_confidence_score(text)
        results.append({"text": text, "result": result, "confidence": confidence})
    return results