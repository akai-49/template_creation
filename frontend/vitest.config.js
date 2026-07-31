import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'

// Separate from vite.config.js: that one pulls in the frappe-ui build plugin, which
// wants a Frappe app layout and a production base URL that tests have no use for.
export default defineConfig({
  plugins: [vue()],
  resolve: { alias: { '@': path.resolve(__dirname, 'src') } },
  test: {
    environment: 'jsdom',
    include: ['src/**/*.test.js'],
  },
})
