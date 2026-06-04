import { useState, useEffect } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import { orderApi } from '../api/api'
import useStore from '../store/useStore'

const STATUS_FLOW = [
  { value: 'ACCEPTED',    label: 'Qabul qilingan',  next: 'IN_DELIVERY', nextLabel: 'Yolga chiqish' },
  { value: 'IN_DELIVERY', label: 'Yetkazilmoqda',   next: 'DELIVERED',   nextLabel: 'Yetkazib bo\'ldim' },
  { value: 'DELIVERED',   label: 'Yetkazildi',      next: null,          nextLabel: null },
  { value: 'CANCELLED',   label: 'Bekor qilindi',   next: null,          nextLabel: null },
]

const STATUS_STYLE = {
  ACCEPTED:    'bg-blue-100 text-blue-700',
  IN_DELIVERY: 'bg-violet-100 text-violet-700',
  DELIVERED:   'bg-green-100 text-green-700',
  CANCELLED:   'bg-red-100 text-red-700',
}

export default function DeliveryPage() {
  const { id } = useParams()
  const navigate = useNavigate()
  const user = useStore(s => s.user)

  const [order, setOrder] = useState(null)
  const [items, setItems] = useState([])
  const [messages, setMessages] = useState([])
  const [msgText, setMsgText] = useState('')
  const [loading, setLoading] = useState(true)
  const [updating, setUpdating] = useState(false)
  const [showChat, setShowChat] = useState(false)

  useEffect(() => {
    Promise.all([
      orderApi.get(id),
      orderApi.items(id),
      orderApi.messages(id),
    ])
      .then(([oRes, iRes, mRes]) => {
        setOrder(oRes.data)
        const iData = iRes.data
        setItems(Array.isArray(iData) ? iData : iData?.items || [])
        const mData = mRes.data
        setMessages(Array.isArray(mData) ? mData : mData?.items || [])
      })
      .catch(() => navigate('/'))
      .finally(() => setLoading(false))
  }, [id])

  const handleNextStatus = async () => {
    const flow = STATUS_FLOW.find(s => s.value === order?.status)
    if (!flow?.next) return
    setUpdating(true)
    try {
      const res = await orderApi.updateStatus(id, flow.next)
      setOrder(res.data)
    } finally {
      setUpdating(false)
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

  const openMap = () => {
    if (order?.latitude && order?.longitude) {
      window.open(
        `https://maps.google.com/?q=${order.latitude},${order.longitude}`,
        '_blank'
      )
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-screen bg-gray-50">
        <div className="w-10 h-10 border-4 border-green-500 border-t-transparent rounded-full animate-spin" />
      </div>
    )
  }

  if (!order) return null

  const flow = STATUS_FLOW.find(s => s.value === order.status)
  const stStyle = STATUS_STYLE[order.status] || 'bg-gray-100 text-gray-600'
  const isFinished = order.status === 'DELIVERED' || order.status === 'CANCELLED'

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col">
      {/* Header */}
      <div className="bg-green-600 px-4 pt-12 pb-5 sticky top-0 z-20">
        <div className="flex items-center gap-3">
          <button
            onClick={() => navigate('/')}
            className="w-9 h-9 bg-green-500 rounded-xl flex items-center justify-center text-white"
          >
            ←
          </button>
          <div>
            <h1 className="text-white font-bold">Buyurtma #{order.id}</h1>
            <span className={`text-xs font-semibold px-2 py-0.5 rounded-full ${stStyle}`}>
              {flow?.label || order.status}
            </span>
          </div>
          <button
            onClick={() => setShowChat(v => !v)}
            className="ml-auto relative w-10 h-10 bg-green-500 rounded-xl flex items-center justify-center text-lg"
          >
            💬
            {messages.length > 0 && (
              <span className="absolute -top-1 -right-1 bg-red-500 text-white text-xs w-4 h-4 rounded-full flex items-center justify-center">
                {messages.length}
              </span>
            )}
          </button>
        </div>
      </div>

      <div className="flex-1 px-4 py-4 space-y-3 pb-36">
        {/* Delivery address */}
        <div className="bg-white rounded-2xl p-4 shadow-sm">
          <h3 className="font-semibold text-gray-800 mb-3">Yetkazib berish manzili</h3>

          <div className="space-y-2">
            <div className="flex items-start gap-3">
              <span className="text-xl w-7">📍</span>
              <div>
                <p className="text-xs text-gray-400">Manzil</p>
                <p className="text-sm font-medium text-gray-800">{order.address || '—'}</p>
              </div>
            </div>

            {order.landmark && (
              <div className="flex items-start gap-3">
                <span className="text-xl w-7">🏁</span>
                <div>
                  <p className="text-xs text-gray-400">Mo'ljal</p>
                  <p className="text-sm text-gray-700">{order.landmark}</p>
                </div>
              </div>
            )}
          </div>

          {order.latitude && order.longitude && (
            <button
              onClick={openMap}
              className="w-full mt-4 py-3 bg-green-50 border border-green-200 text-green-700 font-medium text-sm rounded-xl flex items-center justify-center gap-2"
            >
              <span>🗺️</span>
              <span>Xaritada ko'rish</span>
            </button>
          )}
        </div>

        {/* Payment */}
        <div className="bg-white rounded-2xl p-4 shadow-sm flex items-center justify-between">
          <div className="flex items-center gap-3">
            <span className="text-2xl">
              {order.payment_method === 'cash' ? '💵' :
               order.payment_method === 'card' ? '💳' : '📱'}
            </span>
            <div>
              <p className="text-xs text-gray-400">To'lov usuli</p>
              <p className="text-sm font-semibold text-gray-800 capitalize">
                {order.payment_method}
              </p>
            </div>
          </div>
          <div className="text-right">
            <p className="text-xs text-gray-400">Jami</p>
            <p className="text-lg font-bold text-green-600">
              {Number(order.total_price).toLocaleString()} so'm
            </p>
          </div>
        </div>

        {/* Order items */}
        <div className="bg-white rounded-2xl shadow-sm overflow-hidden">
          <div className="px-4 py-3 border-b border-gray-100">
            <h3 className="font-semibold text-gray-800">Mahsulotlar</h3>
          </div>
          {items.map((item, idx) => (
            <div key={item.id}>
              <div className="flex items-center justify-between px-4 py-3">
                <div>
                  <p className="text-sm font-medium text-gray-800">
                    {item.product?.name || `Mahsulot #${item.product_id}`}
                  </p>
                  <p className="text-xs text-gray-400 mt-0.5">
                    {item.quantity} dona
                  </p>
                </div>
                <p className="font-semibold text-green-600 text-sm">
                  {(item.quantity * item.price).toLocaleString()} so'm
                </p>
              </div>
              {idx < items.length - 1 && <div className="mx-4 h-px bg-gray-100" />}
            </div>
          ))}
        </div>

        {/* Chat (collapsible) */}
        {showChat && (
          <div className="bg-white rounded-2xl shadow-sm overflow-hidden">
            <div className="px-4 py-3 border-b border-gray-100">
              <h3 className="font-semibold text-gray-800">Chat</h3>
            </div>
            <div className="p-4 space-y-3 max-h-64 overflow-y-auto">
              {messages.length === 0 ? (
                <p className="text-center text-gray-400 text-sm">Xabarlar yo'q</p>
              ) : (
                messages.map(msg => (
                  <div
                    key={msg.id}
                    className={`flex ${msg.sender_id === user?.id ? 'justify-end' : 'justify-start'}`}
                  >
                    <div className={`max-w-[75%] px-4 py-2 rounded-2xl text-sm
                      ${msg.sender_id === user?.id
                        ? 'bg-green-500 text-white rounded-br-sm'
                        : 'bg-gray-100 text-gray-800 rounded-bl-sm'}`}
                    >
                      {msg.text}
                    </div>
                  </div>
                ))
              )}
            </div>
            <div className="px-3 pb-3 flex gap-2">
              <input
                type="text"
                value={msgText}
                onChange={e => setMsgText(e.target.value)}
                onKeyDown={e => e.key === 'Enter' && handleSendMsg()}
                placeholder="Xabar..."
                className="flex-1 bg-gray-50 rounded-xl px-4 py-2.5 text-sm outline-none border border-gray-200"
              />
              <button
                onClick={handleSendMsg}
                disabled={!msgText.trim()}
                className="w-10 h-10 bg-green-500 text-white rounded-xl flex items-center justify-center disabled:opacity-40"
              >
                →
              </button>
            </div>
          </div>
        )}
      </div>

      {/* Action button */}
      {!isFinished && flow?.next && (
        <div className="fixed bottom-0 left-0 right-0 bg-white border-t border-gray-100 px-4 py-4 pb-8">
          <button
            onClick={handleNextStatus}
            disabled={updating}
            className="w-full bg-green-500 text-white py-4 rounded-2xl font-semibold shadow-lg shadow-green-200 disabled:opacity-60 active:scale-[0.98] transition-transform flex items-center justify-center gap-2"
          >
            {updating ? (
              <>
                <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin" />
                <span>Yangilanmoqda...</span>
              </>
            ) : (
              <>
                <span>{flow.value === 'ACCEPTED' ? '🏍️' : '✓'}</span>
                <span>{flow.nextLabel}</span>
              </>
            )}
          </button>
        </div>
      )}

      {isFinished && (
        <div className="fixed bottom-0 left-0 right-0 bg-white border-t border-gray-100 px-4 py-4 pb-8">
          <div className={`w-full py-4 rounded-2xl font-semibold text-center
            ${order.status === 'DELIVERED' ? 'bg-green-50 text-green-700' : 'bg-red-50 text-red-700'}`}
          >
            {order.status === 'DELIVERED' ? '✓ Yetkazib berildi' : '✗ Bekor qilindi'}
          </div>
        </div>
      )}
    </div>
  )
}
