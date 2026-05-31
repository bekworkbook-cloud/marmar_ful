import { create } from 'zustand'
import { persist } from 'zustand/middleware'

const useStore = create(
  persist(
    (set) => ({
      user: null,
      token: localStorage.getItem('access_token') || null,

      setUser: (user) => set({ user }),
      setToken: (token) => {
        localStorage.setItem('access_token', token)
        set({ token })
      },
      clearAuth: () => {
        localStorage.removeItem('access_token')
        set({ user: null, token: null })
      },
    }),
    {
      name: 'marmar-courier',
      partialize: (s) => ({ token: s.token }),
    }
  )
)

export default useStore
