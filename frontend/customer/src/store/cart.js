// store/cart.js

import { create } from 'zustand';

export const useCartStore = create((set, get) => ({
  // --- 1. ДАННЫЕ КОРЗИНЫ (State) ---
  // В items мы храним полные объекты продуктов (id, name, price, quantity), чтобы рисовать UI
  items: [], 
  
  // Данные для оформления заказа (соответствуют полям твоего JSON)
  branch_id: null,
  payment_method: "cash", // дефолтное значение
  address: "",
  landmark: "",
  latitude: 0,
  longitude: 0,

  // --- 2. ВЫЧИСЛЯЕМЫЕ ЗНАЧЕНИЯ (Getters) ---
  // Динамически считаем общее количество и сумму (total_price)
  getTotalCount: () => get().items.reduce((total, item) => total + item.quantity, 0),
  getTotalPrice: () => get().items.reduce((total, item) => total + (item.price * item.quantity), 0),

  // --- 3. ДЕЙСТВИЯ (Actions) ---

  // Добавить товар (или увеличить количество, если он уже есть)
  addItem: (product) => set((state) => {
    const existingItem = state.items.find(item => item.id === product.id);
    if (existingItem) {
      return {
        items: state.items.map(item => 
          item.id === product.id 
            ? { ...item, quantity: item.quantity + 1 } 
            : item
        )
      };
    } else {
      // Если товара нет, добавляем его с quantity: 1
      return {
        items: [...state.items, { ...product, quantity: 1 }]
      };
    }
  }),

  // Уменьшить количество (или удалить, если осталась 1 штука)
  removeItem: (productId) => set((state) => {
    const existingItem = state.items.find(item => item.id === productId);
    if (existingItem?.quantity > 1) {
      return {
        items: state.items.map(item => 
          item.id === productId 
            ? { ...item, quantity: item.quantity - 1 } 
            : item
        )
      };
    } else {
      return {
        items: state.items.filter(item => item.id !== productId)
      };
    }
  }),

  // Сохранить данные доставки/оплаты перед отправкой заказа
  setCheckoutData: (data) => set((state) => ({
    ...state,
    ...data
  })),

  // Очистить корзину после успешного оформления
  clearCart: () => set({ 
    items: [],
    // Заметь: branch_id мы можем оставить, чтобы клиенту не пришлось заново выбирать филиал для следующего заказа
    address: "",
    landmark: "", 
  }),

  // --- 4. ГЕНЕРАТОР PAYLOAD ДЛЯ FASTAPI ---
  // Функция берет данные из памяти и собирает их строго по твоему JSON-формату
  getPayloadForApi: (currentUserId) => {
    const state = get();
    
    return {
      // Если branch_id нет в стейте, пробуем достать из localStorage (где мы его сохранили на экране филиалов)
      branch_id: state.branch_id || parseInt(localStorage.getItem("currentBranchId")),
      payment_method: state.payment_method,
      address: state.address,
      landmark: state.landmark,
      latitude: state.latitude,
      longitude: state.longitude,
      current_user_id: currentUserId,
      // Формируем массив order_items, оставляя только нужные ключи
      order_items: state.items.map(item => ({
        product_id: item.id,
        quantity: item.quantity
      }))
    };
  }
}));