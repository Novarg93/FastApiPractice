<script setup lang="ts">
import DefaultLayout from '@/layouts/DefaultLayout.vue';

import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from '@/components/ui/card'
import Button from '@/components/ui/button/Button.vue';
import Input from '@/components/ui/input/Input.vue';
import { useCartStore } from '@/stores/cart'

const cart = useCartStore()
</script>

<template>
  <DefaultLayout>
    
    <section class="w-[90%] 2xl:w-[75%] mx-auto rounded mt-10 py-12 lg:pb-20">
      <div class="mx-auto max-w-screen-xl px-4 2xl:px-0">
        <h2 class="text-xl font-semibold sm:text-2xl">Shopping Cart ({{ cart.totalItems }})</h2>

        <div class="mt-6 sm:mt-8 md:gap-6 lg:flex lg:items-start xl:gap-8">
          <!-- Лист товаров -->
          <div class="mx-auto w-full flex-none lg:max-w-2xl xl:max-w-4xl">
            <div class="space-y-6">

              <Card v-for="it in cart.items" :key="it.id" class="border-border">
                <CardHeader class="flex items-center justify-between gap-6">
                  <!-- image -->
                  <a :href="`/item/${it.id}`" class="shrink-0">
                    <img  @error="(e) => e.target.src = '/images/placeholder.png'" :src="`/images/${it.image}`" :alt="it.name" class="h-20 w-20 rounded object-cover" />
                  </a>

                  <!-- title + actions -->
                  <div class="flex-1 min-w-0">
                    <router-link :to="`/item/${it.id}`" class="text-base font-medium hover:underline">
                      {{ it.name }}
                    </router-link>

                    <div class="flex items-center gap-4 mt-2">
                      <Button variant="ghost" size="sm">❤️ Add to Favorites</Button>
                      <Button variant="ghost" size="sm" class="text-red-600" @click="cart.remove(it.id)">❌ Remove</Button>
                    </div>
                  </div>

                  <!-- qty + price -->
                  <div class="flex items-center gap-4">
                    <div class="flex items-center gap-2">
                      <Button variant="outline" size="icon" @click="cart.decrement(it.id)">−</Button>
                      <Input
                        class="w-14 text-center"
                        :model-value="it.quantity"
                        @update:model-value="(v: string | number) => cart.setQuantity(it.id, Number(v))"
                        type="number" min="1"
                      />
                      <Button variant="outline" size="icon" @click="cart.increment(it.id)">＋</Button>
                    </div>
                    <div class="text-end w-28">
                      <p class="text-base font-bold">{{ it.price * it.quantity }}$</p>
                    </div>
                  </div>
                </CardHeader>
              </Card>

              <!-- Пустая корзина -->
              <Card v-if="cart.items.length === 0" class="border-dashed">
                <CardContent class="py-10 text-center text-muted-foreground">
                  Корзина пуста. <router-link to="/catalog" class="underline">Вернуться в каталог</router-link>
                </CardContent>
              </Card>
            </div>
          </div>

          <!-- Summary -->
          <div class="mx-auto mt-6 max-w-4xl flex-1 space-y-6 lg:mt-0 lg:w-full">
            <Card class="border-border">
              <CardContent class="space-y-4 pt-6">
                <p class="text-xl font-semibold">Order summary</p>

                <div class="space-y-2">
                  <div class="flex items-center justify-between">
                    <span>Items</span>
                    <span>{{ cart.totalItems }}</span>
                  </div>
                  <div class="flex items-center justify-between">
                    <span>Subtotal</span>
                    <span class="font-medium">{{ cart.subtotal }}$</span>
                  </div>
                </div>

                <Button class="w-full" :disabled="cart.items.length === 0" @click="$router.push('/checkout')">
                  Proceed to Checkout
                </Button>

                <Button variant="ghost" class="w-full" @click="cart.clear" :disabled="cart.items.length === 0">
                  Clear cart
                </Button>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </section>
  </DefaultLayout>
</template>