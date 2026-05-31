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
    http.post('/auth/init_data/customer_bot', {}, {
      headers: { 'x-telegram-init-data': initData },
    }),
  login: (username, password) =>
    http.post('/auth/login/', { username, password }),
  me: () => http.get('/auth/me'),
}

export const branchApi = {
  list: () => http.get('/branches/'),
}

export const categoryApi = {
  list: (branchId) =>
    http.get('/categories/', { params: { branch_id: branchId, limit: 100 } }),
}

export const productApi = {
  list: (categoryId) =>
    http.get('/products/', { params: { category_id: categoryId, limit: 100 } }),
  get: (id) => http.get(`/products/${id}`),
}

export const orderApi = {
  create: (data) => http.post('/orders/', data),
  list: () => http.get('/orders/', { params: { limit: 30 } }),
  get: (id) => http.get(`/orders/${id}/`),
  items: (id) => http.get(`/orders/${id}/items/`),
}
