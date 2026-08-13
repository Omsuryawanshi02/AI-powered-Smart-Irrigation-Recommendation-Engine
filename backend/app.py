import os
from datetime import datetime, timezone
from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv

from db import init_db, get_db
from model_service import predict_irrigation_need, model_status
from recommendation import generate_recommendation
from weather_service import get_weather

load_dotenv()

app = Flask(__name__)
CORS(app)

init_db()


def error(message, status=400):
    return jsonify({"success": False, "error": message}), status


def as_float(data, key, default=None):
    value = data.get(key, default)
    if value is None or value == "":
        return default
    try:
        return float(value)
    except (TypeError, ValueError):
        raise ValueError(f"{key} must be numeric")


@app.get("/api/health")
def health():
    return jsonify({
        "success": True,
        "service": "AquaSmart Smart Irrigation Backend",
        "status": "running",
        "model": model_status(),
        "timestamp": datetime.now(timezone.utc).isoformat()
    })


@app.get("/api/model/status")
def model_info():
    return jsonify({"success": True, **model_status()})


@app.get("/api/fields")
def list_fields():
    db = get_db()
    rows = db.execute("SELECT * FROM fields ORDER BY id DESC").fetchall()
    return jsonify({"success": True, "fields": [dict(r) for r in rows]})


@app.post("/api/fields")
def create_field():
    data = request.get_json(silent=True) or {}
    required = ["field_name", "crop_type", "soil_type"]
    missing = [x for x in required if not data.get(x)]
    if missing:
        return error(f"Missing fields: {', '.join(missing)}")

    db = get_db()
    cur = db.execute("""
        INSERT INTO fields
        (field_name, area_hectare, crop_type, crop_growth_stage, sowing_date,
         soil_type, soil_ph, irrigation_type, water_source, region)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        data["field_name"],
        as_float(data, "area_hectare", 0),
        data["crop_type"],
        data.get("crop_growth_stage", "Vegetative"),
        data.get("sowing_date"),
        data["soil_type"],
        as_float(data, "soil_ph", 6.5),
        data.get("irrigation_type", "Drip"),
        data.get("water_source", "Groundwater"),
        data.get("region", "Central")
    ))
    db.commit()
    row = db.execute("SELECT * FROM fields WHERE id = ?", (cur.lastrowid,)).fetchone()
    return jsonify({"success": True, "field": dict(row)}), 201


@app.get("/api/fields/<int:field_id>")
def get_field(field_id):
    db = get_db()
    row = db.execute("SELECT * FROM fields WHERE id = ?", (field_id,)).fetchone()
    if not row:
        return error("Field not found", 404)
    return jsonify({"success": True, "field": dict(row)})


@app.post("/api/fields/<int:field_id>/sensor-readings")
def add_sensor_reading(field_id):
    data = request.get_json(silent=True) or {}
    db = get_db()
    field = db.execute("SELECT * FROM fields WHERE id = ?", (field_id,)).fetchone()
    if not field:
        return error("Field not found", 404)

    try:
        reading = {
            "soil_moisture": as_float(data, "soil_moisture"),
            "soil_ph": as_float(data, "soil_ph", field["soil_ph"] or 6.5),
            "organic_carbon": as_float(data, "organic_carbon", 1.0),
            "electrical_conductivity": as_float(data, "electrical_conductivity", 1.0),
            "temperature": as_float(data, "temperature", 25),
            "humidity": as_float(data, "humidity", 60),
            "rainfall_mm": as_float(data, "rainfall_mm", 0),
            "sunlight_hours": as_float(data, "sunlight_hours", 7),
            "wind_speed_kmh": as_float(data, "wind_speed_kmh", 5),
            "previous_irrigation_mm": as_float(data, "previous_irrigation_mm", 0)
        }
        if reading["soil_moisture"] is None:
            raise ValueError("soil_moisture is required")
        if not 0 <= reading["soil_moisture"] <= 100:
            raise ValueError("soil_moisture must be between 0 and 100")
    except ValueError as exc:
        return error(str(exc))

    cur = db.execute("""
        INSERT INTO sensor_readings
        (field_id, soil_moisture, soil_ph, organic_carbon, electrical_conductivity,
         temperature, humidity, rainfall_mm, sunlight_hours, wind_speed_kmh,
         previous_irrigation_mm, recorded_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        field_id, reading["soil_moisture"], reading["soil_ph"],
        reading["organic_carbon"], reading["electrical_conductivity"],
        reading["temperature"], reading["humidity"], reading["rainfall_mm"],
        reading["sunlight_hours"], reading["wind_speed_kmh"],
        reading["previous_irrigation_mm"],
        datetime.now(timezone.utc).isoformat()
    ))
    db.commit()

    return jsonify({
        "success": True,
        "reading_id": cur.lastrowid,
        "reading": reading
    }), 201


@app.get("/api/fields/<int:field_id>/readings/latest")
def latest_reading(field_id):
    db = get_db()
    row = db.execute("""
        SELECT * FROM sensor_readings
        WHERE field_id = ? ORDER BY id DESC LIMIT 1
    """, (field_id,)).fetchone()
    if not row:
        return error("No sensor reading found for this field", 404)
    return jsonify({"success": True, "reading": dict(row)})


@app.post("/api/irrigation/recommend")
def recommend():
    data = request.get_json(silent=True) or {}

    # Accept either field_id + latest sensor reading, or a complete payload.
    field = None
    db = get_db()
    if data.get("field_id"):
        field = db.execute(
            "SELECT * FROM fields WHERE id = ?", (int(data["field_id"]),)
        ).fetchone()
        if not field:
            return error("Field not found", 404)

    try:
        soil_moisture = as_float(data, "soil_moisture")
        if soil_moisture is None and field:
            latest = db.execute("""
                SELECT * FROM sensor_readings
                WHERE field_id = ? ORDER BY id DESC LIMIT 1
            """, (field["id"],)).fetchone()
            if latest:
                data = {**dict(latest), **data}
                soil_moisture = as_float(data, "soil_moisture")

        if soil_moisture is None:
            raise ValueError("soil_moisture is required")

        features = {
            "Soil_Type": data.get("soil_type", field["soil_type"] if field else "Loam"),
            "Soil_pH": as_float(data, "soil_ph", field["soil_ph"] if field else 6.5),
            "Soil_Moisture": soil_moisture,
            "Organic_Carbon": as_float(data, "organic_carbon", 1.0),
            "Electrical_Conductivity": as_float(data, "electrical_conductivity", 1.0),
            "Temperature_C": as_float(data, "temperature", 25),
            "Humidity": as_float(data, "humidity", 60),
            "Rainfall_mm": as_float(data, "rainfall_mm", 0),
            "Sunlight_Hours": as_float(data, "sunlight_hours", 7),
            "Wind_Speed_kmh": as_float(data, "wind_speed_kmh", 5),
            "Crop_Type": data.get("crop_type", field["crop_type"] if field else "Wheat"),
            "Crop_Growth_Stage": data.get("crop_growth_stage", field["crop_growth_stage"] if field else "Vegetative"),
            "Season": data.get("season", "Kharif"),
            "Irrigation_Type": data.get("irrigation_type", field["irrigation_type"] if field else "Drip"),
            "Water_Source": data.get("water_source", field["water_source"] if field else "Groundwater"),
            "Field_Area_hectare": as_float(data, "field_area_hectare", field["area_hectare"] if field else 1.0),
            "Mulching_Used": data.get("mulching_used", "Yes"),
            "Previous_Irrigation_mm": as_float(data, "previous_irrigation_mm", 0),
            "Region": data.get("region", field["region"] if field else "Central")
        }

        rain_forecast = as_float(data, "rain_forecast", 0)
        prediction = predict_irrigation_need(features)

        result = generate_recommendation(
            irrigation_need=prediction["label"],
            soil_moisture=soil_moisture,
            rain_forecast=rain_forecast,
            temperature=features["Temperature_C"],
            humidity=features["Humidity"],
            rainfall=features["Rainfall_mm"]
        )

        result.update({
            "model": prediction["model"],
            "confidence": prediction.get("confidence"),
            "crop_type": features["Crop_Type"],
            "crop_growth_stage": features["Crop_Growth_Stage"],
            "recommended_water_liters": calculate_water_liters(
                result["irrigation_need"], features["Field_Area_hectare"]
            )
        })

        if field:
            db.execute("""
                INSERT INTO recommendations
                (field_id, irrigation_need, priority, action, reason,
                 water_liters, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                field["id"], result["irrigation_need"], result["priority"],
                result["action"], result["reason"],
                result["recommended_water_liters"],
                datetime.now(timezone.utc).isoformat()
            ))
            db.commit()

        return jsonify({"success": True, "recommendation": result})

    except (ValueError, TypeError) as exc:
        return error(str(exc))
    except Exception as exc:
        app.logger.exception("Recommendation failed")
        return error(f"Recommendation failed: {exc}", 500)


def calculate_water_liters(need, area_hectare):
    # Prototype planning estimate; replace with crop-specific ETc/water-depth
    # calculations when field calibration data is available.
    rates = {"Low": 0, "Medium": 25000, "High": 50000}
    return round(rates.get(str(need).title(), 0) * float(area_hectare), 2)


@app.get("/api/fields/<int:field_id>/recommendations")
def recommendation_history(field_id):
    db = get_db()
    rows = db.execute("""
        SELECT * FROM recommendations
        WHERE field_id = ? ORDER BY id DESC LIMIT 50
    """, (field_id,)).fetchall()
    return jsonify({"success": True, "recommendations": [dict(r) for r in rows]})


@app.post("/api/weather")
def weather():
    data = request.get_json(silent=True) or {}
    city = data.get("city")
    lat = data.get("lat")
    lon = data.get("lon")
    if not city and (lat is None or lon is None):
        return error("Provide city or lat/lon")

    try:
        result = get_weather(city=city, lat=lat, lon=lon)
        return jsonify({"success": True, "weather": result})
    except Exception as exc:
        return error(str(exc), 502)


@app.get("/api/dashboard/<int:field_id>")
def dashboard(field_id):
    db = get_db()
    field = db.execute("SELECT * FROM fields WHERE id = ?", (field_id,)).fetchone()
    if not field:
        return error("Field not found", 404)

    reading = db.execute("""
        SELECT * FROM sensor_readings
        WHERE field_id = ? ORDER BY id DESC LIMIT 1
    """, (field_id,)).fetchone()

    recommendations = db.execute("""
        SELECT * FROM recommendations
        WHERE field_id = ? ORDER BY id DESC LIMIT 10
    """, (field_id,)).fetchall()

    usage = db.execute("""
        SELECT COALESCE(SUM(water_liters), 0) AS total_water
        FROM water_usage WHERE field_id = ?
    """, (field_id,)).fetchone()

    return jsonify({
        "success": True,
        "field": dict(field),
        "latest_reading": dict(reading) if reading else None,
        "recent_recommendations": [dict(x) for x in recommendations],
        "water_usage_liters": usage["total_water"]
    })


@app.post("/api/water-usage")
def water_usage():
    data = request.get_json(silent=True) or {}
    if not data.get("field_id"):
        return error("field_id is required")
    try:
        liters = as_float(data, "water_liters")
        if liters is None or liters < 0:
            raise ValueError("water_liters must be >= 0")
    except ValueError as exc:
        return error(str(exc))

    db = get_db()
    field = db.execute("SELECT id FROM fields WHERE id = ?", (int(data["field_id"]),)).fetchone()
    if not field:
        return error("Field not found", 404)

    cur = db.execute("""
        INSERT INTO water_usage (field_id, water_liters, irrigation_method, recorded_at)
        VALUES (?, ?, ?, ?)
    """, (
        int(data["field_id"]), liters, data.get("irrigation_method", "Drip"),
        datetime.now(timezone.utc).isoformat()
    ))
    db.commit()
    return jsonify({"success": True, "usage_id": cur.lastrowid}), 201


if __name__ == "__main__":
    port = int(os.getenv("PORT", "5000"))
    app.run(host="0.0.0.0", port=port, debug=os.getenv("FLASK_DEBUG", "1") == "1")
