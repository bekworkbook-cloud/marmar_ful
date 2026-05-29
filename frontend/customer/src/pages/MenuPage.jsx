// 1. ДОБАВЛЕНЫ ВСЕ НУЖНЫЕ ИМПОРТЫ
import { useState, useEffect } from 'react';
import { AlertTriangle } from 'lucide-react';
import { apiClient } from '../api/client';
import ProductCard from '../components/ProductCard';
import BackButton from '../components/BackButton';

// Временные данные удалены, они больше не нужны!

// 2. ДОБАВЛЕН ПРОПС onAuthError
export default function MenuPage({ onProductSelect, onBack, onAuthError }) {
  const [products, setProducts] = useState([]);
  const [categories, setCategories] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  
  const currentBranchId = localStorage.getItem("currentBranchId");

useEffect(() => {
    const fetchMenuData = async () => {
      try {
        setLoading(true);

        // ШАГ 1: Загружаем список категорий для выбранного филиала
        const categoriesData = await apiClient(`/categories/?branch_id=${currentBranchId}`);
        const loadedCategories = categoriesData.categories || [];
        setCategories(loadedCategories);

        // ШАГ 2: Если категории успешно загрузились, получаем их продукты
        if (loadedCategories.length > 0) {
          
          // Создаем массив "обещаний" (запросов) для каждой категории
          const productRequests = loadedCategories.map(category => 
            apiClient(`/products/?category_id=${category.id}`)
          );

          // Promise.all запускает все эти запросы ОДНОВРЕМЕННО. 
          // Это спасет нас от долгой загрузки, если категорий будет много.
          const productsResults = await Promise.all(productRequests);

          // productsResults — это массив ответов: [{products: [...]}, {products: [...]}].
          // Функция flatMap "сплющивает" их в один большой плоский массив продуктов.
          const allProducts = productsResults.flatMap(res => res.products || []);
          
          setProducts(allProducts);
        }

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

    fetchMenuData();
  }, [currentBranchId, onAuthError]);

  const scrollToCategory = (id) => {
    const element = document.getElementById(`category-${id}`);
    if (element) {
      const y = element.getBoundingClientRect().top + window.scrollY - 100;
      window.scrollTo({ top: y, behavior: 'smooth' });
    }
  };

  return (
    <div className="flex-1 flex flex-col pb-24">
      <header className="sticky top-0 z-20 bg-surface/95 backdrop-blur border-b border-slate-800 pt-[calc(env(safe-area-inset-top)+16px)]">
        <BackButton onClick={onBack} title={"Менью"}/>

        <div className="flex overflow-x-auto px-5 pb-3 gap-2 no-scrollbar">
          {/* 4. ИСПРАВЛЕНО: categories вместо products */}
          {categories.map(cat => (
            <button
              key={cat.id}
              onClick={() => scrollToCategory(cat.id)}
              className="px-4 py-2 bg-slate-800 rounded-xl whitespace-nowrap text-sm font-medium active:scale-95 transition"
            >
              {cat.name}
            </button>
          ))}
        </div>
      </header>

      <main className="px-5 py-4 flex flex-col gap-8">
        {loading && <div className="text-center text-slate-400 animate-pulse mt-10">Загрузка меню...</div>}
        
        {error && (
          <div className="bg-red-900/30 border border-red-800 rounded-2xl p-4 text-red-300 flex items-center gap-3">
            <AlertTriangle className="w-6 h-6 shrink-0 text-red-500" />
            <p className="text-sm font-mono">{error}</p>
          </div>
        )}

        {!loading && !error && categories.map(category => {
          // 5. ИСПРАВЛЕНО: фильтруем реальные данные state (products), а не моки
          const categoryProducts = products.filter(p => p.category_id === category.id);
          
          if (categoryProducts.length === 0) return null;

          return (
            <section key={category.id} id={`category-${category.id}`} className="scroll-mt-32">
              <h2 className="text-2xl font-bold mb-4">{category.name}</h2>
              <div className="grid grid-cols-2 gap-4">
                {categoryProducts.map(product => (
                  <ProductCard 
                    key={product.id} 
                    product={product} 
                    onProductClick={onProductSelect} 
                  />
                ))}
              </div>
            </section>
          );
        })}
      </main>
    </div>
  );
}