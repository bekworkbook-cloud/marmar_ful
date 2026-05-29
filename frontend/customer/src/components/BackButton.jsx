import React, { useEffect } from 'react';
import { ChevronLeft } from 'lucide-react'; // Добавляем красивую иконку

export default function BackButton({ onClick, title }) {
  useEffect(() => {
    // Проверяем, запущено ли приложение внутри Telegram
    const tgButton = window.Telegram?.WebApp?.BackButton;

    if (tgButton) {
      // Показываем нативную кнопку при монтировании компонента
      tgButton.show();
      // Навешиваем твой обработчик клика
      tgButton.onClick(onClick);
    }

    // Чистим за собой, когда пользователь уходит со страницы
    return () => {
      if (tgButton) {
        tgButton.hide();
        tgButton.offClick(onClick);
      }
    };
  }, [onClick]);

  return (
    // Добавили отступы, выравнивание и легкую анимацию
    <div className="px-5 py-4 flex items-center gap-2 fade-up">
      {/* Фолбэк-кнопка для обычного браузера. 
        Используем тусклый цвет (txtDim), который при клике реагирует.
      */}
      <div className="tg-hidden:hidden block md:block">
        <button 
          onClick={onClick} 
          className="flex items-center justify-center p-1 -ml-2 text-txtDim active:text-txt active:scale-90 transition-all"
        >
          <ChevronLeft className="w-7 h-7" />
        </button>
      </div>
      
      {/* Заголовок в стиле Mar Mar: крупный, жирный, белый */}
      <h1 className="text-2xl font-extrabold text-txt tracking-tight">
        {title}
      </h1>
    </div>
  );
}