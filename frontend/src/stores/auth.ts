import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { http } from '@/lib/http'

type User = { id: number; email: string; name?: string | null }
type LoginResp = { access_token: string; token_type: string }

const ACCESS_KEY = 'access_token'

export const useAuthStore = defineStore('auth', () => {
  const user = ref<User | null>(null)
  const accessToken = ref<string | null>(localStorage.getItem(ACCESS_KEY))
  const loading = ref(false)
  const error = ref<string | null>(null)

  const isAuthenticated = computed(() => !!user.value)

  function setAccess(token: string | null) {
    accessToken.value = token
    if (token) localStorage.setItem(ACCESS_KEY, token)
    else localStorage.removeItem(ACCESS_KEY)
  }

  async function fetchUser() {
    if (!accessToken.value) { user.value = null; return }
    loading.value = true; error.value = null
    try {
      const { data } = await http.get<User>('/auth/me')
      user.value = data
    } catch (e: any) {
      const status = e?.response?.status
      if (status === 401) {
        setAccess(null)
        user.value = null
      }
      error.value = 'Не удалось получить профиль'
    } finally {
      loading.value = false
    }
  }

  async function login(email: string, password: string) {
    loading.value = true; error.value = null
    try {
      const { data } = await http.post<LoginResp>('/auth/login', { email, password })
      setAccess(data.access_token)
      await fetchUser()
    } catch (e: any) {
      error.value = e?.response?.data?.detail ?? 'Ошибка входа'
      throw e
    } finally {
      loading.value = false
    }
  }

  async function logout() {
    try { await http.post('/auth/logout') } catch {}
    setAccess(null)
    user.value = null
  }

  async function init() {
    await fetchUser()
  }

  return { user, accessToken, isAuthenticated, loading, error, init, fetchUser, login, logout }
})