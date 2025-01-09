// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  devtools: { enabled: true },
  css: ['~/assets/css/main.css'],
  postcss: {
    plugins: {
      tailwindcss: {},
      autoprefixer: {},
    },
  },
    // 设置为静态站点
    ssr: true,
    nitro: {
      preset: 'static'
    },
      // 可选：配置静态资源生成
  generate: {
    routes: ['/'] // 添加需要预渲染的路由
  },
  modules: ['@nuxt/content', // 添加 shadcn-vue
  '@nuxtjs/tailwindcss', // 添加这行
  '@nuxtjs/color-mode', 'shadcn-nuxt', '@pinia/nuxt'],
  primevue: {
    options: {
      unstyled: true
    },
    importPT: { as: 'Aura', from: '~/presets/aura' }     //import and apply preset
  },
  colorMode: {
    classSuffix: '',
    preference: 'system', // default value of $colorMode.preference
    fallback: 'light',    // fallback value if not system preference found
  },
  shadcn: {
    /**
     * Prefix for all the imported component
     */
    prefix: '',
    /**
     * Directory that the component lives in.
     * @default "./components/ui"
     */
    componentDir: './components/ui'
  },
  content: {
    // Content 模块配置
    highlight: {
      theme: 'github-dark'
    }
  },
  imports: {
    dirs: ['stores']
  }
})