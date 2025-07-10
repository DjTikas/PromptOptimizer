<template>
  <div class="avatar" :class="[size]">
    <img 
      v-if="src" 
      :src="src" 
      :alt="alt"
      :style="{
        width: size + 'px', 
        height: size + 'px',
        'object-fit': 'cover'
      }"
    >
    <div v-else class="avatar-placeholder">
      {{ initials }}
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  src: String,
  name: String,
  size: {
    type: String,
    default: 'medium',
    validator: (value) => ['small', 'medium', 'large'].includes(value)
  }
})

const initials = computed(() => {
  if (!props.name) return ''
  const parts = props.name.split(' ')
  return parts.map(part => part[0].toUpperCase()).join('')
})
</script>

<style scoped>
.avatar {
  border-radius: 50%;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #e5e7eb;
  color: #4b5563;
  font-weight: 600;
}

.avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.avatar.small {
  width: 32px;
  height: 32px;
  font-size: 12px;
}

.avatar.medium {
  width: 48px;
  height: 48px;
  font-size: 16px;
}

.avatar.large {
  width: 64px;
  height: 64px;
  font-size: 20px;
}
</style>