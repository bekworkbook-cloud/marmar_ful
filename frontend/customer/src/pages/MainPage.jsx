import React, { useState, useEffect } from 'react';
import { Store, AlertTriangle, ClipboardList, ChevronRight, Loader2 } from 'lucide-react';
import { apiClient } from '../api/client';
import BranchCard from '../components/BranchCard';
import { useCartStore } from '../store/cart';

export default function MainPage({ onAuthError, onBranchSelect, onOrdersSelect }) {
  const [branches, setBranches] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  
  const setCheckoutData = useCartStore(state => state.setCheckoutData);

  useEffect(() => {
    const fetchBranches = async () => {
      try {
        const data = await apiClient('/branches/');
        setBranches(data.branches || []);
      } catch (err) {
        if (err.message === "unauthorized") {
          onAuthError();
        } else {
          setError(err.message);
        }
      } finally {
        setLoading(false);
      }
    };

    fetchBranches();
  }, [onAuthError]);

  const handleBranchClick = (branch) => {
    window.Telegram?.WebApp?.HapticFeedback.notificationOccurred('success');
    localStorage.setItem("selected_branch", JSON.stringify(branch));
    localStorage.setItem("currentBranchId", branch.id);
    setCheckoutData({ branch_id: branch.id }); 
    onBranchSelect();
  };  

  return (
    // Глубокий тёмный фон всего приложения
    <div className="min-h-screen flex flex-col bg-surface text-txt selection:bg-accent/20"> 
        
        {/* Хедер в стиле панели администратора */}
        <header className="sticky top-0 z-20 bg-surface border-b border-slate-800 px-5 pt-[calc(env(safe-area-inset-top)+16px)] pb-4 flex flex-col gap-1 shadow-sm">
          <div className="flex items-center justify-between gap-3">
            <div>
              <h1 className="text-3xl font-extrabold tracking-tight text-txt">Филиалы</h1>
              <div className="text-sm text-txtDim font-medium mt-1">Выберите точку получения заказа</div>
            </div>
            {/* Акцентная золотая кнопка/иконка */}
            <div className="w-12 h-12 rounded-full bg-accent flex items-center justify-center shrink-0 shadow-lg shadow-accent/10">
              <Store className="w-6 h-6 text-surface stroke-[2.5]" />
            </div>
          </div>
        </header>

        {/* Основной контент */}
        <main className="flex-1 px-4 py-5 pb-[calc(env(safe-area-inset-bottom)+32px)] flex flex-col gap-5 fade-up">
          
          {/* СКЕЛЕТОН / ЗАГРУЗКА */}
          {loading && (
            <div className="flex flex-col items-center justify-center py-24 gap-4 text-txtDim">
              <Loader2 className="w-8 h-8 animate-spin text-accent" />
              <span className="text-sm font-medium animate-pulse">Загружаем локации...</span>
            </div>
          )}
          
          {/* ОШИБКА */}
          {error && (
            <div className="bg-red-900/20 border border-red-900/50 rounded-2xl p-4 text-alert flex items-start gap-3">
              <AlertTriangle className="w-5 h-5 shrink-0 text-alert mt-0.5" />
              <div className="flex flex-col gap-1">
                <span className="font-semibold text-sm">Не удалось загрузить данные</span>
                <p className="text-xs text-alert/70 font-mono">{error}</p>
              </div>
            </div>
          )}

          {/* ИСТОРИЯ ЗАКАЗОВ (В стиле тёмных карточек) */}
          {!loading && !error && (
            <button 
              onClick={() => {
                window.Telegram?.WebApp?.HapticFeedback.impactOccurred('light');
                onOrdersSelect();
              }}
              className="w-full bg-card border border-slate-800 rounded-2xl p-4 flex items-center justify-between active:scale-[0.98] transition-all shadow-md group"
            >
              <div className="flex items-center gap-4 min-w-0">
                {/* Вдавленная плашка для иконки */}
                <div className="w-12 h-12 rounded-xl bg-surface flex items-center justify-center shrink-0">
                  <ClipboardList className="w-6 h-6 text-accent" />
                </div>
                <div className="text-left min-w-0">
                  <div className="font-bold text-lg text-txt tracking-tight">История заказов</div>
                  <div className="text-sm text-txtDim mt-0.5 truncate">Статусы ваших прошлых покупок</div>
                </div>
              </div>
              <ChevronRight className="w-6 h-6 text-txtDim group-hover:text-accent transition-colors shrink-0" />
            </button>
          )}

          {/* СПИСОК ФИЛИАЛОВ */}
          {!loading && !error && (
            <div className="flex flex-col gap-3">
              <div className="text-xs font-bold text-txtDim uppercase tracking-widest pl-2 mb-1">
                Ближайшие к вам
              </div>
              
              {branches.length === 0 ? (
                 <div className="text-center p-8 bg-card rounded-2xl text-txtDim text-sm shadow-md border border-slate-800">
                   К сожалению, сейчас нет доступных филиалов.
                 </div>
              ) : (
                branches.map((branch, index) => (
                  <BranchCard 
                    key={branch.id} 
                    branch={branch} 
                    index={index} 
                    onClick={handleBranchClick} 
                  />
                ))
              )}
            </div>
          )}
        </main>
    </div>
  );
}