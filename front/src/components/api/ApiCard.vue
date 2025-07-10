<template>
  <div class="api-card">
    <div class="api-header">
      <h3>{{ api.api_name }}</h3>
      <div class="actions">
        <button @click="$emit('edit', api)" class="edit-btn">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path>
            <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path>
          </svg>
        </button>
        <button @click="$emit('delete', api.key_id)" class="delete-btn">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <polyline points="3 6 5 6 21 6"></polyline>
            <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
          </svg>
        </button>
      </div>
    </div>
    <div class="api-details">
      <div class="detail">
        <label>API 地址:</label>
        <div class="value">{{ api.api_address }}</div>
      </div>
      <div class="detail">
        <label>默认模型:</label>
        <div class="value">{{ api.api_type }}</div>
      </div>
      <div class="detail">
        <label>API 密钥:</label>
        <div class="value">
          <span v-if="showKey">{{ api.api_key }}</span>
          <span v-else>••••••••••••••••</span>
          <button @click="showKey = !showKey" class="toggle-key">
            {{ showKey ? '隐藏' : '显示' }}
          </button>
          <button @click="copyKey" class="copy-btn">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect>
              <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path>
            </svg>
          </button>
        </div>
      </div>
    </div>
    <div class="api-footer">
      <span class="created-at">创建于: {{ formatDate(api.created_at) }}</span>
      <span class="status" :class="{ active: api.is_active }">
        {{ api.is_active ? '激活' : '停用' }}
      </span>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const props = defineProps({
  api: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['edit', 'delete'])

const showKey = ref(false)

const formatDate = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleDateString()
}

const copyKey = () => {
  navigator.clipboard.writeText(props.api.api_key)
  alert('API密钥已复制到剪贴板')
}
</script>

<style scoped>
.api-card {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  padding: 1.5rem;
  transition: transform 0.2s, box-shadow 0.2s;
}

.api-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.api-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
  border-bottom: 1px solid #eee;
  padding-bottom: 0.5rem;
}

.api-header h3 {
  margin: 0;
  font-size: 1.25rem;
  color: #1f2937;
}

.actions {
  display: flex;
  gap: 0.5rem;
}

.actions button {
  background: none;
  border: none;
  cursor: pointer;
  padding: 0.25rem;
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.actions button svg {
  width: 16px;
  height: 16px;
}

.edit-btn {
  color: #4f46e5;
}

.edit-btn:hover {
  background-color: #eef2ff;
}

.delete-btn {
  color: #ef4444;
}

.delete-btn:hover {
  background-color: #fee2e2;
}

.api-details {
  margin-bottom: 1rem;
}

.detail {
  display: flex;
  margin-bottom: 0.75rem;
}

.detail label {
  font-weight: 500;
  color: #6b7280;
  width: 100px;
  flex-shrink: 0;
}

.detail .value {
  flex: 1;
  word-break: break-all;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.toggle-key {
  background: none;
  border: none;
  color: #4f46e5;
  cursor: pointer;
  font-size: 0.75rem;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
}

.toggle-key:hover {
  background-color: #eef2ff;
}

.copy-btn {
  background: none;
  border: none;
  cursor: pointer;
  padding: 0.25rem;
  border-radius: 4px;
  color: #6b7280;
}

.copy-btn:hover {
  background-color: #f3f4f6;
}

.copy-btn svg {
  width: 16px;
  height: 16px;
}

.api-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.875rem;
  color: #6b7280;
  border-top: 1px solid #eee;
  padding-top: 0.5rem;
}

.status {
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.75rem;
  font-weight: 500;
}

.status.active {
  background-color: #dcfce7;
  color: #16a34a;
}

.status:not(.active) {
  background-color: #fee2e2;
  color: #dc2626;
}
</style>