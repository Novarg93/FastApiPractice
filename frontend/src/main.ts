import { createApp } from 'vue'
import { createPinia } from 'pinia'
import '@/assets/animations.css';
import { createHead } from '@vueuse/head'
import App from './App.vue'
import router from './router'

const app = createApp(App)
const head = createHead()
app.use(head)
app.use(createPinia())
app.use(router)

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
