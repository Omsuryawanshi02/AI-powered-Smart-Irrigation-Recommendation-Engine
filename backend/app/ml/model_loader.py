"""
Loads the trained irrigation-need classification model (models/irrigation_model_package.pkl)
and exposes a simple predict() function used by the recommendation engine.

The package was produced by notebooks/02_irrigation_model_training.ipynb and is a dict:
    {
        "model": sklearn.pipeline.Pipeline (preprocessor + XGBoost classifier),
        "label_mapping": {0: "Low", 1: "Medium", 2: "High"},
    }
"""
import logging
import threading
from typing import Any, Dict

import joblib
import pandas as pd

from ..config import MODEL_PATH

logger = logging.getLogger("irrigation.ml")

NUMERIC_FEATURES = [
    "soil_ph", "soil_moisture", "organic_carbon", "electrical_conductivity",
    "temperature_c", "humidity", "rainfall_mm", "sunlight_hours",
    "wind_speed_kmh", "field_area_hectare", "previous_irrigation_mm",
]

CATEGORICAL_FEATURES = [
    "soil_type", "crop_type", "crop_growth_stage", "season",
    "mulching_used", "region",
]

FEATURE_ORDER = NUMERIC_FEATURES + CATEGORICAL_FEATURES

_lock = threading.Lock()
_model = None
_label_mapping: Dict[int, str] = {0: "Low", 1: "Medium", 2: "High"}
_load_error: str | None = None


def _load():
    global _model, _label_mapping, _load_error
    with _lock:
        if _model is not None or _load_error is not None:
            return
        try:
            package = joblib.load(MODEL_PATH)
            _model = package["model"]
            _label_mapping = package.get("label_mapping", _label_mapping)
            logger.info("Irrigation ML model loaded from %s", MODEL_PATH)
        except Exception as exc:  # noqa: BLE001
            _load_error = str(exc)
            logger.warning("Could not load ML model (%s). Falling back to rule-based heuristic.", exc)


def is_model_available() -> bool:
    _load()
    return _model is not None


def _heuristic_predict(features: Dict[str, Any]) -> str:
    """Fallback used only if the pickled model can't be loaded (e.g. missing
    xgboost dependency). Keeps the API functional end-to-end regardless."""
    moisture = float(features.get("soil_moisture", 50))
    rainfall = float(features.get("rainfall_mm", 0))
    temperature = float(features.get("temperature_c", 25))

    score = 0
    score += 2 if moisture < 25 else (1 if moisture < 40 else 0)
    score += 1 if temperature >= 32 else 0
    score += 1 if rainfall < 5 else 0

    if score >= 3:
        return "High"
    if score >= 1:
        return "Medium"
    return "Low"


def predict_irrigation_need(features: Dict[str, Any]) -> Dict[str, Any]:
    """
    Predict irrigation need (Low / Medium / High) from a feature dict.
    Missing categorical fields default to the most common training value;
    missing numeric fields default to a neutral mid-range value.

    Returns {"irrigation_need": str, "confidence": float | None, "model": "ml" | "heuristic"}
    """
    _load()

    row = {k: features.get(k) for k in FEATURE_ORDER}

    if _model is None:
        label = _heuristic_predict(features)
        return {"irrigation_need": label, "confidence": None, "model": "heuristic"}

    df = pd.DataFrame([row])
    pred = _model.predict(df)[0]

    confidence = None
    if hasattr(_model, "predict_proba"):
        try:
            proba = _model.predict_proba(df)[0]
            confidence = float(max(proba))
        except Exception:  # noqa: BLE001
            confidence = None

    label = _label_mapping.get(int(pred), str(pred)) if not isinstance(pred, str) else pred
    return {"irrigation_need": label, "confidence": confidence, "model": "ml"}
