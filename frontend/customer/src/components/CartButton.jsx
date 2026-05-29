import React from 'react';
import { ShoppingBag } from 'lucide-react';
import { useCartStore } from '../store/cart';

export default function CartButton({ currentView, onClick }) {
  const totalCount = useCartStore((state) => state.getTotalCount());
  const totalPrice = useCartStore((state) => state.getTotalPrice());

  if (totalCount === 0 || currentView === 'cart') {
    return null;
  }

  return (
    <div className="fixed bottom-[calc(env(safe-area-inset-bottom)+16px)] left-4 right-4 z-50 fade-up">
      <button 
        onClick={() => {
          window.Telegram?.WebApp?.HapticFeedback.impactOccurred('medium');
          onClick();
        }}
        // Плотный золотой фон (bg-accent), тёмный текст (text-surface) для максимального контраста
        className="w-full bg-accent text-surface font-bold h-14 rounded-2xl shadow-md flex items-center justify-between px-5 active:scale-[0.97] transition-all duration-200"
      >
        <div className="flex items-center gap-3">
          {/* Иконка в слегка затемненном квадрате для выделения на золотом фоне */}
          <div className="relative w-9 h-9 flex items-center justify-center bg-black/15 rounded-xl">
            <ShoppingBag className="w-5 h-5 stroke-[2.5]" />
            
            {/* Счётчик: фон цвета приложения (bg-surface) и золотая цифра */}
            <span className="absolute -top-1.5 -right-1.5 bg-surface text-accent text-[11px] font-black w-5 h-5 flex items-center justify-center rounded-full border-2 border-accent">
              {totalCount}
            </span>
          </div>
          
          <span className="text-lg tracking-tight font-extrabold">Корзина</span>
        </div>
        
        {/* Цена в аккуратной затемнённой плашке */}
        <div className="text-base font-extrabold bg-black/15 px-3 py-1.5 rounded-xl tracking-tight">
          {totalPrice.toLocaleString()} сум
        </div>
      </button>
    </div>
  );
}