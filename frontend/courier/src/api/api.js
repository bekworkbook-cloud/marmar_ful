import axios from 'axios'

const BASE_URL = import.meta.env.VITE_API_URL || (window.location.origin + '/api/v1')
const http = axios.create(
  {
    baseURL: BASE_URL, 
    headers: {
      'ngrok-skip-browser-warning': 'true',
    } 
  }
)

http.interceptors.request.use(cfg => {
  // читаем из zustand persist — единый источник правды
  try {
    const state = JSON.parse(localStorage.getItem('marmar-courier') || '{}')
    const token = state?.state?.token
    if (token) cfg.headers.Authorization = `Bearer ${token}`
  } catch {}
  return cfg
})

http.interceptors.response.use(
  res => res,
  err => Promise.reject(err)
)

export const authApi = {
  initTelegram: (initData) =>
    http.post('/auth/init_data/courier_bot', {}, {
      headers: {
        'x-telegram-init-data': initData,
        'ngrok-skip-browser-warning': 'true',
      },
    }),
  login: (username, password) =>
    http.post('/auth/login', { username, password }),
  me: () => http.get('/auth/me'),
}

export const orderApi = {
  list: (params = {}) =>
    http.get('/orders/', { params: { limit: 50, ...params } }),
  get: (id) => http.get(`/orders/${id}`),
  items: (id) => http.get(`/orders/${id}/items`),
  updateStatus: (id, status) =>
    http.patch(`/orders/${id}/status`, { status }),
  messages: (id) => http.get(`/orders/${id}/messages`),
  sendMessage: (id, text) =>
    http.post(`/orders/${id}/messages`, { text }),
}