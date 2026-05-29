'use client';

import React, { useEffect } from 'react';
import { useCartStore } from '../store/cart';
import LeafletMap from '../components/LeafletMap';
// ❌ убрали: import { useNavigate } from 'react-router-dom';

export default function CartPage({ onBack, onOrderSuccess }) {
  // ❌ убрали: const navigate = useNavigate();

  const items = useCartStore((s) => s.items ?? []);
  const payment_method = useCartStore((s) => s.payment_method ?? 'cash');
  const address = useCartStore((s) => s.address ?? '');
  const landmark = useCartStore((s) => s.landmark ?? '');
  const latitude = useCartStore((s) => s.latitude ?? null);
  const longitude = useCartStore((s) => s.longitude ?? null);
  const addItem = useCartStore((s) => s.addItem);
  const removeItem = useCartStore((s) => s.removeItem);
  const setCheckoutData = useCartStore((s) => s.setCheckoutData);
  const getTotalPrice = useCartStore((s) => s.getTotalPrice);
  const getPayloadForApi = useCartStore((s) => s.getPayloadForApi);
  const clearCart = useCartStore((s) => s.clearCart);

  const totalPrice = typeof getTotalPrice === 'function' ? getTotalPrice() : 0;

  const handleMapClick = (lat, lng) => {
    setCheckoutData({ latitude: lat, longitude: lng });
  };

  const handleOrderSubmit = async () => {
    try {
      const rawPayload = getPayloadForApi();
      const { current_user_id, ...payload } = rawPayload;

      const token = localStorage.getItem('jwt');
      const response = await fetch('/api/v1/orders/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify(payload),
      });

      if (!response.ok) throw new Error(`Ошибка сервера: ${response.status}`);

      clearCart();

      if (payload.payment_method === 'cash') {
        onOrderSuccess?.(); // ✅ вместо navigate('/')
      } else if (payload.payment_method === 'click' || payload.payment_method === 'payme') {
        window.Telegram?.WebApp?.close?.();
      }
    } catch (error) {
      alert('Ошибка: ' + error.message);
    }
  };

  const hasLocation = latitude !== null && latitude !== 0;
  const isDisabled = items.length === 0 || !hasLocation || !address;

  return (
    <div
      className="max-w-md mx-auto p-4 bg-gray-50 min-h-screen text-gray-800"
      style={{ paddingBottom: '120px' }}
    >
      {/* Кнопка назад */}
      <button onClick={onBack} className="mb-4 text-sm text-gray-500">← Назад</button>
      <h1 className="text-2xl font-bold mb-4">Корзина</h1>

      {/* 1. СПИСОК ТОВАРОВ */}
      <div className="bg-white rounded-xl p-4 shadow-sm mb-4">
        <h2 className="text-lg font-semibold mb-3">Ваш заказ</h2>
        {items.length === 0 ? (
          <p className="text-gray-400 text-center py-4">В корзине пока пусто</p>
        ) : (
          <div className="divide-y divide-gray-100">
            {items.map((item) => (
              <div key={item.id} className="flex justify-between items-center py-3">
                <div>
                  <h3 className="font-medium text-sm">{item.name}</h3>
                  <p className="text-gray-500 text-xs">{item.price} сум</p>
                </div>
                <div className="flex items-center gap-3 bg-gray-100 rounded-lg p-1">
                  <button onClick={() => removeItem(item.id)} className="w-7 h-7 bg-white rounded-md shadow-sm font-bold">-</button>
                  <span className="font-semibold text-sm w-4 text-center">{item.quantity}</span>
                  <button onClick={() => addItem(item)} className="w-7 h-7 bg-white rounded-md shadow-sm font-bold">+</button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* 2. ДАННЫЕ ДОСТАВКИ */}
      <div className="bg-white rounded-xl p-4 shadow-sm mb-4 space-y-4">
        <h2 className="text-lg font-semibold">Детали доставки</h2>

        <div>
          <label className="block text-xs font-medium text-gray-500 mb-1">Адрес доставки</label>
          <input
            type="text" placeholder="Улица, дом, квартира" value={address}
            onChange={(e) => setCheckoutData({ address: e.target.value })}
            className="w-full border border-gray-200 rounded-lg p-2 text-sm focus:outline-none focus:border-yellow-500"
          />
        </div>

        <div>
          <label className="block text-xs font-medium text-gray-500 mb-1">Ориентир</label>
          <input
            type="text" placeholder="Например: возле школы" value={landmark}
            onChange={(e) => setCheckoutData({ landmark: e.target.value })}
            className="w-full border border-gray-200 rounded-lg p-2 text-sm focus:outline-none focus:border-yellow-500"
          />
        </div>

        <div>
          <label className="block text-xs font-medium text-gray-500 mb-1">Способ оплаты</label>
          <select
            value={payment_method}
            onChange={(e) => setCheckoutData({ payment_method: e.target.value })}
            className="w-full border border-gray-200 rounded-lg p-2 text-sm bg-white"
          >
            <option value="cash">Наличные</option>
            <option value="payme">Payme</option>
            <option value="click">Click</option>
          </select>
        </div>

        <div>
          <label className="block text-xs font-medium text-gray-500 mb-1">
            Укажите точку на карте
            {hasLocation && (
              <span className="text-green-600 font-mono ml-2">
                ({latitude.toFixed(4)}, {longitude.toFixed(4)})
              </span>
            )}
          </label>
          <div style={{ width: '100%', height: '192px', borderRadius: '8px', overflow: 'hidden', border: '1px solid #e5e7eb', position: 'relative', zIndex: 1 }}>
            <LeafletMap latitude={latitude} longitude={longitude} onMapClick={handleMapClick} />
          </div>
        </div>
      </div>

      {/* 3. КНОПКА ЗАКАЗА */}
      <div style={{ position: 'fixed', bottom: 0, left: 0, right: 0, backgroundColor: 'white', padding: '16px', borderTop: '1px solid #f3f4f6', boxShadow: '0 -4px 10px rgba(0,0,0,0.05)', zIndex: 1000 }}>
        <div className="flex justify-between items-center mb-2">
          <span className="text-gray-500 text-sm">Итого:</span>
          <span className="text-xl font-bold text-gray-900">{totalPrice} сум</span>
        </div>
        <button
          onClick={handleOrderSubmit}
          disabled={isDisabled}
          style={{ pointerEvents: isDisabled ? 'none' : 'auto' }}
          className={`w-full py-3 rounded-xl font-semibold text-center transition-all ${
            isDisabled ? 'bg-gray-200 text-gray-400 cursor-not-allowed' : 'bg-yellow-400 text-gray-900 active:scale-[0.98]'
          }`}
        >
          {items.length === 0 ? 'Добавьте товары' : !hasLocation ? 'Укажите адрес на карте' : 'Оформить заказ'}
        </button>
      </div>
    </div>
  );
}