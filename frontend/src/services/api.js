const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000";

async function request(path, options = {}) {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    headers: {
      "Content-Type": "application/json",
      ...(options.headers || {})
    },
    ...options
  });

  const data = await response.json().catch(() => ({}));
  if (!response.ok) {
    const message = data.message || "Falha ao comunicar com a API.";
    throw new Error(message);
  }
  return data;
}

export function checkHealth() {
  return request("/health");
}

export function createIncident(payload) {
  return request("/api/incidents", {
    method: "POST",
    body: JSON.stringify(payload)
  });
}

export function listIncidents(limit = 20) {
  return request(`/api/incidents?limit=${limit}`);
}

export function getRules() {
  return request("/api/rules");
}

export function getStats() {
  return request("/api/stats");
}

export function seedIncidents() {
  return request("/api/seed", {
    method: "POST",
    body: JSON.stringify({})
  });
}
