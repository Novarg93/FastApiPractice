<script setup lang="ts">
import { ref, onMounted, watch, computed } from 'vue';
import axios from 'axios';
import { Input } from '@/components/ui/input'
import {
  Select,
  SelectContent,
  SelectGroup,
  SelectItem,
  SelectLabel,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select'
import { Skeleton } from '@/components/ui/skeleton'
import { useCartStore } from '@/stores/cart';
import type { Product } from '@/types'
import { toast } from 'vue-sonner'
import { SearchCheck, ShoppingCart } from 'lucide-vue-next';
import { X } from 'lucide-vue-next';
import { useAuthStore } from '@/stores/auth'
import Pagination from '@/components/Pagination.vue';
import { stringifyQuery, useRoute, useRouter } from 'vue-router'
import DefaultLayout from '@/layouts/DefaultLayout.vue';
import { description } from './Dashboard.vue';
import Button from '@/components/ui/button/Button.vue';
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
  CardFooter,
} from "@/components/ui/card";
import { ToastAction } from 'reka-ui';


interface Item {
  id: number;
  name: string;
  price: number;
  image?: string | null;
  quantity?: number | null;
  quality?: number | null
}

type SortChoice = 'name-asc' | 'name-desc' | 'price-asc' | 'price-desc'

const items = ref<Item[]>([])
const searchQuery = ref('')
const sortChoice = ref<SortChoice>('name-asc')
const sortType = ref<'name' | 'price'>('name')
const sortOrder = ref<'asc' | 'desc'>('asc')
const isLoading = ref(false);
const searchTimeout = ref<number | null>(null)

const SKELETON_COUNT = 10


const sleep = (ms: number) => new Promise(res => setTimeout(res, ms))
const MIN_LOAD_MS = 1000


const fetchItems = async () => {
  isLoading.value = true
  const started = performance.now()
  try {
    const { data } = await axios.get('http://127.0.0.1:8000/items/', {
      params: {
        q: searchQuery.value || '',
        sort_by: sortType.value,
        order: sortOrder.value
      }
    })
    items.value = data.items
  } catch (e) {
    console.error(e)
  } finally {
    const elapsed = performance.now() - started
    if (elapsed < MIN_LOAD_MS) {
      await sleep(MIN_LOAD_MS - elapsed) 
    }
    isLoading.value = false
  }
}

const cart = useCartStore()



const addToCartAndNotify = (product: Product) => {
  cart.addToCart(product)
  toast.success('Succesfully added to cart')
}

watch(searchQuery, () => {
  if (searchTimeout.value) {
    clearTimeout(searchTimeout.value);
  }
  searchTimeout.value = setTimeout(() => {
    fetchItems();
  }, 1000);
})

watch(sortChoice, (val) => {
  if (val.startsWith('name')) sortType.value = 'name'
  if (val.startsWith('price')) sortType.value = 'price'
  sortOrder.value = val.endsWith('asc') ? 'asc' : 'desc'
  fetchItems()
}, { immediate: true })

onMounted(() => {
  fetchItems();
});


</script>

<template>

  <DefaultLayout>
    <section class=" w-[90%] 2xl:w-[75%]  mx-auto  rounded  mt-10 py-12 lg:pb-20">
      <div>

        <div class="flex flex-col items-center gap-4 justify-between w-full p-2">
          <div>
            <span class="text-xl">Товаров всего: {{ items.length }}</span>
          </div>
          <div class="flex gap-4  items-center pr-4 pt-2">
            <Input class="border w-96 rounded-md px-2" v-model="searchQuery" placeholder="Filter by name" />

            <Select v-model="sortChoice">
              <SelectTrigger>
                <SelectValue placeholder="Sort" />
              </SelectTrigger>
              <SelectContent class="border-border">
                <SelectGroup>
                  <SelectItem value="name-asc">A → Z</SelectItem>
                  <SelectItem value="name-desc">Z → A</SelectItem>
                  <SelectItem value="price-asc">Цена ↑</SelectItem>
                  <SelectItem value="price-desc">Цена ↓</SelectItem>
                </SelectGroup>
              </SelectContent>
            </Select>
          </div>
        </div>
        <div v-if="isLoading" class="flex flex-wrap w-full gap-4 mt-4 justify-between items-start" aria-busy="true">
          <div v-for="n in SKELETON_COUNT" :key="n"
            class=" flex flex-col w-full max-w-xs md:max-w-none mx-auto md:w-[30%] lg:w-[23%] xl:w-[20%] 2xl:w-[18%] h-full overflow-hidden rounded-xl border border-border p-0">
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

        <!-- Нормальные карточки -->
        <div v-else class="flex flex-wrap w-full gap-4 mt-4 justify-between items-start">
          <Card v-for="item in items" :key="item.id"
            class="bg-muted/60 dark:bg-card flex flex-col w-full max-w-xs md:max-w-none mx-auto md:w-[30%] lg:w-[23%] xl:w-[20%] 2xl:w-[18%] h-full overflow-hidden group/hoverimg border-border">
            <CardHeader class="p-0 gap-0">
              <div class="h-full overflow-hidden">
                <img @error="(e) => e.target.src = '/images/placeholder.png'" :src="`/images/${item.image}`" :alt="item.name" 
                  class="w-full aspect-square object-contain saturate-0 transition-all duration-200 ease-linear size-full group-hover/hoverimg:saturate-100 group-hover/hoverimg:scale-[1.01]" />
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

        <!-- Пусто после загрузки -->
        <div v-if="!isLoading && items.length === 0" class="text-sm text-muted-foreground mt-6">
          Ничего не найдено
        </div>


      </div>
    </section>
  </DefaultLayout>


</template>