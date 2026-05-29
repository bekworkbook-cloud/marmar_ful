import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  // Жестко указываем путь, по которому приложение будет доступно извне
  base: '/webapp/in/operator_bot/', 
  build: {
    outDir: '../../static/operator',
    emptyOutDir: true 
  }
})