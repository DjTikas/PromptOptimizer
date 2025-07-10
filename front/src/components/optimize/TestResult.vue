<template>
  <div class="test-result-container">
    <!-- 模型配置部分 -->
    <ConfigForm 
      v-model="modelConfig" 
      class="config-section"
    />
    
    <!-- 测试结果部分 -->
    <div class="test-section">
      <h3>提示词测试</h3>
      
      <div class="tabs">
        <button 
          :class="{ active: activeTab === 'original' }" 
          @click="activeTab = 'original'"
        >
          原始提示词
        </button>
        <button 
          :class="{ active: activeTab === 'optimized' }" 
          @click="activeTab = 'optimized'"
        >
          优化后提示词
        </button>
      </div>
      
      <div class="content">
        <div v-if="activeTab === 'original'" class="prompt-content">
          <pre>{{ original }}</pre>
          <button 
            @click="test('original')" 
            :disabled="isTesting"
            class="test-btn"
          >
            {{ isTesting ? '测试中...' : '测试原始提示词' }}
          </button>
        </div>
        
        <div v-else class="prompt-content">
          <pre>{{ optimized }}</pre>
          <button 
            @click="test('optimized')" 
            :disabled="isTesting"
            class="test-btn"
          >
            {{ isTesting ? '测试中...' : '测试优化提示词' }}
          </button>
        </div>
      </div>
      
      <div v-if="testResult" class="test-output">
        <h4>测试输出</h4>
        <div class="output-content">
          <pre>{{ testResult }}</pre>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import ConfigForm from '@/components/optimize/ConfigForm.vue'

const props = defineProps({
  original: {
    type: String,
    required: true
  },
  optimized: {
    type: String,
    required: true
  }
})

const activeTab = ref('optimized')
const testResult = ref('')
const isTesting = ref(false)

const modelConfig = ref({
  enabled: false,
  name: '',
  model: {
    model: 'gpt-3.5-turbo',
    api_base: 'https://api.chatanywhere.tech',
    api_key: 'sk-QGEkpTzYOdG6jkOtTR2UIpR09XINClFMG77POafAefkknppB',
    api_type: 'openai'
  }
})

const test = async (type) => {
  isTesting.value = true
  testResult.value = '测试中...'
  
  try {
    const prompt = type === 'original' ? props.original : props.optimized
    
    // 1. 确保API地址正确
    const apiUrl = 'http://47.121.119.236/optimize/test'
    
    const response = await fetch(apiUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        prompt,
        config: modelConfig.value.model
      })
    })
    
    // 2. 先检查响应内容类型
    const contentType = response.headers.get('content-type')
    
    if (!contentType || !contentType.includes('application/json')) {
      const text = await response.text()
      throw new Error(`无效的响应格式: ${text.slice(0, 100)}...`)
    }
    
    if (!response.ok) {
      const errorData = await response.json()
      throw new Error(errorData.detail || `请求失败: ${response.status}`)
    }
    
    const data = await response.json()
    testResult.value = data.result || JSON.stringify(data, null, 2)
    
  } catch (err) {
    testResult.value = `测试失败: ${err.message}`
    console.error('测试错误:', err)
  } finally {
    isTesting.value = false
  }
}

console.log('接收的原始提示词:', props.original)
console.log('接收的优化提示词:', props.optimized)
</script>

<style scoped>
.test-result-container {
  display: flex;
  gap: 2rem;
  margin-top: 2rem;
  width: 100%; /* 添加这一行确保占满父容器 */
}

.config-section {
  flex: 0 0 250px; /* 固定配置部分宽度 */
}

.test-section {
  flex: 0 0 750px; /* 让测试部分占据剩余所有空间 */
  min-width: 0; /* 防止内容溢出 */
}

.tabs {
  display: flex;
  border-bottom: 1px solid #eee;
  margin-bottom: 1rem;
}

.tabs button {
  padding: 0.75rem 1.5rem;
  background: none;
  border: none;
  cursor: pointer;
  font-size: 1rem;
  color: #6b7280;
  border-bottom: 2px solid transparent;
}

.tabs button.active {
  color: #4f46e5;
  border-bottom-color: #4f46e5;
  font-weight: 500;
}

.prompt-content {
  margin-bottom: 1.5rem;
  width: 100%;
}

.prompt-content pre {
  white-space: pre-wrap;
  word-break: break-word;
  background-color: #f9fafb;
  padding: 1rem;
  border-radius: 4px;
  font-family: inherit;
  margin-bottom: 1rem;
  width: 100%; /* 添加这一行 */
}

.test-btn {
  padding: 0.75rem 1.5rem;
  background-color: #4f46e5;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
  transition: background-color 0.2s;
}

.test-btn:hover:not(:disabled) {
  background-color: #4338ca;
}

.test-btn:disabled {
  background-color: #a5b4fc;
  cursor: not-allowed;
}

.test-output {
  border-top: 1px solid #eee;
  padding-top: 1rem;
  margin-top: 1rem;
  width: 100%; /* 确保输出框占满 */
}

.test-output h4 {
  margin-top: 0;
  margin-bottom: 0.5rem;
  color: #4b5563;
  width: 100%; /* 确保输出框占满 */
}

.output-content {
  background-color: #f9fafb;
  padding: 1rem;
  border-radius: 4px;
  white-space: pre-wrap;
  word-break: break-word;
  max-height: 300px;
  overflow-y: auto;
  width: 100%; /* 确保输出框占满 */
}

.content {
  width: 100%; /* 确保内容区域占满 */
}

@media (max-width: 768px) {

  
  .config-section,
  .test-section {
    width: 100%;
  }
}
</style>