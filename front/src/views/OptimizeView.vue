<template>
  <div class="optimize-view">
    <h1>提示词优化</h1>
    
    <div class="optimize-container">
      <div class="prompt-box">   
        <div class="input-section">
          <h2>原始提示词</h2>
          <textarea
            v-model="originalPrompt" 
            placeholder="请输入需要优化的提示词..." 
            style="height: 300px;" >
          </textarea>
        </div>

        <!-- 优化后的提示词框（移动到下方） -->
        <div class="optimized-section" >
          <h2>优化后的提示词</h2>
          <textarea v-model="optimizedPrompt" readonly style="height: 300px;" >
      
          </textarea>
        </div>
      </div>
      
      <div class="config-section">
        <h2>优化配置</h2>
        
        <!-- 模型配置 - 改为下拉选择 -->
        <div class="model-selector">
          <div class="selector-header">
            <h3><i class="icon fas fa-cogs"></i> 模型配置</h3>
            <div class="status-indicator" v-if="selectedConfig">
              {{ selectedConfig.is_active ? '已激活' : '未激活' }}
            </div>
          </div>
          
          <div class="selector-container">
            <div class="custom-select">
              <select v-model="selectedConfigId" @change="handleConfigChange">
                <!-- 只显示激活的配置 -->
                <option 
                  v-for="config in activeApiConfigs" 
                  :key="config.key_id" 
                  :value="config.key_id"
                  :class="{ 'inactive-option': !config.is_active }"
                >
                  {{ config.api_name }} 
                  <span v-if="!config.is_active">(未激活)</span>
                </option>
                <option value="manage" class="add-option">
                  <i class="fas fa-plus-circle"></i> 添加新配置
                </option>
              </select>
              <div class="select-arrow">
                <i class="fas fa-chevron-down"></i>
              </div>
            </div>
            <button class="manage-btn" @click="goToApiManagement">
              <i class="fas fa-external-link-alt"></i> 管理配置
            </button>
          </div>
          
          <!-- 显示当前配置详情 -->
          <div v-if="selectedConfig" class="config-details">
            <div class="detail-item">
              <i class="icon fas fa-code"></i>
              <div class="detail-content">
                <div class="detail-label">API 类型</div>
                <div class="detail-value">{{ selectedConfig.api_type }}</div>
              </div>
            </div>
            
            <div class="detail-item">
              <i class="icon fas fa-link"></i>
              <div class="detail-content">
                <div class="detail-label">API 地址</div>
                <div class="detail-value">{{ selectedConfig.api_address }}</div>
              </div>
            </div>
            
            <!-- 配置状态提示 -->
            <div v-if="!selectedConfig.is_active" class="config-warning">
              <i class="fas fa-exclamation-triangle"></i>
              此配置当前未激活，无法使用
            </div>
          </div>
        </div>
        <!-- 角色配置 -->
        <RoleForm v-model="roleConfig" />
        <!-- 示例配置 -->
        <ExampleForm v-model="examples" />
        
        <div class="cot-config">
          <label>
            <input type="checkbox" v-model="useCoT" /> 启用思维链 (CoT)
          </label>
          <select v-if="useCoT" v-model="cotLevel">
            <option value="basic">基础 (2-3步)</option>
            <option value="intermediate">中级 (4-5步)</option>
            <option value="advanced">高级 (多层级推理)</option>
            <option value="custom">自定义</option>
          </select>
          <div v-if="useCoT && cotLevel === 'custom'" class="custom-cot">
            <div v-for="(step, index) in customSteps" :key="index" class="cot-step">
              <input v-model="customSteps[index]" placeholder="步骤描述">
              <button @click="removeStep(index)">删除</button>
            </div>
            <button @click="addStep">添加步骤</button>
          </div>
        </div>
      </div>
      
      <div class="actions">
        <button 
          @click="optimizePrompt" 
        >
          {{ isOptimizing ? '优化中...' : '优化提示词' }}
        </button>
      </div>
      

      <!-- 提示词测试部分 -->
      <div class="test-section" v-if="optimizedPrompt">
        <h2>提示词测试</h2>
        
        <!-- 对比开关 -->
        <div class="compare-toggle">
          <label>
            <input type="checkbox" v-model="showCompare" /> 
            开启结果对比
          </label>
        </div>
        
        <div class="test-results">
          <!-- 原始提示词测试 -->
          <div class="test-result" v-if="showCompare">
            <div class="result-header">
              <h3>原始提示词测试结果</h3>
              <!-- 复用模型选择器样式 -->
              <div class="model-selector test-config">
                <div class="selector-header">
                  <h3><i class="icon fas fa-cogs"></i> 测试模型配置</h3>
                </div>
                <div class="selector-container">
                  <div class="custom-select">
                    <select v-model="testConfigOriginalId">
                      <option 
                        v-for="config in activeApiConfigs" 
                        :key="config.key_id" 
                        :value="config.key_id"
                      >
                        {{ config.api_name }} 
                      </option>
                    </select>
                    <div class="select-arrow">
                      <i class="fas fa-chevron-down"></i>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <div class="test-area">
              <button @click="testOriginalPrompt">测试原始提示词</button>
              <textarea 
                v-model="testResultOriginal" 
                readonly 
                placeholder="原始提示词测试结果将显示在这里"
                style="height: 300px;"
              ></textarea>
            </div>
          </div>
          
          <!-- 优化提示词测试 -->
          <div class="test-result">
            <div class="result-header">
              <h3>优化提示词测试结果</h3>
              <!-- 复用模型选择器样式 -->
              <div class="model-selector test-config">
                <div class="selector-header">
                  <h3><i class="icon fas fa-cogs"></i> 测试模型配置</h3>
                </div>
                <div class="selector-container">
                  <div class="custom-select">
                    <select v-model="testConfigOptimizedId">
                      <option 
                        v-for="config in activeApiConfigs" 
                        :key="config.key_id" 
                        :value="config.key_id"
                      >
                        {{ config.api_name }} 
                      </option>
                    </select>
                    <div class="select-arrow">
                      <i class="fas fa-chevron-down"></i>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <div class="test-area">
              <button @click="testOptimizedPrompt">测试优化提示词</button>
              <textarea 
                v-model="testResultOptimized" 
                readonly 
                placeholder="优化提示词测试结果将显示在这里"
                style="height: 300px;"
              ></textarea>
            </div>
          </div>
        </div>
      </div>

      <!-- 新增收藏区域 -->
      <div v-if="optimizedPrompt" class="save-section">
        <h3>保存优化结果</h3>
        <div class="save-options">
          <label>
            <input type="checkbox" v-model="isShared" /> 公开分享
          </label>
          <button @click="saveOptimizedPrompt" :disabled="isSaving">
            {{ isSaving ? '保存中...' : '收藏提示词' }}
          </button>
        </div>
        
        <FolderSelectDialog 
          v-if="showFolderSelect"
          :folders="folders"
          :visible="showFolderSelect"
          @select="handleFolderSelect"
          @close="showFolderSelect = false"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref , computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
const router = useRouter()
import { useApi } from '@/composables/useApi'
import { usePrompt } from '@/composables/usePrompt'
import { useNotificationStore } from '@/store/notification'
import ConfigForm from '@/components/optimize/ConfigForm.vue'
import RoleForm from '@/components/optimize/RoleForm.vue'
import ExampleForm from '@/components/optimize/ExampleForm.vue'
import TestResult from '@/components/optimize/TestResult.vue'
import FolderSelectDialog from '@/components/FolderSelectDialog.vue'

const { post, isLoading: isOptimizing, error } = useApi()
const { get } = useApi()


// 新增测试相关状态
const showCompare = ref(true)
const testConfigOriginalId = ref(null)
const testConfigOptimizedId = ref(null)
const testResultOriginal = ref('')
const testResultOptimized = ref('')

// 设置默认测试配置
const activeApiConfigs = computed(() => {
  return apiConfigs.value.filter(config => config.is_active)
})



const { 
  fetchFolders, 
  createFolder, 
  movePrompt,
  isLoading: isPromptLoading,
  createPrompt
} = usePrompt()
const notification = useNotificationStore()

const originalPrompt = ref('')
const optimizedPrompt = ref('')
const config = ref({
  name: '',
  model: {
    api_key: 'sk-QGEkpTzYOdG6jkOtTR2UIpR09XINClFMG77POafAefkknppB',
    model: 'gpt-3.5-turbo',
    api_base: 'https://api.chatanywhere.tech',
    api_type: 'openai'
  }
})

const dj_isOptimizing = ref(false)
// 计算属性判断按钮是否应禁用
const isButtonDisabled = computed(() => {
  return originalPrompt.value.trim() === '' || dj_isOptimizing.value
})

// API 配置列表
const apiConfigs = ref([])
// 当前选中的配置ID
const selectedConfigId = ref(null)

// 获取当前选中的配置
const selectedConfig = computed(() => {
  return apiConfigs.value.find(c => c.key_id === selectedConfigId.value)
})

// 加载API配置
const loadApiConfigs = async () => {
  try {
    const data = await get('/key/')
    apiConfigs.value = data
    
    // 默认选择第一个配置
    if (data.length > 0) {
      selectedConfigId.value = data[0].key_id
    }
  } catch (err) {
    console.error('加载API配置失败:', err)
    window.$notify.error('加载配置列表失败：' + (err.message || '请检查原因'))
  }
}

// 配置变更处理
const handleConfigChange = (event) => {
  if (event.target.value === 'manage') {
    goToApiManagement()
    // 重置选择
    selectedConfigId.value = apiConfigs.value.length > 0 ? apiConfigs.value[0].key_id : null
  }
}

// 跳转到API管理页面
const goToApiManagement = () => {
  router.push({ name: 'api' }) // 确保路由名称正确
}

const roleConfig = ref({
  enabled: false,
  role_name: '',
  description: ''
})
const examples = ref([])
const useCoT = ref(false)
const cotLevel = ref('intermediate')
const customSteps = ref(['', ''])

const addStep = () => {
  customSteps.value.push('')
}

const removeStep = (index) => {
  customSteps.value.splice(index, 1)
}

const optimizePrompt = async () => {
  //if (isButtonDisabled.value) return
  
  //dj_isOptimizing.value = true

  // 定义本地错误消息（如果不想用Pinia/store）
  const localErrorMessage = ref(null)

  console.log('selectedConfig:', selectedConfig.value)
  
  try {
    // 1. 验证必要字段
    if (!originalPrompt.value?.trim()) {
      throw new Error('原始提示词(original_prompt)不能为空')
    }

    // 2. 准备CoT配置
    const cotConfig = useCoT.value ? {
      enabled: true,
      level: cotLevel.value === 'custom' ? 'intermediate' : cotLevel.value, // 确保level合法
      custom_steps: cotLevel.value === 'custom' 
        ? customSteps.value.filter(s => s.trim())
        : []
    } : { 
      enabled: false,
      level: 'intermediate', // 默认值
      custom_steps: [] 
    }

    // 3. 构建完整请求数据（确保包含config.name）
    const requestData = {
      original_prompt: originalPrompt.value.trim(),
      config: {
        name: selectedConfig.value.api_name || '未命名配置', // 使用配置名称
        model: {
          // 使用 selectedConfig 的数据
          model: selectedConfig.value.api_type || 'gpt-3.5-turbo', // 模型名称
          api_base: selectedConfig.value.api_address, // API 地址
          api_key: selectedConfig.value.api_key, // API 密钥
          api_type: 'openai' // API 类型
        },
        role: {
          ...roleConfig.value,
          enabled: roleConfig.value.enabled || false
        },
        examples: examples.value.filter(ex => ex.input && ex.output),
        exam_enabled: examples.value.length > 0,
        cot: cotConfig,
        advanced: {
          temperature: 0.7,
          max_tokens: 500,
          top_p: 0.9
        }
      }
    }

    console.debug('请求数据:', {
      ...requestData,
      config: {
        ...requestData.config,
        model: {
          ...requestData.config.model,
          api_key: requestData.config.model.api_key ? '***隐藏***' : '空' // 隐藏敏感信息
        }
      }
    })

    // 4. 发送请求
    const controller = new AbortController()
    const timeoutId = setTimeout(() => controller.abort(), 15000)
    const result = await post('/optimize/optimize', requestData, {
      signal: controller.signal
    }).finally(() => clearTimeout(timeoutId))

    // 5. 验证响应
    if (!result?.optimized_prompt) {
      throw new Error('API返回数据不完整')
    }

    optimizedPrompt.value = result.optimized_prompt
    localErrorMessage.value = null // 清空错误
    return result

  } catch (err) {
    console.error('优化失败:', err)
    
    // 设置错误消息（根据你的项目选择一种方式）
    
    // 方式A: 使用本地ref（需在setup中return）
    localErrorMessage.value = err.response?.data?.detail?.[0]?.msg 
      || err.message 
      || '优化失败，请检查配置后重试'
    
    // 方式B: 直接抛出（由调用方处理）
    // throw err 
    
    // 方式C: 使用Pinia/Vuex store
    // errorStore.setError(err.message)
    
    throw err // 保持错误传播
  }
}

const testPrompt = async (prompt) => {
  try {
    const result = await post('/optimize/test', {
      prompt,
      config: config.value.model
    })
    return result.result
  } catch (err) {
    console.error('Test failed:', err)
    return '测试失败: ' + err.message
  }
}

const isShared = ref(false) // 新增：是否公开分享
const isSaving = ref(false) // 新增：保存状态
const showFolderSelect = ref(false) // 新增：显示收藏夹选择对话框
const folders = ref([]) // 新增：收藏夹列表
const selectedPromptId = ref(null) // 新增：当前选择的提示词ID

// 获取收藏夹列表
const loadFolders = async () => {
  try {
    folders.value = await fetchFolders()
  } catch (err) {
    notification.showError('获取收藏夹失败: ' + err.message)
  }
}

// 保存优化后的提示词
const saveOptimizedPrompt = async () => {
  if (!optimizedPrompt.value) return
  
  isSaving.value = true
  try {
    const promptData = {
      original_content: originalPrompt.value,
      optimized_content: optimizedPrompt.value,
      is_shared: isShared.value,
      // 可选字段可以省略或设为默认值
      session_id: 1,  // 根据实际需求调整
      usage_count: 0  // 初始使用次数
    }
    
    const result = await createPrompt(promptData)
    
    if (result && result.prompt_id) {
      selectedPromptId.value = result.prompt_id
      await loadFolders()
      showFolderSelect.value = true
      notification.addMessage('提示词创建成功!', 'success')
    } else {
      throw new Error('API返回数据不完整')
    }
  } catch (err) {
    const errorMsg = err.response?.data?.detail?.[0]?.msg || 
                   err.response?.data?.message || 
                   err.message
    notification.addMessage(`创建提示词失败: ${errorMsg}`, 'error')
  } finally {
    isSaving.value = false
  }
}

// 处理收藏夹选择
const handleFolderSelect = async (folder) => {
  if (!selectedPromptId.value) return
  
  try {
    console.log('folder.folder_id:' , folder.folder_id)

    const folderId = Number(folder.folder_id); // 确保是数字

    console.log('folderId: ', folderId)
    
    // 移动提示词到收藏夹
    await movePrompt(folderId, {
      prompt_ids: [selectedPromptId.value],
      move: true
    })
    
    notification.addMessage('提示词收藏成功!', 'success')
    window.$notify.success('收藏成功！')
    showFolderSelect.value = false
    
    // 可选: 刷新当前数据或跳转
    // await loadPrompts()
  } catch (err) {
    const errorMsg = err.response?.data?.detail?.[0]?.msg || 
                   err.response?.data?.message || 
                   err.message
    notification.addMessage(`收藏失败: ${errorMsg}`, 'error')
    window.$notify.error('收藏失败：' + (err.message || '请检查原因'))
  }
}


onMounted(() => {
  loadApiConfigs().then(() => {
    if (activeApiConfigs.value.length > 0) {
      testConfigOriginalId.value = activeApiConfigs.value[0].key_id
      testConfigOptimizedId.value = activeApiConfigs.value[0].key_id
    }
  })
})


// 测试原始提示词
const testOriginalPrompt = async () => {
  try {
    const config = activeApiConfigs.value.find(c => c.key_id === testConfigOriginalId.value)
    if (!config) throw new Error('请选择有效的模型配置')
    
    testResultOriginal.value = '测试中...'
    const result = await post('/optimize/test', {
      prompt: originalPrompt.value,
      config: {
        model: config.api_type || 'gpt-3.5-turbo',
        api_base: config.api_address,
        api_key: config.api_key,
        api_type: 'openai'
      }
    })
    testResultOriginal.value = result.result || '无返回结果'
  } catch (err) {
    console.error('原始提示词测试失败:', err)
    testResultOriginal.value = '测试失败: ' + (err.message || '未知错误')
  }
}

// 测试优化提示词
const testOptimizedPrompt = async () => {
  try {
    const config = activeApiConfigs.value.find(c => c.key_id === testConfigOptimizedId.value)
    if (!config) throw new Error('请选择有效的模型配置')
    
    testResultOptimized.value = '测试中...'
    const result = await post('/optimize/test', {
      prompt: optimizedPrompt.value,
      config: {
        model: config.api_type || 'gpt-3.5-turbo',
        api_base: config.api_address,
        api_key: config.api_key,
        api_type: 'openai'
      }
    })
    testResultOptimized.value = result.result || '无返回结果'
  } catch (err) {
    console.error('优化提示词测试失败:', err)
    testResultOptimized.value = '测试失败: ' + (err.message || '未知错误')
  }
}

</script>

<style scoped>
.optimized-section {
  grid-column: 1;
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  margin-top: 1rem;
}

.test-section {
  grid-column: 1 / -1;
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  margin-top: 2rem;
}

.compare-toggle {
  margin-bottom: 1.5rem;
  padding: 0.5rem 0;
  border-bottom: 1px solid #eee;
}

.compare-toggle label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-weight: 500;
  cursor: pointer;
}

.test-results {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
}

.test-result {
  border: 1px solid #e0e7ff;
  border-radius: 8px;
  padding: 1.2rem;
  background: #f9fafb;
}

.result-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.result-header h3 {
  margin: 0;
  font-size: 1.1rem;
  color: #4f46e5;
}

.test-config {
  width: 70%;
}

.test-config .model-selector {
  padding: 0;
  box-shadow: none;
  border: none;
  margin-bottom: 0;
}

.test-config .selector-header h3 {
  font-size: 0.95rem;
}

.test-area {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.test-area textarea {
  min-height: 150px;
  background: white;
}

.test-area button {
  align-self: flex-start;
  padding: 0.5rem 1rem;
  background-color: #6366f1;
}

.test-area button:hover {
  background-color: #4f46e5;
}

/* 响应式调整 */
@media (max-width: 768px) {
  .test-results {
    grid-template-columns: 1fr;
  }
  
  .result-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }
  
  .test-config {
    width: 100%;
  }
}

.save-section {
  grid-column: 1 / -1;
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  margin-top: 2rem;
}

.save-options {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-top: 1rem;
}

.save-options label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
}

.save-options button {
  padding: 0.5rem 1rem;
}

.optimize-view {
  max-width: 1200px;
  margin: 0 auto;
  padding: 1rem;
}

.optimize-container {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
  margin-top: 2rem;
}

.input-section, .config-section {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

textarea {
  width: 100%;
  min-height: 200px;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  resize: vertical;
}

.actions {
  grid-column: 1 / -1;
  display: flex;
  justify-content: center;
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

button:disabled {
  background-color: #a5b4fc;
  cursor: not-allowed;
}

.cot-config {
  margin-top: 1.5rem;
  padding-top: 1.5rem;
  border-top: 1px solid #eee;
}

.custom-cot {
  margin-top: 1rem;
}

.cot-step {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 0.5rem;
}

.cot-step input {
  flex: 1;
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
}




.model-selector {
  grid-column: span 2;
  background: linear-gradient(135deg, #f8f9ff, #ffffff);
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 6px 16px rgba(79, 70, 229, 0.1);
  border: 1px solid #e0e7ff;
  margin-bottom: 1.5rem;
  transition: all 0.3s ease;
}

.model-selector:hover {
  box-shadow: 0 8px 24px rgba(79, 70, 229, 0.15);
}

.selector-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.2rem;
}

.selector-header h3 {
  margin: 0;
  font-size: 1.25rem;
  color: #4f46e5;
  display: flex;
  align-items: center;
  gap: 10px;
}

.icon {
  color: #818cf8;
}

.status-indicator {
  background-color: #dcfce7;
  color: #16a34a;
}

.status-indicator.inactive {
  background-color: #fee2e2;
  color: #dc2626;
}

/* 选择器容器 */
.selector-container {
  display: flex;
  gap: 1rem;
  margin-top: 0.5rem;
  position: relative;
}

/* 自定义下拉选择框 */
.custom-select {
  flex: 1;
  position: relative;
}

.custom-select select {
  width: 100%;
  padding: 0.85rem 1.2rem;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  font-size: 1rem;
  background-color: white;
  appearance: none;
  outline: none;
  transition: all 0.3s;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
  color: #374151;
}

.custom-select select:focus {
  border-color: #818cf8;
  box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.2);
}

.select-arrow {
  position: absolute;
  right: 1rem;
  top: 50%;
  transform: translateY(-50%);
  pointer-events: none;
  color: #9ca3af;
}

.manage-btn {
  padding: 0.85rem 1.5rem;
  background: linear-gradient(135deg, #4f46e5, #7c3aed);
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  white-space: nowrap;
  font-weight: 500;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 8px;
  box-shadow: 0 4px 6px rgba(79, 70, 229, 0.2);
}

.manage-btn:hover {
  background: linear-gradient(135deg, #4338ca, #6d28d9);
  transform: translateY(-2px);
  box-shadow: 0 6px 10px rgba(79, 70, 229, 0.3);
}

.manage-btn:active {
  transform: translateY(0);
}

/* 配置详情样式 */
.config-details {
  margin-top: 1.5rem;
  padding: 1.2rem;
  background: #f0f4ff;
  border-radius: 10px;
  border-left: 4px solid #4f46e5;
}

.detail-item {
  display: flex;
  gap: 1rem;
  align-items: center;
  padding: 0.8rem 0;
}

.detail-item:not(:last-child) {
  border-bottom: 1px solid #e0e7ff;
}

.detail-item .icon {
  font-size: 1.2rem;
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #e0e7ff;
  border-radius: 8px;
  color: #4f46e5;
}

.detail-content {
  flex: 1;
}

.detail-label {
  font-size: 0.85rem;
  color: #6b7280;
  font-weight: 500;
  margin-bottom: 3px;
}

.detail-value {
  font-size: 1rem;
  color: #1f2937;
  font-weight: 500;
  word-break: break-all;
}

/* 下拉选项样式 */
.add-option {
  color: #4f46e5;
  font-weight: 600;
  background-color: #f0f4ff;
}

/* 响应式调整 */
@media (max-width: 768px) {
  .selector-container {
    flex-direction: column;
  }
  
  .manage-btn {
    width: 100%;
    justify-content: center;
  }
}
</style>