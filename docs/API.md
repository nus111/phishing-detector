# API Documentation

## Base URL
```
http://localhost:8000/api/v1
```

## Authentication

All protected endpoints require a Bearer token in the Authorization header:
```
Authorization: Bearer <access_token>
```

---

### POST /auth/register
Register a new user.

**Request:**
```json
{
    "name": "John Doe",
    "email": "john@example.com",
    "password": "securepassword",
    "preferred_language": "en"
}
```

**Response (201):**
```json
{
    "id": "uuid",
    "email": "john@example.com",
    "name": "John Doe",
    "preferred_language": "en",
    "role": "user",
    "created_at": "2026-05-05T00:00:00"
}
```

---

### POST /auth/login
Authenticate and get tokens.

**Request:**
```json
{
    "email": "john@example.com",
    "password": "securepassword"
}
```

**Response (200):**
```json
{
    "access_token": "eyJ...",
    "refresh_token": "eyJ...",
    "token_type": "bearer"
}
```

---

### GET /auth/me
Get current user info. **🔒 Protected**

---

### POST /analyze
Analyze a message for phishing. **🔒 Protected**

**Request:**
```json
{
    "text": "您的签证已被取消，立即点击链接重新申请",
    "language": "zh"
}
```

**Response (200):**
```json
{
    "id": "uuid",
    "input_text": "您的签证已被取消...",
    "detected_language": "zh",
    "risk_score": 85.0,
    "risk_level": "high",
    "detected_patterns": [
        {
            "type": "threat_language",
            "confidence": 0.85,
            "evidence": "签证",
            "explanation": "Contains threat or fear-inducing language"
        }
    ],
    "recommendation": "This message has a high probability...",
    "model_version": "placeholder-v1.0",
    "created_at": "2026-05-05T00:00:00"
}
```

---

### GET /analyze/history?page=1&limit=20
Get analysis history. **🔒 Protected**

---

### GET /education?language=en
List education content. Optionally filter by language.

### GET /education/{id}
Get single education content detail.

### POST /education/quiz/submit
Submit quiz answers. **🔒 Protected**

### GET /education/progress
Get user's learning progress. **🔒 Protected**

---

### GET /admin/dashboard
Admin dashboard stats. **🔒 Admin Only**

### GET /admin/threats?language=zh
Threat trends. **🔒 Admin Only**

### GET /admin/users
User list. **🔒 Admin Only**

### POST /admin/retrain
Trigger model retraining. **🔒 Admin Only**

### GET /admin/feedback
User feedback list. **🔒 Admin Only**
