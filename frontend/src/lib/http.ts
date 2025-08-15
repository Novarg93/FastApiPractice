import axios from 'axios'
import router from '@/router'
import { useAuthStore } from '@/stores/auth'

export const API_BASE_URL = import.meta.env.VITE_API_URL ?? 'http://localhost:8000'
export const http = axios.create({ baseURL: API_BASE_URL })

// если у тебя есть отдельный адрес для сборки абсолютных ссылок (часто == API_BASE_URL)
export const API_BASE = import.meta.env.VITE_API_BASE ?? API_BASE_URL

export function toAbsolute(url?: string | null) {
  if (!url) return null
  if (/^https?:\/\//i.test(url)) return url
  // склеиваем API_BASE + относительный путь типа /media/avatars/...
  return API_BASE.replace(/\/$/, '') + (url.startsWith('/') ? '' : '/') + url
}

// ↓ твои интерцепторы как были
http.interceptors.request.use((config) => {
  const auth = useAuthStore()
  const token =
    auth.token ||
    localStorage.getItem('access_token') ||
    sessionStorage.getItem('access_token')
  if (token) {
    config.headers = config.headers || {}
    ;(config.headers as any).Authorization = `Bearer ${token}`
  }
  return config
})

http.interceptors.response.use(
  (resp) => resp,
  async (error) => {
    const status = error?.response?.status
    const cfg = error?.config || {}
    if ((cfg as any).__skipAuthRedirect) return Promise.reject(error)
    if (status === 401) {
      const auth = useAuthStore()
      try { await auth.logout() } catch {}
      const current = router.currentRoute.value
      if (current?.meta?.requiresAuth) {
        router.push({ path: '/login', query: { redirect: current.fullPath } })
      }
    }
    return Promise.reject(error)
  }
)