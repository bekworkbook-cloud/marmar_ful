import { create } from 'zustand'
import { persist } from 'zustand/middleware'

const useStore = create(
  persist(
    (set, get) => ({
      user: null,
      token: localStorage.getItem('access_token') || null,
      selectedBranch: null,
      cart: [],

      setUser: (user) => set({ user }),

      setToken: (token) => {
        localStorage.setItem('access_token', token)
        set({ token })
      },

      clearAuth: () => {
        localStorage.removeItem('access_token')
        set({ user: null, token: null })
      },

      setSelectedBranch: (branch) => set({ selectedBranch: branch, cart: [] }),

      addToCart: (product) => {
        const { cart } = get()
        const existing = cart.find(i => i.product_id === product.id)
        if (existing) {
          set({
            cart: cart.map(i =>
              i.product_id === product.id ? { ...i, quantity: i.quantity + 1 } : i
            ),
          })
        } else {
          set({
            cart: [
              ...cart,
              { product_id: product.id, product, quantity: 1, price: Number(product.price) },
            ],
          })
        }
      },

      removeFromCart: (productId) =>
        set(s => ({ cart: s.cart.filter(i => i.product_id !== productId) })),

      changeQty: (productId, delta) => {
        const { cart } = get()
        const item = cart.find(i => i.product_id === productId)
        if (!item) return
        const newQty = item.quantity + delta
        if (newQty <= 0) {
          set({ cart: cart.filter(i => i.product_id !== productId) })
        } else {
          set({ cart: cart.map(i => i.product_id === productId ? { ...i, quantity: newQty } : i) })
        }
      },

      clearCart: () => set({ cart: [] }),

      cartTotal: () =>
        get().cart.reduce((sum, i) => sum + i.price * i.quantity, 0),

      cartCount: () =>
        get().cart.reduce((sum, i) => sum + i.quantity, 0),
    }),
    {
      name: 'marmar-customer',
      partialize: (s) => ({
        selectedBranch: s.selectedBranch,
        cart: s.cart,
        token: s.token,
      }),
    }
  )
)

export default useStore
