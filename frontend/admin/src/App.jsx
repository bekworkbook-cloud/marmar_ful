import { useEffect, useState } from 'react'
import { HashRouter, Routes, Route, Navigate } from 'react-router-dom'
import useAdminStore from './store/useAdminStore'
import DashboardPage from './pages/DashboardPage'
import OrdersPage from './pages/OrdersPage'
import MenuPage from './pages/MenuPage'
import BranchesPage from './pages/BranchesPage'
import StaffPage from './pages/StaffPage'

function PrivateRoute({ children, ready }) {
  const token = useAdminStore(s => s.token)
  if (!ready) return null
  return token ? children : <div style={{ padding: 24, color: 'red' }}>Нет доступа</div>
}

export default function App() {
  const { token, setToken, logout } = useAdminStore()
  const [ready, setReady] = useState(false)

  useEffect(() => {
    const tg = window.Telegram?.WebApp
    if (tg) {
      tg.ready()
      tg.expand()
    }

    const boot = async () => {
      const initData = tg?.initData

      try {
        if (!initData) throw new Error('No initData')

        const { authApi } = await import('./api/api')
        const data = await authApi.loginTelegram(initData)
        setToken(data.access_token)
      } catch {
        logout()
      } finally {
        setReady(true)
      }
    }

    boot()
  }, [])

  // слушаем 401 — токен протух
  useEffect(() => {
    if (!token) return
    const handle = () => logout()
    window.addEventListener('unauthorized', handle)
    return () => window.removeEventListener('unauthorized', handle)
  }, [token])

  return (
    <HashRouter>
      <Routes>
        <Route path="/"         element={<PrivateRoute ready={ready}><DashboardPage /></PrivateRoute>} />
        <Route path="/orders"   element={<PrivateRoute ready={ready}><OrdersPage /></PrivateRoute>} />
        <Route path="/menu"     element={<PrivateRoute ready={ready}><MenuPage /></PrivateRoute>} />
        <Route path="/branches" element={<PrivateRoute ready={ready}><BranchesPage /></PrivateRoute>} />
        <Route path="/staff"    element={<PrivateRoute ready={ready}><StaffPage /></PrivateRoute>} />
        <Route path="*"         element={<Navigate to="/" replace />} />
      </Routes>
    </HashRouter>
  )
}