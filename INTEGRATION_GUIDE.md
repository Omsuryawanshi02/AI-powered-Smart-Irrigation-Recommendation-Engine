# AquaSmart - Backend & Frontend Integration Guide

## Quick Start

The frontend and backend are now connected! Follow these steps to get everything running.

### Prerequisites
- Python 3.8+
- Node.js (optional, for frontend development server)
- Git

### 1. Install Backend Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Run the Backend Server

```bash
cd backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The backend will be available at: `http://localhost:8000`

### 3. Open the Frontend

Simply open any of these HTML files in your browser:
- `frontend/home_dashboard.html` - Main dashboard
- `frontend/add_field.html` - Add new field
- `frontend/alerts.html` - View alerts
- `frontend/water_analytics.html` - Water usage analytics
- `frontend/irrigation_schedule.html` - Irrigation schedule

Or serve the frontend with a simple HTTP server:

```bash
# Python 3.6+
cd frontend
python -m http.server 8080
```

Then open: `http://localhost:8080`

### 4. Configure API URL (if needed)

By default, the frontend expects the backend at `http://localhost:8000`.

To use a different API URL:
1. Open browser DevTools (F12)
2. Go to Console
3. Run: `localStorage.setItem('apiBaseUrl', 'http://your-api-url:port')`

Or add this to any HTML file before loading api.js:
```html
<script>
  localStorage.setItem('apiBaseUrl', 'http://your-custom-url:8000');
</script>
```

## API Features

The frontend now has full API integration through `api.js`:

### User Management
- `api.createUser(userData)` - Create new user
- `api.getUser(userId)` - Get user info
- `api.updateUser(userId, userData)` - Update user

### Fields
- `api.createField(fieldData)` - Create field
- `api.listFields(userId)` - List all fields
- `api.getField(fieldId)` - Get field details
- `api.updateField(fieldId, fieldData)` - Update field
- `api.deleteField(fieldId)` - Delete field

### Sensors
- `api.recordSensorReading(fieldId, sensorData)` - Log sensor reading
- `api.getSensorReadings(fieldId, limit)` - Get sensor readings
- `api.getLatestReading(fieldId)` - Get latest reading

### Weather
- `api.getWeatherForecast(latitude, longitude)` - Get weather forecast
- `api.getWeatherCurrent(latitude, longitude)` - Get current weather

### Recommendations
- `api.getRecommendation(fieldId, overrides)` - Get irrigation recommendation
- `api.getIrrigationSchedule(fieldId)` - Get irrigation schedule

### Alerts & Analytics
- `api.getAlerts(userId)` - Get alerts
- `api.acknowledgeAlert(alertId)` - Mark alert as seen
- `api.getWaterAnalytics(fieldId)` - Get water usage analytics
- `api.getCropAnalytics(fieldId)` - Get crop analytics

## Frontend Pages

### Home Dashboard (home_dashboard.html)
- Displays today's weather conditions
- Shows AI-generated irrigation recommendations
- Displays sensor health and water usage status
- Navigation menu to other pages

### Add Field (add_field.html)
- Create new irrigation fields
- Set field parameters (crop type, size, location, etc.)
- Automatically saves to backend

### Field Details (field_details.html)
- View detailed information about a specific field
- See soil conditions and sensor data

### Irrigation Schedule (irrigation_schedule.html)
- View recommended irrigation schedule
- See upcoming irrigation times

### Alerts (alerts.html)
- View all alerts and notifications
- Mark alerts as acknowledged

### Water Analytics (water_analytics.html)
- View water usage statistics
- Compare against baseline usage
- Track savings

### Weather Forecast (weather_forecast.html)
- Extended weather forecast
- See how weather impacts irrigation needs

### Profile Settings (profile_setting.html)
- User profile management
- Preferences and settings

## Troubleshooting

### "Failed to load dashboard data" error
1. Make sure the backend is running: `python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000`
2. Check that CORS is enabled in backend/app/config.py
3. Verify the API URL is correct: check browser console and check localStorage

### CORS errors
The backend is configured with `CORS_ORIGINS: "*"` by default in `backend/app/config.py`.
If you get CORS errors, check that the backend was restarted after changing config.

### Port already in use
If port 8000 is in use, run backend with different port:
```bash
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8001
```

Then set API URL:
```javascript
localStorage.setItem('apiBaseUrl', 'http://localhost:8001');
```

## Development Tips

### Testing API calls in browser console
```javascript
// Check backend health
await api.checkHealth();

// Create a field
await api.createField({
  user_id: 1,
  name: "Test Field",
  crop_type: "corn",
  field_size: 10,
  size_unit: "hectares",
  sowing_date: "2024-01-15",
  soil_type: "Loamy",
  region: "Central",
  season: "Kharif",
  irrigation_type: "Drip",
  water_source: "Groundwater",
  mulching_used: false,
  latitude: 28.7041,
  longitude: 77.1025
});

// Get all fields for user 1
await api.listFields(1);

// Get recommendation for field 1
await api.getRecommendation(1);
```

### Enabling debug logging
Open browser DevTools (F12) and check the Console tab for detailed API call logs.

## File Structure

```
frontend/
  ├── api.js                    # API client library
  ├── home_dashboard.html       # Main dashboard
  ├── add_field.html           # Add field form
  ├── field_details.html       # Field details
  ├── alerts.html              # Alerts page
  ├── irrigation_schedule.html # Schedule page
  ├── water_analytics.html     # Analytics page
  ├── weather_forecast.html    # Weather page
  ├── profile_setting.html     # Settings page
  └── onboarding.html          # Onboarding page

backend/
  ├── app/
  │   ├── main.py              # FastAPI app
  │   ├── config.py            # Configuration
  │   ├── models.py            # Database models
  │   ├── schemas.py           # Request/response schemas
  │   ├── routers/             # API endpoints
  │   │   ├── users.py
  │   │   ├── fields.py
  │   │   ├── sensors.py
  │   │   ├── weather.py
  │   │   ├── recommendations.py
  │   │   ├── alerts.py
  │   │   └── analytics.py
  │   └── ml/                  # Machine learning
  │       └── model_loader.py
  └── requirements.txt
```

## Next Steps

1. ✅ Backend and frontend are now connected
2. 📝 Create a test field using the Add Field form
3. 🌍 Check the dashboard for recommendations
4. 📊 View analytics and alerts
5. 🔄 Set up sensor data recording

Enjoy using AquaSmart!
