import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import axios from 'axios'

export const useAuthStore = defineStore('auth', () => {
  const user = ref(null)

  async function fetchUser() {
    try {
      const response = await axios.get('/api/user') // ⚠️ замени на свой эндпоинт
      user.value = response.data
    } catch (error) {
      user.value = null
    }
  }

  async function login(email: string, password: string) {
    try {
      await axios.post('/api/login', { email, password })
      await fetchUser()
    } catch (error) {
      throw error
    }
  }

  async function logout() {
    await axios.post('/api/logout')
    user.value = null
  }

  return {
    user,
    fetchUser,
    login,
    logout,
    isAuthenticated: computed(() => user.value !== null),
  }
})