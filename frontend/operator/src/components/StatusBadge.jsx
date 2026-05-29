// src/components/StatusBadge.jsx
import { ShieldAlert, CheckCircle2, Clock, Truck, XCircle } from 'lucide-react';

export default function StatusBadge({ status, isAccepted }) {
  // Если заказ еще не принят оператором, принудительно подсвечиваем как "Новый"
  if (!isAccepted && status === 'pending') {
    return (
      <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded-lg text-[11px] font-bold bg-amber-550/10 border border-amber-500/30 text-amber-400 uppercase tracking-wider animate-pulse">
        <ShieldAlert className="w-3.5 h-3.5 text-amber-400" />
        Новый
      </span>
    );
  }

  switch (status) {
    case 'pending':
      return (
        <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded-lg text-[11px] font-bold bg-blue-500/10 border border-blue-500/20 text-blue-400 uppercase tracking-wider">
          <Clock className="w-3.5 h-3.5" />
          Ожидает
        </span>
      );
    case 'accepted':
      return (
        <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded-lg text-[11px] font-bold bg-indigo-500/10 border border-indigo-500/20 text-indigo-400 uppercase tracking-wider">
          <CheckCircle2 className="w-3.5 h-3.5" />
          Принят
        </span>
      );
    case 'delivering':
      return (
        <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded-lg text-[11px] font-bold bg-purple-500/10 border border-purple-500/20 text-purple-400 uppercase tracking-wider">
          <Truck className="w-3.5 h-3.5" />
          В пути
        </span>
      );
    case 'completed':
      return (
        <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded-lg text-[11px] font-bold bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 uppercase tracking-wider">
          <CheckCircle2 className="w-3.5 h-3.5" />
          Доставлен
        </span>
      );
    case 'cancelled':
      return (
        <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded-lg text-[11px] font-bold bg-rose-500/10 border border-rose-500/20 text-rose-400 uppercase tracking-wider">
          <XCircle className="w-3.5 h-3.5" />
          Отменен
        </span>
      );
    default:
      return (
        <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded-lg text-[11px] font-bold bg-slate-800 border border-slate-700 text-slate-400 uppercase tracking-wider">
          {status}
        </span>
      );
  }
}