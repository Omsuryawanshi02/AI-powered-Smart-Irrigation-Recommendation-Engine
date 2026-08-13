from app import app

def test_health():
    client = app.test_client()
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json["success"] is True

def test_high_irrigation_case():
    client = app.test_client()
    response = client.post("/api/irrigation/recommend", json={
        "soil_moisture": 12,
        "temperature": 36,
        "humidity": 42,
        "rainfall_mm": 0,
        "rain_forecast": 5,
        "crop_type": "Wheat",
        "crop_growth_stage": "Vegetative",
        "soil_type": "Clay"
    })
    assert response.status_code == 200
    result = response.json["recommendation"]
    assert result["irrigation_need"] in ["High", "Medium", "Low"]
