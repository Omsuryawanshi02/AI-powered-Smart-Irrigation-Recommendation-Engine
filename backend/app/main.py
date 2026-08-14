import logging
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

from .config import CORS_ORIGINS
from .database import Base, engine
from . import models  # noqa: F401  (ensures models are registered on Base before create_all)
from .routers import users, fields, sensors, weather, recommendations, alerts, analytics

logging.basicConfig(level=logging.INFO)

PROJECT_ROOT = Path(__file__).resolve().parents[2]
FRONTEND_DIR = PROJECT_ROOT / "frontend"

app = FastAPI(
    title="Smart Irrigation Recommendation Engine API",
    description=(
        "AI-based backend that turns soil, weather and crop-stage data into "
        "actionable irrigation recommendations, schedules, alerts and water-usage analytics."
    ),
    version="1.0.0",
)

origins = ["*"] if CORS_ORIGINS.strip() == "*" else [o.strip() for o in CORS_ORIGINS.split(",")]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)


@app.get("/", tags=["health"], include_in_schema=False)
def root():
    return RedirectResponse(url="/frontend/login.html")


@app.get("/frontend", include_in_schema=False)
def frontend_root():
    return RedirectResponse(url="/frontend/login.html")


@app.get("/api/health", tags=["health"])
def health():
    from .ml.model_loader import is_model_available
    return {"status": "ok", "ml_model_loaded": is_model_available()}


app.mount("/frontend", StaticFiles(directory=str(FRONTEND_DIR), html=True), name="frontend")

app.include_router(users.router)
app.include_router(fields.router)
app.include_router(sensors.router)
app.include_router(weather.router)
app.include_router(recommendations.router)
app.include_router(alerts.router)
app.include_router(analytics.router)
