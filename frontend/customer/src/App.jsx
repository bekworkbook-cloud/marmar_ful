import { useEffect } from 'react'
import { HashRouter, Routes, Route, Navigate } from 'react-router-dom'
import useStore from './store/useStore'
import { authApi } from './api/api'
import MainPage from './pages/MainPage'
import MenuPage from './pages/MenuPage'
import ProductPage from './pages/ProductPage'
import CartPage from './pages/CartPage'
import OrdersPage from './pages/OrdersPage'

export default function App() {
  const { token, setToken, setUser, clearAuth } = useStore()

  useEffect(() => {
    const tg = window.Telegram?.WebApp
    if (tg) {
      tg.ready()
      tg.expand()
    }

    const boot = async () => {
      const initData = tg?.initData
      try {
        if (initData) {
          const res = await authApi.initTelegram(initData)
          setToken(res.data.access_token)
        }
        const me = await authApi.me()
        setUser(me.data)
      } catch {
        clearAuth()
      }
    }

    boot()
  }, [])

  return (
    <HashRouter>
      <Routes>
        <Route path="/" element={<MainPage />} />
        <Route path="/menu" element={<MenuPage />} />
        <Route path="/product/:id" element={<ProductPage />} />
        <Route path="/cart" element={<CartPage />} />
        <Route path="/orders" element={<OrdersPage />} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </HashRouter>
  )
}
