// src/store/auth.js
import { create } from 'zustand';

// Функция для безопасного извлечения id из JWT (payload)
const getCourierIdFromToken = (token) => {
  if (!token) return null;
  try {
    const base64Url = token.split('.')[1];
    const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
    const jsonPayload = decodeURIComponent(
      atob(base64)
        .split('')
        .map((c) => '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2))
        .join('')
    );
    const payload = JSON.parse(jsonPayload);
    alert('JWT payload: ' + JSON.stringify(payload));
    // Предполагаем, что бэкенд зашивает id пользователя в поле sub или id
    return payload.sub ? Number(payload.sub) : (payload.id ? Number(payload.id) : null);
  } catch (e) {
    return null;
  }
};

export const useAuthStore = create((set) => ({
  token: localStorage.getItem('jwt'),
  courierId: getCourierIdFromToken(localStorage.getItem('jwt')),
  
  setToken: (token) => {
    localStorage.setItem('jwt', token);
    set({ token, courierId: getCourierIdFromToken(token) });
  },
  
  clearAuth: () => {
    localStorage.removeItem('jwt');
    set({ token: null, courierId: null });
  }
}));