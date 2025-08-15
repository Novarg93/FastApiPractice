<script setup lang="ts">
import { ref } from 'vue'
import { http } from '@/lib/http'
import { useAuthStore } from '@/stores/auth'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import InputError from '@/components/InputError.vue'
import { toAbsolute } from '@/lib/http'
import AppSidebar from '@/components/AppSidebar.vue'
import {
    Breadcrumb,
    BreadcrumbItem,
    BreadcrumbLink,
    BreadcrumbList,
    BreadcrumbPage,
    BreadcrumbSeparator,
} from '@/components/ui/breadcrumb'
import { Separator } from '@/components/ui/separator'
import {
    SidebarInset,
    SidebarProvider,
    SidebarTrigger,
} from '@/components/ui/sidebar'
import { computed, onMounted } from 'vue'
import { LoaderCircle, UploadCloud, Trash2 } from 'lucide-vue-next'
import { useRouter } from 'vue-router'
import { toast } from 'vue-sonner'

const auth = useAuthStore()
const router = useRouter()

// ---------- Профиль ----------
const name = ref('')
const email = computed(() => auth.user?.email ?? '')
const avatarUrl = ref<string | null>(null)            // текущий аватар (из стора или ответа бэка)
const avatarFile = ref<File | null>(null)             // выбранный файл
const avatarPreview = ref<string | null>(null)        // превью (blob url)
const profileLoading = ref(false)
const profileErrors = ref<Record<string, string>>({})

onMounted(async () => {
    if (!auth.user) {
        await auth.fetchMe().catch(() => { })
    }
    name.value = auth.user?.name ?? ''
    avatarUrl.value = (auth.user as any)?.avatar ?? null
})

function onPickAvatar(e: Event) {
    const files = (e.target as HTMLInputElement).files
    if (!files || !files[0]) return
    const file = files[0]
    if (!['image/jpeg','image/png','image/webp'].includes(file.type)) {
        profileErrors.value.avatar = 'Поддерживаются JPEG/PNG/WebP'
        return
        }
        if (file.size > 2 * 1024 * 1024) { // 2MB — как на бэке
        profileErrors.value.avatar = 'Файл слишком большой (макс. 2MB)'
        return
        }
    avatarFile.value = file
    avatarPreview.value = URL.createObjectURL(file)
    profileErrors.value.avatar = ''
}

async function saveProfile() {
  profileErrors.value = {}
  profileLoading.value = true
  try {
    // 1) Имя
    const prevName = auth.user?.name ?? ''
    const nextName = (name.value ?? '').trim()
    if (nextName && nextName !== prevName) {
      const { data } = await http.patch(
        '/users/me',
        { name: nextName },
        { headers: auth.authHeader() }
      )
      // унифицируем поле аватара из ответа (avatar_url) к нашему стору (avatar)
      auth.user = {
        ...auth.user!,
        name: data?.name ?? nextName,
        avatar: data?.avatar_url ?? (auth.user as any)?.avatar ?? null,
      }
    }

    // 2) Аватар (multipart)
    if (avatarFile.value) {
      const fd = new FormData()
      fd.append('file', avatarFile.value)

      const { data } = await http.post('/users/me/avatar', fd, {
        headers: { ...auth.authHeader(), 'Content-Type': 'multipart/form-data' },
      })

      const url = data?.avatar_url ?? null
        if (url) {
        avatarUrl.value = toAbsolute(url)
        auth.user = { ...auth.user!, avatar: toAbsolute(url) } // храним уже абсолютный — удобно для <img>
        }

      if (avatarPreview.value) URL.revokeObjectURL(avatarPreview.value)
      avatarPreview.value = null
      avatarFile.value = null
    }
    toast.success('Profile changed')
    // тут можно показать тост «Saved»
  } catch (e: any) {
    profileErrors.value.general = e?.response?.data?.detail ?? 'Не удалось сохранить профиль'
  } finally {
    profileLoading.value = false
  }
}

// ---------- Смена пароля ----------
const currentPassword = ref('')
const newPassword = ref('')
const confirmPassword = ref('')
const pwLoading = ref(false)
const pwErrors = ref<Record<string, string>>({})

async function changePassword() {
  pwErrors.value = {}
  pwLoading.value = true

  // локальная валидация до запроса
  if (newPassword.value !== confirmPassword.value) {
    pwErrors.value.confirm_password = 'Passwords do not match'
    pwLoading.value = false
    return
  }

  try {
    await http.post(
      '/users/me/change_password',
      { current_password: currentPassword.value, 
        new_password: newPassword.value,
        confirm_password: confirmPassword.value,
       },
      { headers: auth.authHeader() }
    )

    // очистка после успешного запроса
    currentPassword.value = ''
    newPassword.value = ''
    confirmPassword.value = ''
    // тост «Password updated»
  } catch (err: any) {
    if (err?.response?.status === 422 && Array.isArray(err.response.data?.detail)) {
      for (const d of err.response.data.detail) {
        const loc = d?.loc
        const field = Array.isArray(loc) ? loc[loc.length - 1] : null // берем ПОСЛЕДНИЙ элемент
        if (field) pwErrors.value[field] = d?.msg ?? 'Invalid'
      }
    } else {
      pwErrors.value.general = err?.response?.data?.detail ?? 'Не удалось изменить пароль'
    }
  } finally {
    pwLoading.value = false
  }
}

// ---------- Удаление аккаунта ----------
const delLoading = ref(false)
async function deleteAccount() {
  if (!confirm('Удалить аккаунт? Это действие необратимо.')) return
  delLoading.value = true
  try {
    await http.delete('/users/me', { headers: auth.authHeader() })
    await auth.logout()
    router.push('/login')
  } finally {
    delLoading.value = false
  }
}

onMounted(async () => {
  if (!auth.user) {
    await auth.fetchMe().catch(() => {})
  }
  name.value = auth.user?.name ?? ''
  // берем avatar | avatar_url, приводим к абсолютному
  const raw = (auth.user as any)?.avatar ?? (auth.user as any)?.avatar_url ?? null
  avatarUrl.value = toAbsolute(raw)
})

</script>







<template>
    <SidebarProvider>
        <AppSidebar />
        <SidebarInset class="border-l border-border rounded-lg">
            <header
                class="flex h-16 shrink-0 items-center gap-2 transition-[width,height] ease-linear group-has-[[data-collapsible=icon]]/sidebar-wrapper:h-12">
                <div class="flex items-center gap-2 px-4">
                    <SidebarTrigger class="-ml-1" />
                    <Separator orientation="vertical" class="mr-2 h-4" />
                    <Breadcrumb>
                        <BreadcrumbList>
                            <BreadcrumbItem class="hidden md:block">
                                <BreadcrumbLink href="/dashboard">
                                    Building Your Application
                                </BreadcrumbLink>
                            </BreadcrumbItem>
                            <BreadcrumbSeparator class="hidden md:block" />
                            <BreadcrumbItem>
                                <BreadcrumbPage>Data Fetching</BreadcrumbPage>
                            </BreadcrumbItem>
                        </BreadcrumbList>
                    </Breadcrumb>
                </div>
            </header>
            
            <div class="flex flex-1 flex-col gap-4 p-4 pt-0">
                <div class=" max-w-2xl p-6 space-y-10">
                    <h1 class="text-2xl font-semibold">Settings</h1>

                    <!-- Профиль -->
                    <section class="space-y-4 border border-border rounded-lg p-4">
                        <h2 class="text-lg font-medium">Profile</h2>

                        <!-- Name -->
                        <div class="grid gap-2">
                            <Label for="name">Name</Label>
                            <Input id="name" v-model="name" type="text" placeholder="Your name" />
                            <InputError :message="profileErrors.name" />
                        </div>

                        <!-- Email (read-only) -->
                        <div class="grid gap-2">
                            <Label for="email">Email</Label>
                            <Input :model-value="email || '—'" type="email" readonly />
                        </div>

                        <!-- Avatar -->
                        <div class="grid gap-2">
                            <Label>Avatar</Label>
                            <div class="flex items-center gap-4">
                                <img v-if="avatarPreview || avatarUrl" :src="avatarPreview || avatarUrl || undefined"
                                    alt="Avatar" class="w-16 h-16 rounded-full object-cover border" />
                                    <img v-else src="/images/vaal_orb.png"
                                    alt="Avatar" class="w-16 h-16 rounded-full object-cover border border-border" />
                                <div class="flex items-center gap-2">
                                    <label
                                        class="inline-flex items-center px-3 py-2 rounded-md border border-border cursor-pointer">
                                        <UploadCloud class="mr-2 h-4 w-4" />
                                        <span>Select image</span>
                                        <Input type="file" accept="image/*" class="hidden" @change="onPickAvatar" />
                                    </label>
                                    <Button variant="secondary" v-if="avatarPreview"
                                        @click="() => { avatarPreview = null; avatarFile = null }">
                                        Cancel
                                    </Button>
                                </div>
                            </div>
                            <InputError :message="profileErrors.avatar" />
                        </div>

                        <InputError :message="profileErrors.general" />
                        <Button class="w-full" :disabled="profileLoading" @click="saveProfile">
                            <LoaderCircle v-if="profileLoading" class="h-4 w-4 animate-spin mr-2" />
                            Save changes
                        </Button>
                    </section>

                    <!-- Password -->
                    <section class="space-y-4 border border-border rounded-lg p-4">
                        <h2 class="text-lg font-medium">Change password</h2>

                        <div class="grid gap-2">
                            <Label for="curr">Current password</Label>
                            <Input id="curr" type="password" v-model="currentPassword"
                                autocomplete="current-password" />
                            <InputError :message="pwErrors.current_password" />
                        </div>

                        <div class="grid gap-2">
                            <Label for="new">New password</Label>
                            <Input id="new" type="password" v-model="newPassword" autocomplete="new-password" />
                            <InputError :message="pwErrors.new_password" />
                        </div>

                        <div class="grid gap-2">
                            <Label for="conf">Confirm password</Label>
                            <Input id="conf" type="password" v-model="confirmPassword" autocomplete="new-password" />
                            <InputError :message="pwErrors.confirm_password" />
                        </div>

                        <InputError :message="pwErrors.general" />
                        <Button class="w-full" :disabled="pwLoading" @click="changePassword">
                            <LoaderCircle v-if="pwLoading" class="h-4 w-4 animate-spin mr-2" />
                            Update password
                        </Button>
                    </section>

                    <!-- Danger zone -->
                    <section class="space-y-3 border border-border rounded-lg p-4">
                        <h2 class="text-lg font-medium text-red-500">Danger zone</h2>
                        <p class="text-sm text-muted-foreground">
                            Deleting your account is permanent and cannot be undone.
                        </p>
                        <Button variant="destructive" class="w-full" :disabled="delLoading" @click="deleteAccount">
                            <Trash2 class="h-4 w-4 mr-2" />
                            Delete account
                        </Button>
                    </section>
                </div>
            </div>
        </SidebarInset>
    </SidebarProvider>
</template>
