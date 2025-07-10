<template>
  <div class="register-view">
    <div class="register-container">
      <h1>创建账号</h1>
      
      <!-- 添加 hidden 字段引导浏览器正确自动填充 -->
      <form @submit.prevent="handleRegister" class="register-form" autocomplete="on">
        <!-- 隐藏的邮箱字段引导自动填充 -->
        <input type="email" name="email" style="display:none">
        
        <div class="form-group">
          <label>邮箱</label>
          <input 
            v-model="registerForm.email" 
            type="email" 
            name="email"
            autocomplete="email"
            required
          >
        </div>
        
        <div class="form-group">
          <label>验证码</label>
          <div class="code-input">
            <input 
              v-model="registerForm.code" 
              name="register-code"
              autocomplete="one-time-code"
              required
            >
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
          <input 
            v-model="registerForm.password" 
            type="password" 
            name="register-password"
            autocomplete="new-password"
            required
          >
        </div>
        
        <div class="form-group">
          <label>确认密码</label>
          <input 
            v-model="registerForm.confirmPassword" 
            type="password" 
            name="register-confirm-password"
            autocomplete="new-password"
            required
          >
        </div>
        
        <div class="form-group">
          <label>头像</label>
          <div class="avatar-options">
            <div 
              v-for="avatar in defaultAvatars" 
              :key="avatar" 
              class="avatar-option"
              :class="{ selected: selectedAvatar === avatar }"
              @click="selectAvatar(avatar)"
            >
              <img :src="avatar" alt="Avatar">
            </div>
          </div>
        </div>
        
        <div class="form-actions">
          <button type="submit" :disabled="isRegistering">
            {{ isRegistering ? '注册中...' : '注册' }}
          </button>
        </div>
        
        <div class="form-footer">
          已有账号? <router-link to="/login">立即登录</router-link>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuth } from '@/composables/useAuth'

const router = useRouter()
const { register, sendVerificationCode: sendCode, isLoading: isRegistering } = useAuth()

const registerForm = ref({
  email: '',
  code: '',
  password: '',
  confirmPassword: ''
})

const selectedAvatar = ref('')
const codeSent = ref(false)
const countdown = ref(60)

const defaultAvatars = [
  'https://api.dicebear.com/7.x/bottts-neutral/svg?seed=Misty',
  'https://api.dicebear.com/7.x/bottts-neutral/svg?seed=Whiskers',
  'https://api.dicebear.com/7.x/bottts-neutral/svg?seed=Smokey',
  'https://api.dicebear.com/7.x/bottts-neutral/svg?seed=Oliver',
  'https://api.dicebear.com/7.x/bottts-neutral/svg?seed=Charlie'
]

onMounted(() => {
  // 更可靠的自动填充处理
  setTimeout(() => {
    // 1. 首先尝试获取隐藏字段的自动填充值
    const hiddenEmail = document.querySelector('input[type="email"][style*="display:none"]')?.value;
    
    // 2. 如果没有，再尝试获取可见邮箱字段的值
    const visibleEmail = document.querySelector('input[name="email"]:not([style*="display:none"])')?.value;
    
    // 3. 优先使用隐藏字段的值，其次是可见字段的值
    if (hiddenEmail) {
      registerForm.value.email = hiddenEmail;
    } else if (visibleEmail) {
      registerForm.value.email = visibleEmail;
    }
  }, 200); // 稍长的延迟确保浏览器完成自动填充
});

const selectAvatar = (avatar) => {
  selectedAvatar.value = avatar
}

const sendVerificationCode = async () => {
  if (!registerForm.value.email) {
    alert('请输入邮箱地址')
    return
  }
  
  try {
    await sendCode(registerForm.value.email)
    codeSent.value = true
    startCountdown()
  } catch (err) {
    alert('发送验证码失败: ' + err.message)
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

const errors = ref({
  email: '',
  password: '',
  confirmPassword: '',
  avatar: ''
})

const validateForm = () => {
  let isValid = true;
  errors.value = {
    email: '',
    password: '',
    confirmPassword: '',
    avatar: ''
  };

  // 邮箱验证
  if (!registerForm.value.email) {
    errors.value.email = '请输入邮箱地址';
    isValid = false;
  } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(registerForm.value.email)) {
    errors.value.email = '请输入有效的邮箱地址';
    isValid = false;
  }

  // 密码验证
  if (!registerForm.value.password) {
    errors.value.password = '请输入密码';
    isValid = false;
  }

  // 确认密码验证
  if (registerForm.value.password !== registerForm.value.confirmPassword) {
    errors.value.confirmPassword = '两次输入的密码不一致';
    isValid = false;
  }

  // 头像选择验证
  if (!selectedAvatar.value) {
    errors.value.avatar = '请选择头像';
    isValid = false;
  }

  return isValid;
};

const handleRegister = async () => {
  try {
    if (!validateForm()) {
      const errorMsg = Object.values(errors.value).filter(e => e).join('\n');
      alert(`请修正以下问题:\n${errorMsg}`);
      return;
    }

    isRegistering.value = true;
    
    const result = await register({
      email: registerForm.value.email,
      password: registerForm.value.password, // 保持原始密码不做任何处理
      avatar_url: selectedAvatar.value,     // 确保字段名完全匹配
      role: 'user'                          // 明确传递合法role值
    });
    
    alert('注册成功！');
    router.push('/login');
  } catch (err) {
    console.error('注册错误:', err);
    
    // 显示详细的API错误信息
    let errorMsg = err.message;
    if (err.response?.data) {
      errorMsg = JSON.stringify(err.response.data, null, 2);
    }
    alert(`注册失败: ${errorMsg}`);
  } finally {
    isRegistering.value = false;
  }
}
</script>

<style scoped>
.error {
  color: #ef4444;
  font-size: 0.75rem;
  margin-top: 0.25rem;
  display: block;
  height: 1rem; /* 确保有空间显示 */
}

.form-group {
  margin-bottom: 1.5rem; /* 增加间距 */
}

input:invalid {
  border-color: #ef4444;
}

.register-view {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #f9fafb;
  padding: 2rem;
}

.register-container {
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

.register-form {
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

.avatar-options {
  display: flex;
  flex-wrap: wrap;
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
  margin-top: 1rem;
  text-align: center;
  font-size: 0.875rem;
  color: #6b7280;
}

.form-footer a {
  color: #4f46e5;
  text-decoration: none;
}

.form-footer a:hover {
  text-decoration: underline;
}
</style>