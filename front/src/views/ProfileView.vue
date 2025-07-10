<template>
  <div class="profile-view">
    <div class="profile-header">
      <div class="avatar-container">
        <button 
          @click="showAvatarModal = true"
          class="avatar-btn"
        >
        <div class="avatar">
          <Avatar 
            :src="userStore.avatar"
            style="width: 90px; height: 90px;"
          />
        </div>
        </button>
      </div>
      
      <div class="user-info">
        <h1>{{ user.username }}</h1>
        <p>{{ user.email }}</p>
        <p>注册于: {{ formatDate(user.created_at) }}</p>
      </div>
      <!-- 添加退出按钮 -->
      <button @click="handleLogout" class="logout-btn">
        退出登录
      </button>
    </div>
    
    <div class="profile-content">
      
      <div class="section">
        <h2>修改密码</h2>
        <form @submit.prevent="changePassword">
          <div class="form-group">
            <label>验证码</label>
            <div class="code-input">
              <input v-model="yanzhma" required>
              <button 
                type="button" 
                @click="sendPasswordCode"
                :disabled="passwordCodeSent"
              >
                {{ passwordCodeSent ? `${passwordCountdown}s后重试` : '获取验证码' }}
              </button>
            </div>
          </div>
          
          <div class="form-group">
            <label>新密码</label>
            <input v-model="passwordForm.newPassword" type="password" required>
          </div>
          
          <div class="form-group">
            <label>确认新密码</label>
            <input v-model="passwordForm.confirmPassword" type="password" required>
          </div>
          
          <div class="form-actions">
            <button type="submit" :disabled="isChangingPassword">
              {{ isChangingPassword ? '修改中...' : '修改密码' }}
            </button>
          </div>
        </form>
      </div>
    </div>
    
    <div v-if="showAvatarModal" class="avatar-modal">
      <div class="modal-content">
        <button class="close-btn" @click="showAvatarModal = false">×</button>
        <h2>选择头像</h2>
        
        <div class="avatar-options">
          <div 
            v-for="avatar in systemAvatars" 
            :key="avatar.name" 
            class="avatar-option"
            :class="{ selected: selectedAvatar === avatar.url }"
            @click="selectedAvatar = avatar.url"
          >
            <img :src="avatar.url" :alt="avatar.name">
            <span class="avatar-name">{{ avatar.name }}</span>
          </div>
        </div>
        
        <div class="upload-section">
          <h3>或上传自定义头像</h3>
          <input type="file" @change="handleFileUpload" accept="image/*">
        </div>
        
        <div class="modal-actions">
          <button @click="saveAvatar" :disabled="!selectedAvatar && !uploadedAvatar">
            保存
          </button>
          <button @click="showAvatarModal = false">
            取消
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useUserStore } from '@/store'
import { useApi } from '@/composables/useApi'
import { useAuth } from '@/composables/useAuth'
import { useRouter } from 'vue-router'
import Avatar from '@/components/common/Avatar.vue'

const userStore = useUserStore()
const router = useRouter()
const { logout } = useAuth()
const { put, post, isLoading: isUpdating } = useApi()

const user = computed(() => userStore)

// 退出登录处理
const handleLogout = async () => {
  try {
    await logout()
    alert('您已成功退出登录')
  } catch (err) {
    console.error('退出登录失败:', err)
    alert('退出登录失败: ' + (err.message || '未知错误'))
  }
}

const profileForm = ref({
  username: userStore.username,
  email: userStore.email
})

const passwordForm = ref({
  currentPassword: '',
  newPassword: '',
  confirmPassword: ''
})

const showAvatarModal = ref(false)
const selectedAvatar = ref(null)
const uploadedAvatar = ref(null)
const isChangingPassword = ref(false)

const systemAvatars = ref([
  { name: 'Misty', url: 'https://api.dicebear.com/7.x/bottts-neutral/svg?seed=Misty' },
  { name: 'Whiskers', url: 'https://api.dicebear.com/7.x/bottts-neutral/svg?seed=Whiskers' },
  { name: 'Smokey', url: 'https://api.dicebear.com/7.x/bottts-neutral/svg?seed=Smokey' },
  { name: 'Oliver', url: 'https://api.dicebear.com/7.x/bottts-neutral/svg?seed=Oliver' },
  { name: 'Charlie', url: 'https://api.dicebear.com/7.x/bottts-neutral/svg?seed=Charlie' }
])

onMounted(() => {
  selectedAvatar.value = userStore.avatar_url
})

const formatDate = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleDateString()
}

const passwordCodeSent = ref(false)
const passwordCountdown = ref(60)

// 发送密码重置验证码
const sendPasswordCode = async () => {
  try {
    // 使用正确的API端点
    await post('/auth/getEmailCode', {
      email: userStore.email  // 使用当前用户的邮箱
    })
    
    passwordCodeSent.value = true
    startPasswordCountdown()
    alert(`验证码已发送到您的邮箱: ${userStore.email}`)
  } catch (err) {
    console.error('发送验证码失败:', err)
    let errorMsg = '验证码发送失败'
    if (err.status === 422) {
      errorMsg = '邮箱格式不正确'
    } else if (err.data?.detail) {
      errorMsg += `: ${err.data.detail}`
    }
    alert(errorMsg)
  }
}

// 密码验证码倒计时
const startPasswordCountdown = () => {
  const timer = setInterval(() => {
    passwordCountdown.value--
    if (passwordCountdown.value <= 0) {
      clearInterval(timer)
      passwordCodeSent.value = false
      passwordCountdown.value = 60
    }
  }, 1000)
}

// 修改密码
const changePassword = async () => {
  // 验证两次密码是否一致
  if (passwordForm.value.newPassword !== passwordForm.value.confirmPassword) {
    alert('两次输入的新密码不一致')
    return
  }
  
  // 密码强度验证（可选）
  if (passwordForm.value.newPassword.length < 8) {
    alert('密码长度不能少于8位')
    return
  }
  
  isChangingPassword.value = true
  
  try {
    // 使用正确的API端点和参数
    await post('/auth/reset-password', {
      email: userStore.email,
      code: passwordForm.value.code,
      new_password: passwordForm.value.newPassword
    })
    
    alert('密码修改成功')
    // 重置表单
    passwordForm.value = {
      code: '',
      newPassword: '',
      confirmPassword: ''
    }
    passwordCodeSent.value = false
  } catch (err) {
    console.error('密码修改失败:', err)
    let errorMsg = '密码修改失败'
    
    // 根据API文档处理422验证错误
    if (err.status === 422) {
      const details = err.data?.detail || []
      if (details.some(d => d.msg.includes('code'))) {
        errorMsg = '验证码错误或已过期'
      } else if (details.some(d => d.msg.includes('password'))) {
        errorMsg = '密码不符合要求'
      }
    } else if (err.data?.detail) {
      errorMsg += `: ${err.data.detail}`
    }
    
    alert(errorMsg)
  } finally {
    isChangingPassword.value = false
  }
}

// 格式化密码错误信息
const formatPasswordError = (err) => {
  if (err.response?.data?.error === 'invalid_code') {
    return '验证码无效或已过期'
  }
  return err.data?.detail || err.message || '未知错误'
}
const handleFileUpload = (e) => {
  const file = e.target.files[0]
  if (!file) return
  
  // 验证文件类型
  const validTypes = ['image/jpeg', 'image/png', 'image/gif', 'image/webp']
  if (!validTypes.includes(file.type)) {
    alert('只支持JPEG、PNG、GIF或WebP格式的图片')
    return
  }
  
  // 验证文件大小 (2MB)
  if (file.size > 2 * 1024 * 1024) {
    alert('头像图片大小不能超过2MB')
    return
  }
  
  uploadedAvatar.value = file
  e.target.value = '' // 重置input，允许重复选择同一文件
}

const saveAvatar = async () => {
  try {
    let newAvatarUrl = ''
    
    if (uploadedAvatar.value) {
      const formData = new FormData()
      formData.append('file', uploadedAvatar.value)
      
      // 上传新头像
      const response = await post('/user/avatar/upload', formData)
      newAvatarUrl = response.avatar_url || response.url || response
    } else if (selectedAvatar.value) {
      // 选择系统头像
      newAvatarUrl = selectedAvatar.value
      await post('/user/avatar/select', { avatar_name: newAvatarUrl })
      newAvatarUrl = selectedAvatar.value
    }
    
    if (newAvatarUrl) {
      // 直接调用userStore的updateAvatar方法
      await userStore.updateAvatar(newAvatarUrl)
      alert('头像更新成功')
      
      // 如果需要强制刷新其他地方的显示
      userStore.refreshAvatar()
    }
    
    showAvatarModal.value = false
  } catch (err) {
    console.error('头像更新失败:', err)
    alert(`头像更新失败: ${err.response?.data?.message || err.message || '未知错误'}`)
  } finally {
    // 重置上传状态
    uploadedAvatar.value = null
    selectedAvatar.value = null
  }
}
</script>

<style scoped>
.avatar-btn {
  background: none; /* 透明背景 */
  border: none;     /* 无边框 */
  padding: 0;       /* 无内边距 */
  margin: 0;        /* 无外边距 */
  cursor: pointer;  /* 保持手型指针 */
  outline: none;    /* 移除焦点轮廓 */
}

/* 移除按钮点击时的默认样式 */
.avatar-btn:active, 
.avatar-btn:focus {
  outline: none;
  box-shadow: none;
}

.code-input {
  display: flex;
  gap: 0.5rem;
}

.avatar-container {
  width: auto;  /* 移除固定宽度 */
  height: auto; /* 移除固定高度 */
  display: inline-block; /* 根据内容自适应 */
}

.avatar-wrapper {
  width: 100%;
  height: 100%;
  border-radius: 50%; /* 保持圆形 */
  overflow: hidden;   /* 确保内容不会超出圆形边界 */
}

.avatar-img {
  width: 100%;
  height: 100%;
  object-fit: cover;  /* 保持图片比例并填满容器 */
  border-radius: 50%;
}

.avatar-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #ccc; /* 背景色 */
  color: white;          /* 文字颜色 */
  font-size: 40px;       /* 文字大小 */
  font-weight: bold;
  border-radius: 50%;    /* 圆形 */
}

.code-input input {
  flex: 1;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.code-input button {
  white-space: nowrap;
  padding: 0 1rem;
  background-color: #f3f4f6;
  border: 1px solid #ddd;
  border-radius: 4px;
  cursor: pointer;
}

.code-input button:disabled {
  cursor: not-allowed;
  opacity: 0.7;
}

.logout-btn {
  margin-top: 1rem;
  padding: 0.5rem 1rem;
  background-color: #fef2f2;
  color: #dc2626;
  border: 1px solid #fecaca;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.2s;
}

.logout-btn:hover {
  background-color: #fee2e2;
}

.hint-text {
  font-size: 0.8rem;
  color: #666;
  margin-top: 0.5rem;
}

.avatar-option {
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.avatar-name {
  margin-top: 0.5rem;
  font-size: 0.8rem;
}

.upload-section {
  margin-top: 2rem;
  padding-top: 1.5rem;
  border-top: 1px solid #eee;
}

.upload-section input[type="file"] {
  margin-top: 0.5rem;
}

.profile-view {
  max-width: 800px;
  margin: 0 auto;
  padding: 2rem;
}

.profile-header {
  display: flex;
  align-items: center;
  gap: 2rem;
  margin-bottom: 2rem;
  padding-bottom: 2rem;
  border-bottom: 1px solid #eee;
}

.change-avatar-btn {
  padding: 0.5rem 1rem;
  background-color: #e0e7ff;
  color: #4f46e5;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.user-info h1 {
  margin: 0;
  color: #1f2937;
}

.user-info p {
  margin: 0.5rem 0 0;
  color: #6b7280;
}

.profile-content {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
}

.section {
  background-color: white;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.section h2 {
  margin-top: 0;
  margin-bottom: 1.5rem;
  color: #4f46e5;
}

.form-group {
  margin-bottom: 1rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: #4b5563;
}

.form-group input {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
}

.form-actions {
  margin-top: 1.5rem;
}

.form-actions button {
  padding: 0.75rem 1.5rem;
  background-color: #4f46e5;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
}

.form-actions button:disabled {
  background-color: #a5b4fc;
  cursor: not-allowed;
}

.avatar-modal {
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
  padding: 2rem;
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

.avatar-options {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(80px, 1fr));
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.avatar-option {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  overflow: hidden;
  cursor: pointer;
  border: 2px solid transparent;
}

.avatar-option.selected {
  border-color: #4f46e5;
}

.avatar-option img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.upload-section {
  margin-top: 1.5rem;
  padding-top: 1.5rem;
  border-top: 1px solid #eee;
}

.upload-section h3 {
  margin-top: 0;
  margin-bottom: 1rem;
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 0.5rem;
  margin-top: 1.5rem;
}

.modal-actions button {
  padding: 0.75rem 1.5rem;
  border-radius: 4px;
  font-size: 1rem;
  cursor: pointer;
}

.modal-actions button:first-child {
  background-color: #4f46e5;
  color: white;
  border: none;
}

.modal-actions button:last-child {
  background-color: #f3f4f6;
  border: 1px solid #ddd;
  color: #4b5563;
}
</style>