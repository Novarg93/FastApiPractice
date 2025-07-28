<script setup lang="ts">
import { onMounted, ref } from 'vue'
const message = ref('')

onMounted(async () => {
  const res = await fetch('http://localhost:8000/')
  const data = await res.json()
  message.value = data.message
})
</script>

<template>
  <div class="p-4 text-xl font-bold">
    {{ message }}
  </div>
</template>