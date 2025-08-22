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


type OptionSelection =
  | { type: 'radio' | 'select'; choiceId: number | null }
  | { type: 'checkbox'; choiceIds: number[] }
  | { type: 'slider' | 'number'; value: number };

type UiOption = {
  id: number
  name: string
  type: 'radio' | 'checkbox' | 'select' | 'slider' | 'number'
  label: string
  min_value?: number | null
  max_value?: number | null
  step?: number | null
  choices: {
    id: number
    value: string
    label: string
    pct: number
    abs_cents: number
    multiplier: number
    sort_order: number
  }[]
  product_meta?: {
    is_required: boolean
    sort_order: number
  } | null
}

interface Item {
  id: number
  name: string
  price: number
  image?: string | null
  options: UiOption[]
}

const selections = ref<Record<number, OptionSelection>>({}) // key: option.id

const basePriceCents = computed(() => Math.round((item.value?.price || 0) * 100))

const finalPriceCents = computed(() => {
  let cents = basePriceCents.value
  let multiplier = 1.0

  for (const opt of item.value?.options ?? []) {
    const sel = selections.value[opt.id]
    if (!sel) continue

    if (opt.type === 'radio' || opt.type === 'select') {
      const ch = opt.choices.find(c => c.id === (sel as any).choiceId)
      if (ch) {
        cents += ch.abs_cents
        cents = Math.round(cents * (1 + ch.pct))
        multiplier *= ch.multiplier
      }
    } else if (opt.type === 'checkbox') {
      const ids = (sel as any).choiceIds as number[]
      for (const id of ids) {
        const ch = opt.choices.find(c => c.id === id)
        if (!ch) continue
        cents += ch.abs_cents
        cents = Math.round(cents * (1 + ch.pct))
        multiplier *= ch.multiplier
      }
    } else if (opt.type === 'slider' || opt.type === 'number') {
      const val = (sel as any).value as number
      // пример: множитель на количество
      multiplier *= val
    }
  }

  cents = Math.round(cents * multiplier)
  return cents
})

const finalPriceFormatted = computed(() =>
  new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' })
    .format(finalPriceCents.value / 100)
)


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

onMounted(async () => {
  await fetchItem()
  // Проставим дефолты
  for (const opt of item.value?.options ?? []) {
    if (opt.type === 'radio' || opt.type === 'select') {
      const first = opt.choices[0]
      selections.value[opt.id] = { type: opt.type, choiceId: first ? first.id : null }
    } else if (opt.type === 'checkbox') {
      selections.value[opt.id] = { type: 'checkbox', choiceIds: [] }
    } else if (opt.type === 'slider' || opt.type === 'number') {
      const min = opt.min_value ?? 1
      selections.value[opt.id] = { type: opt.type, value: min }
    }
  }
})
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

                <CardContent class="py-6 space-y-8">
                  <template v-for="opt in item.options" :key="opt.id">
                    <!-- RADIO -->
                    <fieldset v-if="opt.type === 'radio'">
                      <legend class="font-medium mb-4">{{ opt.label }} <span v-if="opt.product_meta?.is_required"
                          class="text-red-500">*</span></legend>
                      <RadioGroup :model-value="(selections[opt.id] as any)?.choiceId"
                        @update:model-value="(val) => selections[opt.id] = { type: 'radio', choiceId: Number(val) }"
                        :orientation="'vertical'">
                        <div v-for="ch in opt.choices" :key="ch.id" class="flex justify-between items-center py-1">
                          <div class="flex items-center gap-2">
                            <RadioGroupItem :id="`opt-${opt.id}-ch-${ch.id}`" :value="ch.id" />
                            <Label class="text-base" :for="`opt-${opt.id}-ch-${ch.id}`">{{ ch.label }}</Label>
                          </div>
                          <div class="text-sm opacity-80">
                            <span v-if="ch.abs_cents">+{{ (ch.abs_cents / 100).toFixed(2) }}$</span>
                            <span v-if="ch.pct"> +{{ Math.round(ch.pct * 100) }}%</span>
                            <span v-if="ch.multiplier !== 1"> ×{{ ch.multiplier }}</span>
                          </div>
                        </div>
                      </RadioGroup>
                    </fieldset>

                    <!-- CHECKBOX -->
                    <fieldset v-else-if="opt.type === 'checkbox'">
                      <legend class="font-medium mb-4">{{ opt.label }}</legend>
                      <div class="flex flex-col gap-3">
                        <div v-for="ch in opt.choices" :key="ch.id" class="flex justify-between items-center">
                          <div class="flex items-center gap-2">
                            <Checkbox :id="`opt-${opt.id}-ch-${ch.id}`"
                              :checked="(selections[opt.id] as any)?.choiceIds?.includes(ch.id)" @update:checked="(checked) => {
                                const cur = (selections[opt.id] as any).choiceIds as number[]
                                const next = new Set(cur)
                                if (checked) next.add(ch.id); else next.delete(ch.id)
                                selections[opt.id] = { type: 'checkbox', choiceIds: [...next] }
                              }" />
                            <Label class="text-base" :for="`opt-${opt.id}-ch-${ch.id}`">{{ ch.label }}</Label>
                          </div>
                          <div class="text-sm opacity-80">
                            <span v-if="ch.abs_cents">+{{ (ch.abs_cents / 100).toFixed(2) }}$</span>
                            <span v-if="ch.pct"> +{{ Math.round(ch.pct * 100) }}%</span>
                            <span v-if="ch.multiplier !== 1"> ×{{ ch.multiplier }}</span>
                          </div>
                        </div>
                      </div>
                    </fieldset>

                    <!-- SELECT -->
                    <fieldset v-else-if="opt.type === 'select'">
                      <legend class="font-medium mb-4">{{ opt.label }}</legend>
                      <Select :model-value="String((selections[opt.id] as any)?.choiceId ?? '')"
                        @update:model-value="(val) => selections[opt.id] = { type: 'select', choiceId: Number(val) }">
                        <SelectTrigger class="w-full">
                          <SelectValue placeholder="Choose..." />
                        </SelectTrigger>
                        <SelectContent>
                          <SelectGroup>
                            <SelectItem v-for="ch in opt.choices" :key="ch.id" :value="String(ch.id)" class="w-full">
                              {{ ch.label }}
                            </SelectItem>
                          </SelectGroup>
                        </SelectContent>
                      </Select>
                    </fieldset>

                    <!-- NUMBER -->
                    <fieldset v-else-if="opt.type === 'number'">
                      <legend class="font-medium mb-4">{{ opt.label }}</legend>
                      <NumberField :default-value="opt.min_value ?? 1" :min="opt.min_value ?? 0"
                        :max="opt.max_value ?? undefined" :step="opt.step ?? 1"
                        :value="(selections[opt.id] as any)?.value"
                        @update:value="(val) => selections[opt.id] = { type: 'number', value: Number(val) }">
                        <NumberFieldContent>
                          <NumberFieldDecrement />
                          <NumberFieldInput class="bg-background border-2 border-secondary-foreground/70" />
                          <NumberFieldIncrement />
                        </NumberFieldContent>
                      </NumberField>
                    </fieldset>

                    <!-- SLIDER -->
                    <fieldset v-else-if="opt.type === 'slider'">
                      <legend class="font-medium mb-4">
                        {{ opt.label }}: {{ (selections[opt.id] as any)?.value ?? (opt.min_value ?? 0) }}
                      </legend>
                      <Slider :model-value="[(selections[opt.id] as any)?.value ?? (opt.min_value ?? 0)]"
                        :min="opt.min_value ?? 0" :max="opt.max_value ?? 100" :step="opt.step ?? 1"
                        @update:model-value="val => selections[opt.id] = { type: 'slider', value: val[0] }" />
                    </fieldset>

                    <Separator class="mb-2 mt-2" />
                  </template>
                </CardContent>

                <CardFooter>
                  <div class="flex flex-col pt-6 border-t w-full gap-4">
                    <div class="text-xl font-semibold">Total: {{ finalPriceFormatted }}</div>

                    <Button class="w-full mt-2 cursor-pointer" @click="() => {
                      // в корзину передаём выбранные опции
                      cart.addToCart({
                        id: item.id,
                        name: item.name,
                        price: finalPriceCents / 100,
                        image: item.image,
                        selections: JSON.parse(JSON.stringify(selections)) // сериализуем простые данные
                      })
                      toast.success('Succesfully added to cart')
                    }">
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