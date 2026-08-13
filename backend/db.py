import os
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = Path(os.getenv("DATABASE_PATH", BASE_DIR / "aquasmart.db"))

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    db = get_db()
    db.executescript("""
    CREATE TABLE IF NOT EXISTS fields (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        field_name TEXT NOT NULL,
        area_hectare REAL DEFAULT 1,
        crop_type TEXT NOT NULL,
        crop_growth_stage TEXT DEFAULT 'Vegetative',
        sowing_date TEXT,
        soil_type TEXT NOT NULL,
        soil_ph REAL DEFAULT 6.5,
        irrigation_type TEXT DEFAULT 'Drip',
        water_source TEXT DEFAULT 'Groundwater',
        region TEXT DEFAULT 'Central',
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS sensor_readings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        field_id INTEGER NOT NULL,
        soil_moisture REAL NOT NULL,
        soil_ph REAL,
        organic_carbon REAL,
        electrical_conductivity REAL,
        temperature REAL,
        humidity REAL,
        rainfall_mm REAL,
        sunlight_hours REAL,
        wind_speed_kmh REAL,
        previous_irrigation_mm REAL,
        recorded_at TEXT NOT NULL,
        FOREIGN KEY(field_id) REFERENCES fields(id) ON DELETE CASCADE
    );

    CREATE TABLE IF NOT EXISTS recommendations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        field_id INTEGER NOT NULL,
        irrigation_need TEXT NOT NULL,
        priority TEXT NOT NULL,
        action TEXT NOT NULL,
        reason TEXT,
        water_liters REAL DEFAULT 0,
        created_at TEXT NOT NULL,
        FOREIGN KEY(field_id) REFERENCES fields(id) ON DELETE CASCADE
    );

    CREATE TABLE IF NOT EXISTS water_usage (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        field_id INTEGER NOT NULL,
        water_liters REAL NOT NULL,
        irrigation_method TEXT,
        recorded_at TEXT NOT NULL,
        FOREIGN KEY(field_id) REFERENCES fields(id) ON DELETE CASCADE
    );
    """)
    db.commit()
    db.close()
