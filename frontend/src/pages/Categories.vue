<script setup lang="ts">
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { RouterLink } from 'vue-router'

type Game = { id: number; name: string; slug: string; image: string; description: string }

const games = ref<Game[]>([])
const loading = ref(true)
const error = ref<string | null>(null)

// если уже есть общий axios instance — импортни его и замени axios на http
const BASE = 'http://127.0.0.1:8000'

function toImg(src?: string | null) {
  // если с бэка приходит просто имя файла — рисуем из /images
  if (!src) return '/images/placeholder.png'
  if (src.startsWith('http')) return src
  return `${src}`
}

async function loadGames() {
  loading.value = true
  error.value = null
  try {
    const { data } = await axios.get<Game[]>(`${BASE}/games`)
    games.value = data
  } catch (e: any) {
    error.value = 'Failed to load games'
  } finally {
    loading.value = false
  }
}

onMounted(loadGames)
</script>

<template>
  <section class="w-[90%] 2xl:w-[75%] mx-auto py-12 md:py-20">
    <div class="mx-auto max-w-2xl lg:max-w-none">
    
      <h2 class="text-2xl font-bold">Games</h2>

      <!-- error -->
      <div v-if="error" class="mt-4 text-sm text-red-500">{{ error }}</div>

      <!-- loading -->
      <div v-else-if="loading" class="mt-6 grid gap-6 lg:grid-cols-3">
        <div v-for="n in 3" :key="n" class="animate-pulse">
          <div class="w-full rounded-lg bg-muted aspect-square" />
          <div class="mt-4 h-4 w-2/3 bg-muted rounded"></div>
          <div class="mt-2 h-3 w-1/2 bg-muted rounded"></div>
        </div>
      </div>

      <!-- list -->
      <div v-else class="mt-6 space-y-12 lg:grid lg:grid-cols-3 lg:space-y-0 lg:gap-x-6">
        <RouterLink
          v-for="g in games"
          :key="g.id"
          :to="{ name: 'catalog', params: { gameSlug: g.slug }, query: { category: 'all' } }"
          class="group relative block"
        >
          <img
            :src="toImg(g.image)"
            :alt="g.name"
            class="w-full rounded-lg bg-white object-cover group-hover:opacity-75 max-sm:h-80 sm:aspect-2/1 lg:aspect-square object-center"
          />
          <h3 class="mt-6 text-sm">{{ g.name }}</h3>
          <p class="text-base font-semibold line-clamp-2">{{ g.description }}</p>
        </RouterLink>
      </div>
    </div>
  </section>
</template>