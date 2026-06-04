const API_BASE = '/api/v1'

const getHeaders = (token, isFormData = false) => {
  const headers = { Authorization: `Bearer ${token}` }
  if (!isFormData) headers['Content-Type'] = 'application/json'
  return headers
}

const handleResponse = async (res) => {
  if (res.status === 401) {
    window.dispatchEvent(new CustomEvent('unauthorized', { detail: { status: 401 } }))
    throw new Error('Unauthorized')
  }
  if (res.status === 204) return null
  const data = await res.json()
  if (!res.ok) {
    const message =
      data?.detail?.[0]?.msg ||
      data?.detail ||
      `HTTP error ${res.status}`
    throw new Error(message)
  }
  return data
}

const buildQuery = (params) =>
  new URLSearchParams(
    Object.fromEntries(Object.entries(params).filter(([, v]) => v != null))
  ).toString()

// ─── Auth ────────────────────────────────────────────────────────────────────

export const authApi = {
  /**
   * POST /api/v1/auth/login
   * Telegram Mini App: отправляем initData, получаем JWT токен
   * @param {string} initData — window.Telegram.WebApp.initData
   * @returns {Promise<TokenDTO>}
   */
  loginTelegram: async (initData) => {
    const res = await fetch(`${API_BASE}/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ init_data: initData }),
    })
    return handleResponse(res)
  },
}

// ─── Orders ──────────────────────────────────────────────────────────────────

export const ordersApi = {
  /** GET /api/v1/orders/ → OrdersDTO */
  getAll: async (token, params = { limit: 100, offset: 0 }) => {
    const res = await fetch(`${API_BASE}/orders/?${buildQuery(params)}`, {
      headers: getHeaders(token),
    })
    return handleResponse(res)
  },

  /** GET /api/v1/orders/{order_id} → OrderDTO */
  getById: async (token, orderId) => {
    const res = await fetch(`${API_BASE}/orders/${orderId}`, {
      headers: getHeaders(token),
    })
    return handleResponse(res)
  },

  /** GET /api/v1/orders/{order_id}/items → OrderItemsDTO */
  getItems: async (token, orderId, params = { limit: 20, offset: 0 }) => {
    const res = await fetch(`${API_BASE}/orders/${orderId}/items?${buildQuery(params)}`, {
      headers: getHeaders(token),
    })
    return handleResponse(res)
  },

  /** PATCH /api/v1/orders/{order_id}/status → OrderDTO */
  updateStatus: async (token, orderId, status) => {
    const res = await fetch(`${API_BASE}/orders/${orderId}/status`, {
      method: 'PATCH',
      headers: getHeaders(token),
      body: JSON.stringify({ status }),
    })
    return handleResponse(res)
  },

  /** PATCH /api/v1/orders/{order_id}/courier → OrderDTO */
  assignCourier: async (token, orderId, courierId) => {
    const res = await fetch(
      `${API_BASE}/orders/${orderId}/courier?order_personnel_dto=${courierId}`,
      { method: 'PATCH', headers: getHeaders(token) },
    )
    return handleResponse(res)
  },

  /** PATCH /api/v1/orders/{order_id}/operator → OrderDTO */
  assignOperator: async (token, orderId, operatorId) => {
    const res = await fetch(
      `${API_BASE}/orders/${orderId}/operator?operator_id=${operatorId}`,
      { method: 'PATCH', headers: getHeaders(token) },
    )
    return handleResponse(res)
  },

  /** PATCH /api/v1/orders/{order_id}/accept → OrderDTO */
  accept: async (token, orderId, isAccepted) => {
    const res = await fetch(`${API_BASE}/orders/${orderId}/accept`, {
      method: 'PATCH',
      headers: getHeaders(token),
      body: JSON.stringify({ is_accepted: isAccepted }),
    })
    return handleResponse(res)
  },
}

// ─── Branches ────────────────────────────────────────────────────────────────

export const branchesApi = {
  /** GET /api/v1/branches/ → BranchesDTO */
  getAll: async (token) => {
    const res = await fetch(`${API_BASE}/branches/`, { headers: getHeaders(token) })
    return handleResponse(res)
  },

  /** POST /api/v1/branches/ → BranchDTO */
  create: async (token, dto) => {
    const res = await fetch(`${API_BASE}/branches/`, {
      method: 'POST',
      headers: getHeaders(token),
      body: JSON.stringify(dto),
    })
    return handleResponse(res)
  },

  /** PUT /api/v1/branches/{branch_id} → BranchDTO */
  update: async (token, branchId, dto) => {
    const res = await fetch(`${API_BASE}/branches/${branchId}`, {
      method: 'PUT',
      headers: getHeaders(token),
      body: JSON.stringify(dto),
    })
    return handleResponse(res)
  },

  /** DELETE /api/v1/branches/{branch_id} → null */
  delete: async (token, branchId) => {
    const res = await fetch(`${API_BASE}/branches/${branchId}`, {
      method: 'DELETE',
      headers: getHeaders(token),
    })
    return handleResponse(res)
  },
}

// ─── Categories ──────────────────────────────────────────────────────────────

export const categoriesApi = {
  /** GET /api/v1/categories/ → CategoriesDTO */
  getAll: async (token, params = { limit: 100, offset: 0 }) => {
    const res = await fetch(`${API_BASE}/categories/?${buildQuery(params)}`, {
      headers: getHeaders(token),
    })
    return handleResponse(res)
  },

  /** POST /api/v1/categories/ → CategoryDTO */
  create: async (token, dto) => {
    const res = await fetch(`${API_BASE}/categories/`, {
      method: 'POST',
      headers: getHeaders(token),
      body: JSON.stringify(dto),
    })
    return handleResponse(res)
  },

  /** PUT /api/v1/categories/{category_id} → CategoryDTO */
  update: async (token, categoryId, dto) => {
    const res = await fetch(`${API_BASE}/categories/${categoryId}`, {
      method: 'PUT',
      headers: getHeaders(token),
      body: JSON.stringify(dto),
    })
    return handleResponse(res)
  },

  /** DELETE /api/v1/categories/{category_id} → null */
  delete: async (token, categoryId) => {
    const res = await fetch(`${API_BASE}/categories/${categoryId}`, {
      method: 'DELETE',
      headers: getHeaders(token),
    })
    return handleResponse(res)
  },
}

// ─── Products ────────────────────────────────────────────────────────────────

export const productsApi = {
  /** GET /api/v1/products/ → ProductsDTO */
  getAll: async (token, params = { limit: 50, offset: 0 }) => {
    const res = await fetch(`${API_BASE}/products/?${buildQuery(params)}`, {
      headers: getHeaders(token),
    })
    return handleResponse(res)
  },

  /** POST /api/v1/products/ → ProductDTO */
  create: async (token, dto) => {
    const res = await fetch(`${API_BASE}/products/`, {
      method: 'POST',
      headers: getHeaders(token),
      body: JSON.stringify(dto),
    })
    return handleResponse(res)
  },

  /** PUT /api/v1/products/{product_id} → ProductDTO */
  update: async (token, productId, dto) => {
    const res = await fetch(`${API_BASE}/products/${productId}`, {
      method: 'PUT',
      headers: getHeaders(token),
      body: JSON.stringify(dto),
    })
    return handleResponse(res)
  },

  /** DELETE /api/v1/products/{product_id} → null */
  delete: async (token, productId) => {
    const res = await fetch(`${API_BASE}/products/${productId}`, {
      method: 'DELETE',
      headers: getHeaders(token),
    })
    return handleResponse(res)
  },

  /** POST /api/v1/products/{product_id}/image (multipart) → ProductDTO */
  uploadImage: async (token, productId, file) => {
    const formData = new FormData()
    formData.append('file', file)
    const res = await fetch(`${API_BASE}/products/${productId}/image`, {
      method: 'POST',
      headers: getHeaders(token, true),
      body: formData,
    })
    return handleResponse(res)
  },
}

// ─── Staff ───────────────────────────────────────────────────────────────────

export const staffApi = {
  /** GET /api/v1/users/ → Array<UserDTO> */
  getAll: async (token, params = { limit: 50, offset: 0 }) => {
    const res = await fetch(`${API_BASE}/users/?${buildQuery(params)}`, {
      headers: getHeaders(token),
    })
    return handleResponse(res)
  },

  /** POST /api/v1/users/ → {} */
  create: async (token, dto) => {
    const res = await fetch(`${API_BASE}/users/`, {
      method: 'POST',
      headers: getHeaders(token),
      body: JSON.stringify(dto),
    })
    return handleResponse(res)
  },

  /** PUT /api/v1/users/{user_id} → {} */
  update: async (token, userId, dto) => {
    const res = await fetch(`${API_BASE}/users/${userId}`, {
      method: 'PUT',
      headers: getHeaders(token),
      body: JSON.stringify(dto),
    })
    return handleResponse(res)
  },

  /** DELETE /api/v1/users/{user_id} → null */
  delete: async (token, userId) => {
    const res = await fetch(`${API_BASE}/users/${userId}`, {
      method: 'DELETE',
      headers: getHeaders(token),
    })
    return handleResponse(res)
  },
}