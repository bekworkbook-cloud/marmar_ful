import { Plus, Minus } from 'lucide-react';
import { useCartStore } from '../store/cart';

export default function ProductPage({ product, onBack }) {
  const items = useCartStore(state => state.items);
  const addItem = useCartStore(state => state.addItem);
  const removeItem = useCartStore(state => state.removeItem);

  const cartItem = items.find(item => item.id === product.id);
  const quantity = cartItem ? cartItem.quantity : 0;

  return (
    <div className="flex-1 flex flex-col h-full bg-surface pb-24">
      <header className="sticky top-0 z-20 bg-surface/95 backdrop-blur px-5 pt-[calc(env(safe-area-inset-top)+16px)] pb-4">
        <button onClick={onBack} className="text-accent font-medium">
          ← Вернуться в меню
        </button>
      </header>

      <div className="flex-1 px-5 overflow-y-auto">
        <div className="w-full aspect-square bg-slate-800 rounded-3xl mb-6 flex items-center justify-center text-slate-500">
          Большое фото {product.name}
        </div>
        
        <h1 className="text-3xl font-bold mb-2">{product.name}</h1>
        <p className="text-slate-400 mb-6 leading-relaxed">
          Вкусное описание товара. Сочный бифштекс, сыр чеддер, свежие овощи и фирменный соус на булочке с кунжутом.
        </p>
        
        <div className="text-2xl font-bold text-accent mb-8">
          {product.price.toLocaleString()} сум
        </div>

        {/* БОЛЬШАЯ КНОПКА ДОБАВЛЕНИЯ / УПРАВЛЕНИЯ */}
        {quantity === 0 ? (
          <button 
            onClick={() => addItem(product)}
            className="w-full bg-slate-800 text-white font-bold py-4 rounded-2xl active:scale-95 transition"
          >
            Добавить в корзину
          </button>
        ) : (
          <div className="flex items-center justify-between bg-slate-800 rounded-2xl p-2 h-16">
            <button 
              onClick={() => removeItem(product.id)}
              className="w-16 h-full bg-slate-700 rounded-xl flex items-center justify-center text-white active:bg-slate-600"
            >
              <Minus className="w-6 h-6" />
            </button>
            <span className="text-xl font-bold">{quantity}</span>
            <button 
              onClick={() => addItem(product)}
              className="w-16 h-full bg-slate-700 rounded-xl flex items-center justify-center text-white active:bg-slate-600"
            >
              <Plus className="w-6 h-6" />
            </button>
          </div>
        )}
      </div>
    </div>
  );
}