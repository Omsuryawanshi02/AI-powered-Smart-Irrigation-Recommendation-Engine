# AquaSmart Backend

Flask REST API for the AI-powered Smart Irrigation Recommendation Engine.

## Architecture

Frontend → Flask REST API → ML Model + Weather API → SQLite database

### Main modules

- `app.py` — API routes
- `model_service.py` — XGBoost model loading and prediction
- `recommendation.py` — farmer-friendly recommendation/safety rules
- `weather_service.py` — OpenWeather integration
- `db.py` — SQLite schema and database connection

## Setup

From the project root:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r backend/requirements.txt
```

Create `backend/.env` from `.env.example` and add the OpenWeather API key.

Make sure the trained model exists at:

```text
models/irrigation_need_model.pkl
```

## Run

```bash
python backend/app.py
```

API base URL:

```text
http://127.0.0.1:5000/api
```

## Core endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/api/health` | Backend/model health |
| GET | `/api/model/status` | ML model status |
| GET | `/api/fields` | List fields |
| POST | `/api/fields` | Add field |
| GET | `/api/fields/<id>` | Field details |
| POST | `/api/fields/<id>/sensor-readings` | Save sensor data |
| GET | `/api/fields/<id>/readings/latest` | Latest sensor reading |
| POST | `/api/irrigation/recommend` | Generate AI recommendation |
| GET | `/api/fields/<id>/recommendations` | Recommendation history |
| POST | `/api/weather` | Get current weather |
| GET | `/api/dashboard/<id>` | Dashboard data |
| POST | `/api/water-usage` | Save water usage |

## Test recommendation

```bash
curl -X POST http://127.0.0.1:5000/api/irrigation/recommend ^
  -H "Content-Type: application/json" ^
  -d "{\"soil_moisture\":12,\"temperature\":36,\"humidity\":42,\"rainfall_mm\":0,\"rain_forecast\":5,\"crop_type\":\"Wheat\",\"crop_growth_stage\":\"Vegetative\",\"soil_type\":\"Clay\"}"
```

Expected result: a High irrigation recommendation.

## Frontend integration

Use JavaScript `fetch()` from your HTML pages:

```javascript
const response = await fetch("http://127.0.0.1:5000/api/irrigation/recommend", {
  method: "POST",
  headers: {"Content-Type": "application/json"},
  body: JSON.stringify({
    soil_moisture: 18,
    temperature: 34,
    humidity: 45,
    rainfall_mm: 0,
    rain_forecast: 5,
    crop_type: "Wheat",
    crop_growth_stage: "Vegetative",
    soil_type: "Clay"
  })
});

const data = await response.json();
console.log(data.recommendation);
```

## Important model note

The training notebook uses an XGBoost classification pipeline with categorical preprocessing. The API sends all 19 model features expected by the trained pipeline.

If the serialized model cannot be loaded because the local Python/scikit-learn/XGBoost versions differ, the API uses a small rule-based fallback so the website remains testable. For final deployment, install the same ML library versions used to create the `.pkl` file and verify `/api/model/status` reports `"loaded": true`.
