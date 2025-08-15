<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useCartStore } from '@/stores/cart'
import { http } from '@/lib/http'
import { toast } from 'vue-sonner'
import DefaultLayout from '@/layouts/DefaultLayout.vue'
import Button from '@/components/ui/button/Button.vue'
import RadioGroup from '@/components/ui/radio-group/RadioGroup.vue'


type OrderItem = {
  id: number
  item_id: number
  quantity: number
  price: number
  item?: { title: string; stored_image: string; short_description?: string; currency?: string }
}

type OrderRead = {
  id: number
  status: string
  total_price: number
  items: OrderItem[]
  // currency?: string // если есть у заказа
}

const router = useRouter()
const auth = useAuthStore()
const cart = useCartStore()

const order = ref<OrderRead | null>(null)
const creating = ref(false)

const currency = computed(() =>
  order.value?.items?.[0]?.item?.currency ?? 'usd'
)

const subtotal = computed(() =>
  order.value?.items?.reduce((s, it) => s + (it.price * it.quantity), 0) ?? 0
)

const shipping = ref(0) // если надо, подтягивай с бэка
const total = computed(() => subtotal.value + shipping.value)

function formatCurrencySymbol(code?: string) {
  const map: Record<string,string> = { usd:'$', eur:'€', gbp:'£', rub:'₽' }
  if (!code) return ''
  return map[code.toLowerCase()] ?? code.toUpperCase()
}

async function createOrderFromCart() {
  if (!auth.isAuthenticated) {
    router.push({ path: '/login', query: { redirect: '/checkout' } })
    return
  }
  if (cart.items.length === 0) {
    router.push('/cart'); return
  }

  creating.value = true
  try {
    // Готовим payload под OrderCreate
    const payload = {
      items: cart.items.map(it => ({
        item_id: it.id,          // ВАЖНО: item_id, а не id
        quantity: it.quantity,
        // price можно не отправлять — бэк возьмёт из БД (надёжнее)
        // но если схема требует, передадим текущую:
        price: it.price,
      }))
    }

    const { data } = await http.post<OrderRead>('/orders', payload, { headers: auth.authHeader() })
    order.value = data
  } catch (e: any) {
    toast.error(e?.response?.data?.detail ?? 'Cannot create order')
  } finally {
    creating.value = false
  }
}

onMounted(createOrderFromCart)

// Удаление позиции — необязательное в чекауте.
// Если хочешь поддержать, нужно:
// 1) удалить в корзине,
// 2) пересоздать order (простой путь) или иметь /orders/{id}/update
// Здесь для простоты просто предупреждаем:
function removeItemWarn() {
  toast.message('Удаление позиции в чекауте пока не поддержано. Вернитесь в Cart.')
}

const selectedPaymentMethod = ref('stripe')

async function placeOrder() {
  if (!order.value) return
  if (!selectedPaymentMethod.value) {
    toast.error('Select a payment method'); return
  }
  try {
    const { data } = await http.post<{ checkout_url: string }>(
      '/orders/checkout',
      { order_id: order.value.id, payment_method: selectedPaymentMethod.value },
      { headers: auth.authHeader() }
    )
    if (data?.checkout_url) {
      window.location.href = data.checkout_url
    } else {
      toast.error('No checkout URL returned')
    }
  } catch (e: any) {
    toast.error(e?.response?.data?.detail ?? 'Payment error')
  }
}
</script>

<template>
  <DefaultLayout>
    <section class="px-4 w-full xl:px-0 xl:w-[90%] 2xl:w-[75%] mx-auto py-12 sm:py-24">
      <div class="mx-auto max-w-3xl text-center">
        <h1 class="mt-4 mb-8 text-4xl lg:text-5xl font-semibold">Secure Checkout</h1>
        <p class="text-base text-muted-foreground md:text-lg">
          Review your order created on the server and proceed to payment.
        </p>
      </div>

      <div v-if="creating" class="text-center py-20">Creating order…</div>

      <div v-else-if="order" class="flex flex-col gap-12 lg:flex-row">
        <!-- Payment methods -->
        <div class="flex-1 xl:max-w-2/3 2xl:max-w-[60%]">
          <p class="text-xl font-medium">Payment Methods</p>
          <p class="text-gray-400">Complete your order by providing your payment details.</p>

          <form class="grid gap-6">
            <RadioGroup class="mt-12" v-model="selectedPaymentMethod">
              <div
                v-for="pm in ['stripe','paypal','skrill','coinbase']"
                :key="pm"
                class="flex items-center gap-4 border hover:border-primary rounded-lg p-2 transition-colors"
                :class="{ 'border-primary bg-primary/10': selectedPaymentMethod === pm }"
                @click="selectedPaymentMethod = pm"
              >
                <RadioGroupItem :value="pm" class="ml-2" />
                <div class="flex items-center flex-1 gap-4">
                  <div class="flex flex-col gap-2">
                    <Label class="text-base font-semibold">{{ pm.toUpperCase() }}</Label>
                    <span class="text-muted-foreground text-sm font-semibold">Choose {{ pm }}</span>
                  </div>
                </div>
              </div>
            </RadioGroup>
          </form>
        </div>

        <!-- Order summary (с сервера) -->
        <div class="xl:w-[40%] 2xl:w-[40%]">
          <p class="text-xl font-medium">Order #{{ order.id }}</p>
          <p class="text-gray-400">Status: {{ order.status }}</p>

          <div class="mt-12">
            <div class="bg-secondary py-4 rounded-lg border px-4 space-y-3 sm:px-6">
              <div class="space-y-3">
                <div
                  v-for="oi in order.items"
                  :key="oi.id"
                  class="flex flex-row gap-4 items-center py-3"
                >
                  <img
                    class="size-12 rounded-md object-cover"
                    :src="oi.item?.stored_image || '/images/placeholder.png'"
                    alt=""
                  />
                  <div class="flex w-full items-center justify-between">
                    <div class="flex flex-col gap-1">
                      <span class="font-semibold">{{ oi.item?.title || ('Item #' + oi.item_id) }}</span>
                      <span
                        v-if="oi.item?.short_description"
                        class="text-muted-foreground text-sm line-clamp-1"
                        v-html="oi.item.short_description"
                      />
                    </div>
                    <div class="flex items-center gap-2">
                      <p>{{ (oi.price * oi.quantity).toFixed(2) }} {{ formatCurrencySymbol(oi.item?.currency || currency) }}</p>
                      <Button variant="link" size="icon" class="hover:text-red-600" @click.prevent="removeItemWarn" title="Remove item">✕</Button>
                    </div>
                  </div>
                </div>
              </div>

              <div class="mt-6 border-t border-b py-2">
                <div class="flex items-center justify-between">
                  <p class="text-sm font-medium">Subtotal</p>
                  <p class="font-semibold">
                    {{ subtotal.toFixed(2) }} {{ formatCurrencySymbol(currency) }}
                  </p>
                </div>
                <div class="flex items-center justify-between">
                  <p class="text-sm font-medium">Shipping</p>
                  <p class="font-semibold">
                    {{ shipping.toFixed(2) }} {{ formatCurrencySymbol(currency) }}
                  </p>
                </div>
              </div>

              <div class="mt-6 flex items-center justify-between">
                <p class="text-sm font-medium">Total</p>
                <p class="text-2xl font-semibold">
                  {{ total.toFixed(2) }} {{ formatCurrencySymbol(currency) }}
                </p>
              </div>

              <Button class="w-full" @click.prevent="placeOrder">Place Order</Button>
            </div>
          </div>
        </div>
      </div>

      <div v-else class="text-center py-20">
        Failed to create order.
      </div>
    </section>
  </DefaultLayout>
</template>