// src/components/OrderCard.jsx
import { ChevronRight, CreditCard, Wallet, MapPin } from 'lucide-react';
import StatusBadge from './StatusBadge';

export default function OrderCard({ order, onClick }) {
  const { id, total_price, payment_method, address, landmark, status, is_accepted } = order;

  // Форматирование цены: 125000 -> "125 000 сум"
  const formatPrice = (price) => {
    return price.toLocaleString('ru-RU') + ' сум';
  };

  // Метод оплаты
  const renderPaymentMethod = () => {
    if (payment_method === 'cash') {
      return (
        <span className="flex items-center gap-1 text-slate-400">
          <Wallet className="w-3.5 h-3.5 text-emerald-500" /> Наличные
        </span>
      );
    }
    return (
      <span className="flex items-center gap-1 text-slate-400">
        <CreditCard className="w-3.5 h-3.5 text-blue-400" /> {payment_method?.toUpperCase()}
      </span>
    );
  };

  return (
    <div 
      onClick={onClick}
      className="w-full bg-slate-900 border border-slate-800/80 rounded-2xl p-4 flex items-center justify-between gap-3 active:bg-slate-850 active:border-slate-700/60 transition shadow-sm"
    >
      {/* Левая содержательная часть */}
      <div className="flex-1 min-w-0 space-y-2.5">
        
        {/* Строка заголовка: ID и Статус */}
        <div className="flex items-center justify-between gap-2">
          <span className="text-sm font-bold text-slate-200">
            Заказ #{id}
          </span>
          <StatusBadge status={status} isAccepted={is_accepted} />
        </div>

        {/* Инфо-строка: Сумма и Оплата */}
        <div className="flex items-center gap-4 text-xs font-medium">
          <span className="text-amber-400 font-bold">
            {formatPrice(total_price)}
          </span>
          {renderPaymentMethod()}
        </div>

        {/* Нижняя строка: Адрес доставки */}
        <div className="flex items-start gap-1.5 text-slate-400 text-xs">
          <MapPin className="w-3.5 h-3.5 text-slate-500 shrink-0 mt-0.5" />
          <div className="truncate">
            <span className="text-slate-300">{address}</span>
            {landmark && (
              <span className="text-slate-500 text-[11px] block truncate mt-0.5">
                Ориентир: {landmark}
              </span>
            )}
          </div>
        </div>

      </div>

      {/* Правая навигационная стрелка */}
      <div className="shrink-0 p-1 bg-slate-950 rounded-xl border border-slate-850 text-slate-500">
        <ChevronRight className="w-4 h-4" />
      </div>

    </div>
  );
}