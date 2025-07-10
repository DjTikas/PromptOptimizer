<template>
  <div class="login-view">
    <div class="login-container">
      <h1>欢迎回来</h1>
      
      <form @submit.prevent="handleLogin" class="login-form">
        <div class="form-group">
          <label>邮箱</label>
          <input v-model="loginForm.email" type="email" required>
        </div>
        
        <div class="form-group">
          <label>密码</label>
          <input v-model="loginForm.password" type="password" required>
        </div>
        
        <div class="form-actions">
          <button type="submit" :disabled="isLoggingIn">
            {{ isLoggingIn ? '登录中...' : '登录' }}
          </button>
        </div>
        
        <div class="form-footer">
          <router-link to="/register">注册新账号</router-link>
          <a href="#" @click.prevent="handleForgotPasswordClick">忘记密码?</a>
        </div>
      </form>
      
    </div>
    
    <div v-if="showForgotPassword" class="forgot-password-modal">
      <div class="modal-content">
        <button class="close-btn" @click="closeResetModal">×</button>
        <h2>重置密码</h2>
        
        <form @submit.prevent="handleResetPassword">
          <div class="form-group">
            <label>邮箱</label>
            <input v-model="resetForm.email" type="email" required>
          </div>
          
          <div class="form-group">
            <label>验证码</label>
            <div class="code-input">
              <input v-model="resetForm.code" required>
              <button 
                type="button" 
                @click="sendResetCode"
                :disabled="resetCodeSent"
              >
                {{ resetCodeSent ? `${resetCountdown}s后重试` : '获取验证码' }}
              </button>
            </div>
          </div>
          
          <div class="form-group">
            <label>新密码</label>
            <input v-model="resetForm.newPassword" type="password" required>
          </div>
          
          <div class="form-group">
            <label>确认新密码</label>
            <input v-model="resetForm.confirmPassword" type="password" required>
          </div>
          
          <div class="form-actions">
            <button type="submit" :disabled="isResetting">
              {{ isResetting ? '处理中...' : '重置密码' }}
            </button>
            <button 
              type="button" 
              class="back-to-login"
              @click="closeResetModal"
            >
              返回登录
            </button>
          </div>
        </form>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/store'
import { useApi } from '@/composables/useApi'

const router = useRouter()
const userStore = useUserStore()
const { post, get } = useApi()
// Toast通知相关状态
const showToast = ref(false)
const toastMessage = ref('')
const toastType = ref('error') // 'error' 或 'success'

// 显示Toast通知
const showNotification = (message, type = 'error') => {
  toastMessage.value = message
  toastType.value = type
  showToast.value = true
  
  // 3秒后自动隐藏
  setTimeout(() => {
    showToast.value = false
  }, 3000)
}

const loginForm = ref({
  email: '',
  password: ''
})

const resetForm = ref({
  email: '',
  code: '',
  newPassword: '',
  confirmPassword: ''
})

const showForgotPassword = ref(false)
const isLoggingIn = ref(false)
const isResetting = ref(false)
const resetCodeSent = ref(false)
const resetCountdown = ref(60)
const errorMessage = ref('')
const loginError = ref(null) // 改名为loginError避免命名冲突

// 添加这个方法
const handleForgotPasswordClick = () => {
  // 确保正确填充邮箱到邮箱字段
  resetForm.value = {
    email: loginForm.value.email,  // 这里确保填充到email字段
    code: '',
    newPassword: '',
    confirmPassword: ''
  }
  showForgotPassword.value = true
}

const closeResetModal = () => {
  showForgotPassword.value = false
  // 保留邮箱以便下次打开时使用
  resetForm.value = {
    email: resetForm.value.email, // 保留当前邮箱
    code: '',
    newPassword: '',
    confirmPassword: ''
  }
}

const handleLogin = async () => {
  isLoggingIn.value = true
  loginError.value = null

  try {
    // 1. 获取token
    const authData = new URLSearchParams({
      grant_type: 'password',
      username: loginForm.value.email,
      password: loginForm.value.password,
      client_id: 'web_app',
      client_secret: 'web_secret'
    })

    const tokenData = await post('/auth/token', authData, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      }
    })

    if (!tokenData?.access_token) {
      throw new Error('无效的令牌响应')
    }

    // 2. 通过store统一处理登录流程
    await userStore.login({
      token: tokenData.access_token
    })
    
    // 3. 跳转首页
    router.push('/')
  } catch (err) {
    console.error('登录失败:', err)
    loginError.value = formatLoginError(err)
    alert(formatLoginError(err))
  } finally {
    isLoggingIn.value = false
  }
}

// 格式化登录错误
const formatLoginError = (err) => {
  if (err.message.includes('无效的登录数据')) {
    return err.message
  }

  if (err.isNetworkError) {
    return '网络连接失败，请检查网络设置'
  }

  let message = '登录失败'
  if (err.status) {
    message += ` (状态码: ${err.status})`
  }

  if (err.data?.detail) {
    return `${message}: ${err.data.detail}`
  }

  if (err.response?.data?.error === 'invalid_grant') {
    return '邮箱或密码不正确'
  }
  
  return `${message}: ${err.message || '未知错误'}`
}

const sendResetCode = async () => {
  try {
    await post('/auth/getEmailCode', { email: resetForm.value.email })
    resetCodeSent.value = true
    startResetCountdown()
    alert('验证码已发送到您的邮箱') // 发送成功提示
  } catch (err) {
    console.error('Failed to send reset code:', err)
    alert('验证码发送失败')
  }
}

const startResetCountdown = () => {
  const timer = setInterval(() => {
    resetCountdown.value--
    if (resetCountdown.value <= 0) {
      clearInterval(timer)
      resetCodeSent.value = false
      resetCountdown.value = 60
    }
  }, 1000)
}

const handleResetPassword = async () => {
  if (resetForm.value.newPassword !== resetForm.value.confirmPassword) {
    alert('两次输入的密码不一致')
    return
  }
  
  isResetting.value = true
  
  try {
    await post('/auth/reset-password', {
      email: resetForm.value.email,
      code: resetForm.value.code,
      new_password: resetForm.value.newPassword
    })
    
    alert('密码重置成功，请使用新密码登录')
    showForgotPassword.value = false
    resetForm.value = {
      email: '',
      code: '',
      newPassword: '',
      confirmPassword: ''
    }
  } catch (err) {
    console.error('Password reset failed:', err)
    alert(formatResetError(err)) 
  } finally {
    isResetting.value = false
  }
}

const formatResetError = (err) => {
  if (err.response?.data) {
    const data = err.response.data
    
    if (data.error === 'invalid_code') {
      return '验证码无效或已过期'
    }
    
    if (data.error === 'password_mismatch') {
      return '两次输入的密码不一致'
    }
    
    if (data.detail) {
      return data.detail
    }
  }
  
  if (err.isNetworkError) {
    return '网络连接失败，请检查网络设置'
  }
  
  return '操作失败，请稍后重试'
}
</script>

<style scoped>
.back-to-login {
  width: 100%;
  padding: 0.75rem;
  background-color: #f3f4f6;
  color: #4b5563;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  margin-top: 0.5rem;
}

.back-to-login:hover {
  background-color: #e5e7eb;
}

.form-actions {
  display: flex;
  flex-direction: column;
}

.toast-error {
  position: fixed;
  top: 20px;
  left: 50%;
  transform: translateX(-50%);
  padding: 12px 24px;
  background-color: #ef4444;
  color: white;
  border-radius: 4px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  z-index: 1000;
  animation: slideDown 0.3s ease-out;
}

@keyframes slideDown {
  from {
    opacity: 0;
    transform: translate(-50%, -20px);
  }
  to {
    opacity: 1;
    transform: translate(-50%, 0);
  }
}

.login-view {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #f9fafb;
  padding: 2rem;
}

.login-container {
  background-color: white;
  padding: 2.5rem;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 400px;
}

h1 {
  margin-top: 0;
  margin-bottom: 2rem;
  text-align: center;
  color: #1f2937;
}

.login-form {
  margin-bottom: 1.5rem;
}

.form-group {
  margin-bottom: 1.25rem;
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
  margin-top: 2rem;
}

.form-actions button {
  width: 100%;
  padding: 0.75rem;
  background-color: #4f46e5;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
}

.form-actions button:disabled {
  background-color: #a5b4fc;
  cursor: not-allowed;
}

.form-footer {
  display: flex;
  justify-content: space-between;
  margin-top: 1rem;
  font-size: 0.875rem;
}

.form-footer a {
  color: #4f46e5;
  text-decoration: none;
}

.form-footer a:hover {
  text-decoration: underline;
}

.social-login {
  border-top: 1px solid #eee;
  padding-top: 1.5rem;
}

.divider {
  position: relative;
  text-align: center;
  margin-bottom: 1rem;
  color: #9ca3af;
}

.divider::before,
.divider::after {
  content: '';
  position: absolute;
  top: 50%;
  width: calc(50% - 1.5rem);
  height: 1px;
  background-color: #eee;
}

.divider::before {
  left: 0;
}

.divider::after {
  right: 0;
}

.google-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  width: 100%;
  padding: 0.75rem;
  background-color: white;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
  cursor: pointer;
}

.google-btn:hover {
  background-color: #f9fafb;
}

.google-btn svg {
  width: 20px;
  height: 20px;
}

.forgot-password-modal {
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
  max-width: 400px;
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

.modal-content h2 {
  margin-top: 0;
  margin-bottom: 1.5rem;
  text-align: center;
}

.code-input {
  display: flex;
  gap: 0.5rem;
}

.code-input input {
  flex: 1;
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
</style>