<script setup lang="ts">
import AuthSimpleLayout from '@/layouts/AuthSimpleLayout.vue';
import AppLogoIcon from '@/components/AppLogoIcon.vue';
import { useRouter } from 'vue-router'

import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import InputError from '@/components/InputError.vue'
import { http } from '@/lib/http'
import { useAuthStore } from '@/stores/auth'
import { LoaderCircle } from 'lucide-vue-next';
import axios from 'axios';
import { ref } from 'vue';

const auth = useAuthStore()

const name = ref('')
const email = ref('')
const password = ref('')
const passwordConfirmation = ref('')
const isLoading = ref(false)
const router = useRouter()

const errors = ref<{ [key: string]: string }>({})

const register = async () => {
  errors.value = {}
  isLoading.value = true
  try {
    
    await http.post('/auth/register', {
      name: name.value,
      email: email.value,
      password: password.value,
      password_confirmation: passwordConfirmation.value,
    })

    
    await auth.login(email.value, password.value, true)

    router.push('/dashboard')
  } catch (error: any) {
    if (error.response?.status === 422 && Array.isArray(error.response.data.detail)) {
      for (const err of error.response.data.detail) {
        const field = err.loc[1]
        errors.value[field] = err.msg
      }
    } else {
      console.error('Register error:', error)
    }
  } finally {
    isLoading.value = false
  }
}




</script>

<template>
  <AuthSimpleLayout>
    <div class="w-full max-w-md  border-border bg-card border-2  rounded-lg p-4 md:p-6">
      <div class="flex flex-col gap-8">
        <div class="flex flex-col items-center gap-4">
          <AppLogoIcon />
          <div class="space-y-2 text-center">
            <h1 class="text-xl font-medium text-white">Create an account</h1>
            <p class="text-center text-sm  text-gray-300">Enter your details below to create your account</p>
          </div>
        </div>
        <form @submit.prevent="register" class="flex flex-col gap-6">
          <div class="grid gap-6">
            <div class="grid gap-2">
              <Label for="name">Name</Label>
              <Input id="name" type="text" required autofocus :tabindex="1" autocomplete="name" v-model="name"
                placeholder="Full name" />
              <InputError :message="errors.name" />
            </div>

            <div class="grid gap-2">
              <Label for="email">Email address</Label>
              <Input id="email" type="email" required :tabindex="2" autocomplete="email" v-model="email"
                placeholder="email@example.com" />
              <InputError :message="errors.email" />
            </div>

            <div class="grid gap-2">
              <Label for="password">Password</Label>
              <Input id="password" type="password" required :tabindex="3" autocomplete="new-password" v-model="password"
                placeholder="Password" />
              <InputError :message="errors.password" />
            </div>

            <div class="grid gap-2">
              <Label for="password_confirmation">Confirm password</Label>
              <Input id="password_confirmation" type="password" required :tabindex="4" autocomplete="new-password"
                v-model="passwordConfirmation" placeholder="Confirm password" />
              <InputError :message="errors.password_confirmation" />
            </div>

            <Button type="submit" class="mt-2 w-full" tabindex="5" :disabled="isLoading">
              <LoaderCircle v-if="isLoading" class="h-4 w-4 animate-spin" />
              Create account
            </Button>
          </div>

          <div class="text-center text-sm text-muted-foreground">
            Already have an account?
            <router-link to="/login" class="underline underline-offset-4 hover:text-primary text-white" :tabindex="6">Log
              in</router-link>
          </div>
        </form>
      </div>
    </div>
  </AuthSimpleLayout>
</template>