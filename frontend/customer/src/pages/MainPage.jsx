import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import useStore from '../store/useStore'
import { branchApi } from '../api/api'

export default function MainPage() {
  const navigate = useNavigate()
  const { selectedBranch, setSelectedBranch , token} = useStore()
  const [branches, setBranches] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    // Проверяем токен: берем либо из стора (если он обновился), либо из localStorage
    const activeToken = token || localStorage.getItem("access_token")

    if (!activeToken) {
      // Если токена нет, просто ждем. Не ставим setLoading(false),
      // иначе покажется пустой экран "Пока нет активных филиалов".
      return
    }

    // Как только токен появился, начинаем загрузку
    setLoading(true)
    setError(null)

    branchApi
      .list()
      .then(r => {
        const data = r.data
        setBranches(Array.isArray(data) ? data : data?.items || [])
      })
      .catch((err) => {
        console.error("Ошибка API:", err)
        setError('Ошибка при загрузке филиалов')
      })
      .finally(() => setLoading(false))

  }, [token])

  const handleSelect = (branch) => {
    setSelectedBranch(branch)
    navigate('/menu')
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-screen bg-orange-50">
        <div className="flex flex-col items-center gap-3">
          <div className="w-12 h-12 border-4 border-orange-500 border-t-transparent rounded-full animate-spin" />
          <p className="text-gray-500 text-sm">Загрузка...</p>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="flex flex-col items-center justify-center h-screen gap-4 px-6">
        <div className="text-5xl">😕</div>
        <p className="text-gray-600 text-center">{error}</p>
        <button
          onClick={() => window.location.reload()}
          className="px-6 py-3 bg-orange-500 text-white rounded-2xl font-medium"
        >
          Повторить
        </button>
      </div>
    )
  }

  const activeBranches = branches.filter(b => b.is_active !== false)

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-gradient-to-b from-orange-500 to-orange-600 px-5 pt-14 pb-10 rounded-b-[2rem]">
        <p className="text-orange-200 text-sm font-medium mb-1">Добро пожаловать!</p>
        <h1 className="text-white text-3xl font-bold">Marmar</h1>
        <p className="text-orange-100 mt-2 text-sm">Выберите ближайший филиал</p>
      </div>

      {/* Branches */}
      <div className="px-4 mt-5 space-y-3 pb-8">
        {activeBranches.length === 0 && (
          <p className="text-center text-gray-500 py-8">Пока нет активных филиалов</p>
        )}

        {activeBranches.map(branch => (
          <button
            key={branch.id}
            onClick={() => handleSelect(branch)}
            className={`w-full text-left p-4 rounded-2xl bg-white shadow-sm border-2 transition-all active:scale-[0.98]
              ${selectedBranch?.id === branch.id
                ? 'border-orange-500 shadow-orange-100 shadow-md'
                : 'border-transparent'}`}
          >
            <div className="flex items-start justify-between gap-3">
              <div className="flex-1 min-w-0">
                <div className="flex items-center gap-2">
                  <span className="text-lg">🏪</span>
                  <p className="font-semibold text-gray-800 truncate">{branch.name}</p>
                </div>
                {branch.address && (
                  <p className="text-gray-400 text-sm mt-1 ml-7">{branch.address}</p>
                )}
              </div>
              <div className="text-right flex-shrink-0">
                {branch.delivery_price != null && (
                  <span className="text-xs bg-orange-50 text-orange-600 font-semibold px-2 py-1 rounded-lg">
                    {Number(branch.delivery_price).toLocaleString()} сум
                  </span>
                )}
                <p className="text-xs text-gray-400 mt-1">доставка</p>
              </div>
            </div>
          </button>
        ))}

        <button
          onClick={() => navigate('/orders')}
          className="w-full mt-2 py-3 rounded-xl border border-gray-200 bg-white text-gray-600 text-sm font-medium flex items-center justify-center gap-2"
        >
          <span>📦</span>
          <span>История заказов</span>
        </button>
      </div>
    </div>
  )
}