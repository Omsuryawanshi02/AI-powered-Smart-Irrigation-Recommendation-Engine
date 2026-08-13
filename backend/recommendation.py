def generate_recommendation(
    irrigation_need,
    soil_moisture,
    rain_forecast=0,
    temperature=None,
    humidity=None,
    rainfall=None
):
    irrigation_need = str(irrigation_need).strip().title()
    soil_moisture = float(soil_moisture)
    rain_forecast = float(rain_forecast)

    if not 0 <= soil_moisture <= 100:
        raise ValueError("soil_moisture must be between 0 and 100")
    if not 0 <= rain_forecast <= 100:
        raise ValueError("rain_forecast must be between 0 and 100")
    if irrigation_need not in {"Low", "Medium", "High"}:
        raise ValueError("irrigation_need must be Low, Medium, or High")

    if rain_forecast >= 70:
        return {
            "status": "Delay Irrigation",
            "priority": "Low",
            "action": "Do not irrigate now",
            "irrigation_need": irrigation_need,
            "reason": "High rainfall probability is expected.",
            "soil_moisture": round(soil_moisture, 2),
            "rain_forecast": round(rain_forecast, 2)
        }

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

    if irrigation_need == "High":
        reasons = ["AI model detected high irrigation requirement."]
        if soil_moisture < 25:
            reasons.append("Soil moisture is critically low.")
        if temperature is not None and temperature >= 32:
            reasons.append("Temperature is high.")
        if humidity is not None and humidity < 50:
            reasons.append("Humidity is relatively low.")
        return {
            "status": "Irrigation Required",
            "priority": "High",
            "action": "Irrigate now",
            "irrigation_need": "High",
            "reason": " ".join(reasons),
            "soil_moisture": round(soil_moisture, 2),
            "rain_forecast": round(rain_forecast, 2)
        }

    if irrigation_need == "Medium":
        reasons = ["AI model detected moderate irrigation requirement."]
        if soil_moisture < 30:
            reasons.append("Soil moisture is below the preferred level.")
        if rain_forecast < 20:
            reasons.append("Significant rainfall is not expected.")
        return {
            "status": "Irrigation Recommended",
            "priority": "Medium",
            "action": "Plan irrigation soon",
            "irrigation_need": "Medium",
            "reason": " ".join(reasons),
            "soil_moisture": round(soil_moisture, 2),
            "rain_forecast": round(rain_forecast, 2)
        }

    return {
        "status": "No Immediate Irrigation",
        "priority": "Low",
        "action": "Wait and monitor",
        "irrigation_need": "Low",
        "reason": "AI model detected low irrigation requirement.",
        "soil_moisture": round(soil_moisture, 2),
        "rain_forecast": round(rain_forecast, 2)
    }
