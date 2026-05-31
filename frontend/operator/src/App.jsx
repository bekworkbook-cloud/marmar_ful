import { useEffect } from 'react'
import { HashRouter, Routes, Route, Navigate } from 'react-router-dom'
import useStore from './store/useStore'
import { authApi } from './api/api'
import DashboardPage from './pages/DashboardPage'
import OrderDetailsPage from './pages/OrderDetailsPage'

export default function App() {
  const { setToken, setUser, clearAuth } = useStore()

  useEffect(() => {
    const tg = window.Telegram?.WebApp
    if (tg) { tg.ready(); tg.expand() }

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
        <Route path="/" element={<DashboardPage />} />
        <Route path="/order/:id" element={<OrderDetailsPage />} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </HashRouter>
  )
}
