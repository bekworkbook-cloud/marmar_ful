import React, { useState, useEffect } from 'react';
import { useAuthStore } from './store/auth';
import DashboardPage from './pages/DashboardPage';
import DeliveryPage from './pages/DeliveryPage';

export default function App() {
  const [currentView, setCurrentView] = useState('dashboard');
  const [selectedOrderId, setSelectedOrderId] = useState(null);
  const [authError, setAuthError] = useState(null); // ← новый стейт

  const token = useAuthStore((s) => s.token);
  const setToken = useAuthStore((s) => s.setToken);
  const [authLoading, setAuthLoading] = useState(!token);

  useEffect(() => {
    const tg = window.Telegram?.WebApp;
    if (tg) {
      tg.ready();
      tg.expand();
    }

    const performAuth = async () => {
      if (token) {
        setAuthLoading(false);
        return;
      }

      const initData = tg?.initData || "";

      if (!initData) {
        // ← Больше не делаем return с пустым токеном
        setAuthError("Приложение доступно только через Telegram Mini App");
        setAuthLoading(false);
        return;
      }

      try {
        const API_BASE = window.location.origin + "/api/v1";
        const response = await fetch(`${API_BASE}/auth/init_data/courier_bot`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'x-telegram-init-data': initData,
            'ngrok-skip-browser-warning': 'true'
          }
        });

        if (!response.ok) {
          const body = await response.text();
          throw new Error(`${response.status}: ${body}`);
        }

        const data = await response.json();
        if (data.access_token) {
          setToken(data.access_token);
        }
      } catch (error) {
        setAuthError("Ошибка авторизации: " + error.message);
      } finally {
        setAuthLoading(false);
      }
    };

    performAuth();
  }, [token, setToken]);

  const handleOrderSelect = (orderId) => {
    setSelectedOrderId(orderId);
    setCurrentView('delivery');
  };

  const handleBackToDashboard = () => {
    setSelectedOrderId(null);
    setCurrentView('dashboard');
  };

  // Экран загрузки
  if (authLoading) {
    return (
      <div className="min-h-screen bg-slate-50 dark:bg-slate-900 flex flex-col items-center justify-center p-6 text-center">
        <div className="w-10 h-10 border-4 border-blue-500 border-t-transparent rounded-full animate-spin mb-4"></div>
        <p className="text-sm font-semibold text-slate-600 dark:text-slate-300">Авторизация курьера...</p>
      </div>
    );
  }

  // ← Экран ошибки авторизации (нет токена — нет дашборда)
  if (authError || !token) {
    return (
      <div className="min-h-screen bg-slate-50 dark:bg-slate-900 flex flex-col items-center justify-center p-6 text-center">
        <p className="text-sm font-semibold text-red-500">{authError || "Не авторизован"}</p>
      </div>
    );
  }

  switch (currentView) {
    case 'delivery':
      return <DeliveryPage orderId={selectedOrderId} onBack={handleBackToDashboard} />;
    case 'dashboard':
    default:
      return <DashboardPage onOrderSelect={handleOrderSelect} />;
  }
}