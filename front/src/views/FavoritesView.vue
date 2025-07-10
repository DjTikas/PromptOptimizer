<template>
  <div class="favorites-view">
    <div class="sidebar">
      <FolderList 
        :folders="folders" 
        :current-folder="currentFolder"
        :my-prompts-count="myPromptsCount"
        @select="selectFolder" 
        @add="addFolder"
        @delete="deleteFolder"
        @rename="renameFolder"
      />
    </div>
    
    <div class="content">
      <div class="search-bar">
        <input 
          v-model="searchQuery" 
          placeholder="搜索收藏夹内容..." 
          @input="handleSearch"
          class="search-input"
        />
        <i class="fas fa-search search-icon"></i>

        <button 
          class="search-toggle"
          @click="toggleSearchScope"
          :title="searchScope === 'folder' ? '在当前文件夹搜索' : '在所有收藏中搜索'"
        >
          <i class="fas" :class="searchScope === 'folder' ? 'fa-folder' : 'fa-globe'"></i>
          <span class="toggle-text">{{ searchScope === 'folder' ? '当前' : '所有' }}</span>
        </button>
      </div>
      
      <div class="content-header">
        <h2 v-if="currentFolder">{{folderName}}</h2>
        <div class="prompt-count">
          {{ filteredPrompts.length }} 个提示词
        </div>
      </div>
      
      <PromptList 
        :prompts="filteredPrompts" 
        :current-folder="currentFolder"
        :folders="folders"
        @delete="deletePrompt"
        @move="movePrompt"
        @refresh="(force) => fetchPrompts(force)"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useApi } from '@/composables/useApi'
import FolderList from '@/components/favorites/FolderList.vue'
import PromptList from '@/components/favorites/PromptList.vue'

const { get, post, put, del, isLoading, error } = useApi()

const folders = ref([])
const currentFolder = ref('my-prompts')
const prompts = ref([])
const searchQuery = ref('')
const myPrompts = ref([]) // 存储用户创建的所有提示词
const myPromptsCount = computed(() => myPrompts.value.length) // 计算属性
const searchScope = ref('folder') // 'folder' 或 'global'
const globalSearchResults = ref([]) // 存储全站搜索结果

const fetchPrompts = async (forceReload = false) => {
  try {
    if (forceReload || currentFolder.value === 'my-prompts') {
      // 强制重新加载或当前是"我的提示词"时完全刷新
      const response = await get('/manage/prompts');
      myPrompts.value = response;
      if (currentFolder.value === 'my-prompts') {
        prompts.value = response;
      }
    }
    
    window.$notify.success('提示词已刷新');
  } catch (err) {
    console.error('获取提示词失败:', err);
    window.$notify.error('刷新提示词失败');
  }
};

// 新增：收藏模糊搜索
const searchGlobalPrompts = async () => {
  if (searchQuery.value.length < 2) {
    globalSearchResults.value = []
    return
  }
  
  try {
    const results = await get('/search/fuzzy/prompts', {
      query: searchQuery.value,
      limit: 100
    })
    globalSearchResults.value = results
  } catch (err) {
    console.error('所有收藏夹搜索失败:', err)
    globalSearchResults.value = []
  }
}

// 修改：处理搜索输入
const handleSearch = () => {
  if (searchScope.value === 'global') {
    searchGlobalPrompts()
  }
  // 文件夹搜索由 computed 属性自动处理
}

const toggleSearchScope = () => {
  searchScope.value = searchScope.value === 'folder' ? 'global' : 'folder'
  if (searchScope.value === 'global' && searchQuery.value) {
    searchGlobalPrompts()
  }
}

// 修改onMounted钩子
onMounted(async () => {
  try {
    // 并行获取文件夹和我的提示词
    const [folderData, myPromptData] = await Promise.all([
      get('/manage/folders'),
      get('/manage/prompts')
    ])
    
    folders.value = folderData
    myPrompts.value = myPromptData
    
    // 默认显示我的提示词，如果有文件夹则显示第一个文件夹
    if (folders.value.length > 0) {
      loadFolderPrompts(folders.value[0].folder_id)
    }
  } catch (err) {
    console.error('初始化加载失败:', err)
    alert('初始化数据加载失败')
  }
})

// 修改selectFolder方法
const selectFolder = (folderId) => {
  currentFolder.value = folderId
  if (folderId === 'my-prompts') {
    prompts.value = myPrompts.value
  } else {
    loadFolderPrompts(folderId)
  }
}

// 修改filteredPrompts计算属性
const filteredPrompts = computed(() => {
  if (searchScope.value === 'global') {
    return globalSearchResults.value
  }

  const sourcePrompts = currentFolder.value === 'my-prompts' 
    ? myPrompts.value 
    : prompts.value
  
  if (!searchQuery.value) return sourcePrompts
  
  const query = searchQuery.value.toLowerCase()
  return sourcePrompts.filter(prompt => 
    prompt.original_content.toLowerCase().includes(query) || 
    prompt.optimized_content.toLowerCase().includes(query)
  )
})

// 修改content-header显示逻辑
const folderName = computed(() => {
  return currentFolder.value === 'my-prompts' 
    ? '我的提示词' 
    : folders.value.find(f => f.folder_id === currentFolder.value)?.folder_name || '未命名收藏夹'
})

const loadFolderPrompts = async (folderId) => {
  try {
    const promptData = await get(`/manage/folders/${folderId}/prompts`)
    prompts.value = promptData
  } catch (err) {
    console.error('Failed to load prompts:', err)
  }
}

//const selectFolder = (folderId) => {
//  currentFolder.value = folderId
//  loadFolderPrompts(folderId)
//}

const renameFolder = async ({ folderId, newName }) => {
  try {
    const updatedFolder = await put(`/manage/folders/${folderId}`, {
      folder_name: newName
    })
    
    const index = folders.value.findIndex(f => f.folder_id === folderId)
    if (index !== -1) {
      folders.value[index] = updatedFolder
    }
    
    return true // 明确返回成功状态
  } catch (err) {
    console.error('Failed to rename folder:', err)
    if (err.response?.data?.detail?.some(e => e.type === 'value_error.folder_exists')) {
      throw new Error('文件夹名称已存在')
    }
    throw new Error('重命名文件夹失败: ' + (err.response?.data?.message || '服务器错误'))
  }
}

const addFolder = async (folderName) => {
  try {
    const newFolder = await post('/manage/folders', { folder_name: folderName })
    folders.value.push(newFolder)
    return true // 返回成功状态
  } catch (err) {
    console.error('Failed to add folder:', err)
    if (err.response?.data?.detail?.some(e => e.type === 'value_error.folder_exists')) {
      alert('文件夹名称已存在，请使用其他名称')
    } else {
      alert('文件夹名称已存在，请使用其他名称')
    }
    return false // 返回失败状态
  }
}

const deleteFolder = async (folderId) => {
  // 添加确认弹窗
  const confirmDelete = confirm('确定要删除这个文件夹吗？文件夹内的所有内容也将被删除！')
  if (!confirmDelete) return

  try {
    await del(`/manage/folders/${folderId}`)
    folders.value = folders.value.filter(f => f.folder_id !== folderId)
    
    // 处理当前选中文件夹被删除的情况
    if (currentFolder.value === folderId) {
      if (folders.value.length > 0) {
        currentFolder.value = folders.value[0].folder_id
        loadFolderPrompts(currentFolder.value)
      } else {
        currentFolder.value = null
        prompts.value = []
      }
    }
    
    alert('文件夹删除成功')
  } catch (err) {
    console.error('Failed to delete folder:', err)
    alert(`删除文件夹失败: ${err.response?.data?.message || err.message}`)
  }
}

const deletePrompt = async (promptIds) => {
  try {
    const ids = Array.isArray(promptIds) ? promptIds : [promptIds]
    if (currentFolder.value === 'my-prompts') {
      // 使用"我的提示词"的删除接口
      await del('/manage/prompts', ids)
      myPrompts.value = myPrompts.value.filter(p => !ids.includes(p.prompt_id))
    } else{
      // 使用收藏夹的删除接口
      await del(`/manage/folders/${currentFolder.value}/prompts`, ids)
      prompts.value = prompts.value.filter(p => !ids.includes(p.prompt_id))
    }
    window.$notify.success('删除成功！')
    return true
  } catch (err) {
    console.error('删除失败:', err)
    alert(`删除失败: ${err.data?.detail?.[0]?.msg || err.message}`)
    return false
  }
}

const movePrompt = async ({ promptIds, targetFolderId, currentFolderId }) => {
  // 双重验证确保数据安全
  const validPromptIds = promptIds.filter(id => 
    id !== null && id !== undefined && Number.isInteger(id)
  )
  
  if (validPromptIds.length === 0) {
    console.warn('没有有效的提示词ID')
    return
  }

  try {
    // 更新本地状态
    if (targetFolderId !== currentFolder.value) {
      prompts.value = prompts.value.filter(p => !validPromptIds.includes(p.prompt_id))
    }
    
    window.$notify.success('移动成功！')

  } catch (err) {
    console.error('更新本地状态失败:', err)
    throw err
  }
}

//const filteredPrompts = computed(() => {
//  if (!searchQuery.value) return prompts.value
//  
//  const query = searchQuery.value.toLowerCase()
//  return prompts.value.filter(prompt => 
//    prompt.original_content.toLowerCase().includes(query) || 
//    prompt.optimized_content.toLowerCase().includes(query)
//  )
//})

const searchInFolder = () => {
  // 搜索逻辑已在 computed 属性中处理
}
</script>

<style scoped>
.search-bar {
  position: relative;
  margin-bottom: 1.5rem;
  display: flex;
  gap: 0.5rem;
}

.search-input {
  flex: 1;
  padding: 0.85rem 1.2rem 0.85rem 40px;
  /* 其他样式保持不变 */
}

.search-toggle {
  padding: 0 1rem;
  background-color: #e0e7ff;
  color: #4f46e5;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center; /* 新增：水平居中 */
  gap: 0.5rem;
  transition: all 0.2s;
  font-weight: 600; /* 新增：字体加粗 */
  min-width: 80px; /* 新增：设置最小宽度 */
}

/* 新增：按钮文本样式 */
.toggle-text {
  font-weight: 600; /* 加粗 */
  text-align: center; /* 居中 */
}

.search-toggle:hover {
  background-color: #c7d2fe;
}

.search-toggle i {
  font-size: 0.9em;
}

.favorites-view {
  display: flex;
  min-height: calc(100vh - 100px);
  background: linear-gradient(135deg, #f8f9ff, #ffffff);
  padding: 1rem;
}

.sidebar {
  width: 280px;
  border-right: 1px solid #e0e7ff;
  padding: 1.5rem;
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(79, 70, 229, 0.08);
  margin-right: 1.5rem;
}

.content {
  flex: 1;
  padding: 1.5rem;
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(79, 70, 229, 0.08);
}

.search-bar {
  position: relative;
  margin-bottom: 1.5rem;
}

.search-input {
  width: 100%;
  padding: 0.85rem 1.2rem 0.85rem 40px;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  font-size: 1rem;
  background-color: #f9fafb;
  transition: all 0.3s;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.search-input:focus {
  border-color: #818cf8;
  box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.2);
  background-color: white;
  outline: none;
}

.search-icon {
  position: absolute;
  left: 15px;
  top: 50%;
  transform: translateY(-50%);
  color: #9ca3af;
}

.content-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
  padding-bottom: 0.75rem;
  border-bottom: 1px solid #e0e7ff;
}

.content-header h2 {
  margin: 0;
  color: #4f46e5;
  font-size: 1.5rem;
}

.prompt-count {
  background-color: #e0e7ff;
  color: #4f46e5;
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.85rem;
  font-weight: 500;
}

/* 响应式调整 */
@media (max-width: 768px) {
  .favorites-view {
    flex-direction: column;
  }
  
  .sidebar {
    width: 100%;
    margin-right: 0;
    margin-bottom: 1.5rem;
  }
  
  .content-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.5rem;
  }

  .search-bar {
    flex-direction: row; /* 保持横向排列 */
    flex-wrap: wrap; /* 允许换行 */
  }
  
  .search-input {
    order: 1; /* 输入框排在第一行 */
    width: 100%;
  }
  
  .search-toggle {
    order: 2; /* 按钮排在第二行 */
    margin-top: 0.5rem;
    padding: 0.5rem 1rem;
    width: 100%; /* 全宽度 */
    justify-content: center; /* 确保居中 */
  }
}
</style>