<script setup lang="ts">
import { Tooltip, TooltipContent, TooltipTrigger } from '@/components/ui/tooltip'
</script>

<template>
  <Tooltip>
    <TooltipTrigger as-child>
      <slot name="trigger" />
    </TooltipTrigger>
    <TooltipContent>
      <slot />
    </TooltipContent>
  </Tooltip>
</template>
