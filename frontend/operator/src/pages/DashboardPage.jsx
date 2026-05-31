import { useState, useEffect, useCallback } from 'react'
import { useNavigate } from 'react-router-dom'
import { orderApi } from '../api/api'

const STATUS_TABS = [
  { key: 'all',         label: 'Все' },
  { key: 'PENDING',     label: 'Новые' },
  { key: 'ACCEPTED',    label: 'Приняты' },
  { key: 'IN_DELIVERY', label: 'В пути' },
  { key: 'DELIVERED',   label: 'Завершены' },
]

const STATUS_STYLE = {
  PENDING:     { dot: 'bg-amber-400',  badge: 'bg-amber-100 text-amber-700',   label: 'Новый' },
  ACCEPTED:    { dot: 'bg-blue-400',   badge: 'bg-blue-100 text-blue-700',     label: 'Принят' },
  IN_DELIVERY: { dot: 'bg-violet-400', badge: 'bg-violet-100 text-violet-700', label: 'В пути' },
  DELIVERED:   { dot: 'bg-green-400',  badge: 'bg-green-100 text-green-700',   label: 'Доставлен' },
  CANCELLED:   { dot: 'bg-red-400',    badge: 'bg-red-100 text-red-700',       label: 'Отменён' },
}

export default function DashboardPage() {
  const navigate = useNavigate()
  const [orders, setOrders] = useState([])
  const [activeTab, setActiveTab] = useState('all')
  const [loading, setLoading] = useState(true)

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

  const filtered = activeTab === 'all'
    ? orders
    : orders.filter(o => o.status === activeTab)

  const pendingCount = orders.filter(o => o.status === 'PENDING').length

  return (
    <div className="min-h-screen bg-slate-50">
      {/* Header */}
      <div className="bg-indigo-600 px-4 pt-12 pb-5">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-white text-xl font-bold">Заказы</h1>
            <p className="text-indigo-200 text-sm mt-0.5">
              Всего: {orders.length}
            </p>
          </div>
          <div className="flex items-center gap-2">
            {pendingCount > 0 && (
              <span className="bg-amber-400 text-amber-900 text-xs font-bold px-2.5 py-1 rounded-full">
                {pendingCount} новых
              </span>
            )}
            <button
              onClick={load}
              className="w-9 h-9 bg-indigo-500 rounded-xl flex items-center justify-center text-white"
            >
              ↻
            </button>
          </div>
        </div>

        {/* Status tabs */}
        <div className="flex gap-2 mt-4 overflow-x-auto scrollbar-hide pb-1">
          {STATUS_TABS.map(tab => (
            <button
              key={tab.key}
              onClick={() => setActiveTab(tab.key)}
              className={`flex-shrink-0 px-3 py-1.5 rounded-full text-xs font-semibold transition-colors
                ${activeTab === tab.key
                  ? 'bg-white text-indigo-700'
                  : 'bg-indigo-500 text-indigo-100'}`}
            >
              {tab.label}
              {tab.key !== 'all' && (
                <span className="ml-1.5 opacity-70">
                  {orders.filter(o => o.status === tab.key).length}
                </span>
              )}
            </button>
          ))}
        </div>
      </div>

      {/* Order list */}
      <div className="px-4 py-4 space-y-3">
        {loading && (
          <div className="flex justify-center py-12">
            <div className="w-8 h-8 border-4 border-indigo-500 border-t-transparent rounded-full animate-spin" />
          </div>
        )}

        {!loading && filtered.length === 0 && (
          <div className="flex flex-col items-center py-12 gap-2">
            <span className="text-5xl">📋</span>
            <p className="text-gray-500 text-sm">Заказов нет</p>
          </div>
        )}

        {filtered.map(order => {
          const st = STATUS_STYLE[order.status] || STATUS_STYLE.PENDING
          return (
            <button
              key={order.id}
              onClick={() => navigate(`/order/${order.id}`)}
              className="w-full text-left bg-white rounded-2xl p-4 shadow-sm border border-gray-100 active:scale-[0.98] transition-transform"
            >
              <div className="flex items-start justify-between mb-2">
                <div className="flex items-center gap-2">
                  <div className={`w-2 h-2 rounded-full ${st.dot}`} />
                  <span className="font-bold text-gray-800">#{order.id}</span>
                </div>
                <span className={`text-xs font-semibold px-2.5 py-1 rounded-full ${st.badge}`}>
                  {st.label}
                </span>
              </div>

              {order.address && (
                <p className="text-sm text-gray-600 mb-2 flex items-start gap-1.5">
                  <span className="text-base">📍</span>
                  <span>{order.address}</span>
                </p>
              )}

              <div className="flex items-center justify-between mt-2 pt-2 border-t border-gray-100">
                <span className="text-xs text-gray-400">
                  {order.created_at
                    ? new Date(order.created_at).toLocaleTimeString('ru-RU', {
                        hour: '2-digit',
                        minute: '2-digit'
                      })
                    : '—'}
                </span>
                <div className="flex items-center gap-3">
                  {order.courier_id ? (
                    <span className="text-xs text-green-600 font-medium">✓ Курьер назначен</span>
                  ) : (
                    <span className="text-xs text-amber-500 font-medium">Курьер не назначен</span>
                  )}
                  <span className="font-bold text-indigo-600">
                    {Number(order.total_price).toLocaleString()} сум
                  </span>
                </div>
              </div>
            </button>
          )
        })}
      </div>
    </div>
  )
}