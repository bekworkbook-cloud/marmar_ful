import { useState, useEffect } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import { orderApi, userApi } from '../api/api'
import useStore from '../store/useStore'

const STATUS_OPTIONS = [
  { value: 'PENDING',     label: 'Ожидается' },
  { value: 'ACCEPTED',    label: 'Принят' },
  { value: 'IN_DELIVERY', label: 'Доставляется' },
  { value: 'DELIVERED',   label: 'Доставлен' },
  { value: 'CANCELLED',   label: 'Отменён' },
]

const STATUS_STYLE = {
  PENDING:     'bg-amber-100 text-amber-700',
  ACCEPTED:    'bg-blue-100 text-blue-700',
  IN_DELIVERY: 'bg-violet-100 text-violet-700',
  DELIVERED:   'bg-green-100 text-green-700',
  CANCELLED:   'bg-red-100 text-red-700',
}

export default function OrderDetailsPage() {
  const { id } = useParams()
  const navigate = useNavigate()
  const user = useStore(s => s.user)

  const [order, setOrder] = useState(null)
  const [items, setItems] = useState([])
  const [couriers, setCouriers] = useState([])
  const [messages, setMessages] = useState([])
  const [msgText, setMsgText] = useState('')
  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)
  const [activeTab, setActiveTab] = useState('info')

  const load = async () => {
    try {
      const [oRes, iRes, mRes] = await Promise.all([
        orderApi.get(id),
        orderApi.items(id),
        orderApi.messages(id),
      ])

      setOrder(oRes.data)

      const iData = iRes.data
      setItems(Array.isArray(iData) ? iData : iData?.items || [])

      const mData = mRes.data
      setMessages(Array.isArray(mData) ? mData : mData?.items || [])

      if (oRes.data?.branch_id) {
        userApi.couriers(oRes.data.branch_id)
          .then(r => {
            const cu = r.data
            setCouriers(Array.isArray(cu) ? cu : cu?.items || [])
          })
          .catch(() => {})
      }
    } catch {
      navigate('/')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    load()
  }, [id])

  const handleStatus = async (status) => {
    setSaving(true)
    try {
      const res = await orderApi.updateStatus(id, status)
      setOrder(res.data)
    } finally {
      setSaving(false)
    }
  }

  const handleCourier = async (courierId) => {
    setSaving(true)
    try {
      const res = await orderApi.assignCourier(id, Number(courierId))
      setOrder(res.data)
    } finally {
      setSaving(false)
    }
  }

  const handleSendMsg = async () => {
    if (!msgText.trim()) return

    try {
      const res = await orderApi.sendMessage(id, msgText)
      setMessages(m => [...m, res.data])
      setMsgText('')
    } catch {}
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="w-10 h-10 border-4 border-indigo-500 border-t-transparent rounded-full animate-spin" />
      </div>
    )
  }

  if (!order) return null

  const stStyle = STATUS_STYLE[order.status] || 'bg-gray-100 text-gray-600'
  const stLabel =
    STATUS_OPTIONS.find(s => s.value === order.status)?.label || order.status

  return (
    <div className="min-h-screen bg-slate-50 flex flex-col">
      {/* Header */}
      <div className="bg-indigo-600 px-4 pt-12 pb-5 sticky top-0 z-20">
        <div className="flex items-center gap-3 mb-3">
          <button
            onClick={() => navigate('/')}
            className="w-9 h-9 bg-indigo-500 rounded-xl flex items-center justify-center text-white"
          >
            ←
          </button>

          <h1 className="text-white font-bold text-lg">
            Заказ #{order.id}
          </h1>

          <span className={`ml-auto text-xs font-semibold px-3 py-1 rounded-full ${stStyle}`}>
            {stLabel}
          </span>
        </div>

        {/* Tabs */}
        <div className="flex gap-1 bg-indigo-500/50 rounded-xl p-1">
          {[
            { key: 'info', label: 'Информация' },
            { key: 'items', label: 'Товары' },
            { key: 'chat', label: `Чат (${messages.length})` },
          ].map(tab => (
            <button
              key={tab.key}
              onClick={() => setActiveTab(tab.key)}
              className={`flex-1 py-1.5 rounded-lg text-xs font-semibold transition-colors
                ${activeTab === tab.key ? 'bg-white text-indigo-700' : 'text-indigo-100'}`}
            >
              {tab.label}
            </button>
          ))}
        </div>
      </div>

      <div className="flex-1 px-4 py-4 pb-6 space-y-3">

        {/* INFO TAB */}
        {activeTab === 'info' && (
          <>
            <div className="bg-white rounded-2xl p-4 shadow-sm space-y-3">
              <h3 className="font-semibold text-gray-800">Доставка</h3>

              <InfoRow icon="📍" label="Адрес" value={order.address || '—'} />

              {order.landmark && (
                <InfoRow icon="🏁" label="Ориентир" value={order.landmark} />
              )}

              <InfoRow
                icon="💳"
                label="Способ оплаты"
                value={order.payment_method}
              />

              <InfoRow
                icon="💰"
                label="Итого"
                value={`${Number(order.total_price).toLocaleString()} сум`}
                bold
              />
            </div>

            {/* Status update */}
            <div className="bg-white rounded-2xl p-4 shadow-sm">
              <h3 className="font-semibold text-gray-800 mb-3">
                Изменить статус
              </h3>

              <div className="grid grid-cols-1 gap-2">
                {STATUS_OPTIONS.map(opt => (
                  <button
                    key={opt.value}
                    onClick={() => handleStatus(opt.value)}
                    disabled={saving || order.status === opt.value}
                    className={`py-2.5 px-4 rounded-xl text-sm font-medium text-left transition-all
                      ${order.status === opt.value
                        ? 'bg-indigo-600 text-white'
                        : 'bg-gray-50 text-gray-700 active:bg-gray-100'}
                      disabled:opacity-50`}
                  >
                    {order.status === opt.value && '✓ '}
                    {opt.label}
                  </button>
                ))}
              </div>
            </div>

            {/* Courier assignment */}
            <div className="bg-white rounded-2xl p-4 shadow-sm">
              <h3 className="font-semibold text-gray-800 mb-3">
                Назначить курьера
              </h3>

              {couriers.length === 0 ? (
                <p className="text-sm text-gray-400">
                  Нет активных курьеров
                </p>
              ) : (
                <div className="space-y-2">
                  {couriers.map(c => (
                    <button
                      key={c.id}
                      onClick={() => handleCourier(c.id)}
                      disabled={saving || order.courier_id === c.id}
                      className={`w-full flex items-center gap-3 p-3 rounded-xl text-sm transition-all
                        ${order.courier_id === c.id
                          ? 'bg-green-50 border-2 border-green-400'
                          : 'bg-gray-50 border-2 border-transparent active:bg-gray-100'}
                        disabled:opacity-50`}
                    >
                      <span className="w-8 h-8 bg-indigo-100 rounded-full flex items-center justify-center text-sm font-bold text-indigo-600">
                        {(c.first_name || c.username || '?')[0].toUpperCase()}
                      </span>

                      <div className="text-left">
                        <p className="font-medium text-gray-800">
                          {c.first_name || c.username}
                        </p>

                        {c.phone_number && (
                          <p className="text-xs text-gray-400">
                            {c.phone_number}
                          </p>
                        )}
                      </div>

                      {order.courier_id === c.id && (
                        <span className="ml-auto text-green-500 font-bold">
                          ✓
                        </span>
                      )}
                    </button>
                  ))}
                </div>
              )}
            </div>
          </>
        )}

        {/* ITEMS TAB */}
        {activeTab === 'items' && (
          <div className="bg-white rounded-2xl shadow-sm overflow-hidden">
            {items.length === 0 ? (
              <p className="text-center text-gray-400 py-8 text-sm">
                Товаров нет
              </p>
            ) : (
              items.map((item, idx) => (
                <div key={item.id}>
                  <div className="flex items-center justify-between px-4 py-3">
                    <div className="flex-1">
                      <p className="text-sm font-medium text-gray-800">
                        {item.product?.name || `Товар #${item.product_id}`}
                      </p>

                      <p className="text-xs text-gray-400 mt-0.5">
                        {item.quantity} × {Number(item.price).toLocaleString()} сум
                      </p>
                    </div>

                    <p className="font-bold text-indigo-600 text-sm">
                      {(item.quantity * item.price).toLocaleString()} сум
                    </p>
                  </div>

                  {idx < items.length - 1 && (
                    <div className="mx-4 h-px bg-gray-100" />
                  )}
                </div>
              ))
            )}

            <div className="mx-4 h-px bg-gray-200" />

            <div className="flex justify-between px-4 py-3">
              <span className="font-semibold text-gray-700">Итого</span>
              <span className="font-bold text-indigo-600">
                {Number(order.total_price).toLocaleString()} сум
              </span>
            </div>
          </div>
        )}

        {/* CHAT TAB */}
        {activeTab === 'chat' && (
          <div className="flex flex-col gap-3">
            <div className="bg-white rounded-2xl p-4 shadow-sm space-y-3 min-h-[200px]">
              {messages.length === 0 ? (
                <p className="text-center text-gray-400 text-sm py-4">
                  Сообщений нет
                </p>
              ) : (
                messages.map(msg => (
                  <div
                    key={msg.id}
                    className={`flex ${
                      msg.sender_id === user?.id
                        ? 'justify-end'
                        : 'justify-start'
                    }`}
                  >
                    <div
                      className={`max-w-[75%] px-4 py-2 rounded-2xl text-sm
                      ${
                        msg.sender_id === user?.id
                          ? 'bg-indigo-500 text-white rounded-br-sm'
                          : 'bg-gray-100 text-gray-800 rounded-bl-sm'
                      }`}
                    >
                      {msg.text}
                    </div>
                  </div>
                ))
              )}
            </div>

            <div className="bg-white rounded-2xl p-3 shadow-sm flex gap-2">
              <input
                type="text"
                value={msgText}
                onChange={e => setMsgText(e.target.value)}
                onKeyDown={e => e.key === 'Enter' && handleSendMsg()}
                placeholder="Введите сообщение..."
                className="flex-1 bg-gray-50 rounded-xl px-4 py-2.5 text-sm outline-none"
              />

              <button
                onClick={handleSendMsg}
                disabled={!msgText.trim()}
                className="w-10 h-10 bg-indigo-500 text-white rounded-xl flex items-center justify-center disabled:opacity-40"
              >
                →
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

function InfoRow({ icon, label, value, bold }) {
  return (
    <div className="flex items-start gap-3">
      <span className="text-base w-6">{icon}</span>

      <div className="flex-1">
        <p className="text-xs text-gray-400">{label}</p>

        <p
          className={`text-sm mt-0.5 ${
            bold
              ? 'font-bold text-indigo-600'
              : 'text-gray-700'
          }`}
        >
          {value}
        </p>
      </div>
    </div>
  )
}