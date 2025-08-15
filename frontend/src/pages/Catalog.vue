<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount, watch } from 'vue'
import axios from 'axios'
import { Input } from '@/components/ui/input'
import {
  Select, SelectContent, SelectGroup, SelectItem, SelectTrigger, SelectValue
} from '@/components/ui/select'
import { Skeleton } from '@/components/ui/skeleton'
import { useCartStore } from '@/stores/cart'
import type { Product } from '@/types'
import { toast } from 'vue-sonner'
import DefaultLayout from '@/layouts/DefaultLayout.vue'
import Button from '@/components/ui/button/Button.vue'
import { Card, CardContent, CardHeader, CardTitle, CardFooter } from "@/components/ui/card"
import { ShoppingCart } from 'lucide-vue-next'

interface Item {
  id: number
  name: string
  price: number
  image?: string | null
  quantity?: number | null
  quality?: number | null
}

type SortChoice = 'name-asc' | 'name-desc' | 'price-asc' | 'price-desc'

const items = ref<Item[]>([])
const searchQuery = ref('')
const sortChoice = ref<SortChoice>('name-asc')
const sortType = ref<'name' | 'price'>('name')
const sortOrder = ref<'asc' | 'desc'>('asc')

// пагинация/инфинити
const page = ref(1)
const limit = ref(24)          // сколько грузим за раз
const total = ref(0)
const hasMore = ref(true)

// загрузка
const isInitialLoading = ref(false) // загрузка первой страницы (скелетоны карточек)
const isAppending = ref(false)      // догрузка следующих страниц (спиннер внизу)
const searchTimeout = ref<number | null>(null)
const SKELETON_COUNT = 10

const cart = useCartStore()

// адаптер под тип корзины (если cart.addToCart ждёт Product)
function toProduct(i: Item): Product {
  return {
    id: i.id,
    title: i.name,
    price: i.price,
    description: '',           // если нужно — подтяни с бэка
    image_url: i.image ? `/images/${i.image}` : '/images/placeholder.png',
  } as Product
}

const addToCartAndNotify = (item: Item) => {
  cart.addToCart(toProduct(item))
  toast.success('Succesfully added to cart')
}

// общий загрузчик
async function fetchPage(p: number) {
  const isFirst = p === 1
  if (isFirst) {
    isInitialLoading.value = true
  } else {
    if (isAppending.value || !hasMore.value) return
    isAppending.value = true
  }

  try {
    const { data } = await axios.get('http://127.0.0.1:8000/items/', {
      params: {
        page: p,
        limit: limit.value,
        q: searchQuery.value || '',
        sort_by: sortType.value,
        order: sortOrder.value,
      },
    })

    // бэк возвращает { items, total }
    const batch: Item[] = data.items ?? []
    total.value = data.total ?? 0

    if (isFirst) items.value = batch
    else items.value = [...items.value, ...batch]

    // есть ли ещё страницы
    hasMore.value = p * limit.value < total.value
    page.value = p + 1
  } catch (e) {
    console.error(e)
  } finally {
    if (isFirst) isInitialLoading.value = false
    else isAppending.value = false
  }
}

function resetAndLoad() {
  page.value = 1
  hasMore.value = true
  items.value = []
  fetchPage(1)
}

// дебаунс поиска
watch(searchQuery, () => {
  if (searchTimeout.value) clearTimeout(searchTimeout.value)
  searchTimeout.value = window.setTimeout(() => resetAndLoad(), 500)
})

// сортировка
watch(
  sortChoice,
  (val) => {
    sortType.value = val.startsWith('name') ? 'name' : 'price'
    sortOrder.value = val.endsWith('asc') ? 'asc' : 'desc'
    resetAndLoad()
  },
  { immediate: true }
)

// IntersectionObserver
const sentinel = ref<HTMLElement | null>(null)
let observer: IntersectionObserver | null = null

function onIntersect(entries: IntersectionObserverEntry[]) {
  const [entry] = entries
  if (entry.isIntersecting) {
    fetchPage(page.value) // догружаем следующую страницу
  }
}

onMounted(() => {
  // первая загрузка уже делается watcher’ом sortChoice (immediate), так что тут ничего не делаем
  observer = new IntersectionObserver(onIntersect, {
    root: null,
    rootMargin: '400px', // подгружать заранее
    threshold: 0,
  })
  if (sentinel.value) observer.observe(sentinel.value)
})

onBeforeUnmount(() => {
  if (observer && sentinel.value) observer.unobserve(sentinel.value)
  observer = null
})
</script>

<template>
  <DefaultLayout>
    <section class="w-[90%] 2xl:w-[75%] mx-auto rounded mt-10 py-12 lg:pb-20">
      <div>
        <div class="flex flex-col items-center gap-4 justify-between w-full p-2">
          <div>
            <!-- показываем общее количество с бэка -->
            <span class="text-xl">Товаров всего: {{ total }}</span>
          </div>
          <div class="flex gap-4 items-center pr-4 pt-2">
            <Input class="border w-96 rounded-md px-2" v-model="searchQuery" placeholder="Filter by name" />
            <Select v-model="sortChoice">
              <SelectTrigger><SelectValue placeholder="Sort" /></SelectTrigger>
              <SelectContent class="border-border">
                <SelectGroup>
                  <SelectItem value="name-asc">A → Z</SelectItem>
                  <SelectItem value="name-desc">Z → A</SelectItem>
                  <SelectItem value="price-asc">Price ↑</SelectItem>
                  <SelectItem value="price-desc">Price ↓</SelectItem>
                </SelectGroup>
              </SelectContent>
            </Select>
          </div>
        </div>

        <!-- первый экран: скелетоны карточек -->
        <div v-if="isInitialLoading" class="flex flex-wrap w-full gap-4 mt-4 justify-between items-start" aria-busy="true">
          <div v-for="n in SKELETON_COUNT" :key="n"
               class="flex flex-col w-full max-w-xs md:max-w-none mx-auto md:w-[30%] lg:w-[23%] xl:w-[20%] 2xl:w-[18%] h-full overflow-hidden rounded-xl border border-border p-0">
            <Skeleton class="w-full aspect-square" />
            <div class="p-6 space-y-3">
              <Skeleton class="h-5 w-3/4" />
              <Skeleton class="h-4 w-1/2" />
            </div>
            <div class="px-6 pb-6">
              <Skeleton class="h-10 w-full" />
            </div>
          </div>
        </div>

        <!-- список карточек -->
        <div v-else class="flex flex-wrap w-full gap-4 mt-4 justify-between items-start">
          <Card v-for="item in items" :key="item.id"
                class="bg-muted/60 dark:bg-card flex flex-col w-full max-w-xs md:max-w-none mx-auto md:w-[30%] lg:w-[23%] xl:w-[20%] 2xl:w-[18%] h-full overflow-hidden group/hoverimg border-border">
            <CardHeader class="p-0 gap-0">
              <div class="h-full overflow-hidden">
                <img
                  @error="(e) => (e.target as HTMLImageElement).src = '/images/placeholder.png'"
                  :src="item.image ? `/images/${item.image}` : '/images/placeholder.png'"
                  :alt="item.name"
                  class="w-full aspect-square object-contain saturate-0 transition-all duration-200 ease-linear size-full group-hover/hoverimg:saturate-100 group-hover/hoverimg:scale-[1.01]"
                />
              </div>
              <CardTitle class="py-6 pb-4 px-6">
                <router-link :to="`/item/${item.id}`" class="hover:text-primary cursor-pointer">
                  {{ item.name }}
                </router-link>
              </CardTitle>
            </CardHeader>

            <CardContent class="text-muted-foreground">
              {{ item.price }} $
            </CardContent>

            <CardFooter class="space-x-4 mt-auto">
              <Button @click="addToCartAndNotify(item)" class="cursor-pointer w-full">
                <ShoppingCart /> Add to cart
              </Button>
            </CardFooter>
          </Card>
        </div>

        <!-- пусто -->
        <div v-if="!isInitialLoading && items.length === 0" class="text-sm text-muted-foreground mt-6">
          Ничего не найдено
        </div>

        <!-- индикатор догрузки -->
        <div class="mt-6 text-center text-sm text-muted-foreground" v-if="!isInitialLoading">
          <div v-if="isAppending">Loading more…</div>
          <div v-else-if="!hasMore">That’s all 👋</div>
        </div>

        <!-- сентинел -->
        <div ref="sentinel" class="h-1"></div>
      </div>
    </section>
  </DefaultLayout>
</template>