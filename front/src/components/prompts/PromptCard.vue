<template>
  <div class="prompt-card" ref="cardRef">
    <!-- 卡片内容 -->
    <div class="card-content" @click="handleCardClick">
      <div class="prompt-content">
        <h3 class="prompt-title">{{ prompt.original_content }}</h3>
        <div class="prompt-body">{{ prompt.optimized_content }}</div>
      </div>
      
      <div class="prompt-footer">
        <div class="tags">
          <span v-for="tag in prompt.tags" :key="tag.tag_id" class="tag">
            {{ tag.tag_name }}
          </span>
        </div>
        
        <div class="actions">
          <button @click.stop="handleLike" class="like-btn" :class="{ liked: isLiked }">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"></path>
            </svg>
            {{ prompt.like_count || 0 }}
          </button>
          <button @click.stop="handleFavorite" class="favorite-btn">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M19 21l-7-5-7 5V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2z"></path>
            </svg>
            收藏
          </button>
        </div>
      </div>
    </div>

    <!-- 详情弹窗 -->
    <teleport to="body" v-if="showDetailModal">
      <div 
        class="prompt-detail-modal"
        @click.self="closeDetail"
      >
        <div class="modal-content">
          <button class="close-btn" @click="closeDetail">×</button>
          <h3>创作信息</h3>
          <div class="detail-content">{{ prompt.user_info.email }}  
          {{ formatDate(prompt.created_at) }}
          </div>
          <h3>原始提示词</h3>
          <div class="detail-content">{{ prompt.original_content }}</div>
          <h3>优化后的提示词</h3>
          <div class="detail-content">{{ prompt.optimized_content }}</div>
          <h3>标签</h3>
          <div class="tags">
            <span v-for="tag in prompt.tags" :key="tag.tag_id" class="tag">
              {{ tag.tag_name }}
            </span>
          </div>
        </div>
      </div>
    </teleport>

    <!-- 紧凑模式 -->
    <div v-if="mode === 'compact'" class="compact-content" @click="handleCardClick">
      <div class="compact-main">
        <span class="rank">{{ prompt.rank }}</span>
        <span class="title">{{ prompt.original_content }}</span>
      </div>
      <div class="compact-footer">
        <span class="likes">{{ prompt.like_count }}赞</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch } from 'vue' // 添加了watch导入
import { useUserStore } from '@/store'

const cardRef = ref(null)

// 添加日期格式化函数
const formatDate = (dateString) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  })
}
const props = defineProps({
  prompt: {
    type: Object,
    required: true
  }
  /*,
  mode: {
    type: String,
    default: 'card' // 'card' 或 'compact'
  }
  */
})


const emit = defineEmits(['like', 'favorite'])
const showDetailModal = ref(false)
const isLiked = computed(() => props.prompt.is_liked === true)
const userStore = useUserStore()

// 鼠标位置状态
const mouseInModal = ref(false)
const mouseInCard = ref(false)

const handleCardClick = (e) => {
  // 排除按钮点击
  if (e.target.closest('button')) {
    return
  }
  showDetailModal.value = true
}

const closeDetail = () => {
  showDetailModal.value = false
}

const handleModalMouseMove = () => {
  mouseInModal.value = true
}

// 全局鼠标移动监听
const handleMouseMove = (e) => {
  const cardEl = document.querySelector('.prompt-card')
  if (cardEl && cardEl.contains(e.target)) {
    mouseInCard.value = true
  } else {
    mouseInCard.value = false
  }
}

// 防止弹窗闪烁的核心逻辑
watch(showDetailModal, (val) => {
  if (val) {
    document.addEventListener('mousemove', handleMouseMove)
  } else {
    document.removeEventListener('mousemove', handleMouseMove)
    mouseInModal.value = false
    mouseInCard.value = false
  }
})

onUnmounted(() => {
  document.removeEventListener('mousemove', handleMouseMove)
})

const handleLike = (e) => {
  e.stopPropagation()
  if (!userStore.isLoggedIn) {
    alert('请先登录')
    return
  }
  emit('like', props.prompt.prompt_id)
}

const handleFavorite = (e) => {
  e.stopPropagation()
  if (!userStore.isLoggedIn) {
    alert('请先登录')
    return
  }
  emit('favorite', props.prompt.prompt_id)
}
/*
defineProps({
  prompt: {
    type: Object,
    required: true
  },
  mode: {
    type: String,
    default: 'card' // 'card' 或 'compact'
  }
})
*/
</script>

<style scoped>
/* 原有卡片样式保持不变 */
.prompt-card {
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  transition: transform 0.2s, box-shadow 0.2s;
  position: relative;
}

.card-content {
  cursor: pointer;
}

.prompt-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.prompt-content {
  padding: 1.5rem;
}

.prompt-title {
  margin-top: 0;
  margin-bottom: 1rem;
  font-size: 1.125rem;
  color: #1f2937;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.prompt-body {
  color: #6b7280;
  font-size: 0.875rem;
  line-height: 1.5;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
}

.prompt-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem 1.5rem;
  border-top: 1px solid #eee;
  background-color: #f9fafb;
}

.tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.tag {
  background-color: #e0e7ff;
  color: #4f46e5;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.75rem;
}

.actions {
  display: flex;
  gap: 0.5rem;
}

.actions button {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  padding: 0.5rem 0.75rem;
  border-radius: 4px;
  font-size: 0.875rem;
  cursor: pointer;
  border: none;
}

.like-btn {
  background-color: #f3f4f6;
  color: #6b7280;
}

.like-btn.liked {
  background-color: #fee2e2;
  color: #ef4444;
}

.like-btn svg {
  width: 16px;
  height: 16px;
  fill: none;
}

.like-btn.liked svg {
  fill: currentColor;
}

.favorite-btn {
  background-color: #e0e7ff;
  color: #4f46e5;
}

.favorite-btn svg {
  width: 16px;
  height: 16px;
  fill: none;
}

/* 弹窗样式 */
.prompt-detail-modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  border-radius: 8px;
  padding: 2rem;
  width: 80%;
  max-width: 800px;
  max-height: 80vh;
  overflow-y: auto;
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

.detail-content {
  margin-bottom: 1.5rem;
  padding: 1rem;
  background: #f9f9f9;
  border-radius: 4px;
  white-space: pre-wrap;
  word-break: break-word;
}

.detail-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 1.5rem;
  padding-top: 1rem;
  border-top: 1px solid #eee;
}

.action-buttons {
  display: flex;
  gap: 0.5rem;
}

/* 紧凑模式样式 */
.prompt-card.compact {
  background: white;
  border-radius: 8px;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
  margin-bottom: 0.5rem;
  transition: all 0.2s;
}

.prompt-card.compact:hover {
  transform: translateY(-1px);
  box-shadow: 0 3px 6px rgba(0, 0, 0, 0.1);
}

.compact-content {
  display: flex;
  flex-direction: column;
  padding: 0.75rem;
  cursor: pointer;
}

.compact-main {
  display: flex;
  align-items: center;
}

.compact-main .rank {
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #f3f4f6;
  border-radius: 4px;
  margin-right: 0.75rem;
  font-size: 0.875rem;
  font-weight: 600;
}

.compact-main .title {
  flex: 1;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  font-size: 0.875rem;
}

.compact-footer {
  display: flex;
  justify-content: flex-end;
  margin-top: 0.25rem;
}

.compact-footer .likes {
  color: #6b7280;
  font-size: 0.75rem;
}
</style>