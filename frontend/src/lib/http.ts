import axios from 'axios'
import router from '@/router'
import { useAuthStore } from '@/stores/auth'


export const API_BASE_URL =
  import.meta.env.VITE_API_URL ?? 'http://localhost:8000'

export const http = axios.create({
  baseURL: API_BASE_URL,
})

export const API_BASE = import.meta.env.VITE_API_BASE ?? 'http://127.0.0.1:8000' // твой бэк

export function toAbsolute(url?: string | null) {
  if (!url) return null
  if (/^https?:\/\//i.test(url)) return url
  return API_BASE.replace(/\/$/, '') + url 
}



http.interceptors.response.use(
  (resp) => resp,
  async (error) => {
    const status = error?.response?.status
    if (status === 401) {
      const auth = useAuthStore()
      const current = router.currentRoute.value
      const redirect = current.fullPath

      try { await auth.logout() } catch {}
      router.push({ path: '/login', query: { redirect } })
    }
    return Promise.reject(error)
  }
)