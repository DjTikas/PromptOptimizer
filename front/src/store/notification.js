import { defineStore } from 'pinia'

export const useNotificationStore = defineStore('notification', {
  state: () => ({
    messages: []
  }),
  actions: {
    addMessage(message, type = 'info') {
      this.messages.push({ id: Date.now(), message, type })
      // 5秒后自动移除
      setTimeout(() => {
        this.removeMessage(this.messages.length - 1)
      }, 5000)
    },
    removeMessage(index) {
      this.messages.splice(index, 1)
    }
  }
})