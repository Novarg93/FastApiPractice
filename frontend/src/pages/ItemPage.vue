<script setup lang="ts">
import { onMounted, ref, computed } from "vue";
import { useRoute } from "vue-router";
import axios from "axios";
import DefaultLayout from "@/layouts/DefaultLayout.vue";
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from '@/components/ui/card'
import { ShoppingCart, MessageCircleQuestion } from 'lucide-vue-next';
import { Label } from '@/components/ui/label'
import { RadioGroup, RadioGroupItem } from '@/components/ui/radio-group'
import { Separator } from "@/components/ui/separator"
import { Checkbox } from "@/components/ui/checkbox"
import type { BreadcrumbItem } from '@/types'; // vue-sonner v2 requires this import
import Button from '@/components/ui/button/Button.vue';

import {
  NumberField,
  NumberFieldContent,
  NumberFieldDecrement,
  NumberFieldIncrement,
  NumberFieldInput,
} from "@/components/ui/number-field"
import { Slider } from '@/components/ui/slider'
import {
  Tabs,
  TabsContent,
  TabsList,
  TabsTrigger,
} from "@/components/ui/tabs"
import {
  Select,
  SelectContent,
  SelectGroup,
  SelectItem,
  SelectLabel,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select'
import {
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger
} from '@/components/ui/tooltip'
import BaseTooltip from '@/components/BaseTooltip.vue';
import { toast } from 'vue-sonner'
import { useCartStore } from '@/stores/cart';


interface Item {
  id: number;
  name: string;
  price: number;
  image?: string;
}

const cart = useCartStore()



const addToCartAndNotify = (item: Item) => {
  cart.addToCart(item)
  toast.success('Succesfully added to cart')
}

const route = useRoute();
const item = ref<Item | null>(null);
const loading = ref(true);

const fetchItem = async () => {
  try {
    const res = await axios.get(`http://127.0.0.1:8000/items/${route.params.id}`);
    item.value = res.data;
  } catch (err) {
    console.error("Ошибка загрузки товара", err);
  } finally {
    loading.value = false;
  }
};


const formData = ref({
  radioOption: "",
  checkOptions: [] as string[],
  quantity: 1,
  sliderQuantity: 1,
  buttonOption: "",
  selectOption: ""
});

function formatCurrency(amount: number, currency: string): string {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency,
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  }).format(amount);
}

const imageUrl = computed(() => {
  return `/images/${item.value?.image || 'placeholder.png'}`
})

function submitForm() {
  console.log("Form submitted:", formData.value);
}
onMounted(fetchItem);
</script>

<template>

  <DefaultLayout>
    <section class="w-[90%] 2xl:w-[75%] mx-auto py-12 md:py-20">
      <router-link to="/catalog" class="text-blue-500 underline">← Назад в каталог</router-link>

      <div v-if="loading" class="mt-6">Загрузка...</div>

      <div v-else-if="item" class="mt-6 ">
        <h1 class="mt-4 mb-8 text-4xl lg:text-5xl font-semibold text-pretty">{{ item.name }}</h1>
        <div class="flex flex-col md:flex-row gap-12  w-full">
          <div :style="{
    backgroundImage: `url('/images/${item?.image || 'placeholder.png'}')`
  }"
            class="before:content-[] relative md:hidden min-h-auto w-full  overflow-hidden rounded-[.5rem]  bg-cover bg-top bg-no-repeat  transition-all duration-300 before:absolute before:top-0 before:left-0 before:z-10 before:block before:size-full  before:transition-all before:duration-300  sm:aspect-square md:aspect-auto md:min-h-[30rem] md:max-w-[30rem]">
            <div class="relative z-20 flex size-full flex-col justify-between gap-20 md:gap-16">
              <div class="text-2xl leading-[1.2] font-normal text-white md:text-3xl p-5">{{ item.name }}</div>
              <div
                class="flex w-full flex-col gap-8 p-5 pt-13  bg-gradient-to-b  from-transparent via-black/80 to-black/70">
                <div class="flex gap-8 text-white">
                  <div class="flex flex-col gap-1">

                    <div class="text-sm  product">
                      <ul>
                        <li>lol</li>
                        <li>kek</li>
                        <li>cheburek</li>
                      </ul>
                    </div>
                  </div>
                </div>

              </div>
            </div>
          </div>
          <article class="prose dark:prose-invert order-2 w-full   md:order-1">
            <div>
              <img @error="(e) => e.target.src = '/images/placeholder.png'" :src="`/images/${item.image}`"
                :alt="item.name"
                class="mt-0 mb-8 aspect-video w-full hidden md:block rounded-lg object-contain object-top" />
            </div>


            <div class="legal">Product Description</div>

          </article>

          <Card class="order-1 md:w-3/4 md:order-2 border-border   h-fit">
            <TooltipProvider>
              <form @submit.prevent="submitForm">
                <CardHeader>
                  <CardTitle class="text-3xl font-semibold pb-6 border-b">Product options</CardTitle>
                </CardHeader>

                <CardContent class=" py-6 ">


                  <fieldset>
                    <legend class="font-medium mb-4">Radio options</legend>
                    <RadioGroup default-value="comfortable" :orientation="'vertical'">
                      <div class="flex justify-between items-center ">
                        <div class="flex items-center gap-2">
                          <RadioGroupItem id="r1" value="default" />
                          <Label class="text-base" for="r1">Radio1</Label>
                        </div>
                        <div class="flex items-center gap-2">
                          <span>+5$</span>
                          <BaseTooltip>
                            <template #trigger>
                              <MessageCircleQuestion class="size-5 hover:text-primary" />
                            </template>
                            <p>Note</p>
                          </BaseTooltip>

                        </div>

                      </div>
                      <div class="flex justify-between items-center ">
                        <div class="flex items-center gap-2">
                          <RadioGroupItem id="r2" value="Radio2" />
                          <Label class="text-base" for="r2">Radio2</Label>
                        </div>
                        <div class="flex items-center gap-2">
                          <span>+5$</span>
                          <BaseTooltip>
                            <template #trigger>
                              <MessageCircleQuestion class="size-5 hover:text-primary" />
                            </template>
                            <p>Note</p>
                          </BaseTooltip>

                        </div>

                      </div>
                      <div class="flex justify-between items-center">
                        <div class="flex items-center gap-2">
                          <RadioGroupItem id="r3" value="Radio3" />
                          <Label class="text-base" for="r3">Radio3</Label>
                        </div>
                        <div class="flex items-center gap-2">
                          <span>+5$</span>
                          <BaseTooltip>
                            <template #trigger>
                              <MessageCircleQuestion class="size-5 hover:text-primary" />
                            </template>
                            <p>Note</p>
                          </BaseTooltip>

                        </div>

                      </div>
                    </RadioGroup>
                  </fieldset>

                  <Separator class="mb-6 mt-8" />


                  <fieldset>
                    <legend class="font-medium mb-4">Checkbox options</legend>

                    <div class="flex flex-col gap-4">
                      <div class="flex justify-between items-center space-x-2">
                        <div class="flex items-center space-x-2">
                          <Checkbox id="c1" />
                          <Label class="text-base" for="c1">Checkbox-1</Label>

                        </div>
                        <div class="flex items-center gap-2">
                          <span>+5$</span>
                          <BaseTooltip>
                            <template #trigger>
                              <MessageCircleQuestion class="size-5 hover:text-primary" />
                            </template>
                            <p>Note</p>
                          </BaseTooltip>

                        </div>
                      </div>

                      <div class="flex justify-between items-center space-x-2">
                        <div class="flex items-center space-x-2">
                          <Checkbox id="c2" />
                          <Label class="text-base" for="c2">Checkbox-2</Label>

                        </div>
                        <div class="flex items-center gap-2">
                          <span>+5$</span>
                          <BaseTooltip>
                            <template #trigger>
                              <MessageCircleQuestion class="size-5 hover:text-primary" />
                            </template>
                            <p>Note</p>
                          </BaseTooltip>

                        </div>
                      </div>

                      <div class="flex justify-between items-center space-x-2">
                        <div class="flex items-center space-x-2">
                          <Checkbox id="c3" />
                          <Label class="text-base" for="c3">Checkbox-1</Label>

                        </div>
                        <div class="flex items-center gap-2">
                          <span>+5$</span>
                          <BaseTooltip>
                            <template #trigger>
                              <MessageCircleQuestion class="size-5 hover:text-primary" />
                            </template>
                            <p>Note</p>
                          </BaseTooltip>

                        </div>
                      </div>
                    </div>


                  </fieldset>

                  <Separator class="mb-6 mt-8" />





                  <fieldset>
                    <legend class="font-medium mb-4">Numberfield options</legend>
                    <NumberField id="age" :default-value="18" :min="0">
                      <Label class="mb-4 text-base" for="age">Quantity</Label>
                      <NumberFieldContent>
                        <NumberFieldDecrement />
                        <NumberFieldInput class="bg-background border-2 border-secondary-foreground/70" />
                        <NumberFieldIncrement />
                      </NumberFieldContent>
                    </NumberField>
                  </fieldset>

                  <Separator class="mb-6 mt-8" />


                  <fieldset>
                    <legend class="font-medium mb-4 ">Quantity slider: {{ formData.sliderQuantity }}
                    </legend>
                    <Slider :model-value="[formData.sliderQuantity]" :default-value="[1]" :max="100" :step="1"
                      @update:model-value="val => formData.sliderQuantity = val[0]" :min="0" />
                  </fieldset>

                  <Separator class="mb-6 mt-8" />

                  <div>
                    <Tabs default-value="selfplay" class="w-full">
                      <TabsList class="grid mb-4 w-full bg-input border-secondary-foreground/70 grid-cols-2">
                        <TabsTrigger class="dark:data-[state=active]:border-primary " value="selfplay">
                          Selfplay
                        </TabsTrigger>
                        <TabsTrigger class="dark:data-[state=active]:border-primary " value="piloted">
                          Piloted
                        </TabsTrigger>
                      </TabsList>
                      <TabsContent class="space-y-4" value="selfplay">

                        <div class="flex items-center space-x-2">
                          <Checkbox id="so1" />
                          <Label class="text-base" for="so1">Selfplay option-1</Label>
                        </div>
                        <div class="flex items-center space-x-2">
                          <Checkbox id="so2" />
                          <Label class="text-base" for="so2">Selfplay option-2</Label>
                        </div>
                        <div class="flex items-center space-x-2">
                          <Checkbox id="so3" />
                          <Label class="text-base" for="so3">Selfplay option-3</Label>
                        </div>

                      </TabsContent>
                      <TabsContent class="space-y-4" value="piloted">

                        <div class="flex items-center space-x-2">
                          <Checkbox id="so1" />
                          <Label class="text-base" for="so1">Piloted option-1</Label>
                        </div>
                        <div class="flex items-center space-x-2">
                          <Checkbox id="so2" />
                          <Label class="text-base" for="so2">Piloted option-2</Label>
                        </div>
                        <div class="flex items-center space-x-2">
                          <Checkbox id="so3" />
                          <Label class="text-base" for="so3">Piloted option-3</Label>
                        </div>

                      </TabsContent>
                    </Tabs>
                  </div>

                  <Separator class="mb-6 mt-8" />


                  <Select>
                    <SelectTrigger class="w-full">
                      <SelectValue placeholder="Piloted" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectGroup>

                        <SelectItem class="w-full " value="Piloted">
                          Piloted
                        </SelectItem>
                        <SelectItem class="w-full " value="Selfplay">
                          Selfplay
                        </SelectItem>
                      </SelectGroup>
                    </SelectContent>
                  </Select>
                </CardContent>

                <CardFooter>
                  <div class="flex flex-col pt-6 border-t w-full gap-2">

                    <div class="flex flex-col gap-1">
                      <span>ETA start: <span class="text-lg font-semibold ml-2">1 hour</span>
                      </span>
                      <span>ETA completion: <span class="text-lg font-semibold ml-2">3
                          hours</span></span>
                    </div>
                    <Button @click="addToCartAndNotify(item)" type="submit" class="w-full mt-6 cursor-pointer">
                      <ShoppingCart />
                      Add to cart
                    </Button>
                  </div>
                </CardFooter>
              </form>
            </TooltipProvider>
          </Card>
        </div>


      </div>

      <div v-else class="mt-6 text-red-500">
        Товар не найден.
      </div>
    </section>

  </DefaultLayout>



</template>