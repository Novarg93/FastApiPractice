<script setup lang="ts">
import { ref, watch, onMounted, onBeforeUnmount } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'
import Input from './ui/input/Input.vue'

type ItemHit = { id: number; name: string; price: number; image?: string | null }

const router = useRouter()
const q = ref('')
const loading = ref(false)
const results = ref<ItemHit[]>([])
const total = ref(0) // <--- общее количество
const error = ref<string | null>(null)
const open = ref(false)
const inputEl = ref<HTMLInputElement | null>(null)

let debounceTimer: number | null = null
let ctrl: AbortController | null = null

async function run() {
  const query = q.value.trim()
  if (query.length < 2) {
    results.value = []
    total.value = 0
    error.value = null
    return
  }

  if (ctrl) ctrl.abort()
  ctrl = new AbortController()

  loading.value = true
  error.value = null
  try {
    const { data } = await axios.get<{ total: number; items: ItemHit[] }>(
      'http://127.0.0.1:8000/search/items',
      { params: { q: query, limit: 10 }, signal: ctrl.signal }
    )
    results.value = data.items
    total.value = data.total
    open.value = true
  } catch (e: any) {
    if (axios.isCancel?.(e) || e?.name === 'CanceledError') return
    results.value = []
    total.value = 0
    error.value = 'Search failed'
    open.value = true
  } finally {
    loading.value = false
  }
}

watch(q, () => {
  if (debounceTimer) clearTimeout(debounceTimer)
  debounceTimer = window.setTimeout(run, 250)
})

function goToItem(id: number) {
  router.push({ name: 'item', params: { id } })
  open.value = false
}
</script>

<template>
  <div class="relative">
    <Input
      ref="inputEl"
      v-model="q"
      type="search"
      placeholder="Search items…"
      class="h-9 w-80 rounded-md border px-3"
      @focus="open = true"
    />

    <div
      v-if="open && (loading || error || results.length || q.length >= 2)"
      class="absolute z-50 mt-1 w-80 rounded-md border border-border bg-popover shadow"
      @pointerdown.prevent
    >
      <div v-if="loading" class="px-3 py-2 text-sm opacity-70">Searching…</div>

      <div v-else-if="error" class="px-3 py-2 text-sm text-red-500">
        {{ error }}
      </div>

      <template v-else>
        <template v-if="results.length">
          <button
            v-for="it in results"
            :key="it.id"
            class="w-full px-3 py-2 text-left hover:bg-accent"
            @click="goToItem(it.id)"
          >
            <div class="text-sm font-medium">{{ it.name }}</div>
            <div class="text-xs opacity-70">{{ it.price }}$</div>
          </button>

          <!-- вот здесь сообщение -->
          <div
            v-if="total > results.length"
            class="px-3 py-2 text-xs opacity-70 border-t"
          >
            and {{ total - results.length }} products more…
          </div>
        </template>

        <div v-else class="px-3 py-2 text-sm opacity-70">No results</div>
      </template>
    </div>
  </div>
</template>