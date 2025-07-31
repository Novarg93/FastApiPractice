import { defineStore } from 'pinia'
import type { Product } from '@/types'

export const useCartStore = defineStore('cart', {
  state: () => ({
    items: [] as Product[],
  }),
  getters: {
    totalItems: (state) => state.items.reduce((sum, item) => sum + (item.quantity ?? 1), 0),
    totalPrice: (state) => state.items.reduce((sum, item) => sum + (item.price * (item.quantity ?? 1)), 0),
  },
  actions: {
    addToCart(product: Product) {
      const existing = this.items.find((p) => p.id === product.id)
      if (existing) {
        existing.quantity = (existing.quantity ?? 1) + 1
      } else {
        this.items.push({ ...product, quantity: 1 })
      }
    },
    removeFromCart(productId: number) {
      this.items = this.items.filter((p) => p.id !== productId)
    },
    clearCart() {
      this.items = []
    },
  },
})