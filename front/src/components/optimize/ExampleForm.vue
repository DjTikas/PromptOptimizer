<template>
  <div class="example-form">
    <div class="header">
      <h3>示例增强</h3>
      <label>
        <input type="checkbox" v-model="enabled" /> 启用
      </label>
    </div>
    
    <div v-if="enabled" class="examples-container">
      <div v-for="(example, index) in localExamples" :key="index" class="example-item">
        <div class="example-header">
          <span>示例 {{ index + 1 }}</span>
          <button @click="removeExample(index)" class="remove-btn">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <polyline points="3 6 5 6 21 6"></polyline>
              <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
            </svg>
          </button>
        </div>
        <div class="form-group">
          <label>输入</label>
          <textarea v-model="example.input" placeholder="输入示例"></textarea>
        </div>
        <div class="form-group">
          <label>输出</label>
          <textarea v-model="example.output" placeholder="期望输出"></textarea>
        </div>
      </div>
      
      <button @click="addExample" class="add-btn" :disabled="localExamples.length >= 5">
        添加示例 ({{ localExamples.length }}/5)
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, computed } from 'vue'

const props = defineProps({
  modelValue: {
    type: Array,
    default: () => []
  }
})

const emit = defineEmits(['update:modelValue'])

const enabled = ref(props.modelValue.length > 0)
const localExamples = ref([...props.modelValue])

if (localExamples.value.length === 0) {
  localExamples.value.push({ input: '', output: '' })
}

watch(enabled, (newVal) => {
  if (!newVal) {
    localExamples.value = []
  } else if (localExamples.value.length === 0) {
    localExamples.value.push({ input: '', output: '' })
  }
  emitUpdate()
})

watch(localExamples, () => {
  emitUpdate()
}, { deep: true })

const emitUpdate = () => {
  emit('update:modelValue', enabled.value ? localExamples.value : [])
}

const addExample = () => {
  if (localExamples.value.length < 5) {
    localExamples.value.push({ input: '', output: '' })
  }
}

const removeExample = (index) => {
  localExamples.value.splice(index, 1)
  if (localExamples.value.length === 0) {
    enabled.value = false
  }
}
</script>

<style scoped>
.example-form {
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

.examples-container {
  border-top: 1px solid #eee;
  padding-top: 1rem;
}

.example-item {
  margin-bottom: 1.5rem;
  padding: 1rem;
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
}

.example-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
  font-weight: 500;
}

.remove-btn {
  background: none;
  border: none;
  cursor: pointer;
  color: #9ca3af;
  padding: 0.25rem;
  border-radius: 4px;
}

.remove-btn:hover {
  color: #ef4444;
  background-color: #fee2e2;
}

.remove-btn svg {
  width: 16px;
  height: 16px;
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

.form-group textarea {
  width: 100%;
  min-height: 80px;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
  resize: vertical;
}

.add-btn {
  width: 100%;
  padding: 0.75rem;
  background-color: #e0e7ff;
  color: #4f46e5;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 500;
}

.add-btn:hover {
  background-color: #c7d2fe;
}

.add-btn:disabled {
  background-color: #f3f4f6;
  color: #9ca3af;
  cursor: not-allowed;
}
</style>