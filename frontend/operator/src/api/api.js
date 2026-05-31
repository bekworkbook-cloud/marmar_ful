import axios from 'axios'

const BASE_URL = import.meta.env.VITE_API_URL || (window.location.origin + '/api/v1')

const http = axios.create({ baseURL: BASE_URL })

http.interceptors.request.use(cfg => {
  const token = localStorage.getItem('access_token')
  if (token) cfg.headers.Authorization = `Bearer ${token}`
  return cfg
})

http.interceptors.response.use(
  res => res,
  err => {
    if (err.response?.status === 401) localStorage.removeItem('access_token')
    return Promise.reject(err)
  }
)

export const authApi = {
  initTelegram: (initData) =>
    http.post('/auth/init_data/operator_bot', {}, {
      headers: { 'x-telegram-init-data': initData },
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
    http.patch(`/orders/${id}/status/`, { status }),
  assignCourier: (id, courierId) =>
    http.patch(
      `/orders/${id}/courier`, 
      null, // Тело запроса пустое
      { params: { courier_id: courierId } }
    ),
  acceptOrder: (id) =>
    http.patch(`/orders/${id}/accept/`),
  messages: (id) => http.get(`/orders/${id}/messages`),
  sendMessage: (id, text) =>
    http.post(`/orders/${id}/messages`, { text }),
}

export const userApi = {
  couriers: (branchId) =>
    http.get('/users/', { params: { role: 'courier', branch_id: branchId, limit: 100 } }),
}
