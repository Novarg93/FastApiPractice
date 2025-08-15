// src/stores/auth.ts
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { http, toAbsolute } from '@/lib/http'

type UserMeResp = {
  id: number
  email: string
  name?: string | null
  avatar?: string | null
  avatar_url?: string | null
}

type User = {
  id: number
  email: string
  name?: string | null
  avatar?: string | null   // ⟵ будем хранить ПОЛЕ avatar как абсолютный url
  avatar_url?: string | null
}
type LoginResp = { access_token: string; token_type: string }
type StorageDriver = 'local' | 'session'
const ACCESS_KEY = 'access_token'

function readToken(): { token: string | null; driver: StorageDriver | null } {
  let t = localStorage.getItem(ACCESS_KEY)
  if (t) return { token: t, driver: 'local' }
  t = sessionStorage.getItem(ACCESS_KEY)
  if (t) return { token: t, driver: 'session' }
  const legacy = localStorage.getItem('token') ?? sessionStorage.getItem('token')
  if (legacy) {
    localStorage.setItem(ACCESS_KEY, legacy)
    localStorage.removeItem('token')
    sessionStorage.removeItem('token')
    return { token: legacy, driver: 'local' }
  }
  return { token: null, driver: null }
}

export const useAuthStore = defineStore('auth', () => {
  const { token: initial, driver: initialDriver } = readToken()
  const token   = ref<string | null>(initial)
  const driver  = ref<StorageDriver>(initialDriver ?? 'local')
  const user    = ref<User | null>(null)
  const loading = ref(false)
  const error   = ref<string | null>(null)

  // ВАЖНО: готовность стора (гидратация + попытка /auth/me завершена)
  const ready   = ref(false)
  let initPromise: Promise<void> | null = null

  const isAuthenticated = computed(() => !!token.value && !!user.value)

  function setToken(next: string | null, target: StorageDriver = driver.value) {
    localStorage.removeItem(ACCESS_KEY)
    sessionStorage.removeItem(ACCESS_KEY)
    if (next) {
      if (target === 'local') localStorage.setItem(ACCESS_KEY, next)
      else sessionStorage.setItem(ACCESS_KEY, next)
      driver.value = target
    }
    token.value = next
  }

  function authHeader() {
    return token.value ? { Authorization: `Bearer ${token.value}` } : {}
  }

  async function fetchMe() {
  // подхватываем токен при старте, как и было у тебя
  if (!token.value) {
    const t = localStorage.getItem('access_token') ?? sessionStorage.getItem('access_token')
    if (t) token.value = t
  }
  if (!token.value) { user.value = null; return }

  loading.value = true; error.value = null
  try {
    const { data } = await http.get<UserMeResp>('/auth/me', {
      // не редиректим при старте
      
      __skipAuthRedirect: true
    })

    // ✅ нормализуем: приводим к единому полю `avatar` (абсолютный url)
    const abs = toAbsolute(data.avatar ?? data.avatar_url ?? null)
    user.value = {
      id: data.id,
      email: data.email,
      name: data.name ?? null,
      avatar_url: data.avatar_url ?? null,
      avatar: abs ?? null,
    }
  } catch (e: any) {
    if (e?.response?.status === 401) {
      setToken(null)
      user.value = null
    }
    error.value = e?.response?.data?.detail ?? 'Не удалось получить профиль'
    throw e
  } finally {
    loading.value = false
  }
}

  // Делает fetchMe один раз и выставляет ready=true
  async function init() {
    if (initPromise) return initPromise
    initPromise = (async () => {
      try { await fetchMe() } catch {} finally { ready.value = true }
    })()
    return initPromise
  }

  async function login(email: string, password: string, remember: boolean) {
    loading.value = true; error.value = null
    try {
      const { data } = await http.post<LoginResp>('/auth/login', { email, password })
      setToken(data.access_token, remember ? 'local' : 'session')
      await fetchMe()
      return true
    } finally {
      loading.value = false
    }
  }

  async function logout() {
    try { await http.post('/auth/logout', {}, { headers: authHeader() }) } catch {}
    setToken(null); user.value = null
  }

  return { token, user, loading, error, ready, isAuthenticated, init, fetchMe, login, logout, authHeader }
})