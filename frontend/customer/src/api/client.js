// src/api/client.js

const API_BASE = window.location.origin + "/api/v1";

export const apiClient = async (endpoint, options = {}) => {
  const token = localStorage.getItem("jwt");
  const headers = new Headers(options.headers || {});
  
  headers.append("Content-Type", "application/json");
  headers.append("ngrok-skip-browser-warning", "true"); // Защита от ngrok

  if (token) {
    const cleanToken = token.replace(/[^A-Za-z0-9\-\._~+\/]/g, "");
    headers.append("Authorization", `Bearer ${cleanToken}`);
  }

  const response = await fetch(`${API_BASE}${endpoint}`, {
    ...options,
    headers,
  });

  if (response.status === 401) {
    localStorage.removeItem("jwt");
    throw new Error("unauthorized");
  }

  if (!response.ok) {
    throw new Error(`HTTP ошибка: ${response.status}`);
  }

  return response.json();
};