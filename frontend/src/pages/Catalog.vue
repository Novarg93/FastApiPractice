<script setup lang="ts">
import { ref, onMounted, watch } from 'vue';
import axios from 'axios';
import { useCartStore } from '@/stores/cart';
import { useToast } from 'vue-toastification'
import { ShoppingCart } from 'lucide-vue-next';
import { X } from 'lucide-vue-next';
import { useAuthStore } from '@/stores/auth'
import Pagination from '@/components/Pagination.vue';
import { useRoute, useRouter } from 'vue-router'


const auth = useAuthStore()

const cart = useCartStore()

interface Product {
  id: number
  title: string
  price:number
  description: string
  image_url: string
}

const toast = useToast()

const addToCartAndNotify = (item:Product) => {
  cart.addToCart(item)
  toast.success('Товар добавлен в корзину!')
}










const data = ref<Product[]>([])

const newTitle = ref('')
const count = ref(0)
const currentPage = ref(1)
const searchQuery = ref('')
const limit = 5
const totalPages = ref(1);


// загрузка начальных данных с бека и счетчик
const fetchItems = async (page = 1) => {
  try {
    const response = await axios.get('http://127.0.0.1:8000/items', {
      params: {
        page,
        limit,
        q: searchQuery.value
      }
    })

    data.value = response.data.items
    count.value = response.data.count
    totalPages.value = response.data.total_pages
    currentPage.value = page
  } catch (error) {
    console.error('Error fetchItems', error)
  }
}

const fetchCount = async () => {
  try {
    const response = await axios.get('http://127.0.0.1:8000/items/count')
    count.value = response.data.count
  } catch (error) {
    console.error('error count', error)
  }
}


// добавление нового товара

const addItem = async () => {
  if (!newTitle.value.trim()) return

  try {
    const response = await axios.post('http://127.0.0.1:8000/items', {
      title: newTitle.value,
    })

    fetchItems(currentPage.value)
    fetchCount()

  } catch (error) {
    console.error('add Error', error)
  } finally {
    newTitle.value = ''
  }
}


// Поиск по названию (при вводе)
const searchItems = () => {
  fetchItems(1)
}

//изменения названия по id (put)


// Поиск по id


const route = useRoute()
const router = useRouter()


const goToPage = (page: number) => {
  router.push({ query: { ...route.query, page } })
}

watch(() => route.query.page, (newPage) => {
  const page = parseInt(newPage as string) || 1
  fetchItems(page)
})

onMounted(() => {
  const pageFromRoute = parseInt(route.query.page as string) || 1
  fetchItems(pageFromRoute)
})
</script>

<template>
  <section class="bg-[#18181b] w-11/12 border rounded mx-auto mt-10">
    <div>
      <div class="text-center mt-4">
        <router-link
          v-if="!auth.isAuthenticated"
          class="text-2xl underline w-full hover:text-green-400"
          to="/login"
        >
          Login
        </router-link>
        <router-link
          v-else
          class="text-2xl underline w-full hover:text-green-400"
          to="/dashboard"
        >
          Go to Dashboard
        </router-link>
      </div>

      <div class="flex justify-between w-full p-2">
        <div>
          <span class="text-xl">Товаров всего: {{ totalPages * limit }}</span>
        </div>
        <div class="flex gap-4 items-center pr-4 pt-2">
          <input
            class="border rounded-md px-2 placeholder:text-indigo-50/30"
            v-model="searchQuery"
            @input="searchItems"
            placeholder="Поиск по названию"
          />
          <router-link to="/cart" class="w-full hover:text-[#34d399] hover:underline">
            <ShoppingCart class="hover:text-blue-600" />
          </router-link>
        </div>
      </div>

      <div class="flex w-full gap-4 items-center">
        <div v-for="item in data" :key="item.id" class="flex w-1/5 flex-col items-center p-2 gap-4">
          <div class="w-full relative">
            <img class="rounded" :src="item.image_url" :alt="item.title">
            <button
              @click="addToCartAndNotify(item)"
              class="hover:text-[#34d399] cursor-pointer transition-colors flex items-center gap-4 p-2 border rounded w-9/10 justify-center bg-black/40 absolute bottom-1 left-4"
            >
              <ShoppingCart /> Add to cart
            </button>
          </div>
          <router-link
            :to="`/product/${item.id}`"
            class="w-full text-center hover:text-[#34d399] transition-colors hover:underline"
          >
            {{ item.title }}
          </router-link>
          <span>{{ item.price }} руб.</span>
        </div>
      </div>

      <div class="flex gap-2 items-center place-self-center my-10">
        
    <Pagination
      :current-page="currentPage"
      :total-pages="totalPages"
      @update:page="goToPage"
    />
      </div>
    </div>
  </section>
</template>