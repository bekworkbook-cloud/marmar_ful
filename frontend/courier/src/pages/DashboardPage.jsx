// src/pages/DashboardPage.jsx
import React, { useState, useEffect } from 'react';
import { apiClient } from '../api/client';
import { useAuthStore } from '../store/auth';
import CourierOrderCard from '../components/CourierOrderCard';

export default function DashboardPage({ onOrderSelect }) {
  const myCourierId = useAuthStore((s) => s.courierId);
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('mine'); // 'mine' | 'available'

  const fetchOrders = async () => {
    setLoading(true);
    try {
      const data = await apiClient('/orders/?limit=50&offset=0');
      const list = Array.isArray(data) ? data : (data.orders || []);
      setOrders(list);
    } catch (error) {
      alert('Ошибка при загрузке заказов: ' + error.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchOrders();
  }, []);

  // String() с обеих сторон — courier_id число, myCourierId строка из JWT sub
  const myActiveOrders = orders.filter(
    (o) => String(o.courier_id) === String(myCourierId) && o.status === 'delivering'
  );

  const availableOrders = orders.filter(
    (o) => o.courier_id === null && ['accepted', 'pending'].includes(o.status)
  );

  const displayedOrders = activeTab === 'mine' ? myActiveOrders : availableOrders;

  return (
    <div className="flex flex-col min-h-screen bg-slate-50 dark:bg-slate-900 px-4 pt-4 pb-[env(safe-area-inset-bottom,16px)]">
      {/* Шапка и кнопка синхронизации */}
      <div className="flex justify-between items-center mb-4 pt-[env(safe-area-inset-top,16px)]">
        <h1 className="text-xl font-black text-slate-900 dark:text-white tracking-tight">Панель Курьера</h1>
        <button
          onClick={fetchOrders}
          disabled={loading}
          className="p-2 bg-white dark:bg-slate-850 border border-slate-200 dark:border-slate-700 rounded-lg text-slate-700 dark:text-slate-200 active:opacity-50 disabled:opacity-40"
        >
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor" className={`w-5 h-5 ${loading ? 'animate-spin' : ''}`}>
            <path strokeLinecap="round" strokeLinejoin="round" d="M16.023 9.348h4.992v-.001M2.985 19.644v-4.992m0 0h4.992m-4.993 0l3.181 3.183a8.25 8.25 0 0013.803-3.7M4.031 9.865a8.25 8.25 0 0113.803-3.7l3.181 3.182m0-4.991v4.99" />
          </svg>
        </button>
      </div>

      {/* Переключатель табов */}
      <div className="grid grid-cols-2 p-1 bg-slate-200 dark:bg-slate-800 rounded-xl mb-4 text-sm font-medium">
        <button
          onClick={() => setActiveTab('mine')}
          className={`py-2 text-center rounded-lg transition-all ${activeTab === 'mine' ? 'bg-white dark:bg-slate-700 text-slate-900 dark:text-white shadow-sm' : 'text-slate-500 dark:text-slate-400'}`}
        >
          Мои в пути ({myActiveOrders.length})
        </button>
        <button
          onClick={() => setActiveTab('available')}
          className={`py-2 text-center rounded-lg transition-all ${activeTab === 'available' ? 'bg-white dark:bg-slate-700 text-slate-900 dark:text-white shadow-sm' : 'text-slate-500 dark:text-slate-400'}`}
        >
          Свободные ({availableOrders.length})
        </button>
      </div>

      {/* Списки заказов */}
      {loading ? (
        <div className="flex-1 flex items-center justify-center text-slate-400 text-sm">Загрузка данных...</div>
      ) : displayedOrders.length === 0 ? (
        <div className="flex-1 flex flex-col items-center justify-center text-slate-400 text-sm border-2 border-dashed border-slate-200 dark:border-slate-800 rounded-2xl p-8">
          <span>Нет доступных заказов в этой категории</span>
        </div>
      ) : (
        <div className="space-y-3 flex-1 overflow-y-auto">
          {displayedOrders.map((order) => (
            <CourierOrderCard
              key={order.id}
              order={order}
              onClick={() => onOrderSelect(order.id)}
            />
          ))}
        </div>
      )}
    </div>
  );
}