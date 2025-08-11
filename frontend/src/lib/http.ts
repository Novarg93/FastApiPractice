import axios from 'axios'

export const http = axios.create({
  baseURL: import.meta.env.VITE_API_URL ?? 'http://127.0.0.1:8000',
})

// request: подставляем токен
http.interceptors.request.use((config) => {
  const t = localStorage.getItem('access_token')
  if (t) config.headers.Authorization = `Bearer ${t}`
  return config
})

// response: глобально обрабатываем 401
http.interceptors.response.use(
  (r) => r,
  (err) => {
    if (err?.response?.status === 401) {
      // мягкий logout, без циклов
      localStorage.removeItem('access_token')
      // можно эмитнуть событие или редиректнуть на /login
    }
    return Promise.reject(err)
  }
)