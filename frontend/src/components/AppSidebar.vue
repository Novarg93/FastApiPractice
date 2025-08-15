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
import { useAuthStore } from '@/stores/auth'
import { storeToRefs } from 'pinia'
import { computed, onMounted } from 'vue'
import { toAbsolute } from '@/lib/http'


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

const auth = useAuthStore()
const { user, isAuthenticated, loading } = storeToRefs(auth)

onMounted(() => {
  if (!user.value) auth.fetchMe().catch(() => {})
})


const sidebarUser = computed(() => {
  const u = auth.user as any
  return {
    name:  (u?.name ?? u?.email?.split('@')[0] ?? 'User') as string,
    email: (u?.email ?? '') as string,
    
    avatar: toAbsolute(u?.avatar ?? u?.avatar_url) || '',
  }
})

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
      <NavUser class="rounded-lg hover:bg-muted/50" :user="sidebarUser" />
    </SidebarFooter>
    <SidebarRail />
  </Sidebar>
</template>