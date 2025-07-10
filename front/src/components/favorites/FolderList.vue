<template>
  <div class="folder-list">
    <div class="header">
      <h3>收藏夹</h3>
      <button @click="showAddFolder = true" class="add-btn">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <line x1="12" y1="5" x2="12" y2="19"></line>
          <line x1="5" y1="12" x2="19" y2="12"></line>
        </svg>
      </button>
    </div>
    
    <ul>
      <!-- 添加"我的提示词"特殊收藏夹 -->
      <li
        :class="{ active: currentFolder === 'my-prompts' }"
        @click="$emit('select', 'my-prompts')"
      >
        <span class="name">我的提示词</span>
      </li>
      <li
        v-for="folder in folders"
        :key="folder.folder_id"
        :class="{ active: currentFolder === folder.folder_id }"
        @click="$emit('select', folder.folder_id)"
      >
        <span class="name">{{ folder.folder_name }}</span>
        <button @click.stop="startRename(folder)" class="rename-btn" title="重命名">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path>
              <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path>
            </svg>
          </button>
        <button @click.stop="$emit('delete', folder.folder_id)" class="delete-btn">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <polyline points="3 6 5 6 21 6"></polyline>
            <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
          </svg>
        </button>
      </li>
    </ul>

    <div v-if="showRenameModal" class="rename-folder-modal">
      <div class="modal-content">
        <h3>重命名文件夹</h3>
        <input
          v-model="renameFolderName"
          type="text"
          placeholder="输入新文件夹名称"
          ref="renameInput"
          @keyup.enter="confirmRename"
        />
        <div class="error-message" v-if="renameError">{{ renameError }}</div>
        <div class="actions">
          <button @click="confirmRename" class="confirm-btn">确认</button>
          <button @click="cancelRename" class="cancel-btn">取消</button>
        </div>
      </div>
    </div>
    
    <div v-if="showAddFolder" class="add-folder-modal">
      <input
        v-model="newFolderName"
        type="text"
        placeholder="输入收藏夹名称"
        ref="folderInput"
        @keyup.enter="addFolder"
      />
      <div class="actions">
        <button @click="addFolder">添加</button>
        <button @click="showAddFolder = false">取消</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, nextTick } from 'vue'

const props = defineProps({
  folders: {
    type: Array,
    required: true
  },
  currentFolder: {
    required: true
  },
  myPromptsCount: { // 新增props
    type: Number,
    default: 0
  }
})

const emit = defineEmits(['select', 'add', 'delete', 'rename'])

// 重命名相关状态
const showRenameModal = ref(false)
const renameFolderName = ref('')
const renameFolderId = ref(null)
const renameError = ref('')
const renameInput = ref(null)

const startRename = (folder) => {
  renameFolderId.value = folder.folder_id
  renameFolderName.value = folder.folder_name
  showRenameModal.value = true
  nextTick(() => {
    renameInput.value.focus()
    renameInput.value.select()
  })
}

const confirmRename = async () => {
  if (!renameFolderName.value.trim()) {
    renameError.value = '文件夹名称不能为空'
    return
  }

  try {
    // 修改这里：直接调用 emit 并等待结果
    const success = await emit('rename', {
      folderId: renameFolderId.value,
      newName: renameFolderName.value.trim()
    })
    
    if (success !== false) { // 只有当明确返回 false 时才不关闭
      showRenameModal.value = false
      renameError.value = ''
    }
  } catch (err) {
    renameError.value = err.message || '重命名失败'
  }
}

const cancelRename = () => {
  showRenameModal.value = false
  renameError.value = ''
}

const showAddFolder = ref(false)
const newFolderName = ref('')
const folderInput = ref(null)

watch(showAddFolder, (val) => {
  if (val) {
    nextTick(() => {
      folderInput.value.focus()
    })
  } else {
    newFolderName.value = ''
  }
})

const addFolder = async () => {
  if (!newFolderName.value.trim()) {
    alert('请输入文件夹名称')
    return
  }
  
  const success = await emit('add', newFolderName.value.trim())
  if (success) {
    showAddFolder.value = false
    newFolderName.value = ''
  } else {
    // 保持对话框打开，让用户修改名称
    nextTick(() => folderInput.value?.focus())
  }
}

</script>

<style scoped>
.folder-list {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.5rem 0;
  border-bottom: 1px solid #eee;
  margin-bottom: 0.5rem;
}

.header h3 {
  margin: 0;
  font-size: 1rem;
  color: #4b5563;
}

.add-btn {
  background: none;
  border: none;
  cursor: pointer;
  color: #4f46e5;
  padding: 0.25rem;
  border-radius: 4px;
}

.add-btn:hover {
  background-color: #eef2ff;
}

.add-btn svg {
  width: 16px;
  height: 16px;
}

ul {
  list-style: none;
  padding: 0;
  margin: 0;
  flex: 1;
  overflow-y: auto;
}

li {
  display: flex;
  align-items: center;
  padding: 0.75rem 0.5rem;
  border-radius: 4px;
  cursor: pointer;
  margin-bottom: 0.25rem;
}

li:hover {
  background-color: #f3f4f6;
}

li.active {
  background-color: #e0e7ff;
  color: #4f46e5;
}

.name {
  flex: 1;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.count {
  background-color: #e5e7eb;
  color: #4b5563;
  font-size: 0.75rem;
  padding: 0.125rem 0.5rem;
  border-radius: 9999px;
  margin: 0 0.5rem;
}

.delete-btn {
  background: none;
  border: none;
  cursor: pointer;
  color: #9ca3af;
  padding: 0.25rem;
  border-radius: 4px;
  opacity: 0;
  transition: opacity 0.2s;
}

li:hover .delete-btn {
  opacity: 1;
}

.delete-btn:hover {
  color: #ef4444;
  background-color: #fee2e2;
}

/* 添加重命名按钮样式 */
.action-buttons {
  display: flex;
  gap: 0.25rem;
}

.rename-btn {
  background: none;
  border: none;
  cursor: pointer;
  color: #9ca3af;
  padding: 0.25rem;
  border-radius: 4px;
  opacity: 0;
  transition: opacity 0.2s;
}

li:hover .rename-btn {
  opacity: 1;
}

.rename-btn:hover {
  color: #4f46e5;
  background-color: #eef2ff;
}

.rename-btn svg {
  width: 16px;
  height: 16px;
}

/* 重命名模态框样式 */
.rename-folder-modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 100;
}

.rename-folder-modal .modal-content {
  background-color: white;
  padding: 1.5rem;
  border-radius: 8px;
  width: 100%;
  max-width: 400px;
}

.rename-folder-modal h3 {
  margin-top: 0;
  margin-bottom: 1rem;
}

.rename-folder-modal input {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
  margin-bottom: 0.5rem;
}

.actions {
  display: flex;
  gap: 0.5rem;
}

.actions button {
  flex: 1;
  padding: 0.75rem;
  border-radius: 4px;
  font-size: 1rem;
  cursor: pointer;
}

.confirm-btn {
  background-color: #4f46e5;
  color: white;
  border: none;
}

.cancel-btn {
  background-color: #f3f4f6;
  border: 1px solid #ddd;
  color: #4b5563;
}

.delete-btn svg {
  width: 16px;
  height: 16px;
}

.add-folder-modal {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(255, 255, 255, 0.9);
  display: flex;
  flex-direction: column;
  justify-content: center;
  padding: 1rem;
  z-index: 10;
}

.add-folder-modal input {
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
  margin-bottom: 1rem;
}

.actions {
  display: flex;
  gap: 0.5rem;
}

.actions button {
  flex: 1;
  padding: 0.75rem;
  border-radius: 4px;
  font-size: 1rem;
  cursor: pointer;
}

.actions button:first-child {
  background-color: #4f46e5;
  color: white;
  border: none;
}

.actions button:last-child {
  background-color: #f3f4f6;
  border: 1px solid #ddd;
  color: #4b5563;
}
</style>