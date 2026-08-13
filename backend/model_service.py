from pathlib import Path
import joblib
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR.parent / "models" / "irrigation_need_model.pkl"

_model = None
_load_error = None

def _load_model():
    global _model, _load_error
    if _model is not None:
        return _model
    if not MODEL_PATH.exists():
        _load_error = f"Model not found: {MODEL_PATH}"
        return None
    try:
        _model = joblib.load(MODEL_PATH)
        return _model
    except Exception as exc:
        _load_error = str(exc)
        return None

def model_status():
    model = _load_model()
    return {
        "loaded": model is not None,
        "path": str(MODEL_PATH),
        "error": _load_error
    }

def predict_irrigation_need(features):
    model = _load_model()

    # Safety fallback keeps the API usable during development if the
    # serialized ML environment is not installed correctly.
    if model is None:
        moisture = float(features["Soil_Moisture"])
        temp = float(features.get("Temperature_C", 25))
        humidity = float(features.get("Humidity", 60))
        rain = float(features.get("Rainfall_mm", 0))

        if moisture < 20 and temp >= 30 and humidity < 50 and rain < 20:
            label, confidence = "High", None
        elif moisture < 35 and rain < 20:
            label, confidence = "Medium", None
        else:
            label, confidence = "Low", None

        return {"label": label, "confidence": confidence, "model": "rule-based fallback"}

    frame = pd.DataFrame([features])
    pred = model.predict(frame)[0]

    # The trained notebook uses XGBoost with labels 0/1/2.
    mapping = {0: "Low", 1: "Medium", 2: "High"}
    label = mapping.get(int(pred), str(pred))

    confidence = None
    if hasattr(model, "predict_proba"):
        try:
            probs = model.predict_proba(frame)[0]
            confidence = round(float(max(probs)), 4)
        except Exception:
            pass

    return {
        "label": label,
        "confidence": confidence,
        "model": "XGBoost"
    }
