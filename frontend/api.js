/**
 * AquaSmart API Client
 * Provides functions to communicate with the Smart Irrigation Recommendation Engine backend
 */

// Configuration
const API_BASE_URL = localStorage.getItem('apiBaseUrl') || 'http://localhost:8000';

// Helper function to make API calls
async function apiCall(endpoint, options = {}) {
  const url = `${API_BASE_URL}${endpoint}`;
  const defaultOptions = {
    headers: {
      'Content-Type': 'application/json',
    },
  };

  const config = { ...defaultOptions, ...options };

  try {
    const response = await fetch(url, config);
    
    if (!response.ok) {
      throw new Error(`API Error: ${response.status} ${response.statusText}`);
    }

    // Handle empty responses
    if (response.status === 204) {
      return null;
    }

    return await response.json();
  } catch (error) {
    console.error(`Error calling ${endpoint}:`, error);
    throw error;
  }
}

// Set the API base URL (useful for dynamic configuration)
function setApiBaseUrl(url) {
  localStorage.setItem('apiBaseUrl', url);
}

// ============ USER ENDPOINTS ============

async function createUser(userData) {
  return apiCall('/api/users', {
    method: 'POST',
    body: JSON.stringify(userData),
  });
}

async function getUser(userId) {
  return apiCall(`/api/users/${userId}`);
}

async function updateUser(userId, userData) {
  return apiCall(`/api/users/${userId}`, {
    method: 'PUT',
    body: JSON.stringify(userData),
  });
}

// ============ FIELD ENDPOINTS ============

async function createField(fieldData) {
  return apiCall('/api/fields', {
    method: 'POST',
    body: JSON.stringify(fieldData),
  });
}

async function listFields(userId = null) {
  const endpoint = userId ? `/api/fields?user_id=${userId}` : '/api/fields';
  return apiCall(endpoint);
}

async function getField(fieldId) {
  return apiCall(`/api/fields/${fieldId}`);
}

async function updateField(fieldId, fieldData) {
  return apiCall(`/api/fields/${fieldId}`, {
    method: 'PUT',
    body: JSON.stringify(fieldData),
  });
}

async function deleteField(fieldId) {
  return apiCall(`/api/fields/${fieldId}`, {
    method: 'DELETE',
  });
}

// ============ SENSOR ENDPOINTS ============

async function recordSensorReading(fieldId, sensorData) {
  return apiCall('/api/sensors/readings', {
    method: 'POST',
    body: JSON.stringify(sensorData),
  });
}

async function getSensorReadings(fieldId, limit = 100) {
  return apiCall(`/api/sensors/readings?field_id=${fieldId}&limit=${limit}`);
}

async function getLatestReading(fieldId) {
  return apiCall(`/api/sensors/readings?field_id=${fieldId}&limit=1`);
}

// ============ WEATHER ENDPOINTS ============

async function getWeatherForecast(latitude, longitude) {
  return apiCall(`/api/weather/forecast?latitude=${latitude}&longitude=${longitude}`);
}

async function getWeatherCurrent(latitude, longitude) {
  return apiCall(`/api/weather/current?latitude=${latitude}&longitude=${longitude}`);
}

// ============ RECOMMENDATION ENDPOINTS ============

async function getRecommendation(fieldId, overrides = {}) {
  return apiCall(`/api/fields/${fieldId}/recommendation`, {
    method: 'POST',
    body: JSON.stringify(overrides),
  });
}

async function getIrrigationSchedule(fieldId) {
  return apiCall(`/api/fields/${fieldId}/irrigation-schedule`);
}

// ============ ALERTS ENDPOINTS ============

async function getAlerts(userId = null) {
  const endpoint = userId ? `/api/alerts?user_id=${userId}` : '/api/alerts';
  return apiCall(endpoint);
}

async function acknowledgeAlert(alertId) {
  return apiCall(`/api/alerts/${alertId}/acknowledge`, {
    method: 'POST',
  });
}

// ============ ANALYTICS ENDPOINTS ============

async function getWaterAnalytics(fieldId) {
  return apiCall(`/api/fields/${fieldId}/analytics/water`);
}

async function getCropAnalytics(fieldId) {
  return apiCall(`/api/fields/${fieldId}/analytics/crop`);
}

// ============ HEALTH CHECK ============

async function checkHealth() {
  return apiCall('/api/health');
}

// Export functions for use in HTML
if (typeof window !== 'undefined') {
  window.api = {
    setApiBaseUrl,
    checkHealth,
    // User
    createUser,
    getUser,
    updateUser,
    // Fields
    createField,
    listFields,
    getField,
    updateField,
    deleteField,
    // Sensors
    recordSensorReading,
    getSensorReadings,
    getLatestReading,
    // Weather
    getWeatherForecast,
    getWeatherCurrent,
    // Recommendations
    getRecommendation,
    getIrrigationSchedule,
    // Alerts
    getAlerts,
    acknowledgeAlert,
    // Analytics
    getWaterAnalytics,
    getCropAnalytics,
  };
}
