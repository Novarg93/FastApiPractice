<script setup lang="ts">
import AppSidebar from '@/components/AppSidebar.vue'
import {
  Breadcrumb, BreadcrumbItem, BreadcrumbLink, BreadcrumbList, BreadcrumbPage, BreadcrumbSeparator,
} from '@/components/ui/breadcrumb'
import { Separator } from '@/components/ui/separator'
import { SidebarInset, SidebarProvider, SidebarTrigger } from '@/components/ui/sidebar'
import { useAuthStore } from '@/stores/auth'
import { storeToRefs } from 'pinia'
import { onMounted, ref, computed } from 'vue'
import { http } from '@/lib/http'
import { Card, CardContent } from '@/components/ui/card'
import Button from '@/components/ui/button/Button.vue'

const auth = useAuthStore()
const { isAuthenticated } = storeToRefs(auth)

/** Типы */
type ItemBrief = { id: number; name?: string | null; image?: string | null; stored_image?: string | null; url_code?: string | null }
type OrderItem = { id: number; item_id: number; quantity: number; price: number; item?: ItemBrief | null }
type OrderRead = { id: number; status: string; total_price: number; items: OrderItem[]; created_at?: string }

/** Состояние */
const orders = ref<OrderRead[]>([])       // уже показанные на странице
const loading = ref(false)
const error = ref<string | null>(null)

/** Параметры загрузки */
const page = ref(1)
const limit = ref(5)                      // ← «оптимальное» начальное кол-во заказов
const total = ref<number | null>(null)    // общее число заказов (если бэк вернёт)
const cacheAll = ref<OrderRead[] | null>(null) // fallback, если бэк не умеет пагинацию

/** Утилиты */
const money = (n: number, currency = 'USD', locale = 'en-US') =>
  new Intl.NumberFormat(locale, { style: 'currency', currency }).format(n)

const fmtDate = (iso?: string) => {
  if (!iso) return '—'
  const d = new Date(iso); if (Number.isNaN(+d)) return '—'
  return d.toLocaleString(undefined, { year: 'numeric', month: 'short', day: '2-digit' })
}

const imgUrl = (it: OrderItem) =>
  it.item?.stored_image || (it.item?.image ? `/images/${it.item.image}` : '/images/placeholder.png')

const productLink = (it: OrderItem) =>
  it.item?.url_code ? `/product/${it.item.url_code}` : `/item/${it.item_id}`

/** Нормализация ответа: либо {items,total}, либо просто массив */
function normalizeOrdersResponse(payload: any): { items: OrderRead[]; total?: number } {
  if (Array.isArray(payload)) return { items: payload }       // старый бэк
  if (payload && Array.isArray(payload.items)) return { items: payload.items, total: payload.total }
  return { items: [] }
}

async function loadInitial() {
  loading.value = true; error.value = null
  try {
    // попытка серверной пагинации
    const { data, headers } = await http.get('/orders/me', {
      params: { page: page.value, limit: limit.value },
      headers: auth.authHeader(),
    })
    const norm = normalizeOrdersResponse(data)

    if (norm.total != null) {
      // сервер умеет пагинацию
      total.value = norm.total
      orders.value = norm.items.sort((a, b) =>
        (b.created_at ? +new Date(b.created_at) : b.id) - (a.created_at ? +new Date(a.created_at) : a.id)
      )
    } else {
      // сервер НЕ умеет пагинацию — грузим всё один раз, режем на клиенте
      const sorted = [...norm.items].sort((a, b) =>
        (b.created_at ? +new Date(b.created_at) : b.id) - (a.created_at ? +new Date(a.created_at) : a.id)
      )
      cacheAll.value = sorted
      total.value = sorted.length
      orders.value = sorted.slice(0, limit.value)
    }
  } catch (e: any) {
    error.value = e?.response?.data?.detail ?? 'Failed to load orders'
  } finally {
    loading.value = false
  }
}

async function loadMore() {
  if (total.value != null && orders.value.length >= total.value) return

  // если есть серверная пагинация — тянем следующую страницу
  if (cacheAll.value == null) {
    loading.value = true
    try {
      page.value += 1
      const { data } = await http.get('/orders/me', {
        params: { page: page.value, limit: limit.value },
        headers: auth.authHeader(),
      })
      const norm = normalizeOrdersResponse(data)
      orders.value = orders.value.concat(norm.items)
      if (norm.total != null) total.value = norm.total
    } catch (e: any) {
      error.value = e?.response?.data?.detail ?? 'Failed to load orders'
    } finally {
      loading.value = false
    }
    return
  }

  // иначе — локальная «пагинация» по кешу
  const nextEnd = Math.min(orders.value.length + limit.value, cacheAll.value.length)
  orders.value = cacheAll.value.slice(0, nextEnd)
}


const displayName = computed(() =>
  auth.user?.name?.trim()
  || auth.user?.email?.split('@')[0]
  || 'User'
)
const displayEmail = computed(() => auth.user?.email || '')
const displayAvatar = computed(() => (auth.user as any)?.avatar || '')


onMounted(async () => {
  if (!auth.user) { try { await auth.fetchMe() } catch { } }
  await loadInitial()
})
</script>

<template>
  <SidebarProvider>
    <AppSidebar />
    <SidebarInset class="border-l border-border rounded-lg">
      <header
        class="flex h-16 shrink-0 items-center gap-2 transition-[width,height] ease-linear group-has-[[data-collapsible=icon]]/sidebar-wrapper:h-12">
        <div class="flex items-center gap-2 px-4">
          <SidebarTrigger class="-ml-1" />
          <Separator orientation="vertical" class="mr-2 h-4" />
          <Breadcrumb>
            <BreadcrumbList>
              <BreadcrumbItem class="hidden md:block">
                <BreadcrumbLink href="/dashboard">Dashboard</BreadcrumbLink>
              </BreadcrumbItem>
              <BreadcrumbSeparator class="hidden md:block" />
              <BreadcrumbItem>
                <BreadcrumbPage>Orders</BreadcrumbPage>
              </BreadcrumbItem>
            </BreadcrumbList>
          </Breadcrumb>
        </div>
      </header>

      <div class="flex flex-1 flex-col gap-4 p-4 pt-0">



        <!-- История заказов (переверстка под твой макет) -->
        <Card class="bg-background border-0">
          <CardContent class="p-4 md:p-6">

            <div class="flex  flex-col items-center gap-4 ">
              <img v-if="displayAvatar" :src="displayAvatar" alt="Avatar" class="w-20 h-20 rounded-full object-cover" />
              <p v-else class="text-gray-500">Avatar : No data from server</p>
              <p v-else class="text-gray-500">Avatar : No data from server</p>
              <div class="flex flex-col justify-center items-center gap-4">
                <h2 class="text-xl font-semibold">{{ displayName }}</h2>
                <p class="text-gray-500">{{ displayEmail || 'Email : No data from server' }}</p>
              </div>
            </div>


            <h2 class="text-xl font-semibold mb-2">Order history</h2>

            <div v-if="loading" class="text-sm text-muted-foreground py-4">Loading orders…</div>
            <div v-else-if="error" class="text-sm text-red-500 py-4">{{ error }}</div>
            <div v-else-if="orders.length === 0" class="text-sm text-muted-foreground py-4">No orders yet.</div>

            <div v-else class="space-y-10">
              <!-- ОДНА КАРТОЧКА ЗАКАЗА -->
              <div v-for="o in orders" :key="o.id" class="space-y-6">
                <!-- ШАПКА ЗАКАЗА -->
                <div
                  class="px-4 py-6 md:p-6 flex flex-col md:flex-row md:justify-between xl:justify-start xl:gap-40 2xl:gap-80 md:items-center bg-card rounded-lg border border-border">
                  <div
                    class="pb-6 md:p-0 flex md:flex-col md:gap-1 justify-between items-center border-b md:border-0 w-full md:w-auto">
                    <p>Date placed</p>
                    <p class="text-muted-foreground">{{ fmtDate(o.created_at) }}</p>
                  </div>

                  <div
                    class="py-6 md:p-0 flex md:flex-col md:gap-1 justify-between items-center border-b md:border-0 w-full md:w-auto">
                    <p>Order number</p>
                    <p class="text-muted-foreground">#{{ o.id }}</p>
                  </div>

                  <div
                    class="py-6 md:p-0 flex md:flex-col md:gap-1 justify-between items-center md:border-0 w-full md:w-auto">
                    <p>Total amount</p>
                    <p class="text-muted-foreground">{{ money(o.total_price) }}</p>
                  </div>

                  <Button class="xl:ml-auto" @click="$router.push(`/invoices/${o.id}`)">View Invoice</Button>
                </div>

                <!-- СПИСОК ПОЗИЦИЙ -->
                <div class="flex flex-col">
                  <!-- Заголовок (desktop) -->
                  <div class="hidden md:flex items-center justify-between border-border border-b py-3 px-4">
                    <div class="md:basis-2/5 xl:basis-1/5">Product</div>
                    <div class="md:basis-1/5 xl:basis-1/6">Price</div>
                    <div class="md:basis-1/5 xl:basis-1/3">Status</div>
                    <div>Info</div>
                  </div>

                  <div v-for="it in o.items" :key="it.id" class="flex justify-between border-b border-border py-6 items-center px-4">
                    <div class="flex gap-6 items-center md:basis-2/5 xl:basis-1/5">
                      <img class="size-16 rounded-md object-cover" :src="imgUrl(it)"
                        :alt="it.item?.name || ('Item #' + it.item_id)"
                        @error="(e: any) => e.target.src = '/images/placeholder.png'" />
                      <div class="flex flex-col gap-1">
                        <p class="line-clamp-2">{{ it.item?.name || ('Item #' + it.item_id) }}</p>
                        <p class="text-muted-foreground md:hidden">{{ money(it.price * it.quantity) }}</p>
                      </div>
                    </div>

                    <p class="text-muted-foreground hidden md:block basis-1/5 xl:basis-1/6">
                      {{ money(it.price * it.quantity) }}
                    </p>

                    <p class="text-muted-foreground hidden md:block basis-1/5 xl:basis-1/3">
                      {{ o.status }} · {{ fmtDate(o.created_at) }}
                    </p>

                    <router-link class="text-primary underline-offset-2 hover:underline" :to="productLink(it)">
                      View
                    </router-link>
                  </div>
                </div>
              </div>

              <!-- Статус + «Показать ещё» -->
              <div class="flex items-center justify-between pt-2">
                <p class="text-sm text-muted-foreground">
                  Shown {{ orders.length }}<span v-if="total !== null"> из {{ total }}</span>
                </p>
                <Button variant="outline" @click="loadMore"
                  :disabled="loading || (total !== null && orders.length >= total)">
                  Load more
                </Button>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </SidebarInset>
  </SidebarProvider>
</template>
