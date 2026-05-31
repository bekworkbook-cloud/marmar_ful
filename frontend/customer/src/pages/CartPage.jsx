import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import useStore from '../store/useStore'
import { orderApi } from '../api/api'
import CartItem from '../components/CartItem'

const PAYMENT_METHODS = [
  { id: 'cash', label: 'Наличные', icon: '💵' },
  // { id: 'card', label: 'Карта', icon: '💳' },
  { id: 'click', label: 'Click', icon: '📱' },
  { id: 'paycom', label: 'Payme', icon: '🟢' },
]

export default function CartPage() {
  const navigate = useNavigate()
  const { cart, cartTotal, cartCount, selectedBranch, user, clearCart } = useStore()
  const total = useStore(s => s.cartTotal())
  const count = useStore(s => s.cartCount())

  const [address, setAddress] = useState('')
  const [landmark, setLandmark] = useState('')
  const [paymentMethod, setPaymentMethod] = useState('cash')
  const [submitting, setSubmitting] = useState(false)
  const [error, setError] = useState(null)

  if (count === 0) {
    return (
      <div className="min-h-screen bg-gray-50 flex flex-col items-center justify-center gap-4 px-6">
        <span className="text-7xl">🛒</span>
        <h2 className="text-xl font-bold text-gray-700">Корзина пуста</h2>
        <p className="text-gray-500 text-center text-sm">Перейдите в меню и добавьте товары</p>
        <button
          onClick={() => navigate('/menu')}
          className="px-8 py-3 bg-orange-500 text-white rounded-2xl font-semibold mt-2"
        >
          Перейти в меню
        </button>
      </div>
    )
  }

  const handleOrder = async () => {
    if (!address.trim()) { setError('Введите адрес'); return }
    setError(null)
    setSubmitting(true)

    const tg = window.Telegram?.WebApp
    const latitude = tg?.locationData?.latitude || 0
    const longitude = tg?.locationData?.longitude || 0

    try {
      await orderApi.create({
        order_items: cart.map(i => ({
          product_id: i.product_id,
          quantity: i.quantity,
          // price: i.price, // убрать из кода который в cart добавляет поле price
        })),
        // customer_id: user?.id,
        branch_id: selectedBranch?.id,
        address,
        landmark,
        latitude,
        longitude,
        payment_method: paymentMethod,
      })
      clearCart()
      navigate('/orders')
    } catch (e) {
      setError(e.response?.data?.detail || 'Ошибка при отправке заказа')
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col">
      {/* Header */}
      <div className="bg-white px-4 pt-12 pb-4 shadow-sm sticky top-0 z-10">
        <div className="flex items-center gap-3">
          <button
            onClick={() => navigate(-1)}
            className="w-9 h-9 flex items-center justify-center rounded-xl bg-gray-100"
          >
            ←
          </button>
          <h1 className="font-bold text-gray-800 text-lg">Корзина</h1>
          <span className="ml-auto text-sm text-gray-400">{count} товаров</span>
        </div>
      </div>

      <div className="flex-1 overflow-y-auto px-4 py-4 space-y-3 pb-52">
        {/* Cart items */}
        <div className="bg-white rounded-2xl overflow-hidden shadow-sm">
          {cart.map((item, idx) => (
            <div key={item.product_id}>
              <CartItem item={item} />
              {idx < cart.length - 1 && <div className="mx-4 h-px bg-gray-100" />}
            </div>
          ))}
        </div>

        {/* Delivery info */}
        <div className="bg-white rounded-2xl p-4 shadow-sm space-y-3">
          <h3 className="font-semibold text-gray-800">Доставка</h3>

          <div>
            <label className="text-xs text-gray-500 font-medium mb-1 block">
              Адрес *
            </label>
            <input
              type="text"
              value={address}
              onChange={e => setAddress(e.target.value)}
              placeholder="Улица, номер дома..."
              className="w-full border border-gray-200 rounded-xl px-4 py-3 text-sm outline-none focus:border-orange-400"
            />
          </div>

          <div>
            <label className="text-xs text-gray-500 font-medium mb-1 block">
              Ориентир (необязательно)
            </label>
            <input
              type="text"
              value={landmark}
              onChange={e => setLandmark(e.target.value)}
              placeholder="Ориентир, название здания..."
              className="w-full border border-gray-200 rounded-xl px-4 py-3 text-sm outline-none focus:border-orange-400"
            />
          </div>
        </div>

        {/* Payment method */}
        <div className="bg-white rounded-2xl p-4 shadow-sm">
          <h3 className="font-semibold text-gray-800 mb-3">Способ оплаты</h3>
          <div className="grid grid-cols-2 gap-2">
            {PAYMENT_METHODS.map(m => (
              <button
                key={m.id}
                onClick={() => setPaymentMethod(m.id)}
                className={`flex items-center gap-2 p-3 rounded-xl border-2 text-sm font-medium transition-all
                  ${paymentMethod === m.id
                    ? 'border-orange-500 bg-orange-50 text-orange-700'
                    : 'border-gray-100 bg-gray-50 text-gray-600'}`}
              >
                <span>{m.icon}</span>
                <span>{m.label}</span>
              </button>
            ))}
          </div>
        </div>

        {/* Summary */}
        <div className="bg-white rounded-2xl p-4 shadow-sm space-y-2">
          <div className="flex justify-between text-sm text-gray-600">
            <span>Товары</span>
            <span>{total.toLocaleString()} сум</span>
          </div>
          {selectedBranch?.delivery_price > 0 && (
            <div className="flex justify-between text-sm text-gray-600">
              <span>Доставка</span>
              <span>{Number(selectedBranch.delivery_price).toLocaleString()} сум</span>
            </div>
          )}
          <div className="h-px bg-gray-100 my-1" />
          <div className="flex justify-between font-bold text-gray-900">
            <span>Итого</span>
            <span className="text-orange-500">
              {(total + Number(selectedBranch?.delivery_price || 0)).toLocaleString()} сум
            </span>
          </div>
        </div>

        {error && (
          <p className="text-red-500 text-sm text-center bg-red-50 p-3 rounded-xl">{error}</p>
        )}
      </div>

      {/* Submit */}
      <div className="fixed bottom-0 left-0 right-0 bg-white border-t border-gray-100 px-4 py-4 pb-8">
        <button
          onClick={handleOrder}
          disabled={submitting}
          className="w-full bg-orange-500 text-white py-4 rounded-2xl font-semibold shadow-lg shadow-orange-200 disabled:opacity-60 active:scale-[0.98] transition-transform flex items-center justify-center gap-2"
        >
          {submitting ? (
            <>
              <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin" />
              <span>Отправка...</span>
            </>
          ) : (
            <span>Оформить заказ</span>
          )}
        </button>
      </div>
    </div>
  )
}