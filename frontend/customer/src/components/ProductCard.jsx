import React from 'react';
import { Plus, Minus, Image as ImageIcon } from 'lucide-react';
import { useCartStore } from '../store/cart';

export default function ProductCard({ product, onProductClick }) {
  // ОПТИМИЗАЦИЯ: Подписываемся только на количество конкретного товара
  const quantity = useCartStore(state =>
    state.items.find(item => item.id === product.id)?.quantity || 0
  );
  
  const addItem = useCartStore(state => state.addItem);
  const removeItem = useCartStore(state => state.removeItem);

  const handleAdd = (e) => {
    e.stopPropagation();
    window.Telegram?.WebApp?.HapticFeedback.impactOccurred('light');
    addItem(product);
  };

  const handleRemove = (e) => {
    e.stopPropagation();
    window.Telegram?.WebApp?.HapticFeedback.impactOccurred('light');
    removeItem(product.id);
  };

  return (
    <div 
      onClick={() => onProductClick(product)}
      // Плотный фон bg-card (без прозрачности), убраны лишние рамки
      className="bg-card rounded-2xl p-3 flex flex-col gap-2.5 relative overflow-hidden active:scale-[0.98] transition-all duration-200 group cursor-pointer shadow-sm"
    >
      {/* ИСПРАВЛЕНИЕ КАРТИНКИ: 
        Убрали aspect-square. Теперь фиксированная высота h-28.
        Цвет фона заглушки — bg-surface (максимально тёмный).
      */}
      <div className="w-full h-28 bg-surface rounded-xl overflow-hidden flex flex-col items-center justify-center text-txtDim gap-1 relative shrink-0">
        {product.image_url ? (
          // object-cover аккуратно заполнит прямоугольник без искажений.
          // Если хочешь, чтобы картинка вообще не обрезалась, замени object-cover на object-contain.
          <img 
            src={product.image_url} 
            alt={product.name} 
            className="w-full h-full object-cover object-center group-hover:scale-105 transition-transform duration-300" 
          />
        ) : (
          <>
            <ImageIcon className="w-6 h-6 text-txtDim/50" />
            <span className="text-[10px] font-medium text-txtDim uppercase tracking-wider px-2 text-center line-clamp-1">
              {product.name}
            </span>
          </>
        )}
      </div>

      {/* Инфо */}
      <div className="flex flex-col gap-1 pr-1 flex-1">
        {/* Белый плотный текст заголовка */}
        <div className="font-bold text-sm text-txt leading-snug line-clamp-2 min-h-[38px]">
          {product.name}
        </div>
        <div className="font-extrabold text-accent text-base mt-auto">
          {product.price.toLocaleString()} <span className="text-[11px] font-medium text-txtDim">сум</span>
        </div>
      </div>

      {/* Кнопки управления корзиной */}
      <div className="absolute bottom-2.5 right-2.5 h-9 flex items-center justify-end z-10">
        {quantity === 0 ? (
          // Полностью золотая кнопка
          <button 
            onClick={handleAdd}
            className="w-9 h-9 rounded-xl bg-accent text-surface flex items-center justify-center active:scale-90 transition-all shadow-md"
          >
            <Plus className="w-5 h-5 stroke-[3]" />
          </button>
        ) : (
          // Контрол со счетчиком: вдавленный фон bg-surface
          <div className="flex items-center bg-surface border border-slate-800 rounded-xl h-9 overflow-hidden shadow-sm animate-scaleIn">
            <button 
              onClick={handleRemove}
              className="w-8 h-full flex items-center justify-center text-txtDim active:text-txt active:bg-slate-800 transition-colors"
            >
              <Minus className="w-4 h-4 stroke-[2.5]" />
            </button>
            <span className="w-6 text-center text-xs font-black text-txt">
              {quantity}
            </span>
            <button 
              onClick={handleAdd}
              className="w-8 h-full flex items-center justify-center text-txtDim active:text-txt active:bg-slate-800 transition-colors"
            >
              <Plus className="w-4 h-4 stroke-[2.5]" />
            </button>
          </div>
        )}
      </div>
    </div>
  );
}