"""
Smart Irrigation Recommendation Engine

This module converts the ML model output
(Low / Medium / High) into a farmer-friendly
irrigation recommendation.

The recommendation also considers:
- Soil moisture
- Rain forecast
- Temperature
- Humidity
- Recent rainfall
"""

from typing import Optional, Dict, Any


def generate_recommendation(
    irrigation_need: str,
    soil_moisture: float,
    rain_forecast: float = 0,
    temperature: Optional[float] = None,
    humidity: Optional[float] = None,
    rainfall: Optional[float] = None,
) -> Dict[str, Any]:
    """
    Generate a final irrigation recommendation.

    Parameters
    ----------
    irrigation_need : str
        ML model prediction: Low, Medium, or High.

    soil_moisture : float
        Current soil moisture percentage.

    rain_forecast : float
        Expected rainfall/probability indicator.
        In the current prototype, values >= 70
        are treated as a high-rain condition.

    temperature : float, optional
        Current temperature in °C.

    humidity : float, optional
        Current relative humidity percentage.

    rainfall : float, optional
        Recent rainfall value.

    Returns
    -------
    dict
        Final irrigation recommendation.
    """

    # ---------------------------------------------------------
    # 1. Normalize input
    # ---------------------------------------------------------
    irrigation_need = str(irrigation_need).strip().title()

    try:
        soil_moisture = float(soil_moisture)
    except (TypeError, ValueError):
        raise ValueError("soil_moisture must be a numeric value.")

    try:
        rain_forecast = float(rain_forecast)
    except (TypeError, ValueError):
        raise ValueError("rain_forecast must be a numeric value.")

    # ---------------------------------------------------------
    # 2. Validate ranges
    # ---------------------------------------------------------
    if not 0 <= soil_moisture <= 100:
        raise ValueError(
            "soil_moisture must be between 0 and 100."
        )

    if not 0 <= rain_forecast <= 100:
        raise ValueError(
            "rain_forecast must be between 0 and 100."
        )

    # ---------------------------------------------------------
    # 3. Safety rule: high rain forecast
    # ---------------------------------------------------------
    if rain_forecast >= 70:

        return {
            "status": "Delay Irrigation",
            "priority": "Low",
            "action": "Do not irrigate now",
            "irrigation_need": irrigation_need,
            "reason": "High rainfall is expected.",
            "soil_moisture": round(soil_moisture, 2),
            "rain_forecast": round(rain_forecast, 2)
        }

    # ---------------------------------------------------------
    # 4. Safety rule: soil already sufficiently wet
    # ---------------------------------------------------------
    if soil_moisture >= 50:

        return {
            "status": "No Immediate Irrigation",
            "priority": "Low",
            "action": "Monitor soil moisture",
            "irrigation_need": irrigation_need,
            "reason": "Soil moisture is currently sufficient.",
            "soil_moisture": round(soil_moisture, 2),
            "rain_forecast": round(rain_forecast, 2)
        }

    # ---------------------------------------------------------
    # 5. High irrigation requirement
    # ---------------------------------------------------------
    if irrigation_need == "High":

        reason_parts = [
            "AI model detected high irrigation requirement."
        ]

        if soil_moisture < 25:
            reason_parts.append(
                "Soil moisture is critically low."
            )

        if temperature is not None and temperature >= 32:
            reason_parts.append(
                "Temperature is high."
            )

        if humidity is not None and humidity < 50:
            reason_parts.append(
                "Humidity is relatively low."
            )

        return {
            "status": "Irrigation Required",
            "priority": "High",
            "action": "Irrigate now",
            "irrigation_need": "High",
            "reason": " ".join(reason_parts),
            "soil_moisture": round(soil_moisture, 2),
            "rain_forecast": round(rain_forecast, 2)
        }

    # ---------------------------------------------------------
    # 6. Medium irrigation requirement
    # ---------------------------------------------------------
    if irrigation_need == "Medium":

        reason_parts = [
            "AI model detected moderate irrigation requirement."
        ]

        if soil_moisture < 30:
            reason_parts.append(
                "Soil moisture is below the preferred level."
            )

        if rain_forecast < 20:
            reason_parts.append(
                "Significant rainfall is not expected."
            )

        return {
            "status": "Irrigation Recommended",
            "priority": "Medium",
            "action": "Plan irrigation soon",
            "irrigation_need": "Medium",
            "reason": " ".join(reason_parts),
            "soil_moisture": round(soil_moisture, 2),
            "rain_forecast": round(rain_forecast, 2)
        }

    # ---------------------------------------------------------
    # 7. Low irrigation requirement
    # ---------------------------------------------------------
    if irrigation_need == "Low":

        return {
            "status": "No Immediate Irrigation",
            "priority": "Low",
            "action": "Wait and monitor",
            "irrigation_need": "Low",
            "reason": (
                "AI model detected low irrigation requirement "
                "under the current conditions."
            ),
            "soil_moisture": round(soil_moisture, 2),
            "rain_forecast": round(rain_forecast, 2)
        }

    # ---------------------------------------------------------
    # 8. Unknown model output
    # ---------------------------------------------------------
    raise ValueError(
        "irrigation_need must be Low, Medium, or High."
    )