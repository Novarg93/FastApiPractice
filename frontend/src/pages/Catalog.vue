<!-- src/pages/CatalogView.vue -->
<script setup lang="ts">
import { ref, computed, watch, onMounted, onBeforeUnmount } from 'vue'
import axios from 'axios'
import { useRoute, useRouter } from 'vue-router'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Card, CardContent, CardHeader, CardTitle, CardFooter } from '@/components/ui/card'
import { Skeleton } from '@/components/ui/skeleton'
import type { Item, Category } from '@/types/catalog'
import { toast } from 'vue-sonner'
import { ShoppingCart } from 'lucide-vue-next'
import DefaultLayout from '@/layouts/DefaultLayout.vue'
import { useCartStore } from '@/stores/cart'

const props = defineProps<{
  gameSlug: string
  initialCategory?: string
}>()

const router = useRouter()
const route = useRoute()
const cart = useCartStore()

// ---- state ----
const gameId = ref<number | null>(null)
const gameName = ref<string>('')
const categories = ref<Category[]>([])
const selectedCategory = ref<string>(props.initialCategory ?? 'all')

// для простоты — работаем с полной выборкой в памяти, пагинация клиентская
const rawItems = ref<Item[]>([])

// поиск/сорт
const search = ref('')
const sort = ref<'name-asc'|'name-desc'|'price-asc'|'price-desc'>('name-asc')

// пагинация (клиентская)
const page = ref(1)
const limit = ref(24)
const isLoading = ref(false)
const isAppending = ref(false)
const SKELETON_COUNT = 10
const sentinel = ref<HTMLElement | null>(null)
let observer: IntersectionObserver | null = null

// ---- helpers ----
function toImgSrc(image?: string | null) {
  return image ? `/images/${image}` : '/images/placeholder.png'
}

function addToCart(item: Item) {
  cart.addToCart({
    id: item.id,
    title: item.name,
    price: item.price,
    image_url: toImgSrc(item.image),
  } as any)
  toast.success('Added to cart')
}

// ---- backend calls (замени пути, если у тебя другие) ----
async function fetchGameBySlug(slug: string) {
  const { data } = await axios.get(`http://127.0.0.1:8000/games/by-slug/${slug}`)
  return data as { id: number; name: string; slug: string }
}

async function fetchCategories(gameId: number) {
  const { data } = await axios.get(`http://127.0.0.1:8000/categories`, {
    params: { game_id: gameId },
  })
  return data as Category[]
}

async function fetchItemsAll(gameId: number) {
  const { data } = await axios.get(`http://127.0.0.1:8000/items/${gameId}/all`)
  return data as Item[]
}

async function fetchItemsByCategory(gameId: number, categorySlug: string) {
  const { data } = await axios.get(`http://127.0.0.1:8000/items/${gameId}/${categorySlug}`)
  return data as Item[]
}

// ---- loading pipeline ----
async function loadGameAndCats() {
  isLoading.value = true
  try {
    const g = await fetchGameBySlug(props.gameSlug)
    gameId.value = g.id
    gameName.value = g.name

    const cats = await fetchCategories(g.id)
    categories.value = cats
  } finally {
    isLoading.value = false
  }
}

async function loadItems(categorySlug: string) {
  if (!gameId.value) return
  isLoading.value = true
  rawItems.value = []
  page.value = 1

  try {
    const list = categorySlug === 'all'
      ? await fetchItemsAll(gameId.value)
      : await fetchItemsByCategory(gameId.value, categorySlug)

    rawItems.value = list
  } finally {
    isLoading.value = false
  }
}

// ---- filters/sort/pagination (клиентские) ----
const filteredSorted = computed(() => {
  let arr = rawItems.value

  // поиск
  const q = search.value.trim().toLowerCase()
  if (q) arr = arr.filter(i => i.name.toLowerCase().includes(q))

  // сорт
  const [key, dir] = sort.value.split('-') as ['name'|'price','asc'|'desc']
  arr = [...arr].sort((a,b) => {
    const va = key === 'name' ? a.name.localeCompare(b.name) : a.price - b.price
    return dir === 'asc' ? va : -va
  })

  return arr
})

const visible = computed(() => filteredSorted.value.slice(0, page.value * limit.value))
const hasMore = computed(() => visible.value.length < filteredSorted.value.length)

// ---- URL sync ----
function pushCategoryToUrl(slug: string) {
  router.replace({ name: 'catalog', params: { gameSlug: props.gameSlug }, query: { category: slug } })
}

// ---- watchers ----
watch(() => props.gameSlug, async () => {
  await loadGameAndCats()
  await loadItems(selectedCategory.value)
}, { immediate: true })

watch(selectedCategory, async (slug) => {
  pushCategoryToUrl(slug)
  await loadItems(slug)
})

watch([search, sort], () => {
  page.value = 1
})

// ---- intersection observer ----
function onIntersect(entries: IntersectionObserverEntry[]) {
  const [entry] = entries
  if (entry.isIntersecting && hasMore.value && !isAppending.value) {
    isAppending.value = true
    setTimeout(() => { // имитация догрузки
      page.value += 1
      isAppending.value = false
    }, 150)
  }
}

onMounted(() => {
  observer = new IntersectionObserver(onIntersect, { rootMargin: '400px', threshold: 0 })
  if (sentinel.value) observer.observe(sentinel.value)
})

onBeforeUnmount(() => {
  if (observer && sentinel.value) observer.unobserve(sentinel.value)
  observer = null
})
</script>

<template>
  <DefaultLayout>
    <section class="w-[90%] 2xl:w-[75%] mx-auto py-8 md:py-12">
      <div class="flex items-end justify-between gap-4 flex-wrap">
        <div>
          <h1 class="text-2xl font-semibold">{{ gameName || 'Catalog' }}</h1>
          <p class="text-sm text-muted-foreground" v-if="rawItems.length">Items: {{ filteredSorted.length }}</p>
        </div>

        <div class="flex items-center gap-3">
          <Input v-model="search" placeholder="Search items…" class="w-64" />
          <select v-model="sort" class="border rounded-md h-9 px-2">
            <option value="name-asc">A → Z</option>
            <option value="name-desc">Z → A</option>
            <option value="price-asc">Price ↑</option>
            <option value="price-desc">Price ↓</option>
          </select>
        </div>
      </div>

      <!-- категории -->
      <div class="mt-6 flex gap-2 flex-wrap">
        <Button
          variant="secondary"
          :class="selectedCategory === 'all' ? 'bg-primary text-primary-foreground' : ''"
          @click="selectedCategory = 'all'"
        >
          All
        </Button>

        <Button
          v-for="c in categories" :key="c.id"
          variant="secondary"
          :class="selectedCategory === c.slug ? 'bg-primary text-primary-foreground' : ''"
          @click="selectedCategory = c.slug"
        >
          {{ c.name }}
        </Button>
      </div>

      <!-- скелетоны -->
      <div v-if="isLoading" class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-4 mt-6">
        <div v-for="n in SKELETON_COUNT" :key="n" class="border rounded-xl overflow-hidden">
          <Skeleton class="w-full aspect-square" />
          <div class="p-4 space-y-2">
            <Skeleton class="h-5 w-3/4" />
            <Skeleton class="h-4 w-1/2" />
            <Skeleton class="h-9 w-full" />
          </div>
        </div>
      </div>

      <!-- список -->
      <div v-else class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-4 mt-6">
        <Card v-for="item in visible" :key="item.id" class="flex flex-col">
          <CardHeader class="p-0">
            <img :src="toImgSrc(item.image)" :alt="item.name" class="w-full aspect-square object-contain" />
            <CardTitle class="px-4 pt-4">
              <router-link :to="`/item/${item.id}`" class="hover:text-primary">{{ item.name }}</router-link>
            </CardTitle>
          </CardHeader>
          <CardContent class="px-4 text-muted-foreground">
            {{ item.price }} $
          </CardContent>
          <CardFooter class="px-4 pb-4 mt-auto">
            <Button class="w-full" @click="addToCart(item)">
              <ShoppingCart class="mr-2" /> Add to cart
            </Button>
          </CardFooter>
        </Card>
      </div>

      <!-- подвал листинга -->
      <div class="mt-6 text-center text-sm text-muted-foreground" v-if="!isLoading">
        <div v-if="isAppending">Loading more…</div>
        <div v-else-if="!hasMore">That’s all 👋</div>
      </div>

      <div ref="sentinel" class="h-1"></div>
    </section>
  </DefaultLayout>
</template>