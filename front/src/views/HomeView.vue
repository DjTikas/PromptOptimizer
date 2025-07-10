<template>
  <div class="home-view">
    <SearchBar @search="handleSearch" @toggle-hot="toggleHotList" />
    
    <!-- 传递事件处理函数 -->
    <HotList 
      v-if="showHotList" 
      @like="handleLike"
      @favorite="handleFavorite"
    />
    
    <div class="prompts-container">
      <PromptCard 
        v-for="prompt in prompts" 
        :key="prompt.prompt_id" 
        :prompt="prompt"
        @like="handleLike"
        @favorite="handleFavorite"
      />
    </div>
    
    <div v-if="isLoading" class="loading">加载中...</div>
    <div v-if="error" class="error">{{ error }}</div>

    <FolderSelectDialog 
      v-if="showFolderSelect"
      :folders="folders"
      :collected-folders="collectedFolders"
      :visible="showFolderSelect"
      @select="handleFolderSelect"
      @close="showFolderSelect = false"
    />
  </div>
  
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useApi } from '@/composables/useApi'
import SearchBar from '@/components/common/SearchBar.vue'
import HotList from '@/components/common/HotList.vue'
import PromptCard from '@/components/prompts/PromptCard.vue'

const collectedFolders = ref([])
const { get, isLoading, error, post, del } = useApi()
const prompts = ref([])
const showHotList = ref(false)

// 添加获取点赞/收藏状态的函数
const fetchPromptStatus = async (promptId) => {
  try {
    const [likeStatus, collectStatus] = await Promise.all([
      get(`/public/prompts/${promptId}/like-status`),
      get(`/public/prompts/${promptId}/collect-status`)
    ])
    return {
      is_liked: likeStatus.liked,
      is_favorited: collectStatus.collected
    }
  } catch (err) {
    console.error('获取状态失败:', err)
    return {
      is_liked: false,
      is_favorited: false
    }
  }
}

// 修改加载提示词列表的逻辑
onMounted(async () => {
  try {
    const data = await get('/public/public-prompts')
    
    // 并行获取每个提示词的点赞/收藏状态
    const promptsWithStatus = await Promise.all(
      data.map(async prompt => {
        const status = await fetchPromptStatus(prompt.prompt_id)
        return {
          ...prompt,
          is_liked: status.is_liked,
          is_favorited: status.is_favorited
        }
      })
    )
    
    prompts.value = promptsWithStatus
    console.log('加载的提示词数据:', prompts.value)
  } catch (err) {
    console.error('Failed to fetch prompts:', err)
  }
})


// 修改搜索处理函数
const handleSearch = async ({ keyword, tags, operator }) => {
  try {
    let endpoint = '/public/public-prompts'
    const params = new URLSearchParams()
    
    // 只有当有关键词时才使用搜索接口
    if (keyword && keyword.trim().length > 0) {
      endpoint = '/public/search-prompts'
      params.append('keyword', keyword.trim())
    }
    
    // 如果有标签筛选条件
    if (tags && tags.length > 0) {
      endpoint = '/public/filter-by-tags'
      params.append('tags', tags.join(','))
      params.append('operator', operator || 'AND')
    }

    const data = await get(`${endpoint}?${params.toString()}`)
    prompts.value = data.map(prompt => ({
      ...prompt,
      is_liked: prompt.is_liked === true
    }))
    
  } catch (err) {
    console.error('搜索失败:', err)
    if (err.status === 422) {
      notification.addMessage('搜索参数无效', 'error')
      window.$notify.error('搜索参数无效' + (err.message || '422'))
    } else {
      notification.addMessage('搜索失败，请稍后再试', 'error')
      window.$notify.error('搜索失败，请稍后再试' + (err.message || 'error'))
    }
  }
}

const toggleHotList = () => {
  showHotList.value = !showHotList.value
}

import { useNotificationStore } from '@/store/notification'
const notification = useNotificationStore()

// 修改点赞处理函数（保持原有逻辑）
const handleLike = async (promptId) => {
  try {
    const prompt = prompts.value.find(p => p.prompt_id === promptId)
    if (!prompt) return

    if (prompt.is_liked) {
      await del(`/public/unlike-prompt/${promptId}`)
      prompt.like_count = Math.max(0, prompt.like_count - 1)
    } else {
      await post(`/public/like-prompt/${promptId}`)
      prompt.like_count = (prompt.like_count || 0) + 1
    }
    prompt.is_liked = !prompt.is_liked
    
    // 更新状态后重新获取最新状态（可选）
    const status = await fetchPromptStatus(promptId)
    prompt.is_liked = status.is_liked
    
  } catch (err) {
    console.error('点赞操作失败:', err)
    notification.addMessage(`操作失败: ${err.message}`, 'error')
  }
}

import FolderSelectDialog from '@/components/FolderSelectDialog.vue'
import { usePrompt } from '@/composables/usePrompt'

const { 
  fetchFolders, 
  createFolder, 
  movePrompt,
  isLoading: isPromptLoading,
  error: promptError
} = usePrompt()
// 其他导入...

// 添加状态
const showFolderSelect = ref(false)
const folders = ref([])
const selectedPromptId = ref(null)

// 修改收藏处理函数
const handleFavorite = async (promptId) => {
  try {
    selectedPromptId.value = promptId
    
    // 获取收藏状态（包含已收藏的文件夹）
    const collectStatus = await get(`/public/prompts/${promptId}/collect-status`)
    
    // 获取用户所有收藏夹
    const allFolders = await fetchFolders()
    
    // 显示收藏夹选择对话框，并传入已收藏的文件夹信息
    showFolderSelect.value = true
    folders.value = allFolders
    collectedFolders.value = collectStatus.folders || []
    
  } catch (err) {
    console.error('获取收藏状态失败:', err)
    notification.addMessage('获取收藏信息失败', 'error')
  }
}

const handleFolderSelect = async (folder) => {
  try {
    const promptId = selectedPromptId.value
    
    // 检查是否已在该文件夹收藏
    const isAlreadyCollected = collectedFolders.value.some(
      f => f.folder_id === folder.folder_id
    )
    
    if (isAlreadyCollected) {
      notification.addMessage('该提示词已在此收藏夹', 'info')
      return
    }
    
    // 添加到收藏夹
    await movePrompt(folder.folder_id, {
      prompt_ids: [promptId],
      move: true
    })
    
    // 更新本地状态
    const prompt = prompts.value.find(p => p.prompt_id === promptId)
    if (prompt) {
      prompt.is_favorited = true
      // 添加到已收藏文件夹列表
      collectedFolders.value.push({
        folder_id: folder.folder_id,
        folder_name: folder.folder_name
      })
    }
    
    notification.addMessage(`已添加到「${folder.folder_name}」`, 'success')
    window.$notify.success('收藏成功！')
    
  } catch (err) {
    console.error('收藏失败:', err)
    notification.addMessage(`收藏失败: ${err.message}`, 'error')
    window.$notify.error('收藏失败：' + (err.message || '请检查原因'))
  } finally {
    showFolderSelect.value = false
  }
}

// 移动到收藏夹的公共方法
const moveToFolder = async (folderId, promptId) => {
  await movePrompt(folderId, {
    prompt_ids: [promptId],
    move: true
  })
  
  // 更新UI状态
  const prompt = prompts.value.find(p => p.prompt_id === promptId)
  if (prompt) {
    prompt.is_favorited = true
  }
}
</script>

<style scoped>
.home-view {
  max-width: 1200px;
  margin: 0 auto;
  padding: 1rem;
}

.prompts-container {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
  margin-top: 2rem;
}

.loading, .error {
  text-align: center;
  padding: 2rem;
  color: #666;
}

.error {
  color: #ef4444;
}

/* 新增响应式调整 */
@media (max-width: 768px) {
  .prompts-container {
    grid-template-columns: 1fr;
  }
}

</style>