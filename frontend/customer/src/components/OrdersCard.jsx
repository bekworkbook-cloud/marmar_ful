import React from 'react';
import { ChevronRight, Package } from 'lucide-react';

export default function OrdersCard({ order, onClick, index = 0 }) {
  const statusLabels = {
    "pending": "В обработке",
    "accepted": "Принят",
    "delivering": "В пути",
    "completed": "Доставлен",
    "cancelled": "Отменен"
  };

  const statusText = statusLabels[order.status] || order.status;

  return (
    <button
      onClick={() => onClick(order)}
      // Матовый фон bg-card, скругление 2xl
      className="fade-up bg-card rounded-2xl p-4 text-left transition-all duration-200 active:scale-[0.97] w-full flex items-center justify-between gap-4"
      style={{ animationDelay: `${index * 0.05}s` }}
    >
      <div className="flex-1 min-w-0 flex flex-col gap-1.5">
        
        {/* Верхняя строка: Номер заказа (как в админке) и Статус */}
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Package className="w-4 h-4 text-txtDim" />
            <span className="text-lg font-black text-brand tracking-tight">
              #{order.id}
            </span>
          </div>
          
          {/* Аккуратный бейдж статуса: тёмный фон, золотой текст */}
          <span className="text-[10px] font-bold px-2 py-1 bg-surface text-accent rounded-md uppercase tracking-wider">
            {statusText}
          </span>
        </div>
        
        {/* Цена: крупно и чётко */}
        <div className="text-lg font-bold text-txt tracking-tight mt-1">
          {order.total_price ? order.total_price.toLocaleString() : 0} <span className="text-sm font-normal text-txtDim">сум</span>
        </div>
        
        {/* Адрес: тусклый цвет, обрезание длинного текста */}
        <div className="text-txtDim text-sm leading-snug truncate">
          {order.address}
        </div>
        
      </div>

      {/* Кнопка-шеврон (фон bg-surface создает глубину) */}
      <div className="w-10 h-10 rounded-xl bg-surface flex items-center justify-center shrink-0">
        <ChevronRight className="w-5 h-5 text-accent" />
      </div>
    </button>
  );
}