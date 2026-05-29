// src/pages/DeliveryPage.jsx
import React, { useState, useEffect } from 'react';
import { apiClient } from '../api/client';
import { useAuthStore } from '../store/auth';
import BackButton from '../components/BackButton';
import StatusBadge from '../components/StatusBadge';
import LeafletMap from '../components/LeafletMap';

export default function DeliveryPage({ orderId, onBack }) {
  const myCourierId = useAuthStore((s) => s.courierId);
  const [order, setOrder] = useState(null);
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [actionLoading, setActionLoading] = useState(false);

  const fetchDetails = async () => {
    setLoading(true);
    try {
      // Параллельные запросы к бэкенду
      const [orderData, itemsData] = await Promise.all([
        apiClient(`/orders/${orderId}`),
        apiClient(`/orders/${orderId}/items`)
      ]);
      setOrder(orderData);
      setItems(itemsData.order_items || []);
    } catch (error) {
      alert('Ошибка получения деталей заказа: ' + error.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (orderId) fetchDetails();
  }, [orderId]);

  // 1. Привязать курьера к заказу (Взять в работу)
  const handleClaimOrder = async () => {
    setActionLoading(true);
    try {
      await apiClient(`/orders/${orderId}/courier?order_personnel_dto=${myCourierId}`, {
        method: 'PATCH'
      });
      // После привязки сразу переводим заказ в статус 'delivering' для непрерывности процесса
      await apiClient(`/orders/${orderId}/status`, {
        method: 'PATCH',
        body: JSON.stringify({ status: 'delivering' })
      });
      await fetchDetails();
    } catch (error) {
      alert('Не удалось взять заказ: ' + error.message);
    } finally {
      setActionLoading(false);
    }
  };

  // 2. Изменить статус (например, перевести из accepted в delivering вручную, если необходимо)
  const handleUpdateStatus = async (targetStatus) => {
    setActionLoading(true);
    try {
      await apiClient(`/orders/${orderId}/status`, {
        method: 'PATCH',
        body: JSON.stringify({ status: targetStatus })
      });
      if (targetStatus === 'completed') {
        onBack(); // Возвращаем на главную панель после завершения
      } else {
        await fetchDetails();
      }
    } catch (error) {
      alert('Ошибка обновления статуса: ' + error.message);
    } finally {
      setActionLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-slate-50 dark:bg-slate-900 flex flex-col">
        <BackButton onClick={onBack} title="Назад к списку" />
        <div className="flex-1 flex items-center justify-center text-slate-400 text-sm">Загрузка информации...</div>
      </div>
    );
  }

  if (!order) return null;

  const isAssignedToMe = order.courier_id === myCourierId;
  const isFreeOrder = order.courier_id === null;
  const formattedTotalPrice = order.total_price.toLocaleString('ru-RU') + ' сум';

  return (
    <div className="min-h-screen bg-slate-50 dark:bg-slate-900 flex flex-col pb-[env(safe-area-inset-bottom,16px)]">
      <BackButton onClick={onBack} title="Заказы" />

      <div className="p-4 space-y-4 flex-1 overflow-y-auto">
        {/* Главный инфо-блок */}
        <div className="bg-white dark:bg-slate-800 p-4 rounded-xl border border-slate-100 dark:border-slate-700 shadow-sm space-y-3">
          <div className="flex justify-between items-center">
            <h2 className="text-lg font-black text-slate-900 dark:text-white">Заказ #{order.id}</h2>
            <StatusBadge status={order.status} />
          </div>
          <div className="text-sm space-y-2 text-slate-600 dark:text-slate-300">
            <p><span className="font-semibold text-slate-900 dark:text-white">Адрес:</span> {order.address}</p>
            {order.landmark && (
              <p className="text-xs bg-slate-50 dark:bg-slate-850 p-2 rounded-lg italic text-slate-500">
                <span className="font-semibold not-italic text-slate-700 dark:text-slate-400">Ориентир:</span> {order.landmark}
              </p>
            )}
            <p><span className="font-semibold text-slate-900 dark:text-white">Оплата:</span> {order.payment_method.toUpperCase()}</p>
          </div>
        </div>

        {/* Интерактивная Read-Only Карта */}
        <LeafletMap latitude={order.latitude} longitude={order.longitude} />

        {/* Содержимое корзины/заказа */}
        <div className="bg-white dark:bg-slate-800 p-4 rounded-xl border border-slate-100 dark:border-slate-700 shadow-sm">
          <h3 className="text-sm font-bold text-slate-400 uppercase tracking-wider mb-3">Состав заказа</h3>
          <div className="divide-y divide-slate-100 dark:divide-slate-700">
            {items.map((item) => (
              <div key={item.id} className="py-2.5 flex justify-between text-sm text-slate-800 dark:text-slate-200">
                <div>
                  <span className="font-semibold">Товар #{item.product_id}</span>
                  <span className="text-xs text-slate-400 block">{item.price_at_purchase.toLocaleString('ru-RU')} сум / шт</span>
                </div>
                <span className="font-bold text-slate-900 dark:text-white">x{item.quantity}</span>
              </div>
            ))}
          </div>
          <div className="pt-3 border-t border-slate-100 dark:border-slate-700 mt-2 flex justify-between font-black text-slate-900 dark:text-white">
            <span>ИТОГО К ОПЛАТЕ:</span>
            <span>{formattedTotalPrice}</span>
          </div>
        </div>
      </div>

      {/* Экшен-кнопки (Фиксированный подвал с безопасной зоной смартфона) */}
      <div className="p-4 bg-white dark:bg-slate-850 border-t border-slate-200 dark:border-slate-700 sticky bottom-0">
        {isFreeOrder && (
          <button
            onClick={handleClaimOrder}
            disabled={actionLoading}
            className="w-full bg-blue-600 text-white font-bold py-3.5 rounded-xl shadow-lg shadow-blue-500/20 active:scale-[0.98] transition-transform disabled:opacity-50"
          >
            {actionLoading ? 'Обработка...' : 'Взять заказ и начать доставку'}
          </button>
        )}

        {isAssignedToMe && order.status === 'accepted' && (
          <button
            onClick={() => handleUpdateStatus('delivering')}
            disabled={actionLoading}
            className="w-full bg-indigo-600 text-white font-bold py-3.5 rounded-xl shadow-lg shadow-indigo-500/20 active:scale-[0.98] transition-transform disabled:opacity-50"
          >
            {actionLoading ? 'Обработка...' : 'Начать доставку (В пути)'}
          </button>
        )}

        {isAssignedToMe && order.status === 'delivering' && (
          <button
            onClick={() => handleUpdateStatus('completed')}
            disabled={actionLoading}
            className="w-full bg-green-600 text-white font-bold py-3.5 rounded-xl shadow-lg shadow-green-500/20 active:scale-[0.98] transition-transform disabled:opacity-50"
          >
            {actionLoading ? 'Обработка...' : 'Завершить заказ (Доставлен)'}
          </button>
        )}

        {!isAssignedToMe && !isFreeOrder && (
          <div className="w-full bg-slate-100 dark:bg-slate-800 text-center text-sm text-slate-500 py-3 rounded-xl font-medium">
            Заказ закреплен за другим курьером
          </div>
        )}
      </div>
    </div>
  );
}