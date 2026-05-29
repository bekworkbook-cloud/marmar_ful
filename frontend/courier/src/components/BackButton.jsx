// src/components/BackButton.jsx
import React from 'react';

export default function BackButton({ onClick, title = 'Назад' }) {
  return (
    <div className="w-full bg-white dark:bg-slate-900 border-b border-slate-200 dark:border-slate-800 p-4 flex items-center sticky top-0 z-50">
      <button 
        onClick={onClick}
        className="flex items-center space-x-2 text-blue-500 font-medium active:opacity-60 transition-opacity"
      >
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={2.5} stroke="currentColor" className="w-5 h-5">
          <path strokeLinecap="round" strokeLinejoin="round" d="M15.75 19.5L8.25 12l7.5-7.5" />
        </svg>
        <span>{title}</span>
      </button>
    </div>
  );
}