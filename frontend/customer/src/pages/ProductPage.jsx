import { useState, useEffect } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import useStore from '../store/useStore'
import { productApi } from '../api/api'

export default function ProductPage() {
  const { id } = useParams()
  const navigate = useNavigate()
  const addToCart = useStore(s => s.addToCart)
  const cartCount = useStore(s => s.cartCount())

  const [product, setProduct] = useState(null)
  const [loading, setLoading] = useState(true)
  const [qty, setQty] = useState(1)
  const [added, setAdded] = useState(false)

  useEffect(() => {
    productApi
      .get(id)
      .then(r => setProduct(r.data))
      .catch(() => navigate(-1))
      .finally(() => setLoading(false))
  }, [id])

  const handleAdd = () => {
    for (let i = 0; i < qty; i++) addToCart(product)
    setAdded(true)
    setTimeout(() => setAdded(false), 1500)
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="w-10 h-10 border-4 border-orange-500 border-t-transparent rounded-full animate-spin" />
      </div>
    )
  }

  if (!product) return null

  return (
    <div className="min-h-screen bg-white flex flex-col">
      {/* Image */}
      <div className="relative">
        {product.image_url ? (
          <img
            src={product.image_url}
            alt={product.name}
            className="w-full h-64 object-cover"
          />
        ) : (
          <div className="w-full h-64 bg-orange-50 flex items-center justify-center text-7xl">
            🍽️
          </div>
        )}

        <button
          onClick={() => navigate(-1)}
          className="absolute top-12 left-4 w-10 h-10 bg-white/80 backdrop-blur rounded-full flex items-center justify-center shadow-sm"
        >
          ←
        </button>

        {cartCount > 0 && (
          <button
            onClick={() => navigate('/cart')}
            className="absolute top-12 right-4 w-10 h-10 bg-white/80 backdrop-blur rounded-full flex items-center justify-center shadow-sm relative"
          >
            🛒
            <span className="absolute -top-1 -right-1 bg-orange-500 text-white text-xs w-5 h-5 rounded-full flex items-center justify-center font-bold">
              {cartCount}
            </span>
          </button>
        )}
      </div>

      {/* Info */}
      <div className="flex-1 px-5 py-5">
        <h1 className="text-xl font-bold text-gray-900">{product.name}</h1>
        {product.description && (
          <p className="text-gray-500 mt-2 text-sm leading-relaxed">{product.description}</p>
        )}

        <div className="mt-4 p-4 bg-orange-50 rounded-2xl flex items-center justify-between">
          <p className="text-orange-500 text-2xl font-bold">
            {Number(product.price).toLocaleString()} сум
          </p>
          {product.maintenance_day && (
            <p className="text-xs text-gray-400">{product.maintenance_day}</p>
          )}
        </div>

        {/* Quantity selector */}
        <div className="mt-5 flex items-center justify-center gap-6">
          <button
            onClick={() => setQty(q => Math.max(1, q - 1))}
            className="w-12 h-12 rounded-full bg-gray-100 text-2xl font-medium flex items-center justify-center active:bg-gray-200"
          >
            −
          </button>
          <span className="text-2xl font-bold text-gray-800 w-8 text-center">{qty}</span>
          <button
            onClick={() => setQty(q => q + 1)}
            className="w-12 h-12 rounded-full bg-orange-500 text-white text-2xl font-medium flex items-center justify-center active:bg-orange-600"
          >
            +
          </button>
        </div>
      </div>

      {/* Add to cart */}
      <div className="px-5 pb-8 pt-2">
        <button
          onClick={handleAdd}
          className={`w-full py-4 rounded-2xl font-semibold text-white transition-all active:scale-[0.98]
            ${added ? 'bg-green-500' : 'bg-orange-500 shadow-lg shadow-orange-200'}`}
        >
          {added
            ? '✓ Добавлено в корзину!'
            : `Добавить в корзину — ${(Number(product.price) * qty).toLocaleString()} сум`}
        </button>
      </div>
    </div>
  )
}