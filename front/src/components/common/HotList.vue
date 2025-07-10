<template>
  <div class="hot-list">
    <h3>热门提示词</h3>
    <div class="hot-prompts">
      <PromptCard 
        v-for="prompt in hotPrompts" 
        :key="prompt.prompt_id" 
        :prompt="prompt"
        mode="compact"
        @like="handleLike"
        @favorite="handleFavorite"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useApi } from '@/composables/useApi'
import PromptCard from '@/components/prompts/PromptCard.vue'


const { get } = useApi()
const hotPrompts = ref([])

onMounted(async () => {
  try {
    const data = await get('/public/hot-prompts')
    // 获取每个提示词的点赞/收藏状态
    const promptsWithStatus = await Promise.all(
      data.map(async (item, index) => {
        const [likeStatus, collectStatus] = await Promise.all([
          get(`/public/prompts/${item.prompt_id}/like-status`),
          get(`/public/prompts/${item.prompt_id}/collect-status`)
        ])
        return {
          ...item,
          rank: index + 1,
          is_liked: likeStatus.liked,
          is_favorited: collectStatus.collected
        }
      })
    )
    hotPrompts.value = promptsWithStatus
  } catch (err) {
    console.error('Failed to fetch hot prompts:', err)
  }
})

const handleLike = (promptId) => {
  emit('like', promptId)
}

const handleFavorite = (promptId) => {
  emit('favorite', promptId)
}

const emit = defineEmits(['like', 'favorite'])
</script>

<style scoped>
.hot-list {
  background: white;
  padding: 1rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  margin-bottom: 1.5rem;
}

.hot-list h3 {
  margin-bottom: 1rem;
  color: #4f46e5;
}

.hot-prompts {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.hot-item {
  display: flex;
  align-items: center;
  padding: 0.75rem 0;
  border-bottom: 1px solid #eee;
}

.hot-item:last-child {
  border-bottom: none;
}

.rank {
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #f3f4f6;
  border-radius: 4px;
  margin-right: 1rem;
  font-size: 0.875rem;
  font-weight: 600;
}

.content {
  flex: 1;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  font-size: 0.875rem;
}

.likes {
  color: #6b7280;
  font-size: 0.75rem;
  margin-left: 1rem;
}
</style>