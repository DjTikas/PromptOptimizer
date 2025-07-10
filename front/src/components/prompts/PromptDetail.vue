<template>
  <div class="prompt-detail">
    <div class="header">
      <h2>提示词详情</h2>
      <div class="actions">
        <button @click="handleEdit" class="edit-btn">编辑</button>
        <button @click="handleDelete" class="delete-btn">删除</button>
      </div>
    </div>
    
    <div class="content">
      <div class="section">
        <h3>原始提示词</h3>
        <pre>{{ prompt.original_content }}</pre>
      </div>
      
      <div class="section">
        <h3>优化后提示词</h3>
        <pre>{{ prompt.optimized_content }}</pre>
      </div>
      
      <div class="section" v-if="prompt.tags && prompt.tags.length > 0">
        <h3>标签</h3>
        <div class="tags">
          <span v-for="tag in prompt.tags" :key="tag.tag_id" class="tag">
            {{ tag.tag_name }}
          </span>
        </div>
      </div>
      
      <div class="section">
        <h3>使用统计</h3>
        <div class="stats">
          <div class="stat-item">
            <span class="stat-label">使用次数</span>
            <span class="stat-value">{{ prompt.usage_count || 0 }}</span>
          </div>
          <div class="stat-item">
            <span class="stat-label">点赞数</span>
            <span class="stat-value">{{ prompt.like_count || 0 }}</span>
          </div>
          <div class="stat-item">
            <span class="stat-label">创建时间</span>
            <span class="stat-value">{{ formatDate(prompt.created_at) }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { defineProps, defineEmits } from 'vue'

const props = defineProps({
  prompt: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['edit', 'delete'])

const formatDate = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleDateString()
}

const handleEdit = () => {
  emit('edit', props.prompt)
}

const handleDelete = () => {
  if (confirm('确定要删除这个提示词吗？')) {
    emit('delete', props.prompt.prompt_id)
  }
}
</script>

<style scoped>
.prompt-detail {
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  border-bottom: 1px solid #eee;
}

.header h2 {
  margin: 0;
  color: #1f2937;
}

.actions {
  display: flex;
  gap: 0.5rem;
}

.edit-btn {
  padding: 0.5rem 1rem;
  background-color: #e0e7ff;
  color: #4f46e5;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.delete-btn {
  padding: 0.5rem 1rem;
  background-color: #fee2e2;
  color: #ef4444;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.content {
  padding: 1.5rem;
}

.section {
  margin-bottom: 2rem;
}

.section h3 {
  margin-top: 0;
  margin-bottom: 1rem;
  color: #4f46e5;
}

.section pre {
  white-space: pre-wrap;
  word-break: break-word;
  background-color: #f9fafb;
  padding: 1rem;
  border-radius: 4px;
  font-family: inherit;
  margin: 0;
}

.tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.tag {
  background-color: #e0e7ff;
  color: #4f46e5;
  padding: 0.5rem 0.75rem;
  border-radius: 4px;
  font-size: 0.875rem;
}

.stats {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  gap: 1rem;
}

.stat-item {
  background-color: #f9fafb;
  padding: 1rem;
  border-radius: 4px;
}

.stat-label {
  display: block;
  font-size: 0.875rem;
  color: #6b7280;
  margin-bottom: 0.25rem;
}

.stat-value {
  font-weight: 500;
  color: #1f2937;
}
</style>