<template>
  <div class="role-form">
    <div class="header">
      <h3>角色扮演</h3>
      <label>
        <input type="checkbox" v-model="enabled" /> 启用
      </label>
    </div>
    
    <div v-if="enabled" class="role-container">
      <div class="form-group">
        <label>角色名称</label>
        <input 
          v-model="localRole.role_name" 
          type="text" 
          placeholder="例如: 资深营养师"
        >
      </div>
      
      <div class="form-group">
        <label>角色描述</label>
        <textarea 
          v-model="localRole.description" 
          placeholder="详细描述角色的专业背景、经验和特点。例如: 擅长儿童膳食规划，拥有10年以上经验..."
        ></textarea>
      </div>
      
      <div class="presets">
        <h4>预设角色</h4>
        <div class="preset-list">
          <button 
            v-for="preset in rolePresets" 
            :key="preset.name"
            @click="applyPreset(preset)"
          >
            {{ preset.name }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'

const props = defineProps({
  modelValue: {
    type: Object,
    default: () => ({
      enabled: false,
      role_name: '',
      description: ''
    })
  }
})

const emit = defineEmits(['update:modelValue'])

const enabled = ref(props.modelValue.enabled)
const localRole = ref({ ...props.modelValue })

const rolePresets = [
  {
    name: '资深营养师',
    description: '擅长儿童膳食规划，拥有10年以上经验，能够根据孩子的年龄、体质和健康状况提供个性化的饮食建议。'
  },
  {
    name: '专业健身教练',
    description: '拥有国际认证的健身教练资格，擅长制定个性化的训练计划，特别关注运动损伤预防和康复训练。'
  },
  {
    name: '心理咨询师',
    description: '拥有心理学硕士学位，擅长认知行为疗法，能够帮助客户处理焦虑、抑郁等情绪问题。'
  },
  {
    name: '商业顾问',
    description: '拥有20年企业管理经验，擅长战略规划和业务转型，曾帮助多家企业实现业绩增长。'
  }
]

watch(enabled, (newVal) => {
  localRole.value.enabled = newVal
  emitUpdate()
})

watch(localRole, () => {
  emitUpdate()
}, { deep: true })

const emitUpdate = () => {
  emit('update:modelValue', localRole.value)
}

const applyPreset = (preset) => {
  localRole.value.role_name = preset.name
  localRole.value.description = preset.description
}
</script>

<style scoped>
.role-form {
  margin-bottom: 1.5rem;
  padding: 1rem;
  background-color: #f9fafb;
  border-radius: 8px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.header h3 {
  margin: 0;
  color: #4f46e5;
}

.header label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
}

.role-container {
  border-top: 1px solid #eee;
  padding-top: 1rem;
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

.form-group input {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
}

.form-group textarea {
  width: 100%;
  min-height: 100px;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
  resize: vertical;
}

.presets {
  margin-top: 1.5rem;
}

.presets h4 {
  margin-bottom: 0.5rem;
  color: #4b5563;
}

.preset-list {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.preset-list button {
  padding: 0.5rem 1rem;
  background-color: #e0e7ff;
  color: #4f46e5;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.875rem;
}

.preset-list button:hover {
  background-color: #c7d2fe;
}
</style>