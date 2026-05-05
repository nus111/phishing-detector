from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import os

app = FastAPI(
    title="Phishing Detector ML Service",
    description="XLM-RoBERTa based phishing detection inference",
    version="1.0.0",
)

# Model placeholder — will be loaded from MODEL_PATH
model = None
MODEL_PATH = os.getenv("MODEL_PATH", "/app/models/xlm-roberta-phishing")


class PredictRequest(BaseModel):
    text: str
    language: Optional[str] = None


class DetectedPattern(BaseModel):
    type: str
    confidence: float
    evidence: str
    explanation: str


class PredictResponse(BaseModel):
    risk_score: float
    risk_level: str
    detected_language: str
    detected_patterns: List[Dict[str, Any]]
    recommendation: str
    model_version: str


@app.on_event("startup")
async def load_model():
    """Load the ML model on startup."""
    global model
    # TODO: Uncomment when model is trained
    # from transformers import pipeline
    # model = pipeline("text-classification", model=MODEL_PATH, return_all_scores=True)
    print(f"[ML Service] Model placeholder loaded (path: {MODEL_PATH})")


@app.get("/health")
async def health():
    return {"status": "healthy", "model_loaded": model is not None}


@app.post("/predict", response_model=PredictResponse)
async def predict(request: PredictRequest):
    """
    Predict phishing risk for a given text message.
    Returns risk score, level, detected patterns, and recommendation.
    """
    # TODO: Replace with actual model inference
    # For now, return a placeholder response
    text = request.text

    # Simple rule-based placeholder
    risk_score = 50.0
    detected_patterns = []
    detected_language = request.language or "en"

    # Placeholder heuristics
    urgency_words = ["立即", "马上", "urgent", "immediately", "click now", "segera"]
    threat_words = ["签证", "冻结", "arrest", "frozen", "visa", "cancel"]
    link_indicators = ["http://", "https://", "bit.ly", "tinyurl"]

    for word in urgency_words:
        if word.lower() in text.lower():
            risk_score += 15
            detected_patterns.append({
                "type": "urgency_pressure",
                "confidence": 0.8,
                "evidence": word,
                "explanation": "Uses urgency language to force quick action",
            })

    for word in threat_words:
        if word.lower() in text.lower():
            risk_score += 20
            detected_patterns.append({
                "type": "threat_language",
                "confidence": 0.85,
                "evidence": word,
                "explanation": "Contains threat or fear-inducing language",
            })

    for indicator in link_indicators:
        if indicator in text.lower():
            risk_score += 10
            detected_patterns.append({
                "type": "suspicious_link",
                "confidence": 0.7,
                "evidence": indicator,
                "explanation": "Contains a link that may be suspicious",
            })

    risk_score = min(risk_score, 100.0)
    risk_level = "low" if risk_score < 40 else ("medium" if risk_score < 70 else "high")

    recommendation = {
        "low": "This message appears to be safe. Always exercise caution with unknown senders.",
        "medium": "This message shows some suspicious patterns. Verify the sender before taking action.",
        "high": "This message has a high probability of being a phishing attempt. Do NOT click any links or provide personal information.",
    }[risk_level]

    return PredictResponse(
        risk_score=risk_score,
        risk_level=risk_level,
        detected_language=detected_language,
        detected_patterns=detected_patterns,
        recommendation=recommendation,
        model_version="placeholder-v1.0",
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
