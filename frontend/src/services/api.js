const API_BASE_URL = "http://127.0.0.1:8000";

async function request(endpoint, options = {}) {
  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    headers: {
      "Content-Type": "application/json",
      ...(options.headers || {}),
    },
    ...options,
  });

  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.detail || "API request failed");
  }

  return data;
}

// ===============================
// FARMS
// ===============================

export const getFarms = () => {
  return request("/farms/");
};

export const getFarm = (farmId) => {
  return request(`/farms/${farmId}`);
};


// ===============================
// CROPS
// ===============================

export const getCrops = () => {
  return request("/crops/");
};

export const getCrop = (cropId) => {
  return request(`/crops/${cropId}`);
};


// ===============================
// CROP CASES
// ===============================

export const createCropCase = (data) => {
  return request("/crop-cases/", {
    method: "POST",
    body: JSON.stringify(data),
  });
};

export const getCropCases = () => {
  return request("/crop-cases/");
};

export const getCropCase = (caseId) => {
  return request(`/crop-cases/${caseId}`);
};


// ===============================
// AI ANALYSIS
// ===============================

export const analyzeCrop = (caseId) => {
  return request(`/analysis/${caseId}`, {
    method: "POST",
  });
};


// ===============================
// FINAL DECISION
// ===============================

export const getFinalDecision = (caseId) => {
  return request(`/decision/${caseId}`);
};


// ===============================
// RECOMMENDATION
// ===============================

export const getRecommendation = (caseId) => {
  return request(`/recommendations/${caseId}`);
};


// ===============================
// SCENARIOS
// ===============================

export const getScenarios = (caseId) => {
  return request(`/scenarios/${caseId}`);
};


// ===============================
// WEATHER
// ===============================

export const getWeather = (farmId) => {
  return request(`/weather/${farmId}`);
};


// ===============================
// MARKET
// ===============================

export const getMarketPrice = (cropName) => {
  return request(`/market/${encodeURIComponent(cropName)}`);
};