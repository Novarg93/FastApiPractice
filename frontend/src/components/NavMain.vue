<script setup lang="ts">

import { useRoute } from 'vue-router'


import {
  SidebarGroup,
  SidebarGroupLabel,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,

} from '@/components/ui/sidebar'
import { type NavItem } from '@/types';
const route = useRoute()
defineProps<{
    items: NavItem[];
}>();


</script>
<template>
  <SidebarGroup>
    <SidebarGroupLabel>Platform</SidebarGroupLabel>
    <SidebarMenu>
      <SidebarMenuItem class=" rounded-lg hover:bg-muted"  :class="item.href === route.path ? 'bg-muted' : ''"   v-for="item in items" :key="item.title">
                <SidebarMenuButton   as-child :is-active="item.href === route.path" :tooltip="item.title">
                    <router-link :to="item.href">
                        <component :is="item.icon" />
                        <span>{{ item.title }}</span>
                    </router-link>
                </SidebarMenuButton>
            </SidebarMenuItem>
    </SidebarMenu>
  </SidebarGroup>
</template>
