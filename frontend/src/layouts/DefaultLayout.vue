<script lang="ts" setup>
import { ref, computed, nextTick, watch, } from "vue";
import { useAuthStore } from '@/stores/auth'
import { Toaster } from '@/components/ui/sonner'
import 'vue-sonner/style.css'
import { useCartStore } from '@/stores/cart'
import { useRouter } from 'vue-router'



const cart = useCartStore()

const auth = useAuthStore()

const { isAuthenticated } = storeToRefs(auth)

import {
  DropdownMenu,
  DropdownMenuTrigger,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
} from '@/components/ui/dropdown-menu'
import { Avatar, AvatarImage, AvatarFallback } from '@/components/ui/avatar'
import { Settings, LogOut, LayoutDashboard } from 'lucide-vue-next'
import {
    Drawer,
    DrawerClose,
    DrawerContent,
    DrawerDescription,
    DrawerHeader,
    DrawerTitle,
    DrawerTrigger,
} from '@/components/ui/drawer'

import { Button } from "@/components/ui/button";
import { Separator } from "@/components/ui/separator";

import { ChevronsDown, Menu, X, ShoppingCart } from "lucide-vue-next";
import { storeToRefs } from "pinia";



const isOpen = ref<boolean>(false);
const router = useRouter()


const displayName = computed(
  () => auth.user?.name?.trim() || auth.user?.email?.split('@')[0] || 'User'
)
const displayEmail = computed(() => auth.user?.email || '')
// store мы уже нормализовали: в user.avatar лежит абсолютный URL
const displayAvatar = computed(() => (auth.user as any)?.avatar || '')

async function onLogout() {
  try { await auth.logout() } finally { router.push('/login') }
}


</script>


<template>
    <div class="flex flex-col min-h-screen">
        
        <header
            class='w-[90%] 2xl:w-[75%]  mx-auto border border-border mt-10  rounded-2xl flex justify-between items-center p-2 bg-card shadow-md'>
            <router-link to="/" class="font-bold text-lg flex items-center">
                <ChevronsDown
                    class="bg-gradient-to-tr from-primary via-primary/70 to-primary rounded-lg w-9 h-9 mr-2 border border-transparent text-white" />
                ShadcnVue
            </router-link>

            <!-- Mobile -->

            <Drawer direction="left" v-model:open="isOpen">
                <DrawerTrigger class="lg:hidden" as-child>
                    <Button variant="ghost">
                        <Menu />
                    </Button>
                </DrawerTrigger>
                <DrawerContent
                    class="flex !w-full flex-col justify-between border-border rounded-tr-2xl rounded-br-2xl ">
                    <div>

                        <DrawerHeader class="bg-card p-2 mx-2 border border-border  my-10 rounded-2xl">
                            <DrawerTitle class="flex justify-between items-center">
                                <a href="/" class="flex items-center">
                                    <ChevronsDown
                                        class="bg-gradient-to-tr border-primary from-primary/70 via-primary to-primary/70 rounded-lg size-9 mr-2 border text-white" />
                                    ShadcnVue
                                </a>
                                <DrawerClose>
                                    <Button variant="ghost">
                                        <X />
                                    </Button>
                                </DrawerClose>
                            </DrawerTitle>

                            <DrawerDescription class="sr-only">
                                Navigation Menu
                            </DrawerDescription>
                        </DrawerHeader>
                        <div class="flex flex-col items-center gap-2">
                            <router-link to="/categories">Categories</router-link>
                            <router-link to="/">FAQ</router-link>
                            <router-link to="/">Reviews</router-link>
                            <router-link to="/">Contact Us</router-link>
                        </div>
                        <Separator class="my-4" />
                        <div class="flex flex-col gap-4 items-center">
                            <router-link class="hover:underline " to="/login">Login</router-link>
                            <router-link class="hover:underline " to="/register">Sign Up</router-link>
                        </div>
                        <div class="hidden flex-col items-center">
                            <router-link class="hover:underline " to="/categories">Categories</router-link>
                        </div>
                    </div>

                </DrawerContent>
            </Drawer>



            <!-- Desktop -->
            <nav class="hidden lg:block">
                <ul class="flex gap-4 items-center">
                    <li>
                        <router-link class="hover:underline " to="/categories">Categories</router-link>
                    </li>
                    <li>
                        <router-link class="hover:underline " to="/catalog">Catalog</router-link>
                    </li>
                    <li>
                        <router-link class="hover:underline " to="/login">Reviews</router-link>
                    </li>
                    <li>
                        <router-link class="hover:underline " to="/login">Contact Us</router-link>
                    </li>
                </ul>
            </nav>

            <div class="hidden lg:flex pr-2 xl:pr-4">
                <div class="flex justify-between gap-8 items-center">
                    <router-link to="/cart" class="relative hover:text-[#34d399] hover:underline">
                        <ShoppingCart class="hover:text-blue-600" />


                        <span v-if="cart.totalItems > 0"
                            class="absolute -top-2 -right-2 bg-red-600 text-white text-xs font-bold px-1.5 py-0.5 rounded-full">
                            {{ cart.totalItems }}
                        </span>
                    </router-link>
                    <div v-if="!isAuthenticated" class="flex items-center gap-4">
                        <router-link class="hover:underline " to="/login">Login</router-link>
                        <router-link class="hover:underline " to="/register">Sign Up</router-link>
                    </div>
                    <div v-else class="flex items-center">
  <DropdownMenu>
    <DropdownMenuTrigger as-child>
      <!-- ТРИГГЕР: только аватар -->
      <button
        class="inline-flex items-center justify-center rounded-full p-0.5 hover:bg-muted/50 transition"
        aria-label="Open user menu"
      >
        <Avatar class="h-8 w-8 rounded-full">
          <AvatarImage :src="displayAvatar" :alt="displayName" />
          <AvatarFallback class="rounded-full text-xs">
            {{ displayName.slice(0,2).toUpperCase() }}
          </AvatarFallback>
        </Avatar>
      </button>
    </DropdownMenuTrigger>

    <DropdownMenuContent class="min-w-56 border-border rounded-lg" align="end" :side-offset="8">
      <DropdownMenuLabel class="p-0 font-normal">
        <div class="flex items-center gap-2 px-2 py-2">
          <Avatar class="h-8 w-8 rounded-full">
            <AvatarImage :src="displayAvatar" :alt="displayName" />
            <AvatarFallback class="rounded-full text-xs">
              {{ displayName.slice(0,2).toUpperCase() }}
            </AvatarFallback>
          </Avatar>
          <div class="grid text-left leading-tight">
            <span class="truncate font-semibold text-sm">{{ displayName }}</span>
            <span class="truncate text-xs text-muted-foreground">{{ displayEmail }}</span>
          </div>
        </div>
      </DropdownMenuLabel>
        <DropdownMenuSeparator />
<router-link to="/dashboard" class="block">
        <DropdownMenuItem class="cursor-pointer">
          <LayoutDashboard class="mr-2 h-4 w-4" />
          Dashboard
        </DropdownMenuItem>
      </router-link>
      <DropdownMenuSeparator />

      <router-link to="/settings" class="block">
        <DropdownMenuItem class="cursor-pointer">
          <Settings class="mr-2 h-4 w-4" />
          Settings
        </DropdownMenuItem>
      </router-link>

      <DropdownMenuSeparator />

      <DropdownMenuItem class="cursor-pointer" @select="onLogout">
        <LogOut class="mr-2 h-4 w-4" />
        Log out
      </DropdownMenuItem>
    </DropdownMenuContent>
  </DropdownMenu>
</div>

                </div>


            </div>
        </header>


        <main class="flex-grow">
            <slot />
        </main>

        <footer
            class='w-[90%] 2xl:w-[75%]  mx-auto border border-border   rounded-2xl  p-4 lg:p-8 bg-card shadow-md mb-10'>
            <div class="grid grid-cols-2 md:grid-cols-4 xl:grid-cols-6 gap-x-12 gap-y-8">
                <div class="col-span-full xl:col-span-2">
                    <a href="#" class="flex font-bold items-center">
                        <ChevronsDown
                            class="bg-gradient-to-tr from-primary via-primary/70 to-primary rounded-lg w-9 h-9 mr-2 border border-transparent text-white" />

                        <h3 class="text-2xl">Shadcn-Vue</h3>
                    </a>
                </div>

                <div class="flex flex-col gap-2">
                    <h3 class="font-bold text-lg">Contact</h3>
                    <div>
                        <a href="#" class="opacity-60 hover:opacity-100">
                            Github
                        </a>
                    </div>

                    <div>
                        <a href="#" class="opacity-60 hover:opacity-100">
                            Twitter
                        </a>
                    </div>

                    <div>
                        <a href="#" class="opacity-60 hover:opacity-100">
                            Instagram
                        </a>
                    </div>
                </div>

                <div class="flex flex-col gap-2">
                    <h3 class="font-bold text-lg">Platforms</h3>
                    <div>
                        <a href="#" class="opacity-60 hover:opacity-100">
                            iOS
                        </a>
                    </div>

                    <div>
                        <a href="#" class="opacity-60 hover:opacity-100">
                            Android
                        </a>
                    </div>

                    <div>
                        <a href="#" class="opacity-60 hover:opacity-100">
                            Web
                        </a>
                    </div>
                </div>

                <div class="flex flex-col gap-2">
                    <h3 class="font-bold text-lg">Help</h3>
                    <div>
                        <a href="#" class="opacity-60 hover:opacity-100">
                            Contact Us
                        </a>
                    </div>

                    <div>
                        <a href="#" class="opacity-60 hover:opacity-100">
                            FAQ
                        </a>
                    </div>

                    <div>
                        <a href="#" class="opacity-60 hover:opacity-100">
                            Feedback
                        </a>
                    </div>
                </div>

                <div class="flex flex-col gap-2">
                    <h3 class="font-bold text-lg">Socials</h3>
                    <div>
                        <a href="#" class="opacity-60 hover:opacity-100">
                            Twitch
                        </a>
                    </div>

                    <div>
                        <a href="#" class="opacity-60 hover:opacity-100">
                            Discord
                        </a>
                    </div>

                    <div>
                        <a href="#" class="opacity-60 hover:opacity-100">
                            Dribbble
                        </a>
                    </div>
                </div>
            </div>

        </footer>
    </div>
    <Toaster />
</template>