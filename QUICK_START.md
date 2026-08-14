# AquaSmart Backend & Frontend Integration - Summary

## What Was Done

I've successfully connected your AquaSmart backend and frontend. Here's what was implemented:

### 1. **API Client Library** (`frontend/api.js`)
   - A complete JavaScript wrapper for all backend API endpoints
   - Handles all HTTP requests, error handling, and response parsing
   - Functions for Users, Fields, Sensors, Weather, Recommendations, Alerts, and Analytics
   - Configurable API base URL (stored in browser localStorage)

### 2. **Frontend Updates**
   - **home_dashboard.html**: Added API integration to load real data from backend
   - **add_field.html**: Added form submission to create fields in backend
   - **test-api.html**: New testing page to verify API connectivity

### 3. **Startup Scripts**
   - **START.bat**: Batch script for Windows (double-click to run)
   - **START.ps1**: PowerShell script for Windows (more advanced)
   - Both scripts start backend and frontend servers automatically

### 4. **Documentation**
   - **INTEGRATION_GUIDE.md**: Comprehensive integration guide with API reference
   - **This file**: Overview and quick start instructions

## Quick Start (5 Minutes)

### Option 1: Use Startup Script (Easiest)
1. Double-click `START.bat` in the project root folder
2. Wait for both backend and frontend servers to start
3. Open browser to `http://localhost:8080`

### Option 2: Manual Setup
1. Open Terminal/Command Prompt
2. Install dependencies: `cd backend && pip install -r requirements.txt`
3. Start backend: `python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000`
4. In another terminal, start frontend: `cd frontend && python -m http.server 8080`
5. Open browser to `http://localhost:8080`

## Testing Your Connection

### Test Page
Open `frontend/test-api.html` to:
- Check backend health
- Test all API endpoints
- Configure API URL
- View stored settings

### In Browser Console
```javascript
// Check health
await api.checkHealth()

// List fields
await api.listFields()

// Get a recommendation
await api.getRecommendation(1)
```

## API Configuration

### Default Configuration
- Backend: `http://localhost:8000`
- Frontend: `http://localhost:8080`

### Change API URL (if backend is on different server)
1. Open browser DevTools (F12)
2. Go to Console tab
3. Run: `localStorage.setItem('apiBaseUrl', 'http://your-server:8000')`
4. Reload page

## Features Implemented

### 1. Dashboard Data Loading
- Fetches weather data from backend
- Loads irrigation recommendations
- Displays sensor readings
- Shows alerts and notifications

### 2. Field Management
- Create new fields via form
- Save field data to backend
- Auto-redirect after creation
- Store field ID in browser

### 3. API Integration
All endpoints are now accessible:
- Users: Create, Get, Update
- Fields: Create, List, Get, Update, Delete
- Sensors: Record readings, Get readings, Get latest
- Weather: Current conditions, Forecast
- Recommendations: Get recommendations, Get schedule
- Alerts: Get alerts, Acknowledge
- Analytics: Water usage, Crop analytics

## Files Modified/Created

### Created Files
```
frontend/
├── api.js                 # API client library ✨ NEW
├── test-api.html          # API testing page ✨ NEW
├── START.bat              # Windows batch startup ✨ NEW
├── START.ps1              # PowerShell startup ✨ NEW
└── INTEGRATION_GUIDE.md   # Detailed integration guide ✨ NEW
```

### Modified Files
```
frontend/
├── home_dashboard.html    # Added API integration
└── add_field.html         # Added form submission
```

## How It Works

### Architecture
```
┌─────────────────────┐
│   Frontend (HTML)   │
│   home_dashboard    │
│   add_field         │
│   weather_forecast  │
│   etc...            │
└──────────┬──────────┘
           │
           │ HTTP Requests
           │ (api.js)
           │
           ▼
┌──────────────────────────┐
│   Backend (FastAPI)      │
│   Port: 8000             │
│   SQLite Database        │
│   ML Model Integration   │
└──────────────────────────┘
```

### Data Flow Example
1. User clicks "Save Field" on add_field.html
2. JavaScript calls `api.createField(formData)`
3. api.js makes POST request to `/api/fields`
4. Backend validates and saves field to database
5. Response returned and success message shown
6. User redirected to dashboard

## Troubleshooting

### Backend Not Starting
- Verify Python 3.8+ is installed: `python --version`
- Install dependencies: `pip install -r backend/requirements.txt`
- Check port 8000 is not in use: `netstat -ano | findstr :8000` (Windows)

### Frontend Can't Connect to Backend
- Verify backend is running on http://localhost:8000
- Check browser console (F12) for CORS errors
- Set correct API URL in localStorage
- Restart browser

### Port Already In Use
- Backend on different port: `python -m uvicorn app.main:app --port 8001`
- Then set API URL: `localStorage.setItem('apiBaseUrl', 'http://localhost:8001')`

## Next Steps

1. **Test the Connection**
   - Open `frontend/test-api.html`
   - Click "Check Health" to verify backend

2. **Try Creating a Field**
   - Go to `frontend/add_field.html`
   - Fill in field details
   - Click "Save Field"

3. **View Dashboard**
   - Open `frontend/home_dashboard.html`
   - See live data from backend

4. **Explore Other Pages**
   - Alerts: `frontend/alerts.html`
   - Analytics: `frontend/water_analytics.html`
   - Weather: `frontend/weather_forecast.html`
   - Schedule: `frontend/irrigation_schedule.html`

## API Reference

### Quick API Call Examples

```javascript
// Create a field
const field = await api.createField({
  user_id: 1,
  name: "North Field",
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

// Get recommendation
const rec = await api.getRecommendation(field.id);

// Get weather
const weather = await api.getWeatherForecast(28.7041, 77.1025);

// Record sensor reading
await api.recordSensorReading(field.id, {
  soil_moisture: 45.2,
  temperature: 28,
  field_id: field.id,
  recorded_at: new Date().toISOString()
});
```

See INTEGRATION_GUIDE.md for complete API reference.

## Support

For issues or questions:
1. Check browser console (F12) for error messages
2. Review INTEGRATION_GUIDE.md for detailed documentation
3. Check backend logs for server-side errors
4. Verify API connectivity using test-api.html

## Summary

✅ Backend and frontend are fully integrated
✅ All API endpoints are connected
✅ Form submission works end-to-end
✅ Dashboard loads live data
✅ Easy startup scripts provided
✅ Comprehensive documentation available

Your AquaSmart irrigation recommendation engine is ready to use!
