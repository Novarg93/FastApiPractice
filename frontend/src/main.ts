import { createApp } from 'vue'
import { createPinia } from 'pinia'
import '@/assets/animations.css';
import { createHead } from '@vueuse/head'
import App from './App.vue'
import router from './router'
import 'vue-sonner/style.css'
import 'vue-toastification/dist/index.css'
import Toast from 'vue-toastification'
import { useCartStore } from '@/stores/cart'


const app = createApp(App)
const head = createHead()
app.use(head)
app.use(createPinia())
app.use(router)
app.use(Toast, { position: 'top-right' })

router.afterEach((to) => {
  head.push({
    title: (to.meta.title as string) || 'My App',
    meta: [
      {
        name: 'description',
        content: (to.meta.description as string) || 'Default description',
      },
    ],
  })
})

app.mount('#app')
useCartStore().init()
