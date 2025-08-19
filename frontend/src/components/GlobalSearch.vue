<script setup lang="ts">
import { ref, watch } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'
import Input from './ui/input/Input.vue';

type ItemHit = { id: number; name: string; price: number; image?: string | null }

const router = useRouter()
const q = ref('')
const loading = ref(false)
const results = ref<ItemHit[]>([])
const open = ref(false)
let t: number | null = null
const error = ref<string | null>(null)


async function run() {
  const query = q.value.trim()
  if (query.length < 2) { results.value = []; error.value = null; return }
  loading.value = true
  error.value = null
  try {
    const { data } = await axios.get<ItemHit[]>('http://127.0.0.1:8000/search/items', {
      params: { q: query, limit: 10 }
    })
    results.value = data
    open.value = true
  } catch (e: any) {
    results.value = []
    
    error.value = axios.isAxiosError(e)
      ? (e.response?.data?.detail ?? 'Search failed')
      : 'Search failed'
    open.value = true
  } finally {
    loading.value = false
  }
}

watch(q, () => {
  if (t) clearTimeout(t)
  t = window.setTimeout(run, 250)  
})

function goToItem(id: number) {
  router.push({ name: 'item', params: { id } })
  open.value = false
}
</script>

<template>
  <div class="relative">
    <Input
      v-model="q"
      type="search"
      placeholder="Search items…"
      class="h-9 w-80 rounded-md border px-3"
      @focus="open = true"
    />

    <div
      v-if="open && (loading || error || results.length)"
      class="absolute z-50 mt-1 w-80 rounded-md border border-border bg-popover shadow"
    >
      <div v-if="loading" class="px-3 py-2 text-sm opacity-70">Searching…</div>

      <div v-else-if="error" class="px-3 py-2 text-sm text-red-500">
        {{ error }}
      </div>

      <template v-else>
        <button
          v-for="it in results" :key="it.id"
          class="w-full px-3 py-2 text-left hover:bg-accent"
          @click="goToItem(it.id)"
        >
          <div class="text-sm font-medium">{{ it.name }}</div>
          <div class="text-xs opacity-70">{{ it.price }}$</div>
        </button>
        <div v-if="!results.length" class="px-3 py-2 text-sm opacity-70">No results</div>
      </template>
    </div>
  </div>
</template>