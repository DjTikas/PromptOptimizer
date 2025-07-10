<template>
  <div class="prompt-list">
    <div v-if="prompts.length === 0" class="empty-state">
      <p>此收藏夹为空</p>
    </div>
    
    <div v-else>
      <div class="list-actions">
        <button 
          v-if="selectedPrompts.length > 0" 
          @click="showMoveDialog = true"
          class="move-btn"
        >
          移动到
        </button>
        <button 
          v-if="selectedPrompts.length > 0" 
          @click="deleteSelected"
          class="delete-btn"
        >
          删除
        </button>
      </div>
      
      <ul>
        <li v-for="prompt in prompts" :key="prompt.prompt_id" class="prompt-item">
          <label class="checkbox">
            <input 
              type="checkbox"
              :checked="isPromptSelected(prompt.prompt_id)"
              @change="togglePromptSelection(prompt.prompt_id)"
            />
          </label>
          <div class="content" @click="() => handleCardClick(prompt)">
            <div class="original">{{ prompt.original_content }}</div>
            <div class="optimized">{{ prompt.optimized_content }}</div>
            <div class="tags">
              <span v-for="tag in prompt.tags" :key="tag.tag_id" class="tag">
                {{ tag.tag_name }}
              </span>
            </div>
          </div>

          <!-- 详情弹窗 - 修改为窗口样式 -->
          <teleport to="body">
            <div 
              v-if="showDetailModal"
              class="prompt-detail-modal"
              @click.self="closeDetail"
            >
              <div class="modal-window">
                <div class="modal-header">
                  <h3>提示词详情</h3>
                </div>
                <div class="modal-body">
                  <div class="detail-section">
                    <h4>创作信息</h4>
                    <div class="detail-content">{{ currentDetailPrompt.user_info.email }}  
                      {{ formatDate(currentDetailPrompt.created_at) }}
                    </div>
                  </div>
                  
                  <div class="detail-section">
                    <h4>原始提示词</h4>
                    <div class="detail-content original-content">{{ currentDetailPrompt.original_content }}</div>
                  </div>
                  
                  <div class="detail-section">
                    <h4>优化后的提示词</h4>
                    <div class="detail-content optimized-content">{{ currentDetailPrompt.optimized_content }}</div>
                  </div>
                  
                  <div class="detail-section">
                    <h4>标签</h4>
                    <div class="tags">
                      <span v-for="tag in currentDetailPrompt.tags" :key="tag.tag_id" class="tag">
                        {{ tag.tag_name }}
                      </span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </teleport>

          <div class="actions">
            <button 
              v-if="currentFolder === 'my-prompts'"
              @click.stop="showEditTags(prompt)"
              class="edit-btn"
              title="编辑标签"
            >
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M20.59 13.41l-7.17 7.17a2 2 0 0 1-2.83 0L2 12V2h10l8.59 8.59a2 2 0 0 1 0 2.82z"></path>
                <line x1="7" y1="7" x2="7.01" y2="7"></line>
              </svg>
            </button>
            <button 
              v-if="currentFolder === 'my-prompts'"
              @click.stop="togglePromptShare(prompt)"
              class="share-btn"
              :class="{ 'shared': prompt.is_shared }"
              :title="prompt.is_shared ? '取消共享' : '共享'"
            >
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M4 12v8a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-8"></path>
                <polyline points="16 6 12 2 8 6"></polyline>
                <line x1="12" y1="2" x2="12" y2="15"></line>
              </svg>
            </button>
            <button @click.stop="deleteSinglePrompt(prompt.prompt_id)" class="delete-btn">
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <polyline points="3 6 5 6 21 6"></polyline>
                <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
              </svg>
            </button>
          </div>

          <teleport to="body">
          <div 
            v-if="showTagEditor"
            class="tag-editor-modal"
            @click.self="closeTagEditor"
          >
            <div class="modal-window">
              <div class="modal-header">
                <h3>管理标签</h3>
                <button class="close-btn" @click="closeTagEditor">×</button>
              </div>
              <div class="modal-body">
                <div class="current-tags">
                  <h4>当前标签</h4>
                  <div class="tags-list">
                    <div 
                      v-for="tag in currentPromptTags" 
                      :key="tag.tag_id"
                      class="tag-item"
                    >
                      <span v-if="!tag.editing" class="tag-display">
                        {{ tag.tag_name }}
                        <button @click.stop="startEditing(tag)" class="edit-tag">✏️</button>
                        <button @click.stop="removeTagAssociation(tag.tag_id)" class="remove-tag">×</button>
                      </span>
                      <div v-else class="tag-edit">
                        <input
                          v-model="tag.editName"
                          type="text"
                          @keyup.enter="saveTagEdit(tag)"
                          @blur="saveTagEdit(tag)"
                          ref="tagInput"
                        />
                        <button @click.stop="saveTagEdit(tag)" class="save-edit">✓</button>
                      </div>
                    </div>
                    <span v-if="currentPromptTags.length === 0" class="no-tags">暂无标签</span>
                  </div>
                </div>
                
                <div class="all-tags">
                  <h4>我的所有标签</h4>
                  <div class="tags-list">
                    <span 
                      v-for="tag in userTags" 
                      :key="tag.tag_id"
                      class="tag"
                      @click="assignTagToPrompt(tag.tag_id)"
                    >
                      {{ tag.tag_name }}
                      <button 
                        @click.stop="confirmDeleteTag(tag)"
                        class="remove-tag"
                        title="删除标签"
                      >×</button>
                    </span>
                    <span v-if="userTags.length === 0" class="no-tags">暂无标签</span>
                  </div>
                </div>
                
                <div class="add-tag">
                  <input
                    v-model="newTagName"
                    type="text"
                    placeholder="输入新标签名称"
                    @keyup.enter="createNewTag"
                  />
                  <button @click="createNewTag">添加</button>
                </div>
              </div>
            </div>
          </div>
          </teleport>
        </li>
      </ul>
    </div>
    
    <div v-if="showAddPrompt" class="add-prompt-modal">
      <div class="modal-content">
        <button class="close-btn" @click="showAddPrompt = false">×</button>
        <h3>添加提示词到收藏夹</h3>
        <div class="search-box">
          <input
            v-model="searchQuery"
            type="text"
            placeholder="搜索提示词..."
            @input="searchPrompts"
          />
        </div>
        <div v-if="searchResults.length > 0" class="search-results">
          <div 
            v-for="result in searchResults" 
            :key="result.prompt_id" 
            class="search-result"
            @click="addPromptToFolder(result)"
          >
            <div class="original">{{ result.original_content }}</div>
            <div class="optimized">{{ result.optimized_content }}</div>
          </div>
        </div>
        <div v-else class="empty-results">
          <p>没有找到匹配的提示词</p>
        </div>
      </div>
    </div>
    
    <div v-if="showMoveDialog" class="move-dialog">
      <div class="modal-content">
        <h3>移动到收藏夹</h3>
        <div class="folder-list">
          <div 
            v-for="folder in allFolders" 
            :key="folder.folder_id"
            class="folder-item"
            :class="{ 'current-folder': folder.folder_id === currentFolder }"
            @click="moveToFolder(folder.folder_id)"
          >
            <span class="folder-name">{{ folder.folder_name }}</span>
            <span v-if="folder.folder_id === currentFolder" class="current-label">(当前)</span>
          </div>
        </div>
        <button @click="showMoveDialog = false" class="cancel-btn">取消</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, nextTick } from 'vue'
import { useApi } from '@/composables/useApi'

const props = defineProps({
  prompts: {
    type: Array,
    default: () => []
  },
  currentFolder: {
    type: [Number, String],
    required: true
  },
  folders: {
    type: Array,
    required: true
  }
})

const emit = defineEmits(['delete', 'move', 'refresh']); 

const { get, post, put, del } = useApi()

const selectedPrompts = ref([])
const showAddPrompt = ref(false)
const showMoveDialog = ref(false)
const searchQuery = ref('')
const searchResults = ref([])
import { useUserStore } from '@/store'
const userStore = useUserStore()

// 修改后的响应式变量和方法
const showTagEditor = ref(false)
const currentEditingPrompt = ref(null)
const currentPromptTags = ref([])
const userTags = ref([])
const newTagName = ref('')


// 添加响应式引用
const tagInputs = ref([]) // 改为数组形式存储多个输入框引用

const startEditing = (tag, index) => {
  tag.editing = true
  tag.editName = tag.tag_name
  nextTick(() => {
    if (tagInputs.value[index]) {
      tagInputs.value[index].focus()
    }
  })
}

// 保存标签编辑
const saveTagEdit = async (tag) => {
  const newName = tag.editName.trim()
  if (!newName || newName === tag.tag_name) {
    tag.editing = false
    return
  }

  try {
    // 调用API更新标签
    const updatedTag = await put(`/search/tag/${tag.tag_id}`, {
      tag_name: newName
    })
    
    // 更新本地状态
    tag.tag_name = updatedTag.tag_name
    tag.editing = false
    
    // 更新所有标签列表中的对应标签
    userTags.value = userTags.value.map(t => 
      t.tag_id === tag.tag_id ? {...t, tag_name: updatedTag.tag_name} : t
    )
    
    window.$notify.success('标签更新成功')
  } catch (err) {
    console.error('更新标签失败:', err)
    window.$notify.error('更新标签失败: ' + (err.response?.data?.message || err.message))
    tag.editing = false
  }
}

// 获取用户所有标签
const fetchUserTags = async () => {
  try {
    const tags = await get('/search/tags');
    // 过滤当前提示词已关联的标签
    userTags.value = tags.filter(tag => 
      !currentPromptTags.value.some(t => t.tag_id === tag.tag_id)
    );
  } catch (err) {
    console.error('获取标签失败:', err);
    window.$notify.error('获取标签失败');
  }
}

// 显示标签编辑器
// 修改showEditTags方法，初始化编辑状态
const showEditTags = async (prompt) => {
  currentEditingPrompt.value = prompt
  // 为每个标签添加编辑状态
  currentPromptTags.value = prompt.tags.map(tag => ({
    ...tag,
    editing: false,
    editName: tag.tag_name
  }))
  await fetchUserTags()
  showTagEditor.value = true
}

// 关闭标签编辑器
const closeTagEditor = () => {
  showTagEditor.value = false;
  currentEditingPrompt.value = null;
  currentPromptTags.value = [];
  newTagName.value = '';
  
  // 新增：关闭时触发刷新
  emit('refresh', true);
}

// 创建新标签并关联到当前提示词
const createNewTag = async () => {
  const tagName = newTagName.value.trim();
  if (!tagName) return;
  
  try {
    // 1. 使用接口1：创建新标签
    const createResponse = await post('/search/tags', {
      tag_names: [tagName]
    });
    
    // 获取新创建的标签
    const newTag = createResponse.tags[0];
    
    // 2. 使用接口3：关联新标签到当前提示词
    await assignTagToPrompt(newTag.tag_id);
    
    // 3. 更新本地状态
    currentPromptTags.value.push({
      ...newTag,
      editing: false,
      editName: newTag.tag_name
    });
    newTagName.value = '';
    
    window.$notify.success('标签创建并关联成功');
  } catch (err) {
    console.error('创建标签失败:', err);
    window.$notify.error('创建标签失败: ' + (err.response?.data?.message || err.message));
  }
}

// 关联标签到提示词
const assignTagToPrompt = async (tagId) => {
  try {
    // 使用接口3：关联标签和提示词
    await post('/search/prompts/tags/assignments', {
      tag_ids: [tagId],
      prompt_ids: [currentEditingPrompt.value.prompt_id]
    });
    
    // 更新本地状态
    const assignedTag = userTags.value.find(t => t.tag_id === tagId);
    if (assignedTag) {
      // 添加到当前提示词的标签列表
      currentPromptTags.value.push({
        ...assignedTag,
        editing: false,
        editName: assignedTag.tag_name
      });
      
      // 从可用标签列表中移除
      userTags.value = userTags.value.filter(t => t.tag_id !== tagId);
    }
    
    window.$notify.success('标签关联成功');
  } catch (err) {
    console.error('关联标签失败:', err);
    window.$notify.error('关联标签失败');
  }
}


// 删除标签关联（不移除标签本身）
const removeTagAssociation = async (tagId) => {
  try {
    // 使用接口4：删除标签和提示词的关联
    await del(
      `/search/prompts/${currentEditingPrompt.value.prompt_id}/tags/${tagId}`
    );
    
    // 更新本地状态
    const removedTag = currentPromptTags.value.find(t => t.tag_id === tagId);
    currentPromptTags.value = currentPromptTags.value.filter(t => t.tag_id !== tagId);
    
    // 如果标签存在，重新加入可用标签列表
    if (removedTag && !userTags.value.some(t => t.tag_id === tagId)) {
      userTags.value.push(removedTag);
    }
    
    window.$notify.success('标签关联已移除');
  } catch (err) {
    console.error('移除关联失败:', err);
    window.$notify.error('移除关联失败');
  }
}


// 确认删除标签
const confirmDeleteTag = (tag) => {
  if (window.confirm(`确定要永久删除标签 "${tag.tag_name}" 吗？\n此操作会同时移除所有提示词与此标签的关联！`)) {
    deleteTag(tag.tag_id);
  }
}

// 完全删除标签
const deleteTag = async (tagId) => {
  try {
    // 使用接口2：完全删除标签
    await del(`/search/tags?tag_ids=${tagId}`);
    
    // 更新本地状态
    userTags.value = userTags.value.filter(t => t.tag_id !== tagId);
    
    // 如果该标签也在当前提示词的标签列表中，也移除
    currentPromptTags.value = currentPromptTags.value.filter(t => t.tag_id !== tagId);
    
    window.$notify.success('标签已永久删除');
  } catch (err) {
    console.error('删除标签失败:', err);
    window.$notify.error('删除标签失败: ' + (err.response?.data?.message || err.message));
  }
}


// 修改共享方法
const togglePromptShare = async (prompt) => {
  try {
    // 只发送必要的字段
    const response = await put(`/manage/prompts/${prompt.prompt_id}`, {
      session_id: 1,
      original_content: prompt.original_content,
      optimized_content: prompt.optimized_content,
      usage_count: 0,
      is_shared: !prompt.is_shared
    })
    
    // 更新本地状态
    prompt.is_shared = !prompt.is_shared
    window.$notify.success(`已${prompt.is_shared ? '共享' : '取消共享'}提示词`)
    return response
  } catch (err) {
    console.error('切换共享状态失败:', err)
    window.$notify.error(`操作失败: ${err.response?.data?.message || err.message}`)
    throw err
  }
}

const isPromptSelected = (promptId) => {
  return selectedPrompts.value.includes(promptId)
}

const togglePromptSelection = (promptId) => {
  if (promptId === null || promptId === undefined) return
  
  const index = selectedPrompts.value.indexOf(promptId)
  if (index === -1) {
    selectedPrompts.value.push(promptId)
  } else {
    selectedPrompts.value.splice(index, 1)
  }
}

const showDetailModal = ref(false)

const currentDetailPrompt = ref({ 
  user_info: { email: '' },
  created_at: '',
  original_content: '',
  optimized_content: '',
  tags: []
})

// 修改 handleCardClick 函数
const handleCardClick = async (prompt) => {
  try {
    const details = await fetchPromptDetails(prompt.prompt_id)
    currentDetailPrompt.value = details
    showDetailModal.value = true
  } catch (error) {
    console.error('Failed to fetch prompt details:', error)
  }
}

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

const closeDetail = () => {
  showDetailModal.value = false
}

const fetchPromptDetails = async (promptId) => {
  try {
    const prompt = await get(`/manage/prompts/${promptId}`)
    return prompt
  } catch (err) {
    console.error('Failed to fetch prompt:', err)
    return null
  }
}

const handleCheckboxChange = async (promptId, isChecked) => {
  if (isChecked) {
    const promptDetail = await fetchPromptDetails(promptId)
    if (promptDetail) {
      if (!selectedPrompts.value.some(p => p.prompt_id === promptId)) {
        selectedPrompts.value.push(promptDetail)
      }
    }
  } else {
    selectedPrompts.value = selectedPrompts.value.filter(p => p.prompt_id !== promptId)
  }
}

const allFolders = computed(() => {
  return props.folders || []
})

// 删除单个提示词
const deleteSinglePrompt = (promptId) => {
  if (confirm('确定要删除这个提示词吗？')) {
    emit('delete', promptId)
  }
}

// 删除选中的多个提示词
const deleteSelected = () => {
  if (selectedPrompts.value.length === 0) return
  
  if (confirm(`确定要删除选中的 ${selectedPrompts.value.length} 个提示词吗？`)) {
    emit('delete', selectedPrompts.value)
    selectedPrompts.value = []
  }
}

const searchPrompts = async () => {
  if (searchQuery.value.length > 1) {
    try {
      const data = await get(`/search/fuzzy/prompts?query=${searchQuery.value}&limit=10`)
      searchResults.value = data
    } catch (err) {
      console.error('Search failed:', err)
      searchResults.value = []
    }
  } else {
    searchResults.value = []
  }
}

const addPromptToFolder = (prompt) => {
  emit('move', {
    promptId: prompt.prompt_id,
    targetFolderId: props.currentFolder
  })
  showAddPrompt.value = false
  searchQuery.value = ''
  searchResults.value = []
}

const moveToFolder = async (folderId) => {
  // 过滤掉任何无效的 prompt_id
  const validPromptIds = selectedPrompts.value.filter(id => 
    id !== null && id !== undefined && Number.isInteger(id)
  )
  
  if (validPromptIds.length === 0) {
    alert('请先选择有效的提示词')
    return
  }

  try {
    if(props.currentFolder=='my-prompts'){
      await post(`/manage/folders/${folderId}/prompts`, {
      prompt_ids: validPromptIds,
      cur_folder_id: 1,
      move: false
    })}else{
      await post(`/manage/folders/${folderId}/prompts`, {
      prompt_ids: validPromptIds,
      cur_folder_id: props.currentFolder,
      move: true
    })}
    
    
    emit('move', {
      promptIds: validPromptIds,
      targetFolderId: folderId,
      currentFolderId: props.currentFolder
    })
    
    // 清空选择
    selectedPrompts.value = []
    showMoveDialog.value = false
    
  } catch (err) {
    console.error('移动提示词失败:', err)
    alert(`移动失败: ${err.response?.data?.message || err.message}`)
  }
}
</script>

<style scoped>
.edit-btn {
  background: none;
  border: none;
  cursor: pointer;
  color: #9ca3af;
  padding: 0.25rem;
  border-radius: 4px;
  margin-right: 0.5rem;
}

.edit-btn:hover {
  color: #10b981;
  background-color: #ecfdf5;
}

.edit-btn svg {
  width: 16px;
  height: 16px;
}

.tag-editor-modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: transparent;
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.tag-editor-modal .modal-window {
  background-color: white;
  border-radius: 8px;
  width: 90%;
  max-width: 500px;
  max-height: 80vh;
  display: flex;
  flex-direction: column;
}

.tag-editor-modal .modal-body {
  padding: 20px;
  overflow-y: auto;
}

.current-tags, .all-tags {
  margin-bottom: 20px;
}

.tags-list {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-top: 10px;
}

.tag {
  background-color: #e0e7ff;
  color: #4f46e5;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 0.875rem;
  display: flex;
  align-items: center;
  cursor: pointer;
}

.remove-tag {
  margin-left: 4px;
  background: none;
  border: none;
  color: #ef4444;
  cursor: pointer;
  font-size: 0.75rem;
  padding: 0 2px;
}

.no-tags {
  color: #6b7280;
  font-size: 0.875rem;
}

.add-tag {
  display: flex;
  gap: 8px;
  margin-top: 20px;
}

.add-tag input {
  flex: 1;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.add-tag button {
  padding: 8px 16px;
  background-color: #4f46e5;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

/* 修改模态窗口样式 */
.prompt-detail-modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: transparent; /* 调整为更透明的背景 */
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
  transition: opacity 0.3s ease; /* 添加淡入淡出效果 */
}

.modal-window {
  background-color: white;
  border-radius: 8px;
  width: 90%;
  max-width: 600px;
  max-height: 80vh;
  display: flex;
  flex-direction: column;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.15);
}

.modal-header {
  padding: 16px 20px;
  border-bottom: 1px solid #eee;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.modal-header h3 {
  margin: 0;
  font-size: 1.25rem;
  color: #333;
}

.modal-header .close-btn {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: #666;
  padding: 0;
  line-height: 1;
}

.modal-body {
  padding: 20px;
  overflow-y: auto;
  flex: 1;
}

.share-btn {
  background: none;
  border: none;
  cursor: pointer;
  color: #9ca3af;
  padding: 0.25rem;
  border-radius: 4px;
  margin-right: 0.5rem;
}

.share-btn:hover {
  color: #3b82f6;
  background-color: #eff6ff;
}

.share-btn.shared {
  color: #3b82f6;
}

.share-btn svg {
  width: 16px;
  height: 16px;
}

.detail-section {
  margin-bottom: 20px;
}

.detail-section h4 {
  margin: 0 0 10px 0;
  font-size: 1rem;
  color: #555;
}

.detail-content {
  padding: 12px;
  background-color: #f8f9fa;
  border-radius: 4px;
  word-break: break-word;
  line-height: 1.5;
}

.original-content {
  border-left: 3px solid #4f46e5;
}

.optimized-content {
  border-left: 3px solid #10b981;
}

.modal-footer {
  padding: 12px 20px;
  border-top: 1px solid #eee;
  display: flex;
  justify-content: flex-end;
}

.cancel-btn {
  padding: 8px 16px;
  background-color: #4f46e5;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.cancel-btn:hover {
  background-color: #4338ca;
}

.prompt-list {
  height: 100%;
  position: relative;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  color: #6b7280;
}

.empty-state p {
  margin-bottom: 1rem;
}

.empty-state button {
  padding: 0.75rem 1.5rem;
  background-color: #4f46e5;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.list-actions {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.list-actions button {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  font-size: 0.875rem;
  cursor: pointer;
}

.add-btn {
  background-color: #4f46e5;
  color: white;
  border: none;
}

.move-btn {
  background-color: #e0e7ff;
  color: #4f46e5;
  border: none;
}

.delete-btn {
  background-color: #fee2e2;
  color: #ef4444;
  border: none;
}

.list-actions button svg {
  width: 16px;
  height: 16px;
}

ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.prompt-item {
  display: flex;
  align-items: flex-start;
  padding: 1rem;
  border-radius: 4px;
  background-color: white;
  margin-bottom: 0.5rem;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
}

.prompt-item:hover {
  background-color: #f9fafb;
}

.checkbox {
  margin-right: 1rem;
}

.content {
  flex: 1;
}

.original {
  font-weight: 500;
  margin-bottom: 0.5rem;
  word-break: break-word;
}

.move-dialog .folder-list {
  max-height: 300px;
  overflow-y: auto;
  margin: 1rem 0;
}

.move-dialog .folder-item {
  padding: 0.75rem;
  border-radius: 4px;
  cursor: pointer;
  display: flex;
  justify-content: space-between;
}

.move-dialog .folder-item:hover {
  background-color: #f3f4f6;
}

.move-dialog .current-folder {
  background-color: #e0e7ff;
  color: #4f46e5;
}

.move-dialog .current-label {
  color: #6b7280;
  font-size: 0.875rem;
}

.optimized {
  color: #6b7280;
  font-size: 0.875rem;
  margin-bottom: 0.5rem;
  word-break: break-word;
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
  margin-left: 1rem;
}

.actions button {
  background: none;
  border: none;
  cursor: pointer;
  color: #9ca3af;
  padding: 0.25rem;
  border-radius: 4px;
}

.actions button:hover {
  color: #ef4444;
  background-color: #fee2e2;
}

.actions button svg {
  width: 16px;
  height: 16px;
}

.add-prompt-modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background-color: white;
  padding: 1.5rem;
  border-radius: 8px;
  width: 100%;
  max-width: 600px;
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

h3 {
  margin-top: 0;
  margin-bottom: 1rem;
}

.search-box {
  margin-bottom: 1rem;
}

.search-box input {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
}

.search-results {
  max-height: 50vh;
  overflow-y: auto;
}

.search-result {
  padding: 1rem;
  border-bottom: 1px solid #eee;
  cursor: pointer;
}

.search-result:hover {
  background-color: #f3f4f6;
}

.search-result .original {
  font-weight: 500;
  margin-bottom: 0.25rem;
}

.search-result .optimized {
  color: #6b7280;
  font-size: 0.875rem;
}

.empty-results {
  padding: 2rem;
  text-align: center;
  color: #6b7280;
}

.move-dialog {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.move-dialog .modal-content {
  background-color: white;
  padding: 1.5rem;
  border-radius: 8px;
  width: 100%;
  max-width: 300px;
}

.move-dialog ul {
  list-style: none;
  padding: 0;
  margin: 1rem 0;
}

.move-dialog li {
  padding: 0.75rem;
  border-radius: 4px;
  cursor: pointer;
}

.move-dialog li:hover {
  background-color: #f3f4f6;
}

.cancel-btn {
  width: 100%;
  padding: 0.75rem;
  background-color: #f3f4f6;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  margin-top: 1rem;
}
</style>