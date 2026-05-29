import { useState, useEffect } from 'react';
import { AlertTriangle } from 'lucide-react';
import { apiClient } from '../api/client';
import BackButton from '../components/BackButton';
import OrdersCard from '../components/OrdersCard';

export default function OrdersPage({ onAuthError, onBack }) {
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchOrders = async () => {
      setLoading(true);
      try {
        const data = await apiClient('/orders/?limit=10&offset=0');
        setOrders(data.orders || []);
      } catch (err) {
        if (err.message === "unauthorized") {
          onAuthError(); 
        } else {
          setError(err.message);
        }
      } finally {
        setLoading(false);
      }
    };
    fetchOrders();
  }, [onAuthError]);

  const handleOrderClick = (order) => {
    localStorage.setItem("selected_order", JSON.stringify(order));
    localStorage.setItem("currentOrderId", order.id);
    // Берем order.id, так как order.name не существует
    alert(`Вы выбрали заказ #${order.id}. Тут будет переход в детали заказа.`);
  };

  return (
    <div className="flex-1 flex flex-col pb-24 bg-surface text-txt min-h-screen">
      <header className="sticky top-0 z-20 bg-surface/95 backdrop-blur border-b border-slate-800 pt-[calc(env(safe-area-inset-top)+16px)]">
        {/* Используем твой готовый компонент */}
        <BackButton onClick={onBack} title="История заказов" />
      </header>

      <main className="px-5 py-5 flex flex-col gap-4">
        {loading && <div className="text-center text-slate-400 animate-pulse mt-10">Загрузка истории заказов...</div>}
        
        {error && (
          <div className="bg-red-900/30 border border-red-800 rounded-2xl p-4 text-red-300 flex items-center gap-3">
            <AlertTriangle className="w-6 h-6 shrink-0 text-red-500" />
            <p className="text-sm font-mono">{error}</p>
          </div>
        )}

        {/* Если загрузка прошла успешно, но список пуст */}
        {!loading && !error && orders.length === 0 && (
          <div className="text-center text-slate-500 mt-10">У вас пока нет заказов.</div>
        )}

        {/* Выводим карточки вертикальным списком */}
        {!loading && !error && orders.map((order, index) => (
          <OrdersCard 
            key={order.id} 
            order={order} 
            index={index} 
            onClick={handleOrderClick} 
          />
        ))}
      </main>
    </div>
  );
}