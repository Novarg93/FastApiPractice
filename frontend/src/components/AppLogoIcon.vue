<script setup lang="ts">
import { ChevronsDown } from "lucide-vue-next";
import { useSidebar } from '@/components/ui/sidebar'
import { computed } from 'vue'

let isCollapsed = computed(() => false) // fallback

try {
  const { state } = useSidebar()
  isCollapsed = computed(() => state.value === 'collapsed')
} catch (err) {
  // useSidebar not available (e.g. outside of SidebarProvider)
  console.warn('AppLogoIcon: useSidebar not found. Assuming not collapsed.')
}
</script>

<template>
  <router-link
    v-if="!isCollapsed"
    to="/"
    class="font-bold text-lg flex items-center"
  >
    <ChevronsDown
      class="bg-gradient-to-tr from-primary via-primary/70 to-primary rounded-lg w-9 h-9 mr-2 border border-transparent text-white"
    />
    <span>ShadcnVue</span>
  </router-link>

  <div v-else class="flex items-center justify-center ">
    <ChevronsDown
      class="bg-gradient-to-tr from-primary via-primary/70 to-primary rounded-lg border border-transparent text-white"
    />
  </div>
</template>
