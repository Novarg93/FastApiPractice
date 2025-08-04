<script setup lang="ts">
import AuthSimpleLayout from '@/layouts/AuthSimpleLayout.vue';
import AppLogoIcon from '@/components/AppLogoIcon.vue';
import { useRouter } from 'vue-router'

import { Button } from '@/components/ui/button';
import { Checkbox } from '@/components/ui/checkbox';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import InputError from '@/components/InputError.vue'
import { LoaderCircle } from 'lucide-vue-next';
import axios from 'axios';
import { ref } from 'vue';


const email = ref('')
const password = ref('')
const remember = ref(false)
const isLoading = ref(false)
const router = useRouter()

const errors = ref<{ [key: string]: string }>({})

const login = async () => {
    errors.value = {}
    isLoading.value = true
    try {
        const { data } = await axios.post('http://localhost:8000/auth/login', {
            email: email.value,
            password: password.value,
            remember: remember.value
        })
        if (remember.value) {
            localStorage.setItem('token', data.access_token)
        } else {
            sessionStorage.setItem('token', data.access_token)
        }
        router.push('/dashboard')
    } catch (error: any) {
        if (error.response?.status === 422 && Array.isArray(error.response.data.detail)) {
            for (const err of error.response.data.detail) {
                const field = err.loc[1] 
                errors.value[field] = err.msg
            }
        } else {
            console.error('Login error:', error)
        }
    } finally {
        isLoading.value = false
    }
}


// ответ от FastApi и  в теле : 
//  {
//   "detail": [
//     { "loc": ["body", "email"], "msg": "Invalid email", "type": "value_error" },
//     { "loc": ["body", "password"], "msg": "Too short", "type": "value_error" }
//   ]
// }

</script>

<template>
    <AuthSimpleLayout>
        <div class="w-full max-w-md  border-border bg-card border-2  rounded-lg p-4 md:p-6">
            <div class="flex flex-col gap-8">
                <div class="flex flex-col items-center gap-4">
                    <AppLogoIcon />
                    <div class="space-y-2 text-center">
                        <h1 class="text-xl font-medium text-white">Login in to your account</h1>
                        <p class="text-center text-sm  text-gray-300">Enter your email and password below to log in</p>
                    </div>
                </div>
                <form @submit.prevent="login" class="flex flex-col gap-6">
                    <div class="grid gap-6">
                        <div class="grid gap-2">
                            <Label for="email">Email address</Label>
                            <Input id="email" type="email" required autofocus :tabindex="1" autocomplete="email"
                                v-model="email" placeholder="email@example.com" class="bg-background" />
                            <InputError :message="errors.email" />
                        </div>

                        <div class="grid gap-2">
                            <div class="flex items-center justify-between">
                                <Label for="password">Password</Label>
                                <router-link to="/forgot-password" class="text-sm underline hover:text-primary" :tabindex="5">
                                    Forgot password?
                                </router-link>
                            </div>
                            <Input id="password" type="password" required :tabindex="2" autocomplete="current-password"
                                v-model="password" placeholder="Password" class="bg-background" />
                            <InputError :message="errors.password" />
                        </div>

                        <div class="flex items-center justify-between">
                            <Label for="remember" class="flex items-center space-x-3">
                                <Checkbox id="remember" v-model="remember" :tabindex="3" />
                                <span>Remember me</span>
                            </Label>
                        </div>

                        <Button type="submit" class="mt-4 w-full" :tabindex="4">
                            <LoaderCircle v-if="isLoading" class="h-4 w-4 animate-spin" />
                            Log in
                        </Button>
                    </div>

                    <div class="text-center text-sm text-muted-foreground">
                        Don't have an account?
                        <router-link to="/register" class="underline text-white hover:text-primary" :tabindex="5">Sign up</router-link>
                    </div>
                </form>
            </div>
        </div>
    </AuthSimpleLayout>
</template>