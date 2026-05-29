// /static/js/api.js

const API_BASE = "/api/v1";

export async function apiFetch(endpoint, options = {}) {
    const token = localStorage.getItem("jwt");

    const response = await fetch(`${API_BASE}${endpoint}`, {
        ...options,
        headers: {
            "Content-Type": "application/json",
            ...(options.headers || {}),
            Authorization: `Bearer ${token}`
        }
    });

    if (response.status === 401) {
        localStorage.removeItem("jwt");
        window.location.href = "/webapp/loader.html";
        return;
    }

    return response;
}