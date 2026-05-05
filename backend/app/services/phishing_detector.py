"""
Phishing detection service.
Tries ML service first, falls back to rule-based detection.
"""
import httpx
import re
from typing import Optional, List, Dict, Any
from app.core.config import settings


# ── Language detection (simple heuristic) ──
def detect_language(text: str) -> str:
    """Simple language detection based on character ranges."""
    if re.search(r'[\u4e00-\u9fff]', text):
        return "zh"
    if re.search(r'[\u0b80-\u0bff]', text):
        return "ta"
    malay_words = ["yang", "dan", "untuk", "adalah", "dengan", "tidak", "ini", "akan"]
    text_lower = text.lower()
    malay_count = sum(1 for w in malay_words if w in text_lower)
    if malay_count >= 2:
        return "ms"
    return "en"


# ── Rule-based detection ──
URGENCY_KEYWORDS = [
    # English
    "urgent", "immediately", "act now", "click here", "click now",
    "expires", "limited time", "don't delay", "right away",
    # Chinese
    "立即", "马上", "紧急", "限时", "尽快", "速速", "立刻",
    # Malay
    "segera", "secepat mungkin", "sekarang", "terus", "penting",
    # Tamil
    "உடனடி", "இப்போது", "விரைவில்", "அவசர",
]

THREAT_KEYWORDS = [
    # English
    "arrest", "frozen", "suspended", "terminated", "illegal",
    "warrant", "police", "court", "legal action", "penalty",
    "deported", "visa cancelled", "blocked", "locked",
    # Chinese
    "逮捕", "冻结", "取消", "违法", "处罚", "遣返",
    "签证", "身份", "账户冻结", "警方", "法院",
    # Malay
    "ditangkap", "dibekukan", "digantung", "dibatalkan",
    "haram", "undang-undang", "polis", "mahkamah", "visa",
    # Tamil
    "கைது", "உறைநிலை", "ரத்து", "சட்டவிரோத",
    "போலீஸ்", "நீதிமன்றம்", "விசா",
]

FINANCIAL_KEYWORDS = [
    "bank account", "credit card", "transfer", "wire", "payment",
    "deposit", "refund", "lottery", "prize", "inheritance",
    "比特币", "转账", "汇款", "银行", "中奖",
    "bank", "pindahan", "wang", "duit", "hadiah",
    "வங்கி", "பரிமாற்றம்", "பணம்",
]

LINK_PATTERNS = [
    r"https?://[^\s]+",
    r"bit\.ly/[^\s]+",
    r"tinyurl\.com/[^\s]+",
    r"t\.co/[^\s]+",
    r"\b\w+\.xyz\b",
    r"\b\w+\.top\b",
]


def rule_based_detect(text: str) -> Dict[str, Any]:
    """Rule-based phishing detection with multi-language support."""
    risk_score = 0.0
    detected_patterns: List[Dict[str, Any]] = []
    text_lower = text.lower()

    # Check urgency keywords
    found_urgency = [kw for kw in URGENCY_KEYWORDS if kw.lower() in text_lower]
    if found_urgency:
        score_boost = min(len(found_urgency) * 12, 30)
        risk_score += score_boost
        detected_patterns.append({
            "type": "urgency_pressure",
            "confidence": min(0.6 + len(found_urgency) * 0.1, 0.95),
            "evidence": ", ".join(found_urgency[:3]),
            "explanation": "Uses urgency language to pressure quick action without thinking",
        })

    # Check threat keywords
    found_threats = [kw for kw in THREAT_KEYWORDS if kw.lower() in text_lower]
    if found_threats:
        score_boost = min(len(found_threats) * 15, 35)
        risk_score += score_boost
        detected_patterns.append({
            "type": "threat_language",
            "confidence": min(0.65 + len(found_threats) * 0.1, 0.95),
            "evidence": ", ".join(found_threats[:3]),
            "explanation": "Contains threatening language designed to create fear and panic",
        })

    # Check financial keywords
    found_financial = [kw for kw in FINANCIAL_KEYWORDS if kw.lower() in text_lower]
    if found_financial:
        score_boost = min(len(found_financial) * 10, 25)
        risk_score += score_boost
        detected_patterns.append({
            "type": "financial_lure",
            "confidence": min(0.5 + len(found_financial) * 0.1, 0.85),
            "evidence": ", ".join(found_financial[:3]),
            "explanation": "Contains financial terms commonly used in fraud schemes",
        })

    # Check for suspicious links
    found_links = []
    for pattern in LINK_PATTERNS:
        matches = re.findall(pattern, text, re.IGNORECASE)
        found_links.extend(matches)
    if found_links:
        risk_score += 15
        detected_patterns.append({
            "type": "suspicious_link",
            "confidence": 0.7,
            "evidence": found_links[0][:60],
            "explanation": "Contains a link that may lead to a phishing website",
        })

    # Cap at 100
    risk_score = min(risk_score, 100.0)
    risk_level = "low" if risk_score < 40 else ("medium" if risk_score < 70 else "high")

    recommendations = {
        "low": "This message appears relatively safe. Always verify the sender's identity before taking any action.",
        "medium": "This message shows some suspicious patterns. Do not click links or share personal info until you verify the sender through official channels.",
        "high": "This message has a HIGH probability of being phishing. Do NOT click any links, do NOT reply, and do NOT provide any personal information. Report this message to the relevant authorities.",
    }

    return {
        "risk_score": round(risk_score, 1),
        "risk_level": risk_level,
        "detected_patterns": detected_patterns,
        "recommendation": recommendations[risk_level],
        "model_version": "rule-based-v1.0",
    }


async def detect_phishing(text: str, language: Optional[str] = None) -> Dict[str, Any]:
    """Main detection entry point. Tries ML service, falls back to rules."""
    detected_language = language or detect_language(text)

    # Try ML service
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.post(
                f"{settings.ML_SERVICE_URL}/predict",
                json={"text": text, "language": detected_language},
            )
            if resp.status_code == 200:
                result = resp.json()
                result["detected_language"] = detected_language
                return result
    except Exception:
        pass  # Fall through to rule-based

    # Fallback: rule-based
    result = rule_based_detect(text)
    result["detected_language"] = detected_language
    return result
