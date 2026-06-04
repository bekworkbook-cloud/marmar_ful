import { create } from 'zustand'
import { persist } from 'zustand/middleware'
import {
  authApi,
  ordersApi,
  branchesApi,
  categoriesApi,
  productsApi,
  staffApi,
} from '../api/api'

const useAdminStore = create(
  persist(
    (set, get) => ({

      // ── state ──────────────────────────────────────────────────────────────

      token: null,
      loading: false,
      error: null,

      selectedBranchId: null,

      orders:     [],
      branches:   [],
      categories: [],
      products:   [],
      staff:      [],

      // ── helpers ────────────────────────────────────────────────────────────

      _req: async (fn) => {
        set({ loading: true, error: null })
        try {
          const result = await fn()
          set({ loading: false })
          return result
        } catch (err) {
          set({ error: err.message, loading: false })
          throw err
        }
      },

      // ── auth ───────────────────────────────────────────────────────────────

      login: async (username, password) => {
        const data = await get()._req(() => authApi.login(username, password))
        set({ token: data.access_token })
      },

      logout: () => set({
        token: null,
        orders: [], branches: [], categories: [], products: [], staff: [],
        selectedBranchId: null,
        error: null,
      }),

      // ── branch filter ──────────────────────────────────────────────────────

      setSelectedBranch: (branchId) => set({ selectedBranchId: branchId }),

      // ── orders ─────────────────────────────────────────────────────────────

      fetchOrders: (params) =>
        get()._req(async () => {
          const data = await ordersApi.getAll(get().token, params)
          set({ orders: data.orders })
        }),

      fetchOrderById: (orderId) =>
        ordersApi.getById(get().token, orderId),

      fetchOrderItems: (orderId, params) =>
        ordersApi.getItems(get().token, orderId, params),

      updateOrderStatus: async (orderId, status) => {
        const updated = await ordersApi.updateStatus(get().token, orderId, status)
        set(s => ({ orders: s.orders.map(o => o.id === orderId ? updated : o) }))
        return updated
      },

      assignCourier: async (orderId, courierId) => {
        const updated = await ordersApi.assignCourier(get().token, orderId, courierId)
        set(s => ({ orders: s.orders.map(o => o.id === orderId ? updated : o) }))
        return updated
      },

      assignOperator: async (orderId, operatorId) => {
        const updated = await ordersApi.assignOperator(get().token, orderId, operatorId)
        set(s => ({ orders: s.orders.map(o => o.id === orderId ? updated : o) }))
        return updated
      },

      acceptOrder: async (orderId, isAccepted) => {
        const updated = await ordersApi.accept(get().token, orderId, isAccepted)
        set(s => ({ orders: s.orders.map(o => o.id === orderId ? updated : o) }))
        return updated
      },

      // ── branches ───────────────────────────────────────────────────────────

      fetchBranches: () =>
        get()._req(async () => {
          const data = await branchesApi.getAll(get().token)
          set({ branches: data.branches })
        }),

      createBranch: async (dto) => {
        const created = await branchesApi.create(get().token, dto)
        set(s => ({ branches: [...s.branches, created] }))
        return created
      },

      updateBranch: async (branchId, dto) => {
        const updated = await branchesApi.update(get().token, branchId, dto)
        set(s => ({ branches: s.branches.map(b => b.id === branchId ? updated : b) }))
        return updated
      },

      deleteBranch: async (branchId) => {
        await branchesApi.delete(get().token, branchId)
        set(s => ({ branches: s.branches.filter(b => b.id !== branchId) }))
      },

      // ── categories ─────────────────────────────────────────────────────────

      fetchCategories: (params) =>
        get()._req(async () => {
          const data = await categoriesApi.getAll(get().token, params)
          set({ categories: data.categories })
        }),

      createCategory: async (dto) => {
        const created = await categoriesApi.create(get().token, dto)
        set(s => ({ categories: [...s.categories, created] }))
        return created
      },

      updateCategory: async (categoryId, dto) => {
        const updated = await categoriesApi.update(get().token, categoryId, dto)
        set(s => ({ categories: s.categories.map(c => c.id === categoryId ? updated : c) }))
        return updated
      },

      deleteCategory: async (categoryId) => {
        await categoriesApi.delete(get().token, categoryId)
        set(s => ({ categories: s.categories.filter(c => c.id !== categoryId) }))
      },

      // ── products ───────────────────────────────────────────────────────────

      fetchProducts: (params) =>
        get()._req(async () => {
          const data = await productsApi.getAll(get().token, params)
          set({ products: data.products })
        }),

      createProduct: async (dto) => {
        const created = await productsApi.create(get().token, dto)
        set(s => ({ products: [...s.products, created] }))
        return created
      },

      updateProduct: async (productId, dto) => {
        const updated = await productsApi.update(get().token, productId, dto)
        set(s => ({ products: s.products.map(p => p.id === productId ? updated : p) }))
        return updated
      },

      deleteProduct: async (productId) => {
        await productsApi.delete(get().token, productId)
        set(s => ({ products: s.products.filter(p => p.id !== productId) }))
      },

      uploadProductImage: async (productId, file) => {
        const updated = await productsApi.uploadImage(get().token, productId, file)
        set(s => ({ products: s.products.map(p => p.id === productId ? updated : p) }))
        return updated
      },

      // ── staff ──────────────────────────────────────────────────────────────

      fetchStaff: (params) =>
        get()._req(async () => {
          const data = await staffApi.getAll(get().token, params)
          set({ staff: Array.isArray(data) ? data : [] })
        }),

      createStaff: async (dto) => {
        await staffApi.create(get().token, dto)
        await get().fetchStaff()
      },

      updateStaff: async (userId, dto) => {
        await staffApi.update(get().token, userId, dto)
        await get().fetchStaff()
      },

      deleteStaff: async (userId) => {
        await staffApi.delete(get().token, userId)
        set(s => ({ staff: s.staff.filter(u => u.id !== userId) }))
      },

      // ── selectors ──────────────────────────────────────────────────────────

      isAuthenticated: () => Boolean(get().token),

      filteredOrders: () => {
        const { orders, selectedBranchId } = get()
        return selectedBranchId
          ? orders.filter(o => o.branch_id === selectedBranchId)
          : orders
      },

      totalRevenue: () =>
        get().filteredOrders().reduce((sum, o) => sum + o.total_price, 0),

      avgOrderValue: () => {
        const orders = get().filteredOrders()
        return orders.length ? get().totalRevenue() / orders.length : 0
      },

      ordersByStatus: () =>
        get().filteredOrders().reduce((acc, o) => {
          const key = o.status ?? 'unknown'
          if (!acc[key]) acc[key] = []
          acc[key].push(o)
          return acc
        }, {}),

      staffByRole: (role) => {
        const { staff } = get()
        return role ? staff.filter(u => u.role === role) : staff
      },
    }),
    {
      name: 'marmar-admin',
      partialize: (s) => ({
        token: s.token,
        selectedBranchId: s.selectedBranchId,
      }),
    }
  )
)

export default useAdminStore