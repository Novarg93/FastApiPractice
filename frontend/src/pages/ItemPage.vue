<script setup lang="ts">
import { onMounted, ref } from "vue";
import { useRoute } from "vue-router";
import axios from "axios";

interface Item {
  id: number;
  name: string;
  price: number;
  image?: string;
}

const route = useRoute();
const item = ref<Item | null>(null);
const loading = ref(true);

const fetchItem = async () => {
  try {
    const res = await axios.get(`http://127.0.0.1:8000/items/${route.params.id}`);
    item.value = res.data;
  } catch (err) {
    console.error("Ошибка загрузки товара", err);
  } finally {
    loading.value = false;
  }
};

onMounted(fetchItem);
</script>

<template>
  <div class="p-6">
    <router-link to="/" class="text-blue-500 underline">← Назад в каталог</router-link>

    <div v-if="loading" class="mt-6">Загрузка...</div>

    <div v-else-if="item" class="mt-6 max-w-xl">
      <img
        :src="item.image"
        alt="Картинка товара"
        class="w-full rounded-lg shadow"
      />

      <h1 class="text-3xl font-bold mt-4">{{ item.name }}</h1>
      <p class="text-lg text-gray-700 mt-2">{{ item.price }} ₽</p>
    </div>

    <div v-else class="mt-6 text-red-500">
      Товар не найден.
    </div>
  </div>
</template>