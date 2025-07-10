<template>
  <div class="search-bar">
    <div class="search-input">
      <input
        v-model="query"
        type="text"
        placeholder="搜索提示词..."
        @keyup.enter="handleSearch"
      />
      <button @click="handleSearch">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <circle cx="11" cy="11" r="8"></circle>
          <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
        </svg>
      </button>
    </div>
    <button class="hot-button" @click="$emit('toggle-hot')">
      {{ showHot ? '隐藏' : '显示' }}热榜
    </button>
    <div v-if="showAdvanced" class="advanced-search">
      <div class="search-mode">
        <label>
          <input type="radio" v-model="mode" value="AND" /> AND
        </label>
        <label>
          <input type="radio" v-model="mode" value="OR" /> OR
        </label>
      </div>
      <TagSelector v-model="selectedTags" />
    </div>
    <button class="toggle-advanced" @click="showAdvanced = !showAdvanced">
      {{ showAdvanced ? '简化搜索' : '高级搜索' }}
    </button>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import TagSelector from './TagSelector.vue'

const emit = defineEmits(['search', 'toggle-hot'])

const props = defineProps({
  showHot: Boolean
})

const query = ref('')
const mode = ref('AND')
const selectedTags = ref([])
const showAdvanced = ref(false)

const handleSearch = () => {
  emit('search', {
    keyword: query.value,
    tags: selectedTags.value,
    operator: mode.value
  })
}

// 添加防抖
let searchTimeout
watch([query, mode, selectedTags], () => {
  clearTimeout(searchTimeout)
  searchTimeout = setTimeout(() => {
    if (query.value || selectedTags.value.length > 0) {
      handleSearch()
    }
  }, 300)
})
</script>

<style scoped>
.search-bar {
  margin-bottom: 1.5rem;
}

.search-input {
  display: flex;
  margin-bottom: 0.5rem;
}

.search-input input {
  flex: 1;
  padding: 0.75rem 1rem;
  border: 1px solid #ddd;
  border-radius: 4px 0 0 4px;
  font-size: 1rem;
}

.search-input button {
  padding: 0 1rem;
  background-color: #4f46e5;
  color: white;
  border: none;
  border-radius: 0 4px 4px 0;
  cursor: pointer;
}

.search-input button svg {
  width: 20px;
  height: 20px;
}

.hot-button {
  margin-left: 0.5rem;
  padding: 0.5rem 1rem;
  background-color: #f3f4f6;
  border: 1px solid #ddd;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.875rem;
}

.hot-button:hover {
  background-color: #e5e7eb;
}

.advanced-search {
  margin-top: 1rem;
  padding: 1rem;
  background-color: #f9fafb;
  border-radius: 4px;
  border: 1px solid #eee;
}

.search-mode {
  display: flex;
  gap: 1rem;
  margin-bottom: 1rem;
}

.search-mode label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
}

.toggle-advanced {
  margin-top: 0.5rem;
  background: none;
  border: none;
  color: #4f46e5;
  cursor: pointer;
  font-size: 0.875rem;
  text-decoration: underline;
}
</style>