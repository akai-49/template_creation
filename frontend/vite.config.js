import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'

export default defineConfig(async ({ mode }) => {
  const config = {
    plugins: [vue()],
    resolve: {
      alias: {
        '@': path.resolve(__dirname, 'src'),
      },
    },
    server: {
      fs: {
        allow: [path.resolve(__dirname, '..')],
      },
    },
  }

  const frappeuiPlugin = (await import('frappe-ui/vite')).default
  config.plugins.unshift(
    frappeuiPlugin({
      frappeProxy: true,
      lucideIcons: true,
      jinjaBootData: true,
      buildConfig: {
        indexHtmlPath: '../marketing_studio/www/marketing_studio.html',
        emptyOutDir: true,
        sourcemap: true,
      },
    }),
  )

  return config
})
