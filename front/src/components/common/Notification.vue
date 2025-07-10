<!-- src/components/Notification.vue -->
<template>
  <transition-group name="notification">
    <div 
      v-for="notification in notifications"
      :key="notification.id"
      class="notification"
      :class="`notification-${notification.type}`"
    >
      {{ notification.message }}
      <button @click="remove(notification.id)">×</button>
    </div>
  </transition-group>
</template>

<script setup>
import { ref } from 'vue'

const notifications = ref([])

const add = (message, type = 'info') => {
  const id = Date.now()
  notifications.value.push({ id, message, type })
  
  // 自动消失（3秒后）
  setTimeout(() => remove(id), 3000)
}

const remove = (id) => {
  notifications.value = notifications.value.filter(n => n.id !== id)
}

// 暴露方法供全局使用
defineExpose({ add, remove })
</script>

<style scoped>
.notification {
  position: fixed;
  right: 20px;
  top: 20px;
  padding: 12px 24px;
  margin-bottom: 10px;
  border-radius: 4px;
  color: white;
  display: flex;
  align-items: center;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
  z-index: 1000;
  animation: slideIn 0.3s ease-out;
}

.notification button {
  margin-left: 15px;
  background: none;
  border: none;
  color: white;
  cursor: pointer;
  font-size: 16px;
}

.notification-info {
  background-color: #3498db;
}

.notification-success {
  background-color: #2ecc71;
}

.notification-warning {
  background-color: #f39c12;
}

.notification-error {
  background-color: #e74c3c;
}

.notification-enter-active,
.notification-leave-active {
  transition: all 0.3s ease;
}

.notification-enter-from,
.notification-leave-to {
  opacity: 0;
  transform: translateX(100%);
}

@keyframes slideIn {
  from {
    transform: translateX(100%);
    opacity: 0;
  }
  to {
    transform: translateX(0);
    opacity: 1;
  }
}
</style>