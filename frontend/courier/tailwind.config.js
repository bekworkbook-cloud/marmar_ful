/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,jsx}'],
  theme: {
    extend: {
      colors: {
        primary: { DEFAULT: '#22c55e', dark: '#16a34a', light: '#f0fdf4' },
      },
    },
  },
  plugins: [],
}
