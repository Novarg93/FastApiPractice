import { defineStore } from 'pinia'
import type { CartItem, Product } from '@/types'

const STORAGE_KEY = 'cart:v1'

export const useCartStore = defineStore('cart', {
  state: () => ({
    items: [] as CartItem[],
  }),

  getters: {
    totalItems: (s) => s.items.reduce((sum, i) => sum + i.quantity, 0),
    subtotal:   (s) => s.items.reduce((sum, i) => sum + i.price * i.quantity, 0),
  },

  actions: {
    _save() {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(this.items))
    },
    _load() {
      const raw = localStorage.getItem(STORAGE_KEY)
      if (raw) {
        try { this.items = JSON.parse(raw) } catch {}
      }
    },

    addToCart(product: Product, qty = 1) {
      const existing = this.items.find(i => i.id === product.id)
      if (existing) existing.quantity += qty
      else this.items.push({ ...product, quantity: qty })
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
    }
  },
})