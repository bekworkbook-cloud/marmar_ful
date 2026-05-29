import React from 'react';
import { ChevronRight } from 'lucide-react';

export default function BranchesCard({ branch, onClick, index = 0 }) {
  return (
    <button
      onClick={() => onClick(branch)}
      // Матовый фон bg-card, скругление 2xl для консистентности с панелью
      className="fade-up bg-card rounded-2xl p-5 text-left transition-all duration-200 active:scale-[0.97] w-full flex items-center justify-between gap-4"
      style={{ animationDelay: `${index * 0.05}s` }}
    >
      <div className="flex-1 min-w-0">
        {/* Жирный белый заголовок */}
        <div className="text-xl font-bold text-txt tracking-tight truncate">
          {branch.name}
        </div>
        {/* Тусклый текст для адреса */}
        <div className="text-txtDim text-sm mt-1.5 leading-relaxed truncate">
          {branch.address}
        </div>
      </div>
      
      {/* Кнопка-шеврон: фон bg-surface (самый тёмный) создает эффект "выреза" в карточке */}
      <div className="w-12 h-12 rounded-xl bg-surface flex items-center justify-center shrink-0">
        <ChevronRight className="w-6 h-6 text-accent" />
      </div>
    </button>
  );
}