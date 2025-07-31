<script setup lang="ts">
import type { SidebarProps } from '@/components/ui/sidebar'
import {
  LayoutGrid,
  MessageCircle,
  Wallet,
  Command,
  Frame,
  GalleryVerticalEnd,
  Map,
  PieChart,
  Settings2,
  SquareTerminal,
  AudioWaveform,
  Bot,
  BookOpen
} from 'lucide-vue-next'
import { type NavItem } from '@/types';
import NavMain from '@/components/NavMain.vue'
import NavUser from '@/components/NavUser.vue'
import AppLogoIcon from './AppLogoIcon.vue'
import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarHeader,
  SidebarRail,
} from '@/components/ui/sidebar'
const props = withDefaults(defineProps<SidebarProps>(), {
  collapsible: 'icon',
})

const mainNavItems: NavItem[] = [
    {
        title: 'Profile',
        href: '/dashboard',
        icon: LayoutGrid,
    },
    {
        title: 'Messages',
        href: '/dashboard',
        icon: MessageCircle,
    },
    {
        title: 'Wallet',
        href: '/dashboard',
        icon: Wallet,
    },
];

const data = {
  user: {
    name: 'shadcn',
    email: 'm@example.com',
    avatar: '/avatars/shadcn.jpg',
  }, 
  
}
</script>
<template>
  <Sidebar class="border-transparent bg-muted/30  " v-bind="props">
    <SidebarHeader>
      <AppLogoIcon class="mt-2 0  "/>
    </SidebarHeader>
    <SidebarContent>
      <NavMain :items="mainNavItems" />      
    </SidebarContent>
    <SidebarFooter>
      <NavUser class="rounded-lg hover:bg-muted/50" :user="data.user" />
    </SidebarFooter>
    <SidebarRail />
  </Sidebar>
</template>