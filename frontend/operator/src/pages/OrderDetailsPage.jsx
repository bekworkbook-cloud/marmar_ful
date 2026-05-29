// src/pages/OrderDetailsPage.jsx
import { useState, useEffect } from 'react';
import { ArrowLeft, Loader2, ShoppingBag, MapPin, Truck, Check, AlertCircle, DollarSign } from 'lucide-react';
import { apiClient } from '../api/client';
import StatusBadge from '../components/StatusBadge';
import LeafletMap from '../components/LeafletMap'; // Напишем на следующем шаге

export default function OrderDetailsPage({ orderId, onAuthError, onBack }) {
  const [order, setOrder] = useState(null);
  const [items, setItems] = useState([]);
  const [couriers, setCouriers] = useState([]);
  
  const [isLoading, setIsLoading] = useState(true);
  const [isActionLoading, setIsActionLoading] = useState(false);
  const [error, setError] = useState(null);
  
  const [selectedCourierId, setSelectedCourierId] = useState('');

  // Загрузка всех данных по заказу
  const loadOrderData = async () => {
    setIsLoading(true);
    setError(null);
    try {
      // Параллельные запросы к API
      const [orderData, itemsData] = await Promise.all([
        apiClient(`/orders/${orderId}`),
        apiClient(`/orders/${orderId}/items?limit=100&offset=0`)
      ]);

      setOrder(orderData);
      setItems(itemsData.order_items || []);

      // После получения заказа запрашиваем курьеров для конкретного филиала
      if (orderData.branch_id) {
        try {
          // GET запрос с query-параметрами role и branch_id
          const couriersData = await apiClient(
            `/users/?role=courier&branch_id=${orderData.branch_id}`
          );
          
          // Безопасно сохраняем массив курьеров
          setCouriers(couriersData.users || couriersData || []);
        } catch (cErr) {
          console.error("Не удалось загрузить список курьеров:", cErr);
        }
      }

      if (orderData.courier_id) {
        setSelectedCourierId(orderData.courier_id.toString());
      }

    } catch (err) {
      console.error(err);
      if (err.message === 'unauthorized') {
        onAuthError();
      } else {
        setError('Ошибка при загрузке данных заказа');
      }
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    if (orderId) loadOrderData();
  }, [orderId]);

  // Изменение статуса через PATCH /orders/{id}/status
  const handleUpdateStatus = async (newStatus) => {
    setIsActionLoading(true);
    try {
      const updatedOrder = await apiClient(`/orders/${orderId}/status`, {
        method: 'PATCH',
        body: JSON.stringify({ status: newStatus })
      });
      setOrder(updatedOrder);
    } catch (err) {
      alert('Не удалось изменить статус заказа');
    } finally {
      setIsActionLoading(false);
    }
  };

  // Принятие заказа через PATCH /orders/{id}/accept
  const handleAcceptOrder = async () => {
    setIsActionLoading(true);
    try {
      const updatedOrder = await apiClient(`/orders/${orderId}/accept`, {
        method: 'PATCH',
        body: JSON.stringify({ is_accepted: true })
      });
      setOrder(updatedOrder);
    } catch (err) {
      alert('Не удалось принять заказ');
    } finally {
      setIsActionLoading(false);
    }
  };

  // Назначение курьера через PATCH /orders/{id}/courier?order_personnel_dto={id}
  const handleAssignCourier = async (e) => {
    const courierId = e.target.value;
    setSelectedCourierId(courierId);
    if (!courierId) return;

    setIsActionLoading(true);
    try {
      const updatedOrder = await apiClient(`/orders/${orderId}/courier?order_personnel_dto=${parseInt(courierId)}`, {
        method: 'PATCH'
      });
      setOrder(updatedOrder);
      alert('Курьер успешно назначен');
    } catch (err) {
      alert('Ошибка при назначении курьера');
    } finally {
      setIsActionLoading(false);
    }
  };

  if (isLoading) {
    return (
      <div className="flex-1 flex flex-col items-center justify-center bg-slate-950 text-slate-400">
        <Loader2 className="w-8 h-8 animate-spin text-amber-500 mb-2" />
        <p className="text-xs">Загрузка информации о заказе...</p>
      </div>
    );
  }

  if (error || !order) {
    return (
      <div className="flex-1 p-4 flex flex-col items-center justify-center bg-slate-950 text-center">
        <AlertCircle className="w-12 h-12 text-rose-500 mb-2" />
        <p className="text-sm text-slate-300 font-medium">{error || 'Заказ не найден'}</p>
        <button onClick={onBack} className="mt-4 px-4 py-2 bg-slate-900 border border-slate-800 rounded-xl text-xs">
          Вернуться назад
        </button>
      </div>
    );
  }

  return (
    <div className="flex-1 flex flex-col w-full bg-slate-950 pb-8" style={{ paddingTop: 'calc(env(safe-area-inset-top) + 0.5rem)' }}>
      
      {/* Верхний Навбар */}
      <div className="px-4 py-2 flex items-center gap-3 border-b border-slate-900 mb-4">
        <button onClick={onBack} className="p-2 bg-slate-900 border border-slate-800 rounded-xl text-slate-400 active:scale-95 transition">
          <ArrowLeft className="w-4 h-4" />
        </button>
        <div>
          <h2 className="text-base font-bold text-slate-200">Заказ #{order.id}</h2>
          <div className="flex items-center gap-2 mt-0.5">
            <span className="text-[11px] font-semibold text-slate-500">Статус:</span>
            <StatusBadge status={order.status} isAccepted={order.is_accepted} />
          </div>
        </div>
      </div>

      <div className="flex-1 px-4 space-y-4 overflow-y-auto no-scrollbar">
        
        {/* Блок действий оператора (Workflow управления) */}
        <div className="bg-slate-900 border border-slate-800/80 rounded-2xl p-4 space-y-3">
          <h3 className="text-xs font-bold text-slate-400 uppercase tracking-wider mb-1">Управление заказом</h3>
          
          {isActionLoading && (
            <div className="flex items-center gap-2 text-xs text-amber-500 py-1 font-medium">
              <Loader2 className="w-3.5 h-3.5 animate-spin" /> Обновление на сервере...
            </div>
          )}

          <div className="grid grid-cols-2 gap-2">
            {/* Кнопка принятия заказа */}
            {!order.is_accepted && order.status === 'pending' && (
              <button
                onClick={handleAcceptOrder}
                disabled={isActionLoading}
                className="col-span-2 py-3 bg-emerald-600 hover:bg-emerald-500 active:scale-98 transition text-slate-950 font-bold text-xs rounded-xl flex items-center justify-center gap-1.5"
              >
                <Check className="w-4 h-4 stroke-[3]" /> Принять в работу
              </button>
            )}

            {/* Логика цепочки статусов */}
            {order.is_accepted && order.status === 'pending' && (
              <button
                onClick={() => handleUpdateStatus('accepted')}
                disabled={isActionLoading}
                className="col-span-2 py-3 bg-indigo-600 text-slate-100 font-bold text-xs rounded-xl transition active:scale-98"
              >
                Начать приготовление
              </button>
            )}

            {order.status === 'accepted' && (
              <button
                onClick={() => handleUpdateStatus('delivering')}
                disabled={isActionLoading}
                className="col-span-2 py-3 bg-purple-600 text-slate-100 font-bold text-xs rounded-xl transition active:scale-98 flex items-center justify-center gap-1"
              >
                <Truck className="w-4 h-4" /> Передать курьеру (В путь)
              </button>
            )}

            {order.status === 'delivering' && (
              <button
                onClick={() => handleUpdateStatus('completed')}
                disabled={isActionLoading}
                className="col-span-2 py-3 bg-emerald-600 text-slate-950 font-bold text-xs rounded-xl transition active:scale-98"
              >
                Завершить заказ (Доставлен)
              </button>
            )}

            {/* Кнопка отмены доступна почти всегда, кроме завершенных */}
            {order.status !== 'completed' && order.status !== 'cancelled' && (
              <button
                onClick={() => {
                  if(confirm('Отменить этот заказ?')) handleUpdateStatus('cancelled');
                }}
                disabled={isActionLoading}
                className="col-span-2 py-2.5 bg-slate-950 border border-rose-950 text-rose-400 font-medium text-xs rounded-xl hover:bg-rose-950/10 transition"
              >
                Отменить заказ
              </button>
            )}
          </div>

          {/* Назначение Курьера (Выпадающий список) */}
          {order.status !== 'completed' && order.status !== 'cancelled' && (
            <div className="pt-2 border-t border-slate-800/60">
              <label className="block text-[11px] font-bold text-slate-500 uppercase tracking-wider mb-1.5">
                Назначить курьера филиала
              </label>
              <select
                value={selectedCourierId}
                onChange={handleAssignCourier}
                disabled={isActionLoading}
                className="w-full px-3 py-2.5 bg-slate-950 border border-slate-800 rounded-xl text-xs text-slate-200 font-medium focus:outline-none focus:border-amber-500/50 appearance-none"
              >
                <option value="">-- Выберите курьера --</option>
                {couriers.map((c) => (
                  <option key={c.id} value={c.id}>
                    {c.name || `Курьер ID: ${c.id}`}
                  </option>
                ))}
              </select>
            </div>
          )}
        </div>

        {/* Состав заказа (Продукты) */}
        <div className="bg-slate-900 border border-slate-800/80 rounded-2xl p-4 space-y-3">
          <h3 className="text-xs font-bold text-slate-400 uppercase tracking-wider flex items-center gap-1.5">
            <ShoppingBag className="w-4 h-4 text-slate-500" /> Состав покупки
          </h3>
          <div className="divide-y divide-slate-800/60">
            {items.map((item) => (
              <div key={item.id} className="py-2.5 flex items-center justify-between text-xs first:pt-0 last:pb-0">
                <div className="pr-2">
                  <p className="font-semibold text-slate-200">Продукт #{item.product_id}</p>
                  <p className="text-[11px] text-slate-500 mt-0.5">
                    Цена за ед.: {item.price_at_purchase.toLocaleString('ru-RU')} сум
                  </p>
                </div>
                <div className="text-right shrink-0">
                  <span className="px-2 py-0.5 bg-slate-950 border border-slate-800 rounded-md font-bold text-slate-300">
                    {item.quantity} шт
                  </span>
                  <p className="font-bold text-slate-400 mt-1.5">
                    {(item.price_at_purchase * item.quantity).toLocaleString('ru-RU')} сум
                  </p>
                </div>
              </div>
            ))}
          </div>

          <div className="pt-3 border-t border-slate-800 flex items-center justify-between font-bold text-sm text-amber-400">
            <span>Итого к оплате:</span>
            <span>{order.total_price.toLocaleString('ru-RU')} сум</span>
          </div>
        </div>

        {/* Адрес и Карта доставки */}
        <div className="bg-slate-900 border border-slate-800/80 rounded-2xl p-4 space-y-3">
          <h3 className="text-xs font-bold text-slate-400 uppercase tracking-wider flex items-center gap-1.5">
            <MapPin className="w-4 h-4 text-slate-500" /> Геолокация и адрес
          </h3>
          <div className="text-xs space-y-1 bg-slate-950 p-3 rounded-xl border border-slate-850">
            <p className="text-slate-300 font-medium">{order.address}</p>
            {order.landmark && (
              <p className="text-[11px] text-slate-500">
                <span className="text-slate-600 font-semibold">Ориентир:</span> {order.landmark}
              </p>
            )}
            <p className="text-[11px] text-slate-500">
              <span className="text-slate-600 font-semibold">Оплата:</span> {order.payment_method?.toUpperCase()}
            </p>
          </div>

          {/* Интеграция LeafletMap для оператора */}
          {order.latitude !== 0 && order.longitude !== 0 ? (
            <div className="h-44 w-full rounded-xl overflow-hidden border border-slate-800">
              <LeafletMap 
                latitude={order.latitude} 
                longitude={order.longitude} 
              />
            </div>
          ) : (
            <p className="text-[11px] text-slate-600 text-center py-2">Координаты на карте не указаны пользователем</p>
          )}
        </div>

      </div>
    </div>
  );
}