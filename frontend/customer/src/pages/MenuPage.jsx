import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import useStore from '../store/useStore'
import { categoryApi, productApi } from '../api/api'
import ProductCard from '../components/ProductCard'

export default function MenuPage() {
  const navigate = useNavigate()
  const { selectedBranch, addToCart } = useStore()
  const cartCount = useStore(s => s.cartCount())
  const cartTotal = useStore(s => s.cartTotal())

  const [categories, setCategories] = useState([])
  const [products, setProducts] = useState([])
  const [activeCategory, setActiveCategory] = useState(null)
  const [loadingCats, setLoadingCats] = useState(true)
  const [loadingProds, setLoadingProds] = useState(false)

  useEffect(() => {
    if (!selectedBranch) { navigate('/'); return }
    categoryApi
      .list(selectedBranch.id)
      .then(r => {
        const cats = Array.isArray(r.data) ? r.data : r.data?.items || []
        const active = cats.filter(c => c.is_active !== false)
        setCategories(active)
        if (active.length > 0) setActiveCategory(active[0].id)
      })
      .finally(() => setLoadingCats(false))
  }, [selectedBranch])

  useEffect(() => {
    if (!activeCategory) return
    setLoadingProds(true)
    productApi
      .list(activeCategory)
      .then(r => {
        const prods = Array.isArray(r.data) ? r.data : r.data?.items || []
        setProducts(prods.filter(p => p.is_active !== false))
      })
      .finally(() => setLoadingProds(false))
  }, [activeCategory])

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col">
      {/* Header */}
      <div className="bg-white px-4 pt-10 shadow-sm sticky top-0 z-20">
        <div className="flex items-center justify-between mb-3">
          <button
            onClick={() => navigate('/')}
            className="w-9 h-9 flex items-center justify-center rounded-xl bg-gray-100 text-gray-600"
          >
            ←
          </button>
          <h2 className="font-bold text-gray-800 text-base">{selectedBranch?.name}</h2>
          <button
            onClick={() => navigate('/cart')}
            className="relative w-9 h-9 flex items-center justify-center rounded-xl bg-gray-100"
          >
            🛒
            {cartCount > 0 && (
              <span className="absolute -top-1 -right-1 bg-orange-500 text-white text-xs w-5 h-5 rounded-full flex items-center justify-center font-bold">
                {cartCount}
              </span>
            )}
          </button>
        </div>

        {/* Category tabs */}
        {loadingCats ? (
          <div className="h-9 mb-3" />
        ) : (
          <div className="flex gap-2 overflow-x-auto pb-3 scrollbar-hide">
            {categories.map(cat => (
              <button
                key={cat.id}
                onClick={() => setActiveCategory(cat.id)}
                className={`flex-shrink-0 px-4 py-1.5 rounded-full text-sm font-medium transition-colors
                  ${activeCategory === cat.id
                    ? 'bg-orange-500 text-white'
                    : 'bg-gray-100 text-gray-600 active:bg-gray-200'}`}
              >
                {cat.name}
              </button>
            ))}
          </div>
        )}
      </div>

      {/* Products */}
      <div className="flex-1 px-4 py-4 pb-36">
        {loadingProds ? (
          <div className="flex justify-center py-16">
            <div className="w-8 h-8 border-4 border-orange-500 border-t-transparent rounded-full animate-spin" />
          </div>
        ) : products.length === 0 ? (
          <div className="flex flex-col items-center py-16 gap-3">
            <span className="text-5xl">🍽️</span>
            <p className="text-gray-500">В этом разделе нет товаров</p>
          </div>
        ) : (
          <div className="grid grid-cols-2 gap-3">
            {products.map(product => (
              <ProductCard
                key={product.id}
                product={product}
                onAdd={() => addToCart(product)}
                onClick={() => navigate(`/product/${product.id}`)}
              />
            ))}
          </div>
        )}
      </div>

      {/* Floating cart button */}
      {cartCount > 0 && (
        <div className="fixed bottom-5 left-4 right-4 z-30">
          <button
            onClick={() => navigate('/cart')}
            className="w-full bg-orange-500 text-white py-4 rounded-2xl font-semibold shadow-xl shadow-orange-200 flex items-center px-5 active:scale-[0.98] transition-transform"
          >
            <span className="bg-orange-600 text-xs px-2 py-1 rounded-lg mr-3">
              {cartCount}
            </span>
            <span className="flex-1">Перейти в корзину</span>
            <span className="font-bold">
              {cartTotal.toLocaleString()} сум
            </span>
          </button>
        </div>
      )}
    </div>
  )
}