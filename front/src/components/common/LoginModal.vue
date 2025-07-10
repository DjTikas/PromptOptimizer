<template>
  <div class="modal-overlay" @click.self="$emit('close')">
    <div class="modal-content">
      <button class="close-btn" @click="$emit('close')">×</button>
      
      <div class="tabs">
        <button 
          :class="{ active: activeTab === 'login' }" 
          @click="activeTab = 'login'"
        >
          登录
        </button>
        <button 
          :class="{ active: activeTab === 'register' }" 
          @click="activeTab = 'register'"
        >
          注册
        </button>
      </div>
      
      <form v-if="activeTab === 'login'" @submit.prevent="handleLogin">
        <div class="form-group">
          <label>邮箱</label>
          <input v-model="loginEmail" type="email" required>
        </div>
        
        <div class="form-group">
          <label>密码</label>
          <input v-model="loginPassword" type="password" required>
        </div>
        
        <button type="submit" :disabled="isLoading">登录</button>
        
        <div class="forgot-password">
          <a href="#" @click.prevent="showForgotPassword = true">忘记密码?</a>
        </div>
      </form>
      
      <form v-else @submit.prevent="handleRegister">
        <div class="form-group">
          <label>昵称</label>
          <input v-model="registerName" required>
        </div>
        
        <div class="form-group">
          <label>邮箱</label>
          <input v-model="registerEmail" type="email" required>
        </div>
        
        <div class="form-group">
          <label>验证码</label>
          <div class="code-input">
            <input v-model="registerCode" required>
            <button 
              type="button" 
              @click="sendVerificationCode"
              :disabled="codeSent"
            >
              {{ codeSent ? `${countdown}s后重试` : '获取验证码' }}
            </button>
          </div>
        </div>
        
        <div class="form-group">
          <label>密码</label>
          <input v-model="registerPassword" type="password" required>
        </div>
        
        <div class="form-group">
          <label>确认密码</label>
          <input v-model="registerConfirmPassword" type="password" required>
        </div>
        
        <div class="form-group">
          <label>头像</label>
          <div class="avatar-options">
            <div 
              v-for="avatar in defaultAvatars" 
              :key="avatar" 
              class="avatar-option"
              :class="{ selected: registerAvatar === avatar }"
              @click="registerAvatar = avatar"
            >
              <img :src="avatar" alt="Avatar">
            </div>
          </div>
        </div>
        
        <button type="submit" :disabled="isLoading">注册</button>
      </form>
      
      <div v-if="showForgotPassword" class="forgot-password-modal">
        <h3>重置密码</h3>
        <div class="form-group">
          <label>邮箱</label>
          <input v-model="resetEmail" type="email" required>
        </div>
        
        <div class="form-group">
          <label>验证码</label>
          <div class="code-input">
            <input v-model="resetCode" required>
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
          <input v-model="newPassword" type="password" required>
        </div>
        
        <div class="form-group">
          <label>确认新密码</label>
          <input v-model="confirmNewPassword" type="password" required>
        </div>
        
        <div class="actions">
          <button @click="handleResetPassword" :disabled="isLoading">重置密码</button>
          <button @click="showForgotPassword = false">取消</button>
        </div>
      </div>
      
      <div v-if="error" class="error-message">{{ error }}</div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useAuth } from '@/composables/useAuth'

const emit = defineEmits(['close'])

const { login, register, sendVerificationCode: sendCode, resetPassword, isLoading, error } = useAuth()

const activeTab = ref('login')
const showForgotPassword = ref(false)

// 登录表单
const loginEmail = ref('')
const loginPassword = ref('')

// 注册表单
const registerName = ref('')
const registerEmail = ref('')
const registerCode = ref('')
const registerPassword = ref('')
const registerConfirmPassword = ref('')
const registerAvatar = ref('')
const codeSent = ref(false)
const countdown = ref(60)

// 重置密码表单
const resetEmail = ref('')
const resetCode = ref('')
const newPassword = ref('')
const confirmNewPassword = ref('')
const resetCodeSent = ref(false)
const resetCountdown = ref(60)

const defaultAvatars = [
  'https://api.dicebear.com/7.x/bottts-neutral/svg?seed=Misty',
  'https://api.dicebear.com/7.x/bottts-neutral/svg?seed=Whiskers',
  'https://api.dicebear.com/7.x/bottts-neutral/svg?seed=Smokey',
  'https://api.dicebear.com/7.x/bottts-neutral/svg?seed=Oliver',
  'https://api.dicebear.com/7.x/bottts-neutral/svg?seed=Charlie'
]

const handleLogin = async () => {
  try {
    await login(loginEmail.value, loginPassword.value)
    emit('close')
  } catch (err) {
    console.error('Login failed:', err)
  }
}

const sendVerificationCode = async () => {
  try {
    await sendCode(registerEmail.value)
    codeSent.value = true
    startCountdown()
  } catch (err) {
    console.error('Failed to send verification code:', err)
  }
}

const startCountdown = () => {
  const timer = setInterval(() => {
    countdown.value--
    if (countdown.value <= 0) {
      clearInterval(timer)
      codeSent.value = false
      countdown.value = 60
    }
  }, 1000)
}

const handleRegister = async () => {
  if (registerPassword.value !== registerConfirmPassword.value) {
    error.value = '两次输入的密码不一致'
    return
  }
  
  if (!registerAvatar.value) {
    registerAvatar.value = defaultAvatars[0]
  }
  
  try {
    await register(
      registerEmail.value,
      registerPassword.value,
      registerName.value,
      registerAvatar.value
    )
    emit('close')
  } catch (err) {
    console.error('Registration failed:', err)
  }
}

const sendResetCode = async () => {
  try {
    await sendCode(resetEmail.value)
    resetCodeSent.value = true
    startResetCountdown()
  } catch (err) {
    console.error('Failed to send reset code:', err)
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
  if (newPassword.value !== confirmNewPassword.value) {
    error.value = '两次输入的密码不一致'
    return
  }
  
  try {
    await resetPassword(
      resetEmail.value,
      resetCode.value,
      newPassword.value
    )
    
    showForgotPassword.value = false
    activeTab.value = 'login'
    error.value = ''
  } catch (err) {
    console.error('Password reset failed:', err)
  }
}
</script>

<style scoped>
.modal-overlay {
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
  max-width: 500px;
  position: relative;
  max-height: 90vh;
  overflow-y: auto;
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

.tabs {
  display: flex;
  margin-bottom: 1.5rem;
  border-bottom: 1px solid #eee;
}

.tabs button {
  padding: 0.75rem 1.5rem;
  background: none;
  border: none;
  cursor: pointer;
  font-size: 1rem;
  color: #666;
  border-bottom: 2px solid transparent;
}

.tabs button.active {
  color: #4f46e5;
  border-bottom-color: #4f46e5;
  font-weight: 500;
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

button[type="submit"] {
  width: 100%;
  padding: 0.75rem;
  background-color: #4f46e5;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  margin-top: 1rem;
  cursor: pointer;
}

button[type="submit"]:disabled {
  background-color: #a5b4fc;
  cursor: not-allowed;
}

.forgot-password {
  text-align: right;
  margin-top: 0.5rem;
}

.forgot-password a {
  color: #666;
  text-decoration: none;
  font-size: 0.875rem;
}

.forgot-password a:hover {
  text-decoration: underline;
}

.avatar-options {
  display: flex;
  gap: 0.5rem;
  margin-top: 0.5rem;
}

.avatar-option {
  width: 40px;
  height: 40px;
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

.forgot-password-modal {
  margin-top: 1.5rem;
  padding-top: 1.5rem;
  border-top: 1px solid #eee;
}

.forgot-password-modal h3 {
  margin-bottom: 1rem;
}

.actions {
  display: flex;
  gap: 0.5rem;
  margin-top: 1rem;
}

.actions button {
  flex: 1;
}

.error-message {
  color: #ef4444;
  margin-top: 1rem;
  text-align: center;
}
</style>