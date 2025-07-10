<template>
  <div class="dialog-overlay" v-if="visible" @click.self="close">
    <div class="dialog-content">
      <h3>选择收藏夹</h3>
      <div class="folder-list">
        <div 
          v-for="folder in folders" 
          :key="folder.folder_id"
          class="folder-item"
          :class="{ 
            'already-collected': isCollected(folder.folder_id),
            'selected': selectedFolderId === folder.folder_id
          }"
          @click="selectFolder(folder)"
        >
          <div class="folder-icon">
            <i class="fas fa-folder"></i>
          </div>
          <div class="folder-info">
            <span class="folder-name">{{ folder.folder_name }}</span>
          </div>
          <div v-if="isCollected(folder.folder_id)" class="collected-badge">
            <i class="fas fa-check-circle"></i> 已收藏
          </div>
        </div>
      </div>
      <div class="dialog-actions">
        <button @click="close" class="cancel-btn">取消</button>
        <button 
          v-if="selectedFolderId" 
          @click="confirmSelection" 
          class="confirm-btn"
        >
          确定
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { defineProps, defineEmits, ref } from 'vue'

const props = defineProps({
  folders: {
    type: Array,
    required: true
  },
  visible: {
    type: Boolean,
    required: true
  },
  collectedFolders: {
    type: Array,
    default: () => []
  }
})

const emit = defineEmits(['select', 'close'])
const selectedFolderId = ref(null)

const isCollected = (folderId) => {
  return props.collectedFolders.some(f => f.folder_id === folderId)
}

const selectFolder = (folder) => {
  if (!isCollected(folder.folder_id)) {
    selectedFolderId.value = folder.folder_id
  }
}

const confirmSelection = () => {
  if (selectedFolderId.value) {
    const folder = props.folders.find(f => f.folder_id === selectedFolderId.value)
    if (folder) {
      emit('select', folder)
      close()
    }
  }
}

const close = () => {
  selectedFolderId.value = null
  emit('close')
}
</script>

<style scoped>
.dialog-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0,0,0,0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
  backdrop-filter: blur(3px);
}

.dialog-content {
  background: white;
  padding: 25px;
  border-radius: 12px;
  width: 380px;
  box-shadow: 0 10px 30px rgba(79, 70, 229, 0.2);
  border: 1px solid #e0e7ff;
}

.dialog-content h3 {
  text-align: center;
  margin-top: 0;
  color: #4f46e5;
  font-size: 1.4rem;
  padding-bottom: 15px;
  border-bottom: 1px solid #e0e7ff;
}

.folder-list {
  max-height: 300px;
  overflow-y: auto;
  margin: 20px 0;
  padding-right: 8px;
}

.folder-item {
  display: flex;
  align-items: center;
  padding: 12px 15px;
  border-radius: 8px;
  margin-bottom: 10px;
  cursor: pointer;
  transition: all 0.3s ease;
  border: 1px solid #e0e7ff;
  background: #f9fafb;
  position: relative;
}

.folder-item:hover {
  background: #f0f4ff;
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(79, 70, 229, 0.1);
}

.folder-item.selected {
  background: #e0e7ff;
  border-color: #a5b4fc;
}

.folder-icon {
  width: 40px;
  height: 40px;
  background: linear-gradient(135deg, #818cf8, #4f46e5);
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 15px;
  flex-shrink: 0;
}

.folder-icon i {
  color: white;
  font-size: 1.2rem;
}

.folder-info {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.folder-name {
  font-weight: 500;
  color: #1f2937;
  font-size: 1.05rem;
  margin-bottom: 3px;
}

.prompt-count {
  font-size: 0.85rem;
  color: #6b7280;
}

.collected-badge {
  background: #dcfce7;
  color: #16a34a;
  padding: 5px 10px;
  border-radius: 20px;
  font-size: 0.85rem;
  display: flex;
  align-items: center;
  gap: 5px;
  margin-left: 10px;
  flex-shrink: 0;
}

.collected-badge i {
  font-size: 1rem;
}

.already-collected {
  opacity: 0.7;
}

.already-collected:hover {
  background: #f9fafb;
  transform: none;
  box-shadow: none;
  cursor: not-allowed;
}

.dialog-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  padding-top: 15px;
  border-top: 1px solid #e0e7ff;
}

button {
  padding: 0.7rem 1.5rem;
  border-radius: 8px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s;
}

.cancel-btn {
  background: #f3f4f6;
  color: #4b5563;
  border: 1px solid #e5e7eb;
}

.cancel-btn:hover {
  background: #e5e7eb;
}

.confirm-btn {
  background: linear-gradient(135deg, #4f46e5, #7c3aed);
  color: white;
  border: none;
  box-shadow: 0 4px 6px rgba(79, 70, 229, 0.2);
}

.confirm-btn:hover {
  background: linear-gradient(135deg, #4338ca, #6d28d9);
  transform: translateY(-2px);
  box-shadow: 0 6px 10px rgba(79, 70, 229, 0.3);
}

/* 滚动条美化 */
.folder-list::-webkit-scrollbar {
  width: 6px;
}

.folder-list::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 10px;
}

.folder-list::-webkit-scrollbar-thumb {
  background: #c7d2fe;
  border-radius: 10px;
}

.folder-list::-webkit-scrollbar-thumb:hover {
  background: #a5b4fc;
}
</style>