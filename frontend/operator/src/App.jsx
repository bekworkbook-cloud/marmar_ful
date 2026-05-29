// src/App.jsx
import { useState, useEffect } from 'react';
import { AlertTriangle, Loader2 } from 'lucide-react';

import DashboardPage from './pages/DashboardPage';
import OrderDetailsPage from './pages/OrderDetailsPage';

const API_BASE = window.location.origin + "/api/v1";

export default function App() {
  const [isAuthLoading, setIsAuthLoading] = useState(true);
  const [authError, setAuthError] = useState(null);

  // Состояние навигации: 'dashboard' или 'details'
  const [currentView, setCurrentView] = useState('dashboard'); 
  const [selectedOrderId, setSelectedOrderId] = useState(null);

  const authenticate = async () => {
    setIsAuthLoading(true);
    setAuthError(null);
    try {
      if (window.Telegram && window.Telegram.WebApp) {
        window.Telegram.WebApp.ready();
        window.Telegram.WebApp.expand();
      }

      const existingToken = localStorage.getItem("jwt");
      if (existingToken && existingToken !== "null") {
        setIsAuthLoading(false);
        return;
      }

      const initData = window.Telegram?.WebApp?.initData;
      if (!initData) {
        throw new Error("Приложение открыто вне Telegram. Запустите через бота оператора.");
      }

      const authHeaders = new Headers();
      authHeaders.append('Content-Type', 'application/json');
      authHeaders.append('x-telegram-init-data', initData);
      authHeaders.append('ngrok-skip-browser-warning', 'true');

      // Используем роут инициализации (при необходимости заменим эндпоинт под оператора)
      const response = await fetch(`${API_BASE}/auth/init_data/customer_bot`, {
        method: 'POST',
        headers: authHeaders
      });

      if (!response.ok) throw new Error("Ошибка авторизации оператора на сервере");
      
      const data = await response.json();
      localStorage.setItem("jwt", data.access_token);
      setIsAuthLoading(false);

    } catch (err) {
      console.error(err);
      setAuthError(err.message);
      setIsAuthLoading(false);
    }
  };

  useEffect(() => {
    authenticate();
  }, []);

  if (isAuthLoading) {
    return (
      <div className="min-h-screen flex flex-col items-center justify-center bg-slate-950 text-slate-400">
        <Loader2 className="w-10 h-10 animate-spin text-amber-500 mb-4" />
        <p className="text-sm font-medium">Вход в панель оператора...</p>
      </div>
    );
  }

  if (authError) {
    return (
      <div className="min-h-screen flex flex-col items-center justify-center bg-slate-950 p-5 text-center">
        <div className="bg-red-950/40 border border-red-900 rounded-3xl p-6 text-red-200 mb-4 max-w-sm">
          <AlertTriangle className="w-12 h-12 text-red-500 mx-auto mb-3" />
          <p className="font-semibold text-base mb-1">Доступ ограничен</p>
          <p className="text-xs text-red-400/80">{authError}</p>
        </div>
        <button 
          onClick={authenticate} 
          className="px-6 py-3 bg-slate-900 border border-slate-800 rounded-xl text-slate-200 text-sm font-medium active:scale-95 transition"
        >
          Повторить попытку
        </button>
      </div>
    );
  }

  const renderCurrentView = () => {
    switch (currentView) {
      case 'dashboard':
        return (
          <DashboardPage 
            onAuthError={authenticate}
            onOrderSelect={(orderId) => {
              setSelectedOrderId(orderId);
              setCurrentView('details');
            }}
          />
        );
      case 'details':
        return (
          <OrderDetailsPage 
            orderId={selectedOrderId}
            onAuthError={authenticate}
            onBack={() => {
              setSelectedOrderId(null);
              setCurrentView('dashboard');
            }}
          />
        );
      default:
        return <DashboardPage onAuthError={authenticate} onOrderSelect={(id) => { setSelectedOrderId(id); setCurrentView('details'); }} />;
    }
  };

  return (
    <div className="min-h-screen w-full bg-slate-950 text-slate-100 flex flex-col relative select-none antialiased">
      {renderCurrentView()}
    </div>
  );
}