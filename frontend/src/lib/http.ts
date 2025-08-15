// src/lib/http.ts
import axios from 'axios'
import router from '@/router'
import { useAuthStore } from '@/stores/auth'

export const API_BASE_URL = import.meta.env.VITE_API_URL ?? 'http://localhost:8000'
export const http = axios.create({ baseURL: API_BASE_URL })

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
    const auth = useAuthStore()

    // Не редиректим, когда:
    // 1) мы явно запретили (fetchMe), или
    // 2) ещё идёт первичная инициализация auth (ready=false)
    if ((cfg as any).__skipAuthRedirect || !auth.ready) {
      return Promise.reject(error)
    }

    if (status === 401) {
      try { await auth.logout() } catch {}
      const current = router.currentRoute.value
      if (current?.meta?.requiresAuth) {
        router.push({ path: '/login', query: { redirect: current.fullPath } })
      }
    }
    return Promise.reject(error)
  }
)