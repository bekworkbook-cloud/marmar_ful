import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  // Жестко указываем путь, по которому приложение будет доступно извне
  base: '/webapp/in/courier_bot/', 
  build: {
    outDir: '../../static/courier',
    emptyOutDir: true 
  },
  // css: {
  //   transformer: 'postcss', // ← явно указываем postcss вместо lightningcss
  // }
})