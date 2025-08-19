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
const error = ref<string | null>(null)
const open = ref(false)
const container = ref<HTMLElement | null>(null)
const inputEl = ref<HTMLInputElement | null>(null)

let debounceTimer: number | null = null
let ctrl: AbortController | null = null

async function run() {
    const query = q.value.trim()
    if (query.length < 2) {
        results.value = []
        error.value = null
        return
    }

    // отменяем прошлый запрос, если он ещё не завершился
    if (ctrl) ctrl.abort()
    ctrl = new AbortController()

    loading.value = true
    error.value = null
    try {
        const { data } = await axios.get<ItemHit[]>('http://127.0.0.1:8000/search/items', {
            params: { q: query, limit: 10 },
            signal: ctrl.signal, // <- ключевой момент
        })
        results.value = data
        open.value = true
    } catch (e: any) {
        // если именно отмена — игнорируем
        if (axios.isCancel?.(e) || e?.name === 'CanceledError' || e?.message === 'canceled') return
        results.value = []
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

// перейти на страницу товара
function goToItem(id: number) {
    router.push({ name: 'item', params: { id } })
    close()
}

// ---- управление открытием/закрытием
function openBox() {
    if ((results.value.length || error.value || loading.value) && q.value.trim().length >= 2) {
        open.value = true
    }
}
function close(clear = false) {
    open.value = false
    if (clear) q.value = ''
}

// Esc глобально (пока инпут в фокусе или вообще)
function onKeydown(e: KeyboardEvent) {
    if (e.key === 'Escape') {
        e.stopPropagation()
        close(/*clear=*/false) // если хочешь очищать строку — передай true
        // вернём фокус в инпут для удобства
        inputEl.value?.focus()
    }
}

// Blur: закрываем, но защитимся от клика по выпадающему списку.
// Трюк: предотвратим блюр, когда кликаем мышью внутри дропдауна (pointerdown.prevent)
function onBlur() {
    // маленькая задержка — чтобы успел отработать click по кнопке
    setTimeout(() => close(false), 80)
}

onMounted(() => {
    document.addEventListener('keydown', onKeydown)
})

onBeforeUnmount(() => {
    document.removeEventListener('keydown', onKeydown)
    if (ctrl) ctrl.abort()
    if (debounceTimer) clearTimeout(debounceTimer)
})
</script>

<template>
    <div class="relative" ref="container">
        <Input ref="inputEl" v-model="q" type="search" placeholder="Search items…"
            class="h-9 w-80 rounded-md border px-3" @focus="openBox()" @blur="onBlur" />

        <div v-if="open && (loading || error || results.length || q.length >= 2)"
            class="absolute z-50 mt-1 w-80 rounded-md border border-border bg-popover shadow" @pointerdown.prevent>
            <div v-if="loading" class="px-3 py-2 text-sm opacity-70">Searching…</div>

            <div v-else-if="error" class="px-3 py-2 text-sm text-red-500">
                {{ error }}
            </div>

            <template v-else>
                <template v-if="results.length">
                    <button v-for="it in results" :key="it.id" class="w-full px-3 py-2 text-left hover:bg-accent"
                        @click="goToItem(it.id)">
                        <div class="text-sm font-medium">{{ it.name }}</div>
                        <div class="text-xs opacity-70">{{ it.price }}$</div>
                    </button>
                </template>
                <div v-else class="px-3 py-2 text-sm opacity-70">No results</div>
            </template>
        </div>
    </div>
</template>