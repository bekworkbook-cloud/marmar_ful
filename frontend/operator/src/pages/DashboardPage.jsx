// src/pages/DashboardPage.jsx
import { useState, useEffect } from 'react';
import { RefreshCw, Loader2, ClipboardList } from 'lucide-react';
import { apiClient } from '../api/client';
import OrderCard from '../components/OrderCard';

export default function DashboardPage({ onAuthError, onOrderSelect }) {
  const [orders, setOrders] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
  
  // Вкладки фильтрации: 'all' | 'pending' | 'processing' | 'done'
  const [activeTab, setActiveTab] = useState('all');

  const fetchOrders = async () => {
    setIsLoading(true);
    setError(null);
    try {
      // Запрашиваем последние 50 заказов для оперативного мониторинга
      const data = await apiClient('/orders/?limit=50&offset=0');
      setOrders(data.orders || []);
    } catch (err) {
      console.error(err);
      if (err.message === 'unauthorized') {
        onAuthError();
      } else {
        setError('Не удалось загрузить список заказов');
      }
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchOrders();
  }, []);

  // Фильтрация заказов на клиенте по статусам из БД
  const filteredOrders = orders.filter(order => {
    if (activeTab === 'all') return true;
    if (activeTab === 'pending') return order.status === 'pending' || !order.is_accepted;
    if (activeTab === 'processing') return order.status === 'accepted' || order.status === 'delivering';
    if (activeTab === 'done') return order.status === 'completed' || order.status === 'cancelled';
    return true;
  });

  return (
    <div className="flex-1 flex flex-col w-full pb-6" style={{ paddingTop: 'calc(env(safe-area-inset-top) + 0.75rem)' }}>
      
      {/* Шапка Панели */}
      <div className="px-4 flex items-center justify-between mb-4">
        <div>
          <h1 className="text-xl font-bold text-slate-100 flex items-center gap-2">
            <ClipboardList className="w-5 h-5 text-amber-500" />
            Панель заказов
          </h1>
          <p className="text-xs text-slate-400 mt-0.5">Всего в базе: {orders.length}</p>
        </div>
        
        <button 
          onClick={fetchOrders}
          disabled={isLoading}
          className="p-2.5 bg-slate-900 border border-slate-800 rounded-xl active:scale-95 transition text-slate-300 disabled:opacity-50"
        >
          <RefreshCw className={`w-4 h-4 ${isLoading ? 'animate-spin text-amber-500' : ''}`} />
        </button>
      </div>

      {/* Горизонтальный Таб-фильтр */}
      <div className="px-4 mb-4 flex gap-2 overflow-x-auto no-scrollbar py-1">
        {[
          { id: 'all', label: 'Все' },
          { id: 'pending', label: 'Новые' },
          { id: 'processing', label: 'В работе' },
          { id: 'done', label: 'Архив' }
        ].map(tab => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id)}
            className={`px-4 py-2 rounded-xl text-xs font-semibold whitespace-nowrap transition border ${
              activeTab === tab.id 
                ? 'bg-amber-500 text-slate-950 border-amber-500 shadow-lg shadow-amber-500/10' 
                : 'bg-slate-900 text-slate-400 border-slate-800/80 active:bg-slate-850'
            }`}
          >
            {tab.label}
          </button>
        ))}
      </div>

      {/* Основной контент */}
      <div className="flex-1 px-4 flex flex-col">
        {isLoading && orders.length === 0 ? (
          <div className="flex-1 flex flex-col items-center justify-center py-20 text-slate-500">
            <Loader2 className="w-8 h-8 animate-spin text-amber-500 mb-2" />
            <p className="text-xs">Загрузка актуальных заказов...</p>
          </div>
        ) : error ? (
          <div className="bg-red-950/20 border border-red-900/50 rounded-2xl p-4 text-center text-xs text-red-400">
            {error}
          </div>
        ) : filteredOrders.length === 0 ? (
          <div className="flex-1 flex flex-col items-center justify-center py-16 text-slate-500 border border-dashed border-slate-900 rounded-2xl bg-slate-900/10">
            <p className="text-sm font-medium">Нет заказов в этой вкладке</p>
            <p className="text-xs text-slate-600 mt-1">Нажмите кнопку обновить выше</p>
          </div>
        ) : (
          <div className="space-y-3">
            {filteredOrders.map(order => (
              <OrderCard 
                key={order.id} 
                order={order} 
                onClick={() => onOrderSelect(order.id)} 
              />
            ))}
          </div>
        )}
      </div>
    </div>
  );
}