// src/components/CourierOrderCard.jsx
import React from 'react';
import StatusBadge from './StatusBadge';

export default function CourierOrderCard({ order, onClick }) {
  const formattedPrice = order.total_price.toLocaleString('ru-RU') + ' сум';

  return (
    <div 
      onClick={onClick}
      className="bg-white dark:bg-slate-800 p-4 rounded-xl border border-slate-100 dark:border-slate-700 shadow-sm active:scale-[0.99] active:bg-slate-50 dark:active:bg-slate-750 transition-all cursor-pointer flex flex-col justify-between space-y-3"
    >
      <div className="flex justify-between items-start">
        <div>
          <span className="text-xs font-bold text-slate-400 block mb-1">ЗАКАЗ</span>
          <h3 className="text-base font-bold text-slate-800 dark:text-slate-100">#{order.id}</h3>
        </div>
        <StatusBadge status={order.status} />
      </div>

      <div className="space-y-1.5 text-sm text-slate-600 dark:text-slate-300">
        <p className="line-clamp-2">
          <span className="font-medium text-slate-900 dark:text-white">Адрес:</span> {order.address}
        </p>
        {order.landmark && (
          <p className="text-xs text-slate-500 italic">
            <span className="font-medium not-italic text-slate-700 dark:text-slate-400">Ориентир:</span> {order.landmark}
          </p>
        )}
      </div>

      <div className="pt-2 border-t border-slate-100 dark:border-slate-700 flex justify-between items-center text-sm">
        <span className="text-slate-500">{order.payment_method.toUpperCase()}</span>
        <span className="font-bold text-slate-900 dark:text-white text-base">{formattedPrice}</span>
      </div>
    </div>
  );
}