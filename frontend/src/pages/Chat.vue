<script setup lang="ts">
import AppSidebar from '@/components/AppSidebar.vue'
import {
    Breadcrumb, BreadcrumbItem, BreadcrumbLink, BreadcrumbList, BreadcrumbPage, BreadcrumbSeparator,
} from '@/components/ui/breadcrumb'
import { Separator } from '@/components/ui/separator'
import { SidebarInset, SidebarProvider, SidebarTrigger } from '@/components/ui/sidebar'
import { useAuthStore } from '@/stores/auth'
import { storeToRefs } from 'pinia'
import { nextTick, ref, computed, watch } from 'vue'
import { http } from '@/lib/http'
import { Card, CardContent } from '@/components/ui/card'
import Button from '@/components/ui/button/Button.vue'
import { Search, EllipsisVertical, Plus } from 'lucide-vue-next';
import { Input } from '@/components/ui/input'
import {
    DropdownMenu,
    DropdownMenuContent,
    DropdownMenuGroup,
    DropdownMenuItem,
    DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu';
import { Skeleton } from '@/components/ui/skeleton'
import { toast } from 'vue-sonner';
import {
    Dialog,
    DialogContent,
    DialogDescription,
    DialogFooter,
    DialogHeader,
    DialogTitle,
} from '@/components/ui/dialog'
import { Textarea } from '@/components/ui/textarea';
import { useChatWS } from '@/composables/useChatWS'

const auth = useAuthStore()
const { isAuthenticated } = storeToRefs(auth)
const selectedChat = ref<User | null>(null)
const currentUserId = computed(() => auth.user?.id ?? 0)
const roomId = computed<number | null>(() => selectedChat.value ? selectedChat.value.id : null)

const wsApi = useChatWS(roomId, currentUserId, import.meta.env.VITE_WS_BASE ?? 'ws://127.0.0.1:8000')

// адаптер сообщений
const messages = computed(() => {
  const raw = wsApi.serverMessages.value
  return raw.map(m => ({
    text: m.content,
    from: m.sender_id === currentUserId.value ? 'me' : 'other' as const,
  }))
})

const visibleMessages = computed(() => selectedChat.value ? messages.value : [])

// отправка
async function sendMessage() {
  if (!newMessage.value.trim()) return
  wsApi.send(newMessage.value.trim())
  newMessage.value = ''
  scrollToBottom()
}

// Chat section
interface Message {
    text: string
    from: 'me' | 'other'
}





const newMessage = ref('')

const chatContainer = ref<HTMLElement | null>(null)

function scrollToBottom() {
    nextTick(() => {
        if (chatContainer.value) {
            chatContainer.value.scrollTop = chatContainer.value.scrollHeight
        }
    })
}





function toggleBan() {
    if (!selectedChat.value) return

    selectedChat.value.isBanned = !selectedChat.value.isBanned

    const isBanned = selectedChat.value.isBanned

    const toastFn = isBanned ? toast.error : toast.success

    toastFn(
        isBanned
            ? 'User was added to the ignore list.'
            : 'User was removed from the ignore list.',
        
    )
}


// contact list
interface User {
    id: number
    name: string
    avatar: string
    isBanned?: boolean
    messages?: Message[]
}


const allUsers = ref<User[]>([
    {
        id: 1,
        name: 'NeoBot',
        avatar: '/images/game-1.png',
        isBanned: false,
        messages: [],
    },
    {
        id: 2,
        name: 'CyberWraith',
        avatar: '/images/game-2.webp',
        isBanned: false,
        messages: [],
    },
    {
        id: 3,
        name: 'ByteHunter',
        avatar: '/images/game-1.png',
        isBanned: false,
        messages: [],
    },
    {
        id: 4,
        name: 'GlitchPhantom',
        avatar: '/images/game-2.webp',
        isBanned: false,
        messages: [],
    },
    {
        id: 5,
        name: 'SynapseX',
        avatar: '/images/game-1.png',
        isBanned: false,
        messages: [],
    },
    {
        id: 6,
        name: 'NeoBot1',
        avatar: '/images/game-1.png',
        isBanned: false,
        messages: [],
    },
    {
        id: 7,
        name: 'CyberWraith1',
        avatar: '/images/game-2.webp',
        isBanned: false,
        messages: [],
    },
    {
        id: 8,
        name: 'ByteHunter1',
        avatar: '/images/game-1.png',
        isBanned: false,
        messages: [],
    },
    {
        id: 9,
        name: 'GlitchPhantom1',
        avatar: '/images/game-2.webp',
        isBanned: false,
        messages: [],
    },
    {
        id: 10,
        name: 'SynapseX1',
        avatar: '/images/game-1.png',
        isBanned: false,
        messages: [],
    }
])

const searchAllUsersQuery = ref('')

const sortedAllUsers = computed(() => {
    return allUsers.value
        .filter(user =>
            user.name.toLowerCase().includes(searchAllUsersQuery.value.toLowerCase())
        )
        .sort((a, b) => a.name.localeCompare(b.name))
})

const recentChats = ref<User[]>([
  { id: 1, name: 'Room 1 (order #1)', avatar: '/images/game-2.webp', messages: [] },
  
])

function deleteChat() {
    if (!selectedChat.value) return

    recentChats.value = recentChats.value.filter(chat => chat.id !== selectedChat.value?.id)
    selectedChat.value = null

    toast.success('Chat deleted',)
}

const openNewChatDialog = ref(false)


function addToRecent(user: User) {
    if (!recentChats.value.find(u => u.id === user.id)) {
        recentChats.value.push(user)
    }
    openNewChatDialog.value = false
}

// sort

const searchQuery = ref('')

const filteredRecentChats = computed<User[]>(() =>
    recentChats.value.filter(chat =>
        chat.name.toLowerCase().includes(searchQuery.value.toLowerCase())
    )
)

// recentChats and chatwindow mechanic




// reports

const reportText = ref('')
const reportTargetId = ref<number | null>(null)

const openReportDialog = ref(false)

function openReport() {
    if (!selectedChat.value) return
    reportTargetId.value = selectedChat.value.id
    openReportDialog.value = true
}

function submitReport() {
    if (!reportTargetId.value || !reportText.value.trim()) {
        toast.error('Please provide a reason for the report')
        return
    }

    console.log('Reported user ID:', reportTargetId.value)
    console.log('Report reason:', reportText.value)


    openReportDialog.value = false
    reportText.value = ''
    reportTargetId.value = null
    toast.success('Report submitted!')
}

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
                                <BreadcrumbLink href="/dashboard">Dashboard</BreadcrumbLink>
                            </BreadcrumbItem>
                            <BreadcrumbSeparator class="hidden md:block" />
                            <BreadcrumbItem>
                                <BreadcrumbPage>Chat</BreadcrumbPage>
                            </BreadcrumbItem>
                        </BreadcrumbList>
                    </Breadcrumb>
                </div>
            </header>

            <div class="flex flex-1 flex-col gap-4 p-4 pt-0">

                <section class="flex flex-col md:flex-row gap-10 md:gap-0 md:justify-between p-4 overflow-hidden">

                    <!-- Contact list -->
                    <div
                        class="lg:w-[39%] xl:w-4/12 2xl:w-3/12 flex flex-col items-center  p-4 xl:p-6 gap-4 border border-border rounded-xl  md:min-h-[87vh] lg:min-h-[86vh]  xl:min-h-[87vh] 2xl:min-h-[87vh]">

                        <div class="flex w-full gap-4 pb-4 md:pb-6  justify-center items-center border-b border-border ">
                            <img class="size-30 xl:size-35 rounded-lg" src="/images/game-1.png" alt="Avatar">
                        </div>

                        <div class="flex-1 w-full  space-y-4  justify-center items-center max-h-[60vh]">
                            <div class="flex relative gap-2 justify-between">
                                <Input v-model="searchQuery" class="pl-9 relative" placeholder="Search" />
                                <Search class="absolute left-1.5 top-1.5" />
                                <Button class="cursor-pointer border-border" variant="outline" @click="openNewChatDialog = true">
                                    <Plus />
                                </Button>
                            </div>
                            <Dialog :open="openNewChatDialog" @update:open="openNewChatDialog = $event">
                                <DialogContent class="border-border">
                                    <DialogHeader>
                                        <DialogTitle>Select user to start new chat</DialogTitle>
                                        <DialogDescription>
                                            Pick a user from the list to begin a new conversation.
                                        </DialogDescription>
                                    </DialogHeader>

                                    <div class="mb-4">
                                        <Input v-model="searchAllUsersQuery" placeholder="Search users"
                                            class="w-full" />
                                    </div>

                                    <!-- all users -->
                                    <div class="flex   flex-col gap-2 min-h-[50vh] max-h-[50vh] overflow-y-auto"
                                        style="scrollbar-width: none;">
                                        <div v-for="user in sortedAllUsers" :key="user.id"
                                            class="flex items-center gap-4 p-2 rounded-lg hover:bg-sidebar-border cursor-pointer"
                                            @click="addToRecent(user)">
                                            <img :src="user.avatar" class="w-10 h-10 rounded-lg" />
                                            <span>{{ user.name }}</span>
                                        </div>
                                    </div>
                                </DialogContent>
                            </Dialog>

                            <!-- Recent chats -->
                            <div class="w-full flex flex-col gap-4 overflow-y-auto max-h-[50vh]  md:max-h-11/12"
                                style="scrollbar-width: none;">
                                <div v-for="chat in filteredRecentChats" :key="chat.id" @click="selectedChat = chat"
                                    class="flex justify-between items-center w-full rounded-lg p-2 hover:bg-sidebar-border cursor-pointer">
                                    <div class="flex gap-4 items-center">
                                        <img class="size-10  rounded-lg" :src="chat.avatar" alt="Avatar" />
                                        <div class="flex flex-col gap-2">
                                            <span class="font-semibold">{{ chat.name }}</span>
                                            <!-- <span class="text-xs md:text-sm w-30 xl:w-40 truncate">Last message of the dialog</span> -->
                                        </div>
                                    </div>
                                    <div class="text-xs text-gray-400">2d</div>
                                </div>
                            </div>
                        </div>
                    </div>


                    <!-- Chat section -->
                    <div
                        class="min-h-[70vh] border-border max-h-[90vh] md:w-7/12 xl:w-[65%] 2xl:w-[70%] flex flex-col p-4 xl:p-6  gap-4 border rounded-xl  md:max-h-[87vh] lg:max-h-[86vh] xl:max-h-[87vh] 2xl:max-h-[50rem]">

                        <div class="flex justify-center md:justify-between border-b border-border relative">
                            <div class="flex flex-col md:flex-row gap-4 pb-4 md:pb-6  justify-center items-center">
                                <img v-if="selectedChat" class="size-30 xl:size-35 rounded-lg"
                                    :src="selectedChat.avatar" :alt="selectedChat.name"
                                    :class="{ 'grayscale': selectedChat.isBanned }">
                                <Skeleton v-else class="size-30 xl:size-35 rounded-lg" />
                                <span v-if="selectedChat">{{ selectedChat.name }}</span>
                                <Skeleton v-else class="w-30 h-4" />
                            </div>


                            <DropdownMenu>
                                <DropdownMenuTrigger class="absolute top-0 right-0 md:block" as-child>
                                    <Button class="cursor-pointer border-border size-6 md:w-10.5 md:h-9" variant="outline">
                                        <EllipsisVertical />
                                    </Button>
                                </DropdownMenuTrigger>

                                <DropdownMenuContent class="border-border" align="end">
                                    <DropdownMenuGroup>
                                        <DropdownMenuItem @click="toggleBan">
                                            <span>{{ selectedChat?.isBanned ? 'Unban' : 'Ban' }}</span>
                                        </DropdownMenuItem>


                                        <DropdownMenuItem @click="openReport">
                                            <span>Report</span>
                                        </DropdownMenuItem>

                                        <DropdownMenuItem @click="deleteChat">
                                            <span>Delete chat</span>
                                        </DropdownMenuItem>
                                    </DropdownMenuGroup>
                                </DropdownMenuContent>
                            </DropdownMenu>


                            <Dialog :open="openReportDialog" @update:open="openReportDialog = $event">
                                <DialogContent class="max-w-11/12 border-border flex-none sm:max-w-[425px]">
                                    <DialogHeader>
                                        <DialogTitle>Report player</DialogTitle>
                                        <DialogDescription>
                                            Describe reason for reporting this player
                                        </DialogDescription>
                                    </DialogHeader>
                                    <div class="overflow-y-auto min-h-[30vh] break-words whitespace-pre-wrap">
                                        <Textarea v-model="reportText" maxlength="300" wrap="hard"
                                            class="overflow-y-auto h-[30vh]" name="Report description" id="report" />
                                        <div class="text-right text-xs text-muted-foreground mt-2">
                                            {{ reportText.length }} / 300 characters
                                        </div>
                                    </div>
                                    <DialogFooter>
                                        <Button type="submit" @click="submitReport">Submit</Button>
                                    </DialogFooter>
                                </DialogContent>
                            </Dialog>
                        </div>

                        <!-- Chat window -->
                        <div class="flex-1 space-y-4 max-h-10/12 overflow-y-auto" style="scrollbar-width: none;"
                            ref="chatContainer">
                            <div v-for="(message, index) in visibleMessages" :key="index"
                                :class="['flex transition-opacity duration-300 ease-out', message.from === 'me' ? 'justify-end' : 'justify-start']">
                                <div
                                    :class="[message.from === 'me' ? 'bg-primary' : 'border-border', 'border border-border opacity-0 animate-fade-in  p-2 rounded-xl max-w-xs ']">
                                    {{ message.text }}
                                </div>
                            </div>
                        </div>

                        <form @submit.prevent="sendMessage" class="flex items-center gap-2 pt-4 border-t border-border">
                            <Input v-model="newMessage" :disabled="selectedChat?.isBanned"
                                :placeholder="selectedChat?.isBanned ? 'This user was added to ignore list' : 'Type your message...'" />
                            <Button type="submit" :disabled="selectedChat?.isBanned"
                                class="py-1.5 md:px-6.5 rounded-lg bg-primary text-white hover:bg-orange-500 transition disabled:opacity-50 cursor-pointer disabled:cursor-not-allowed">
                                Send
                            </Button>
                        </form>
                    </div>
                </section>


            </div>
        </SidebarInset>
    </SidebarProvider>
</template>
