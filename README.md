# Smart Irrigation Recommendation Engine — Backend API

FastAPI backend for the AI-powered Smart Irrigation Recommendation Engine. It turns
soil sensor data, live weather, and crop growth stage into actionable irrigation
recommendations, a forward-looking schedule, mobile alerts, and water-usage analytics —
powered by the trained ML model in `models/irrigation_model_package.pkl` and the
`generate_recommendation()` rules engine from the original `src/recommendation.py`.

## Features implemented

| Feature (from problem statement) | Endpoints |
|---|---|
| Soil moisture monitoring | `POST/GET /api/fields/{id}/sensors` |
| Weather integration | `GET /api/weather/current`, `GET /api/weather/fields/{id}` (Open-Meteo, free/no key) |
| AI irrigation scheduling | `POST /api/fields/{id}/recommendations/generate`, `GET /api/fields/{id}/schedule` |
| Crop-stage analysis | crop stage stored/auto-estimated on each `Field`, fed into the ML model |
| Mobile alerts | `GET /api/fields/{id}/alerts`, `PATCH /api/alerts/{id}/read` (auto-created on Medium/High recommendations) |
| Water usage analytics | `POST/GET /api/fields/{id}/water-usage`, `GET /api/fields/{id}/analytics/summary`, `.../analytics/timeseries` |

## Architecture

```
backend/
├── app/
│   ├── main.py              # FastAPI app, CORS, router wiring, startup DB init
│   ├── config.py            # env-driven settings
│   ├── database.py          # SQLAlchemy engine/session (SQLite by default)
│   ├── models.py            # ORM tables: User, Field, SensorReading, Recommendation, Alert, WaterUsageLog
│   ├── schemas.py            # Pydantic request/response models
│   ├── recommendation.py    # unmodified rules engine from the original src/ (ML label -> action)
│   ├── weather_service.py   # Open-Meteo integration, with offline mock fallback
│   ├── utils.py              # unit conversion, crop-stage & season estimators
│   ├── ml/
│   │   └── model_loader.py  # loads irrigation_model_package.pkl, predict_irrigation_need()
│   └── routers/
│       ├── users.py
│       ├── fields.py
│       ├── sensors.py
│       ├── weather.py
│       ├── recommendations.py
│       ├── alerts.py
│       └── analytics.py
├── models/irrigation_model_package.pkl   # trained XGBoost pipeline + label mapping
├── requirements.txt
└── .env.example
```

### Recommendation pipeline

`POST /api/fields/{field_id}/recommendations/generate`:

1. Loads the field's latest sensor reading (soil moisture, pH, EC, organic carbon…).
2. Fetches live weather for the field's coordinates (temperature, humidity, rainfall,
   rain-forecast probability) — any value not provided by the sensor is filled in from
   weather, then a sane default.
3. Builds the exact feature row the trained model expects (`soil_ph`, `soil_moisture`,
   `organic_carbon`, `electrical_conductivity`, `temperature_c`, `humidity`, `rainfall_mm`,
   `sunlight_hours`, `wind_speed_kmh`, `field_area_hectare`, `previous_irrigation_mm`,
   `soil_type`, `crop_type`, `crop_growth_stage`, `season`, `mulching_used`, `region`)
   and runs it through the trained XGBoost pipeline → `Low` / `Medium` / `High`.
4. Passes that label plus soil moisture / rain forecast / temperature / humidity into
   `generate_recommendation()` (the original rules engine, unmodified) to get a final,
   farmer-friendly status/action/reason.
5. Estimates a recommended irrigation depth (mm), stores the `Recommendation`, and
   auto-creates a mobile `Alert` for anything Medium/High priority.

If the pickled model can't be loaded (e.g. an xgboost version mismatch in a bare-bones
environment) the API automatically falls back to a transparent rule-based heuristic so
every endpoint keeps working — check `GET /api/health` to see which is active.

Any prediction input can be overridden per-request via the request body (e.g. to simulate
"what if soil moisture were 15%") without needing a new sensor reading.

## Setup

```bash
cd backend
python3 -m venv .venv && source .venv/bin/activate     # optional but recommended
pip install -r requirements.txt
cp .env.example .env       # optional, defaults work out of the box
uvicorn app.main:app --reload --port 8000
```

Open http://localhost:8000/docs for interactive Swagger UI (all endpoints, try-it-out).

## Quick walkthrough (curl)

```bash
# 1. Register a farmer
curl -X POST localhost:8000/api/users -H "Content-Type: application/json" \
  -d '{"name":"Ramesh Kumar","phone":"9876543210"}'

# 2. Add a field (size in acres or hectares — auto-converted)
curl -X POST localhost:8000/api/fields -H "Content-Type: application/json" -d '{
  "user_id": 1, "name": "North Wheat Field", "crop_type": "Wheat",
  "sowing_date": "2026-06-01", "field_size": 5, "size_unit": "acre",
  "soil_type": "Clay", "region": "North", "latitude": 18.5204, "longitude": 73.8567
}'

# 3. Record a soil-moisture sensor reading
curl -X POST localhost:8000/api/fields/1/sensors -H "Content-Type: application/json" \
  -d '{"soil_moisture": 18, "soil_ph": 6.2}'

# 4. Ask the AI engine for a recommendation (auto-pulls weather + latest sensor reading)
curl -X POST localhost:8000/api/fields/1/recommendations/generate -H "Content-Type: application/json" -d '{}'

# 5. Get a 5-day forward irrigation schedule
curl localhost:8000/api/fields/1/schedule?days=5

# 6. Log actual water applied, then check analytics
curl -X POST localhost:8000/api/fields/1/water-usage -H "Content-Type: application/json" \
  -d '{"water_applied_mm": 12, "source": "recommended"}'
curl localhost:8000/api/fields/1/analytics/summary
```

## Notes for connecting the existing frontend (`frontend/*.html`)

The provided HTML pages are static mockups with matching intent:

- `onboarding.html` (name, phone) → `POST /api/users`
- `add_field.html` (fieldName, cropType, fieldSize, sizeUnit, sowingDate) → `POST /api/fields`
- `home_dashboard.html` / `field_details.html` → `GET /api/fields`, `GET /api/fields/{id}/recommendations/latest`
- `irrigation_schedule.html` → `GET /api/fields/{id}/schedule`
- `weather_forecast.html` → `GET /api/weather/fields/{id}`, `GET /api/weather/fields/{id}/forecast`
- `alerts.html` → `GET /api/fields/{id}/alerts`, `PATCH /api/alerts/{id}/read`
- `water_analytics.html` → `GET /api/fields/{id}/analytics/summary`, `.../analytics/timeseries`

CORS is open (`*`) by default so the HTML files can call the API directly from the
browser during development — tighten `CORS_ORIGINS` in `.env` for production.

## Design notes / things to harden for production

- Auth is intentionally minimal (name+phone, no password/JWT) to match the onboarding
  screen in the mockups — swap in real auth before going to production.
- `_estimate_water_mm()` and the fixed-schedule baseline in analytics are simple,
  transparent heuristics for a prototype; replace with a proper crop-water-balance
  model (ET₀/Kc-based) for production-grade dosing.
- SQLite is used by default for zero-setup local running; set `DATABASE_URL` to a
  Postgres/MySQL DSN for production.
