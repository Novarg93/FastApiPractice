import { defineStore } from 'pinia'
import type { CartItem, Product } from '@/types'

const STORAGE_KEY = 'cart:v1'

export const useCartStore = defineStore('cart', {
  state: () => ({
    items: [] as CartItem[],
  }),

  getters: {
    totalItems: (s) => s.items.reduce((sum, i) => sum + i.quantity, 0),

    // считаем в центах, чтобы не ловить артефакты плавающей точки
    subtotalCents: (s): number =>
      s.items.reduce(
        (sum, i) => sum + Math.round(Number(i.price) * 100) * i.quantity,
        0
      ),

    // доступ к другому геттеру — через this и обычную функцию
    subtotal(): number {
      return this.subtotalCents / 100
    },

    // (опционально) сумма по конкретной позиции в центах
    itemTotalCents: (s) => (id: number) => {
      const it = s.items.find(i => i.id === id)
      return it ? Math.round(Number(it.price) * 100) * it.quantity : 0
    },
  },

  actions: {
    _save() {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(this.items))
    },
    _load() {
      const raw = localStorage.getItem(STORAGE_KEY)
      if (!raw) return
      try {
        const arr = JSON.parse(raw)
        this.items = Array.isArray(arr)
          ? arr.map((i: any) => ({
              ...i,
              price: Number(i.price) || 0,
              quantity: Math.max(1, Number(i.quantity) || 1),
            }))
          : []
      } catch {
        /* ignore */
      }
    },

    addToCart(product: Product, qty = 1) {
      const existing = this.items.find(i => i.id === product.id)
      if (existing) {
        existing.quantity += qty
      } else {
        this.items.push({
          ...product,
          price: Number(product.price), // на всякий случай приведём
          quantity: qty,
        })
      }
      this._save()
    },

    increment(id: number) {
      const it = this.items.find(i => i.id === id)
      if (!it) return
      it.quantity += 1
      this._save()
    },
    decrement(id: number) {
      const it = this.items.find(i => i.id === id)
      if (!it) return
      it.quantity = Math.max(1, it.quantity - 1)
      this._save()
    },
    setQuantity(id: number, qty: number) {
      const it = this.items.find(i => i.id === id)
      if (!it) return
      it.quantity = Math.max(1, Math.floor(qty || 1))
      this._save()
    },
    remove(id: number) {
      this.items = this.items.filter(i => i.id !== id)
      this._save()
    },
    clear() {
      this.items = []
      this._save()
    },
    // вызывать один раз при старте приложения
    init() {
      this._load()
    },
  },
})