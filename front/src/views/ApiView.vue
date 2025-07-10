<template>
  <div class="api-view">
    <h1>API 管理</h1>
    
    <div class="actions">
      <button @click="showApiForm = true">添加 API</button>
    </div>
    
    <div class="api-cards">
      <ApiCard 
        v-for="api in apis" 
        :key="api.key_id" 
        :api="api"
        @edit="handleEdit"
        @delete="handleDelete"
      />
    </div>
    
    <ApiForm 
      v-if="showApiForm" 
      :api="editingApi || {}"
      @save="handleSave"
      @cancel="cancelEdit"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useApi } from '@/composables/useApi'
import ApiCard from '@/components/api/ApiCard.vue'
import ApiForm from '@/components/api/ApiForm.vue'

const { get, post, put, del } = useApi()
const apis = ref([])
const showApiForm = ref(false)
const editingApi = ref(null)

onMounted(async () => {
  try {
    const data = await get('/key/')
    apis.value = data
  } catch (err) {
    console.error('Failed to load APIs:', err)
  }
})

const handleEdit = (api) => {
  editingApi.value = api ? { ...api } : null
  showApiForm.value = true
}

const handleDelete = async (apiId) => {
  try {
    await del(`/key/${apiId}`)
    apis.value = apis.value.filter(a => a.key_id !== apiId)
  } catch (err) {
    console.error('Failed to delete API:', err)
  }
}

const handleSave = async (apiData) => {
  try {
    const payload = {
      api_name: apiData.api_name,
      api_address: apiData.api_address,
      api_type: apiData.api_type,
      api_key: apiData.api_key,  // 直接使用用户输入的密钥
      is_active: apiData.is_active
    }

    if (apiData.key_id) {
      // 更新逻辑
      const updatedApi = await put(`/key/${apiData.key_id}`, payload)
      apis.value = apis.value.map(a => 
        a.key_id === updatedApi.key_id ? updatedApi : a
      )
    } else {
      // 新增逻辑 - 直接使用用户提供的密钥
      const newApi = await post('/key/', payload)
      apis.value.push(newApi)
    }
    
    showApiForm.value = false
    editingApi.value = null
  } catch (err) {
    console.error('保存失败:', err)
    alert(`操作失败: ${err.data?.detail || err.message}`)
  }
}

const cancelEdit = () => {
  showApiForm.value = false
  editingApi.value = null
}
</script>

<style scoped>
.api-view {
  max-width: 1200px;
  margin: 0 auto;
  padding: 1rem;
}

.actions {
  margin-bottom: 1.5rem;
}

button {
  background-color: #4f46e5;
  color: white;
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
  transition: background-color 0.2s;
}

button:hover {
  background-color: #4338ca;
}

.api-cards {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
}
</style>