<script setup lang="ts">
import { ref, onMounted, watch, computed } from 'vue';
import axios from 'axios';
import { useCartStore } from '@/stores/cart';
import { useToast } from 'vue-toastification'
import { ShoppingCart } from 'lucide-vue-next';
import { X } from 'lucide-vue-next';
import { useAuthStore } from '@/stores/auth'
import Pagination from '@/components/Pagination.vue';
import { useRoute, useRouter } from 'vue-router'
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

const auth = useAuthStore()

const cart = useCartStore()

interface Product {
  id: number
  name: string
  price: number
  description: string
  image: string
}

const toast = useToast()

const addToCartAndNotify = (item: Product) => {
  cart.addToCart(item)
  toast.success('Товар добавлен в корзину!')
}



const data = ref<Product[]>([])

const currentPage = ref(1);

const limit = ref(10); // лимит на страницу

const searchQuery = ref("");

const sortType = ref<"alpha" | "price">("alpha"); // активный тип сортировки
const sortOrder = ref<"asc" | "desc">("asc"); // направление


// загрузка начальных данных с бека и счетчик
const fetchItems = async () => {
  try {
    const response = await axios.get("http://127.0.0.1:8000/items", {
      params: {
        page: 1,
        limit: 100 // грузим всё
      }
    });
    data.value = response.data.items;
  } catch (error) {
    console.error("Error fetchItems", error);
  }
};

// сортировка

const filteredAndSortedItems = computed(() => {
  let result = [...data.value];

  // Фильтрация по поиску
  if (searchQuery.value.trim()) {
    const q = searchQuery.value.toLowerCase();
    result = result.filter(item => item.name.toLowerCase().includes(q));
  }

  // Сортировка
  if (sortType.value === "alpha") {
    result.sort((a, b) => {
      const dir = sortOrder.value === "asc" ? 1 : -1;
      return a.name.localeCompare(b.name) * dir;
    });
  } else if (sortType.value === "price") {
    result.sort((a, b) => {
      const dir = sortOrder.value === "asc" ? 1 : -1;
      return (a.price - b.price) * dir;
    });
  }

  return result;
});


const paginatedItems = computed(() => {
  const start = (currentPage.value - 1) * limit.value;
  const end = start + limit.value;
  return filteredAndSortedItems.value.slice(start, end);
});


const totalPages = computed(() => {
  return Math.ceil(filteredAndSortedItems.value.length / limit.value);
});



// Поиск по названию (при вводе)
const searchItems = () => {
  fetchItems()
}

//pagination




// Поиск по id


const route = useRoute()
const router = useRouter()


function goToPage(page: number) {
  currentPage.value = page;
}

watch(() => route.query.page, (newPage) => {
  const page = parseInt(newPage as string) || 1
  fetchItems()
})

onMounted(() => {
  const pageFromRoute = parseInt(route.query.page as string) || 1
  fetchItems()
})
</script>

<template>

  <DefaultLayout>
    <section class=" w-[90%] 2xl:w-[75%]  mx-auto  rounded  mt-10">
      <div>

        <div class="flex flex-col items-center gap-4 justify-between w-full p-2">
          <div>
            <span class="text-xl">Товаров всего: {{ filteredAndSortedItems.length }}</span>
          </div>
          <div class="flex gap-4 items-center pr-4 pt-2">
            <input class="border rounded-md px-2 placeholder:text-indigo-50/30" v-model="searchQuery"
              @input="searchItems" placeholder="Поиск по названию" />

            <select v-model="sortOrder" @focus="sortType = 'alpha'" class="border rounded px-2">
              <option value="asc">A → Z</option>
              <option value="desc">Z → A</option>
            </select>

            <!-- Сортировка по цене -->
            <select v-model="sortOrder" @focus="sortType = 'price'" class="border rounded px-2">
              <option value="asc">Цена ↑</option>
              <option value="desc">Цена ↓</option>
            </select>
            <router-link to="/cart" class="w-full hover:text-[#34d399] hover:underline">
              <ShoppingCart class="hover:text-blue-600" />
            </router-link>
          </div>
        </div>

        <div class="flex flex-wrap w-full gap-4 mt-4  justify-between items-center">
          <Card v-for="item in paginatedItems" :key="item.id"
            class="bg-muted/60 dark:bg-card flex flex-col w-full  max-w-xs md:max-w-none mx-auto md:w-[30%] lg:w-[23%] xl:w-[20%]  2xl:w-[18%] h-full overflow-hidden group/hoverimg border-border">
            <CardHeader class="p-0 gap-0">
              <div class="h-full overflow-hidden">
                <img :src="item.image" alt=""
                  class="w-full aspect-square object-cover saturate-0 transition-all duration-200 ease-linear size-full group-hover/hoverimg:saturate-100 group-hover/hoverimg:scale-[1.01]" />
              </div>
              <CardTitle class="py-6 pb-4 px-6">
                <span class="hover:text-primary cursor-pointer">{{ item.name }}</span>
              </CardTitle>
            </CardHeader>
            <CardContent class='text-muted-foreground '>
              {{ item.price }} $
            </CardContent>

            <CardFooter class="space-x-4 mt-auto">
              <Button class="cursor-pointer w-full">
                <ShoppingCart /> Add to cart
              </Button>
            </CardFooter>
          </Card>


          <!-- <div v-for="item in data" :key="item.id" class="flex w-[18%] flex-col items-center p-2 gap-4">
          <div class="w-full relative">
            <img class="rounded" :src="item.image_url" :alt="item.title">
            <Button
              @click="addToCartAndNotify(item)"
              class="hover:text-[#34d399] cursor-pointer transition-colors flex items-center gap-4 p-2 border rounded w-9/10 justify-center bg-black/40 absolute bottom-1 left-4"
            >
              <ShoppingCart /> Add to cart
            </Button>
          </div>
          <router-link
            :to="`/product/${item.id}`"
            class="w-full text-center hover:text-[#34d399] transition-colors hover:underline"
          >
            {{ item.title }}
          </router-link>
          <span>{{ item.price }} руб.</span>
        </div> -->
        </div>

        <div class="flex gap-2 items-center place-self-center my-10">

          <Pagination :current-page="currentPage" :total-pages="totalPages" @update:page="goToPage" />
        </div>
      </div>
    </section>
  </DefaultLayout>


</template>