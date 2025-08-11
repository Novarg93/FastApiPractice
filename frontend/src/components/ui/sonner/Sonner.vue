<script lang="ts" setup>
import type { ToasterProps } from "vue-sonner"
import { Toaster as Sonner } from "vue-sonner"

const props = defineProps<ToasterProps>()
</script>

<template>
  <Sonner
    v-bind="props"
    class="toaster group"
    :style="{
      /* обычные тосты */
      '--normal-bg': `hsl(var(--background))`,
      '--normal-text': `hsl(var(--popover-foreground))`,
      '--normal-border': `hsl(var(--border))`,

      /* success */
      '--success-bg': `hsl(var(--background))`,
      '--success-text': `hsl(var(--primary-foreground))`,
      '--success-border': `hsl(var(--border))`,

      /* error */
      '--error-bg': `hsl(var(--destructive))`,
      '--error-text': `hsl(var(--destructive-foreground))`,
      '--error-border': `hsl(var(--destructive))`,

      /* info */
      '--info-bg': `hsl(var(--secondary))`,
      '--info-text': `hsl(var(--secondary-foreground))`,
      '--info-border': `hsl(var(--secondary))`,
    }"
  />
</template>
