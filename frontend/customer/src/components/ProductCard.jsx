export default function ProductCard({ product, onAdd, onClick }) {
  return (
    <div className="bg-white rounded-2xl overflow-hidden shadow-sm border border-gray-100 flex flex-col">
      <div onClick={onClick} className="cursor-pointer">
        {product.image_url ? (
          <img
            src={product.image_url}
            alt={product.name}
            className="w-full h-32 object-cover"
            loading="lazy"
          />
        ) : (
          <div className="w-full h-32 bg-orange-50 flex items-center justify-center text-4xl">
            🍽️
          </div>
        )}
      </div>

      <div className="p-3 fleф flex-col flex-1">
        <p
          onClick={onClick}
          className="text-sm font-medium text-gray-800 line-clamp-2 flex-1 cursor-pointer"
        >
          {product.name}
        </p>

        <div className="flex items-center justify-between mt-2">
          <span className="text-orange-500 font-bold text-sm">
            {Number(product.price).toLocaleString()} сум
          </span>
          <button
            onClick={e => { e.stopPropagation(); onAdd() }}
            className="w-8 h-8 bg-orange-500 text-white rounded-full flex items-center justify-center text-xl font-medium active:scale-90 transition-transform shadow-sm shadow-orange-200"
          >
            +
          </button>
        </div>
      </div>
    </div>
  )
}