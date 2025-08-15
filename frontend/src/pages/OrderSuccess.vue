<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { http } from '@/lib/http'
import DefaultLayout from '@/layouts/DefaultLayout.vue'
import { Card, CardContent, CardHeader, CardTitle, CardFooter } from '@/components/ui/card'
import Button from '@/components/ui/button/Button.vue'

type OrderItem = { id: number; item_id: number; quantity: number; price: number }
type OrderRead = { id: number; status: string; total_price: number; items: OrderItem[] }

const route = useRoute()
const router = useRouter()
const auth = useAuthStore()

const sessionId = computed(() => (route.query.session_id as string) || '')
const loading = ref(true)
const error = ref<string | null>(null)

const order = ref<OrderRead | null>(null)
const paymentStatus = ref('unknown')
const amountTotal = ref(0)
const currency = ref('USD')

const money = (n:number, curr=currency.value, locale='en-US') =>
  new Intl.NumberFormat(locale, { style:'currency', currency: curr }).format(n)

onMounted(async () => {
  if (!sessionId.value) {
    error.value = 'Missing session_id'
    loading.value = false
    return
  }
  try {
    const { data } = await http.get('/orders/stripe/success', {
      params: { session_id: sessionId.value },
      headers: auth.authHeader(),
    })
    order.value = data.order
    paymentStatus.value = data.payment_status
    amountTotal.value = data.amount_total
    currency.value = (data.currency || 'USD').toUpperCase()
  } catch (e: any) {
    error.value = e?.response?.data?.detail ?? 'Failed to load order'
  } finally {
    loading.value = false
  }
})

function goOrders() { router.push('/dashboard') } // или сделай отдельную страницу заказов
function goCatalog() { router.push('/catalog') }
</script>

<template>
  <DefaultLayout>
    <section class="w-[90%] 2xl:w-[75%] mx-auto rounded mt-10 py-12 lg:pb-20">
      <div class="mx-auto max-w-3xl text-center">
        <h1 class="text-3xl font-semibold">
          <template v-if="!loading && !error && paymentStatus === 'paid'">
            ✅ Оплата прошла успешно
          </template>
          <template v-else-if="!loading && !error">
            ⏳ Статус оплаты: {{ paymentStatus }}
          </template>
          <template v-else>
            Подтверждение оплаты
          </template>
        </h1>
        <p class="text-muted-foreground mt-2" v-if="!loading && !error">
          Session: <code class="text-xs">{{ $route.query.session_id }}</code>
        </p>
      </div>

      <div class="mt-8 max-w-3xl mx-auto">
        <Card v-if="loading" class="border-border">
          <CardContent class="p-6">Загружаем данные заказа…</CardContent>
        </Card>

        <Card v-else-if="error" class="border-destructive">
          <CardHeader><CardTitle>Ошибка</CardTitle></CardHeader>
          <CardContent class="text-red-500">{{ error }}</CardContent>
          <CardFooter class="flex gap-2">
            <Button variant="outline" @click="goCatalog">В каталог</Button>
          </CardFooter>
        </Card>

        <Card v-else class="border-border">
          <CardHeader>
            <CardTitle>Заказ № {{ order?.id }} — {{ order?.status }}</CardTitle>
          </CardHeader>
          <CardContent class="space-y-4">
            <div class="flex items-center justify-between">
              <span>Сумма по Stripe:</span>
              <strong>{{ money(amountTotal) }}</strong>
            </div>

            <div class="border-t pt-4 space-y-2">
              <div class="font-medium">Состав заказа</div>
              <div v-if="order?.items?.length">
                <div v-for="oi in order?.items" :key="oi.id" class="flex items-center justify-between text-sm py-1">
                  <div>Товар #{{ oi.item_id }} × {{ oi.quantity }}</div>
                  <div>{{ money(oi.price * oi.quantity) }}</div>
                </div>
              </div>
              <div v-else class="text-muted-foreground text-sm">Нет позиций</div>
            </div>

            <div class="border-t pt-4 flex items-center justify-between">
              <span>Итого (по заказу):</span>
              <strong>{{ money(order?.total_price || 0) }}</strong>
            </div>
          </CardContent>
          <CardFooter class="flex gap-2">
            <Button @click="goOrders">К моим заказам</Button>
            <Button variant="outline" @click="goCatalog">В каталог</Button>
          </CardFooter>
        </Card>
      </div>
    </section>
  </DefaultLayout>
</template>