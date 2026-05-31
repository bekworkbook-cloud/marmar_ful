import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { orderApi } from '../api/api'

const STATUS_MAP = {
  PENDING:     { label: 'Ожидается',      color: 'bg-yellow-100 text-yellow-700' },
  ACCEPTED:    { label: 'Принят',         color: 'bg-blue-100 text-blue-700' },
  IN_DELIVERY: { label: 'Доставляется',   color: 'bg-purple-100 text-purple-700' },
  DELIVERED:   { label: 'Доставлен',      color: 'bg-green-100 text-green-700' },
  CANCELLED:   { label: 'Отменён',        color: 'bg-red-100 text-red-700' },
}

export default function OrdersPage() {
  const navigate = useNavigate()
  const [orders, setOrders] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    orderApi
      .list()
      .then(r => {
        const data = r.data
        setOrders(Array.isArray(data) ? data : data?.items || [])
      })
      .catch(() => setError('Ошибка при загрузке заказов'))
      .finally(() => setLoading(false))
  }, [])

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white px-4 pt-12 pb-4 shadow-sm sticky top-0 z-10">
        <div className="flex items-center gap-3">
          <button
            onClick={() => navigate('/')}
            className="w-9 h-9 flex items-center justify-center rounded-xl bg-gray-100"
          >
            ←
          </button>
          <h1 className="font-bold text-gray-800 text-lg">Заказы</h1>
        </div>
      </div>

      <div className="px-4 py-4 space-y-3">
        {loading && (
          <div className="flex justify-center py-16">
            <div className="w-8 h-8 border-4 border-orange-500 border-t-transparent rounded-full animate-spin" />
          </div>
        )}

        {error && (
          <div className="flex flex-col items-center py-12 gap-3">
            <span className="text-4xl">😕</span>
            <p className="text-gray-500 text-center text-sm">{error}</p>
            <button
              onClick={() => window.location.reload()}
              className="px-6 py-2 bg-orange-500 text-white rounded-xl text-sm"
            >
              Повторить
            </button>
          </div>
        )}

        {!loading && !error && orders.length === 0 && (
          <div className="flex flex-col items-center py-16 gap-3">
            <span className="text-6xl">📦</span>
            <h3 className="font-semibold text-gray-700">Заказов нет</h3>
            <p className="text-gray-400 text-sm text-center">
              Вы ещё не сделали ни одного заказа
            </p>
            <button
              onClick={() => navigate('/')}
              className="mt-2 px-6 py-3 bg-orange-500 text-white rounded-2xl font-medium"
            >
              Оформить заказ
            </button>
          </div>
        )}

        {orders.map(order => {
          const st = STATUS_MAP[order.status] || { label: order.status, color: 'bg-gray-100 text-gray-600' }
          return (
            <div key={order.id} className="bg-white rounded-2xl p-4 shadow-sm">
              <div className="flex items-start justify-between mb-3">
                <div>
                  <p className="font-semibold text-gray-800">Заказ #{order.id}</p>
                  {order.created_at && (
                    <p className="text-xs text-gray-400 mt-0.5">
                      {new Date(order.created_at).toLocaleDateString('ru-RU', {
                        day: '2-digit',
                        month: 'short',
                        hour: '2-digit',
                        minute: '2-digit',
                      })}
                    </p>
                  )}
                </div>
                <span className={`text-xs font-semibold px-3 py-1 rounded-full ${st.color}`}>
                  {st.label}
                </span>
              </div>

              {order.address && (
                <div className="flex items-start gap-2 text-sm text-gray-600 mb-3">
                  <span>📍</span>
                  <span>{order.address}</span>
                </div>
              )}

              <div className="flex items-center justify-between pt-3 border-t border-gray-100">
                <div>
                  <p className="text-xs text-gray-400">Оплата</p>
                  <p className="text-sm font-medium text-gray-700 capitalize">
                    {order.payment_method}
                  </p>
                </div>
                <div className="text-right">
                  <p className="text-xs text-gray-400">Итого</p>
                  <p className="font-bold text-orange-500">
                    {Number(order.total_price).toLocaleString()} сум
                  </p>
                </div>
              </div>
            </div>
          )
        })}
      </div>
    </div>
  )
}