<script lang="ts" setup>
import { computed } from 'vue';
import { defineProps, defineEmits } from 'vue';
import { Button } from './ui/button';



const props = defineProps<{
  currentPage: number;
  totalPages: number;
}>();

const emit = defineEmits<{
  (e: 'update:page', page: number): void;
}>();

function goToPage(page: number) {
  if (page >= 1 && page <= props.totalPages) {
    emit('update:page', page);
  }
}

function getPagination(currentPage: number, totalPages: number): (number | string)[] {
  const pages: (number | string)[] = []
  const delta = 2

  const start = Math.max(1, currentPage - delta)
  const end = Math.min(totalPages, currentPage + delta)

  for (let i = start; i <= end; i++) {
    pages.push(i)
  }

  // если после текущего диапазона есть пропущенные страницы перед totalPages
  if (totalPages > end) {
    if (totalPages > end + 1) {
      pages.push('...')
    }
    pages.push(totalPages)
  }

  return pages
}


const pagination = computed(() => getPagination(props.currentPage, props.totalPages));
</script>



<template>
  <nav class="pagination flex gap-2 items-center">
    <Button class="cursor-pointer" variant="ghost" @click="goToPage(1)" :disabled="currentPage === 1">
      &laquo;
    </Button>
    <Button class="cursor-pointer" variant="ghost" @click="goToPage(currentPage - 1)" :disabled="currentPage === 1">
      &lt;
    </Button>

    <Button v-for="page in pagination" :key="page" variant="ghost"
      :class="page === currentPage ? ' font-bold text-black bg-white ' : 'cursor-pointer'"
      @click="typeof page === 'number' && goToPage(page)"
      :disabled="typeof page !== 'number'"
      >
      {{ page }}
    </Button>

    <Button class="cursor-pointer" variant="ghost" @click="goToPage(currentPage + 1)"
      :disabled="currentPage === totalPages">
      &gt;
    </Button>
    <Button class="cursor-pointer" variant="ghost" @click="goToPage(totalPages)" :disabled="currentPage === totalPages">
      &raquo;
    </Button>
  </nav>
</template>