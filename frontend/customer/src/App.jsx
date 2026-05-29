// /App.jsx

import { useState, useEffect } from 'react';
import { AlertTriangle, Loader2 } from 'lucide-react';

// Чистые импорты всех 5 твоих страниц + кнопка корзины
import MainPage from './pages/MainPage';
import MenuPage from './pages/MenuPage';
import ProductPage from './pages/ProductPage';
import CartPage from './pages/CartPage';
import OrdersPage from './pages/OrdersPage';
import CartButton from './components/CartButton';

const API_BASE = window.location.origin + "/api/v1";

export default function App() {
  const [isAuthLoading, setIsAuthLoading] = useState(true);
  const [authError, setAuthError] = useState(null);

  const [currentView, setCurrentView] = useState('main'); 
  const [selectedProduct, setSelectedProduct] = useState(null);

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
        throw new Error("Приложение открыто вне Telegram. Запустите через бота.");
      }

      const authHeaders = new Headers();
      authHeaders.append('Content-Type', 'application/json');
      authHeaders.append('x-telegram-init-data', initData);
      authHeaders.append('ngrok-skip-browser-warning', 'true');

      const response = await fetch(`${API_BASE}/auth/init_data/customer_bot`, {
        method: 'POST',
        headers: authHeaders
      });

      if (!response.ok) throw new Error("Ошибка авторизации на сервере");
      
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
      <div className="min-h-screen flex flex-col items-center justify-center bg-surface text-slate-400">
        <Loader2 className="w-10 h-10 animate-spin text-accent mb-4" />
        <p>Инициализация профиля...</p>
      </div>
    );
  }

  if (authError) {
    return (
      <div className="min-h-screen flex flex-col items-center justify-center bg-surface p-5 text-center">
        <div className="bg-red-900/30 border border-red-800 rounded-3xl p-6 text-red-300 mb-4">
          <AlertTriangle className="w-12 h-12 text-red-500 mx-auto mb-3" />
          <p className="font-semibold">{authError}</p>
        </div>
        <button 
          onClick={authenticate} 
          className="px-6 py-3 bg-slate-800 rounded-xl text-txt font-medium active:scale-95 transition"
        >
          Попробовать снова
        </button>
      </div>
    );
  }

  const renderCurrentView = () => {
    switch (currentView) {
      case 'main':
        return (
          <MainPage 
            onAuthError={authenticate} 
            // После выбора филиала идем в меню
            onBranchSelect={() => setCurrentView('menu')}
            onOrdersSelect={() => setCurrentView('orders')}
          />
        );
      case 'menu':
        return (
          <MenuPage 
            onAuthError={authenticate}
            onProductSelect={(product) => {
              setSelectedProduct(product);
              setCurrentView('product');
            }}
            onBack={() => setCurrentView('main')}
          />
        );
      case 'product':
        return (
          <ProductPage 
            product={selectedProduct} 
            // Из карточки товара возвращаемся в меню
            onBack={() => setCurrentView('menu')} 
          />
        );
      case 'cart':
        return (
          <CartPage 
            // Из корзины возвращаемся в меню
            onBack={() => setCurrentView('menu')} 
            // После успешного заказа логично кинуть юзера на экран заказов
            onOrderSuccess={() => setCurrentView('orders')} 
          />
        );
      case 'orders':
        return (
          <OrdersPage 
            // Из истории заказов возвращаемся на главную
            onBack={() => setCurrentView('main')} 
          />
        );
      default:
        return <MainPage onAuthError={authenticate} onBranchSelect={() => setCurrentView('menu')} />; 
    }
  };

  return (
    <div className="min-h-screen w-full bg-surface text-txt flex flex-col relative">
      
      {/* Рендерим активный экран */}
      {renderCurrentView()}
      
      {/* Передаем текущий экран. Кнопка сама скроется, если мы внутри cart или orders */}
      <CartButton 
        currentView={currentView} 
        onClick={() => setCurrentView('cart')} 
      />

    </div>
  );
}
