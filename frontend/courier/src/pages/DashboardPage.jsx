import { useState, useEffect, useCallback } from 'react'
import { useNavigate } from 'react-router-dom'
import { orderApi } from '../api/api'
import useStore from '../store/useStore'

const STATUS_STYLE = {
  ACCEPTED:    { badge: 'bg-blue-100 text-blue-700',    label: 'Принят' },
  IN_DELIVERY: { badge: 'bg-violet-100 text-violet-700',label: 'Доставляется' },
  PENDING:     { badge: 'bg-amber-100 text-amber-700',  label: 'Ожидается' },
  DELIVERED:   { badge: 'bg-green-100 text-green-700',  label: 'Доставлен' },
  CANCELLED:   { badge: 'bg-red-100 text-red-700',      label: 'Отменён' },
}

export default function DashboardPage() {
  const navigate = useNavigate()
  const user = useStore(s => s.user)
  const [orders, setOrders] = useState([])
  const [loading, setLoading] = useState(true)
  const [activeTab, setActiveTab] = useState('active')

  const load = useCallback(() => {
    setLoading(true)
    orderApi
      .list()
      .then(r => {
        const data = r.data
        setOrders(Array.isArray(data) ? data : data?.items || [])
      })
      .finally(() => setLoading(false))
  }, [])

  useEffect(() => {
    load()
    const interval = setInterval(load, 30000)
    return () => clearInterval(interval)
  }, [load])

  const activeOrders = orders.filter(o =>
    ['ACCEPTED', 'IN_DELIVERY'].includes(o.status)
  )
  const historyOrders = orders.filter(o =>
    ['DELIVERED', 'CANCELLED'].includes(o.status)
  )

  const displayed = activeTab === 'active' ? activeOrders : historyOrders

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-green-600 px-4 pt-12 pb-5">
        <div className="flex items-center justify-between mb-1">
          <div>
            <p className="text-green-200 text-xs">Панель курьера</p>
            <h1 className="text-white text-xl font-bold">
              {user?.first_name || user?.username || 'Курьер'}
            </h1>
          </div>
          <button
            onClick={load}
            className="w-10 h-10 bg-green-500 rounded-xl flex items-center justify-center text-white text-lg"
          >
            ↻
          </button>
        </div>

        {/* Stats */}
        <div className="grid grid-cols-2 gap-3 mt-4">
          <div className="bg-green-500/60 rounded-xl p-3 text-center">
            <p className="text-2xl font-bold text-white">{activeOrders.length}</p>
            <p className="text-green-200 text-xs mt-0.5">Активные заказы</p>
          </div>
          <div className="bg-green-500/60 rounded-xl p-3 text-center">
            <p className="text-2xl font-bold text-white">{historyOrders.filter(o => o.status === 'DELIVERED').length}</p>
            <p className="text-green-200 text-xs mt-0.5">Доставлено (сегодня)</p>
          </div>
        </div>

        {/* Tabs */}
        <div className="flex gap-1 bg-green-500/40 rounded-xl p-1 mt-3">
          {[
            { key: 'active',  label: `Активные (${activeOrders.length})` },
            { key: 'history', label: `История (${historyOrders.length})` },
          ].map(tab => (
            <button
              key={tab.key}
              onClick={() => setActiveTab(tab.key)}
              className={`flex-1 py-1.5 rounded-lg text-xs font-semibold transition-colors
                ${activeTab === tab.key ? 'bg-white text-green-700' : 'text-green-100'}`}
            >
              {tab.label}
            </button>
          ))}
        </div>
      </div>

      {/* Orders */}
      <div className="px-4 py-4 space-y-3">
        {loading && (
          <div className="flex justify-center py-12">
            <div className="w-8 h-8 border-4 border-green-500 border-t-transparent rounded-full animate-spin" />
          </div>
        )}

        {!loading && displayed.length === 0 && (
          <div className="flex flex-col items-center py-12 gap-2">
            <span className="text-5xl">{activeTab === 'active' ? '🏍️' : '📦'}</span>
            <p className="text-gray-500 text-sm">
              {activeTab === 'active' ? 'Нет активных заказов' : 'История пуста'}
            </p>
          </div>
        )}

        {displayed.map(order => {
          const st = STATUS_STYLE[order.status] || STATUS_STYLE.PENDING
          return (
            <button
              key={order.id}
              onClick={() => navigate(`/delivery/${order.id}`)}
              className="w-full text-left bg-white rounded-2xl p-4 shadow-sm border border-gray-100 active:scale-[0.98] transition-transform"
            >
              <div className="flex items-start justify-between mb-2">
                <span className="font-bold text-gray-800">#{order.id}</span>
                <span className={`text-xs font-semibold px-2.5 py-1 rounded-full ${st.badge}`}>
                  {st.label}
                </span>
              </div>

              {order.address && (
                <p className="text-sm text-gray-600 flex items-start gap-1.5 mb-2">
                  <span>📍</span>
                  <span>{order.address}</span>
                </p>
              )}

              {order.landmark && (
                <p className="text-xs text-gray-400 flex items-start gap-1.5 mb-2">
                  <span>🏁</span>
                  <span>{order.landmark}</span>
                </p>
              )}

              <div className="flex items-center justify-between pt-2 border-t border-gray-100">
                <span className="text-xs text-gray-400 capitalize">{order.payment_method}</span>
                <span className="font-bold text-green-600">
                  {Number(order.total_price).toLocaleString()} сум
                </span>
              </div>
            </button>
          )
        })}
      </div>
    </div>
  )
}