// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: '2025-07-02',
  ssr: false,
  devtools: { enabled: true },
  pages: true,
  nitro: {
    output: {
      publicDir: '../ui'
    }
  },
  vite: {
    server: {
      proxy: {
        '/api': {
          target: 'http://127.0.0.1:8000',
          changeOrigin: true,
        }
      },
    }
  }
})
