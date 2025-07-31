<script setup lang="ts">
import AuthSimpleLayout from '@/layouts/AuthSimpleLayout.vue';
import AppLogoIcon from '@/components/AppLogoIcon.vue';


import { Button } from '@/components/ui/button';

import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import InputError from '@/components/InputError.vue'

import { LoaderCircle } from 'lucide-vue-next';
import axios from 'axios';
import { ref } from 'vue';



const email = ref('')
const isLoading = ref(false)
const status = ref('')

const errors = ref<{ [key: string]: string }>({})

const forgotPassword = async () => {
  errors.value = {}
  status.value = ''
  isLoading.value = true
  try {
    const { data } = await axios.post('http://localhost:8000/api/password/forgot', {
      email: email.value
    })

    status.value = 'Password reset link sent to your email.'

  } catch (error: any) {
    if (error.response?.status === 422 && Array.isArray(error.response.data.detail)) {
      for (const err of error.response.data.detail) {
        const field = err.loc[1]
        errors.value[field] = err.msg
      }
    } else {
      status.value = 'Something went wrong. Please try again.'
      console.error('Forgot password error:', error)
    }
  } finally {
    isLoading.value = false
  }
}


// {
//   "message": "Password reset link has been sent to your email"
// }

</script>

<template>
  <AuthSimpleLayout>
    <div class="w-full max-w-md  border-border bg-card border-2  rounded-lg p-4 md:p-6">
      <div class="flex flex-col gap-8">
        <div class="flex flex-col items-center gap-4">
          <AppLogoIcon />
          <div class="space-y-2 text-center">
            <h1 class="text-xl font-medium text-white">Forgot password</h1>
            <p class="text-center text-sm  text-gray-300">Enter your email to receive a password reset link</p>
          </div>
        </div>
        <div v-if="status" class="mb-4 text-center text-sm font-medium text-green-600">
          {{ status }}
        </div>
        <form @submit.prevent="forgotPassword">
          <div class="grid gap-2">
            <Label for="email">Email address</Label>
            <Input id="email" type="email" name="email" autocomplete="off" v-model="email" autofocus
              placeholder="email@example.com" />
            <InputError :message="errors.email" />
          </div>

          <div class="my-6 flex items-center justify-start">
            <Button class="w-full" :disabled="isLoading">
              <LoaderCircle v-if="isLoading" class="h-4 w-4 animate-spin" />
              Email password reset link
            </Button>
          </div>
        </form>

        <div class="space-x-1 text-center text-sm text-muted-foreground">
          <span>Or, return to</span>
          <router-link class="hover:text-primary underline text-white" to="/login">log in</router-link>
        </div>
      </div>
    </div>
  </AuthSimpleLayout>
</template>