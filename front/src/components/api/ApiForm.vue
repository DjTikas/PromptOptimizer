<template>
  <div class="modal-overlay" @click.self="$emit('cancel')">
    <div class="modal-content">
      <!-- 欺骗表单 -->
      <form style="height:0;overflow:hidden">
        <input type="text" name="username">
        <input type="password" name="password">
      </form>

      <button class="close-btn" @click="$emit('cancel')">×</button>
      <h2>{{ api.key_id ? '编辑 API' : '添加新 API' }}</h2>
      
      <form @submit.prevent="handleSubmit">

        <div class="form-group">
          <label>API 名称</label>
          <input v-model="formData.api_name" type="text" required>
        </div>
        
        <!-- API地址字段 -->
        <div class="form-group">
          <label>API 地址</label>
          <input 
            v-model="formData.api_address"
            type="text"
            required
            autocomplete="off"
            :name="'api-addr-' + Math.random()"
          >
        </div>
        
        <!-- 修改为文本输入的API类型 -->
        <div class="form-group">
          <label>默认模型</label>
          <input 
            v-model="formData.api_type" 
            type="text" 
            required
            placeholder="例如: gpt-3.5-turbo, deepseek-v3 等"
          >
        </div>
        
        <!-- API密钥字段 -->
        <div class="form-group">
          <label>API 密钥</label>
          <div class="input-with-action">
            <input 
              v-model="formData.api_key"
              :type="showApiKey ? 'text' : 'password'"
              required
              autocomplete="new-password"
              :name="'api-key-' + Math.random()"
            >
            <button type="button" @click="showApiKey = !showApiKey">
              {{ showApiKey ? '隐藏' : '显示' }}
            </button>
          </div>
        </div>
        
        <div class="form-group">
          <label>
            <input v-model="formData.is_active" type="checkbox"> 激活
          </label>
        </div>
        
        <div class="form-actions">
          <button type="button" @click="$emit('cancel')">取消</button>
          <button type="submit">保存</button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, onMounted, computed } from 'vue'
// 新增的响应式变量
const showApiKey = ref(false)
//const isInitialLoad = ref(true)

/*
// 生成随机字符串用于autocomplete和name属性
const randomString = () => Math.random().toString(36).substring(2, 15)
const randomAutocomplete = computed(() => `new-password-${randomString()}`)
const randomName = computed(() => `no-autofill-${randomString()}`)

const unlockInput = (e) => {
  e.target.removeAttribute('readonly')
  // 确保清空可能被自动填充的值
  if (e.target.value === 'auto-filled-value') {
    e.target.value = ''
  }
}

onMounted(() => {
  // 最终保险：500ms后强制清空
  setTimeout(() => {
    formData.value.api_address = ''
    formData.value.api_key = ''
    //isInitialLoad.value = false
  }, 500)
  
  // 防止自动填充样式
  const style = document.createElement('style')
  style.innerHTML = `
    input:-webkit-autofill,
    input:-webkit-autofill:hover,
    input:-webkit-autofill:focus {
      -webkit-text-fill-color: #000 !important;
      -webkit-box-shadow: 0 0 0px 1000px white inset !important;
      transition: background-color 9999s ease-in-out 0s !important;
    }
  `
  document.head.appendChild(style)
})

// 新增的类型变更处理函数
const handleTypeChange = () => {
  if (formData.value.api_type !== 'other') {
    formData.value.custom_type = ''
  }
}
*/


const props = defineProps({
  api: {
    type: Object,
    default: () => ({
      api_name: '',
      api_address: '',
      api_type: '',
      api_key: '',
      is_active: true
    })
  }
})

const emit = defineEmits(['save', 'cancel'])

const formData = ref({
  api_name: '',
  api_address: '',
  api_type: '',
  api_key: '',
  is_active: true
})

// 初始化表单数据
watch(() => props.api, (newVal) => {
  formData.value = {
    api_name: newVal.api_name || '',
    api_address: newVal.api_address || '',
    api_type: newVal.api_type || '',
    api_key: newVal.api_key || '',
    is_active: newVal.is_active ?? true,
    key_id: newVal.key_id || null
  }
}, { immediate: true, deep: true })

const handleSubmit = () => {
  emit('save', formData.value)
}
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.input-with-action {
  display: flex;
  gap: 0.5rem;
}

.input-with-action input {
  flex: 1;
}

.toggle-visibility {
  padding: 0 1rem;
  background-color: #f3f4f6;
  border: 1px solid #ddd;
  border-radius: 4px;
  cursor: pointer;
}

.modal-content {
  background-color: white;
  padding: 2rem;
  border-radius: 8px;
  width: 100%;
  max-width: 500px;
  position: relative;
}

.close-btn {
  position: absolute;
  top: 1rem;
  right: 1rem;
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: #666;
}

h2 {
  margin-top: 0;
  margin-bottom: 1.5rem;
  color: #1f2937;
}

.form-group {
  margin-bottom: 1rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
}

.form-group input{
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
}

.form-group input[type="checkbox"] {
  width: auto;
  margin-right: 0.5rem;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 0.5rem;
  margin-top: 1.5rem;
}

.form-actions button {
  padding: 0.75rem 1.5rem;
  border-radius: 4px;
  font-size: 1rem;
  cursor: pointer;
}

.form-actions button[type="button"] {
  background-color: #f3f4f6;
  border: 1px solid #ddd;
  color: #4b5563;
}

.form-actions button[type="submit"] {
  background-color: #4f46e5;
  color: white;
  border: none;
}
</style>