import useStore from '../store/useStore'

export default function CartItem({ item }) {
  const changeQty = useStore(s => s.changeQty)
  const removeFromCart = useStore(s => s.removeFromCart)

  return (
    <div className="flex items-center gap-3 p-4">
      {item.product?.image_url ? (
        <img
          src={item.product.image_url}
          alt={item.product.name}
          className="w-14 h-14 rounded-xl object-cover flex-shrink-0"
        />
      ) : (
        <div className="w-14 h-14 rounded-xl bg-orange-50 flex items-center justify-center text-2xl flex-shrink-0">
          🍽️
        </div>
      )}

      <div className="flex-1 min-w-0">
        <p className="text-sm font-medium text-gray-800 truncate">
          {item.product?.name}
        </p>
        <p className="text-orange-500 font-bold text-sm mt-0.5">
          {(item.price * item.quantity).toLocaleString()} сум
        </p>
      </div>

      <div className="flex items-center gap-2 flex-shrink-0">
        <button
          onClick={() => changeQty(item.product_id, -1)}
          className="w-8 h-8 rounded-full bg-gray-100 flex items-center justify-center text-gray-700 font-bold active:bg-gray-200"
        >
          −
        </button>
        <span className="w-6 text-center font-semibold text-gray-800 text-sm">
          {item.quantity}
        </span>
        <button
          onClick={() => changeQty(item.product_id, 1)}
          className="w-8 h-8 rounded-full bg-orange-500 flex items-center justify-center text-white font-bold active:bg-orange-600"
        >
          +
        </button>
      </div>
    </div>
  )
}