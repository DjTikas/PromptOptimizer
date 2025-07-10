<template>
  <div class="tag-selector">
    <div class="selected-tags">
      <span v-for="tag in modelValue" :key="tag" class="tag">
        {{ tag }}
        <button @click="removeTag(tag)">×</button>
      </span>
      <input
        v-model="inputValue"
        type="text"
        placeholder="添加标签..."
        @keydown.enter="addTag"
        @keydown.backspace="handleBackspace"
        @blur="addTag"
      />
    </div>
    <div v-if="suggestions.length > 0" class="suggestions">
      <div
        v-for="tag in suggestions"
        :key="tag.tag_id"
        class="suggestion"
        @click="selectTag(tag)"
      >
        {{ tag.tag_name }}
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { useApi } from '@/composables/useApi'

const props = defineProps({
  modelValue: {
    type: Array,
    default: () => []
  }
})

const emit = defineEmits(['update:modelValue'])

const { get } = useApi()
const inputValue = ref('')
const suggestions = ref([])

watch(inputValue, async (newValue) => {
  if (newValue.length > 1) {
    try {
      const data = await get(`/public/search-tags?query=${newValue}&limit=5`)
      suggestions.value = data
    } catch (err) {
      console.error('获取标签建议失败:', err)
      suggestions.value = []
    }
  } else {
    suggestions.value = []
  }
})

const addTag = () => {
  const tag = inputValue.value.trim()
  if (tag && !props.modelValue.includes(tag)) {
    emit('update:modelValue', [...props.modelValue, tag])
    inputValue.value = ''
    suggestions.value = []
  }
}

const removeTag = (tag) => {
  emit('update:modelValue', props.modelValue.filter(t => t !== tag))
}

const selectTag = (tag) => {
  if (!props.modelValue.includes(tag.tag_name)) {
    emit('update:modelValue', [...props.modelValue, tag.tag_name])
  }
  inputValue.value = ''
  suggestions.value = []
}
</script>

<style scoped>
.tag-selector {
  position: relative;
}

.selected-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  align-items: center;
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  min-height: 40px;
}

.tag {
  display: inline-flex;
  align-items: center;
  background-color: #e0e7ff;
  color: #4f46e5;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.875rem;
}

.tag button {
  margin-left: 0.25rem;
  background: none;
  border: none;
  color: #4f46e5;
  cursor: pointer;
  font-size: 0.875rem;
  line-height: 1;
}

.selected-tags input {
  flex: 1;
  min-width: 100px;
  border: none;
  outline: none;
  padding: 0.25rem;
}

.suggestions {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  background-color: white;
  border: 1px solid #ddd;
  border-radius: 0 0 4px 4px;
  z-index: 10;
  max-height: 200px;
  overflow-y: auto;
}

.suggestion {
  padding: 0.5rem 1rem;
  cursor: pointer;
}

.suggestion:hover {
  background-color: #f3f4f6;
}
</style>