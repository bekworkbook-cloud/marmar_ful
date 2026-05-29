// src/components/StatusBadge.jsx
import React from 'react';

export default function StatusBadge({ status }) {
  const config = {
    pending: { text: 'Ожидает', bg: 'bg-yellow-100 text-yellow-800 border-yellow-200' },
    accepted: { text: 'Принят', bg: 'bg-blue-100 text-blue-800 border-blue-200' },
    delivering: { text: 'В пути', bg: 'bg-indigo-100 text-indigo-800 border-indigo-200' },
    completed: { text: 'Доставлен', bg: 'bg-green-100 text-green-800 border-green-200' },
    cancelled: { text: 'Отменен', bg: 'bg-red-100 text-red-800 border-red-200' },
  };

  const current = config[status] || { text: status, bg: 'bg-gray-100 text-gray-800 border-gray-200' };

  return (
    <span className={`text-xs font-semibold px-2.5 py-1 rounded-full border ${current.bg}`}>
      {current.text}
    </span>
  );
}