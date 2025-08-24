// src/composables/useChatWS.ts
import { ref, type Ref, watch, onMounted, onBeforeUnmount } from 'vue'

type ServerMsg = {
  id: number
  sender_id: number
  content: string
  type: 'text' | 'media' | 'system'
  created_at: string
}

export function useChatWS(
  roomId: Ref<number | null>,
  currentUserId: Ref<number>,
  wsBase = 'ws://127.0.0.1:8000'
) {
  const ws = ref<WebSocket | null>(null)
  const serverMessages = ref<ServerMsg[]>([])
  const connected = ref(false)
  const connecting = ref(false)

  function doConnect(id: number) {
    connecting.value = true
    const socket = new WebSocket(`${wsBase}/ws/chat/${id}`)
    ws.value = socket

    socket.onopen = () => { connected.value = true; connecting.value = false }
    socket.onclose = () => { connected.value = false; connecting.value = false }
    socket.onerror = () => { /* можно добавить retry */ }

    socket.onmessage = (e) => {
      const msg: ServerMsg = JSON.parse(e.data)
      serverMessages.value.push(msg)
    }
  }

  function disconnect() {
    ws.value?.close()
    ws.value = null
  }

  function send(content: string) {
    if (!ws.value || ws.value.readyState !== WebSocket.OPEN) return
    ws.value.send(JSON.stringify({ sender_id: currentUserId.value, content }))
  }

  // подключаемся/переключаемся при изменении roomId
  watch(roomId, (id) => {
    disconnect()
    if (id) {
      doConnect(id)
    } else {
      serverMessages.value = []
    }
  }, { immediate: true })

  onMounted(() => {
    if (roomId.value) doConnect(roomId.value)
  })

  onBeforeUnmount(() => {
    disconnect()
  })

  return { serverMessages, send, connected, connecting, disconnect }
}