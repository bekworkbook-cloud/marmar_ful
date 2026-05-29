import React from 'react';
import { ChevronRight, MapPin } from 'lucide-react';

export default function BranchCard({ branch, onClick, index = 0 }) {
  return (
    <button
      onClick={() => onClick(branch)}
      // Матовый плотный фон bg-card без лишних рамок
      className="fade-up bg-card rounded-2xl p-4 text-left transition-all duration-200 active:scale-[0.97] w-full flex items-center justify-between gap-4"
      style={{ animationDelay: `${index * 0.05}s` }}
    >
      <div className="flex-1 min-w-0">
        {/* Главный заголовок: плотный белый text-txt */}
        <div className="text-lg font-bold text-txt tracking-tight truncate">
          {branch.name}
        </div>
        {/* Адрес: тусклый серый text-txtDim */}
        <div className="text-txtDim text-sm mt-1 flex items-center gap-1.5">
          <MapPin className="w-4 h-4 shrink-0 opacity-80" />
          <span className="truncate">{branch.address}</span>
        </div>
      </div>
      
      {/* Кнопка-шеврон: фон в цвет самого глубокого фона приложения (bg-surface) и золотая иконка */}
      <div className="w-10 h-10 rounded-xl bg-surface flex items-center justify-center shrink-0">
        <ChevronRight className="w-5 h-5 text-accent" />
      </div>
    </button>
  );
}