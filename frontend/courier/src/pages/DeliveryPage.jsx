import { useState, useEffect } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import { orderApi } from '../api/api'
import useStore from '../store/useStore'

// Изменили цепочку: теперь из 'confirmed' (Принят) курьер сразу переходит к 'in_transit' (Выехать в путь)
const STATUS_FLOW = [
  { value: 'confirmed',        label: 'Принят',          next: 'courier_assigned',       nextLabel: 'Взять заказ' },
  { value: 'courier_assigned', label: 'Курьер назначен', next: 'in_transit',       nextLabel: 'Выехать в путь' }, // Оставили для обратной совместимости, если бэкенд вернет этот статус
  { value: 'in_transit',       label: 'Доставляется',    next: 'delivered',        nextLabel: 'Доставлено' },
  { value: 'delivered',        label: 'Доставлен',       next: null,               nextLabel: null },
  { value: 'cancelled',        label: 'Отменен',         next: null,               nextLabel: null },
]

const STATUS_STYLE = {
  confirmed:        'bg-gray-100 text-gray-700',
  courier_assigned: 'bg-blue-100 text-blue-700',
  in_transit:       'bg-violet-100 text-violet-700',
  delivered:        'bg-green-100 text-green-700',
  cancelled:        'bg-red-100 text-red-700',
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

  useEffect(() => {
    Promise.all([
      orderApi.get(id),
      orderApi.items(id),
      orderApi.messages(id),
    ])
      .then(([oRes, iRes, mRes]) => {
        const fetchedOrder = oRes.data
        if (fetchedOrder?.status) {
          fetchedOrder.status = fetchedOrder.status.toLowerCase()
        }
        
        setOrder(fetchedOrder)
        const iData = iRes.data
        setItems(Array.isArray(iData) ? iData : iData?.items || [])
        const mData = mRes.data
        setMessages(Array.isArray(mData) ? mData : mData?.items || [])
      })
      .catch(() => navigate('/'))
      .finally(() => setLoading(false))
  }, [id, navigate])

  const handleNextStatus = async () => {
    const flow = STATUS_FLOW.find(s => s.value === order?.status)
    if (!flow?.next) return
    
    setUpdating(true)
    try {
      const res = await orderApi.updateStatus(id, flow.next)
      
      const updatedOrder = res.data
      if (updatedOrder?.status) {
        updatedOrder.status = updatedOrder.status.toLowerCase()
      }
      setOrder(updatedOrder)
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
        `https://yandex.ru/maps/?rtext=~${order.latitude},${order.longitude}&rtt=pd`,
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
  const isFinished = order.status === 'delivered' || order.status === 'cancelled'

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
            <h1 className="text-white font-bold">Заказ #{order.id}</h1>
            <span className={`text-xs font-semibold px-2 py-0.5 rounded-full ${stStyle}`}>
              {flow?.label || order.status}
            </span>
          </div>
        </div>
      </div>

      <div className="flex-1 px-4 py-4 space-y-3 pb-36">
        {/* Delivery address */}
        <div className="bg-white rounded-2xl p-4 shadow-sm">
          <h3 className="font-semibold text-gray-800 mb-3">Адрес доставки</h3>

          <div className="space-y-2">
            <div className="flex items-start gap-3">
              <span className="text-xl w-7">📍</span>
              <div>
                <p className="text-xs text-gray-400">Адрес</p>
                <p className="text-sm font-medium text-gray-800">{order.address || '—'}</p>
              </div>
            </div>

            {order.landmark && (
              <div className="flex items-start gap-3">
                <span className="text-xl w-7">🏁</span>
                <div>
                  <p className="text-xs text-gray-400">Ориентир</p>
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
              <span>Показать на карте</span>
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
              <p className="text-xs text-gray-400">Способ оплаты</p>
              <p className="text-sm font-semibold text-gray-800 capitalize">
                {order.payment_method === 'cash' ? 'Наличные' : order.payment_method === 'card' ? 'Карта' : order.payment_method}
              </p>
            </div>
          </div>
          <div className="text-right">
            <p className="text-xs text-gray-400">Итого</p>
            <p className="text-lg font-bold text-green-600">
              {Number(order.total_price).toLocaleString()} сум
            </p>
          </div>
        </div>

        {/* Order items */}
        <div className="bg-white rounded-2xl shadow-sm overflow-hidden">
          <div className="px-4 py-3 border-b border-gray-100">
            <h3 className="font-semibold text-gray-800">Товары</h3>
          </div>
          {items.map((item, idx) => (
            <div key={item.id}>
              <div className="flex items-center justify-between px-4 py-3">
                <div>
                  <p className="text-sm font-medium text-gray-800">
                    {item.product?.name || `Товар #${item.product_id}`}
                  </p>
                  <p className="text-xs text-gray-400 mt-0.5">
                    {item.quantity} шт.
                  </p>
                </div>
                <p className="font-semibold text-green-600 text-sm">
                  {(item.quantity * item.price).toLocaleString()} сум
                </p>
              </div>
              {idx < items.length - 1 && <div className="mx-4 h-px bg-gray-100" />}
            </div>
          ))}
        </div>
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
                <span>Обновление...</span>
              </>
            ) : (
              <>
                <span>
                  {flow.next === 'courier_assigned' ? '✋' : 
                   flow.next === 'in_transit' ? '🏍️' : '✓'}
                </span>
                <span>{flow.nextLabel}</span>
              </>
            )}
          </button>
        </div>
      )}

      {/* Finished state banner */}
      {isFinished && (
        <div className="fixed bottom-0 left-0 right-0 bg-white border-t border-gray-100 px-4 py-4 pb-8">
          <div className={`w-full py-4 rounded-2xl font-semibold text-center flex items-center justify-center gap-2
            ${order.status === 'delivered' ? 'bg-green-50 text-green-700' : 'bg-red-50 text-red-700'}`}
          >
            {order.status === 'delivered' ? (
              <>
                <span>🎉</span>
                <span>Успешно доставлено</span>
              </>
            ) : (
              <>
                <span>✗</span>
                <span>Заказ отменен</span>
              </>
            )}
          </div>
        </div>
      )}
    </div>
  )
}