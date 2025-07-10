<template>
  <div class="config-form">
    <div class="header">
      <h3>模型配置</h3>
      <label class="enable-toggle">
        <input type="checkbox" v-model="enabled" /> 启用
      </label>
    </div>

    <div v-if="enabled" class="config-container"> 
      <div class="form-group">
        <label>配置名称</label>
        <input v-model="localConfig.name" type="text" placeholder="例如: GPT-3.5 优化配置">
      </div>
      
      <div class="form-group">
        <label>API 地址</label>
        <input v-model="localConfig.model.api_base" type="url" placeholder="例如: https://api.openai.com/v1">
      </div>
      
      <div class="form-group">
        <label>API 密钥</label>
        <div class="api-key-input">
          <input 
            v-model="localConfig.model.api_key" 
            :type="showApiKey ? 'text' : 'password'" 
            placeholder="输入 API 密钥"
          >
          <button @click="showApiKey = !showApiKey" class="toggle-btn">
            {{ showApiKey ? '隐藏' : '显示' }}
          </button>
          <button @click="selectFromApiList" class="select-btn">
            选择 API
          </button>
        </div>
      </div>
      
      <!-- 修改为文本输入的API类型 -->
      <div class="form-group">
        <label>默认模型</label>
        <input 
          v-model="localConfig.model.model" 
          type="text" 
          placeholder="例如: gpt-3.5-turbo, deepseek-v3 等"
        >
      </div>
    </div>
  </div>
</template>


<script setup>
import { ref, watch } from 'vue'

const props = defineProps({
  modelValue: {
    type: Object,
    required: true,
    default: () => ({
      enabled: false,
      name: '',
      model: {
        model: '',
        api_base: '',
        api_key: '',
        api_type: '' // 默认值改为文本形式
      }
    })
  }
})

const emit = defineEmits(['update:modelValue'])

// 初始化时直接使用传入的值
const enabled = ref(props.modelValue.enabled || false)
const localConfig = ref({ 
  ...props.modelValue,
  model: {
    ...props.modelValue.model,
    api_type: props.modelValue.model?.api_type || '' // 确保有默认值
  }
})

const showApiKey = ref(false)

// 监听变化并触发更新
watch(enabled, (newVal) => {
  localConfig.value.enabled = newVal
  emitUpdate()
})

watch(localConfig, (newVal) => {
  emitUpdate()
}, { deep: true })

const emitUpdate = () => {
  emit('update:modelValue', localConfig.value)
}

const selectFromApiList = () => {
  console.log('打开 API 选择器')
}
</script>


<style scoped>
.config-form {
  margin-bottom: 1.5rem;
  padding: 1rem;
  background-color: #f9fafb;
  border-radius: 8px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0; /* 移除底部边距 */
}

.header h3 {
  margin: 0;
  color: #4f46e5;
}

.enable-toggle {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
}

.config-container {
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: 1px solid #eee;
}

h3 {
  margin-top: 0;
  margin-bottom: 1rem;
  color: #4f46e5;
}

.form-group {
  margin-bottom: 1rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: #4b5563;
}

.role-container {
  border-top: 1px solid #eee;
  padding-top: 1rem;
}

.form-group input,
.form-group select {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
}

.api-key-input {
  display: flex;
  gap: 0.5rem;
}

.api-key-input input {
  flex: 1;
}

.toggle-btn {
  padding: 0 1rem;
  background-color: #e5e7eb;
  border: 1px solid #ddd;
  border-radius: 4px;
  cursor: pointer;
  white-space: nowrap;
}

.select-btn {
  padding: 0 1rem;
  background-color: #4f46e5;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  white-space: nowrap;
}
</style>