import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/store'
import { useApi } from './useApi'

export function useAuth() {
  const router = useRouter()
  const userStore = useUserStore()
  const { post, isLoading, error } = useApi()

  const login = async (email, password) => {
    try {
      const formData = new URLSearchParams()
      formData.append('grant_type', 'password')
      formData.append('username', email)
      formData.append('password', password)
      formData.append('client_id', 'web_app') // 添加客户端ID
      formData.append('client_secret', 'web_secret') // 添加客户端密钥
      formData.append('scope', '') // 添加scope参数
  
      const tokenData = await post('/auth/token', formData, {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded'
        }
      })
      
      if (!tokenData.access_token) {
        throw new Error('登录失败: 未获取到访问令牌')
      }
  
      const userInfo = await get('/auth/me', null, {
        headers: {
          Authorization: `Bearer ${tokenData.access_token}`
        }
      })
      
      userStore.login({
        token: tokenData.access_token,
        user: {
          id: userInfo.user_id,
          email: userInfo.email,
          role: userInfo.role,
          avatar: userInfo.avatar_url,
          username: userInfo.username || email.split('@')[0]
        }
      })
      
      return true
    } catch (err) {
      console.error('登录失败:', err)
      error.value = err.response?.data?.detail || err.message || '登录失败，请重试'
      throw err
    }
  }

  const register = async (data) => {
    try {
      console.log('最终注册请求数据:', JSON.stringify({
        email: data.email,
        password_hash: data.password,
        avatar_url: data.avatar_url,
        role: "user"
      }, null, 2));
  
      const response = await post('/auth/register', {
        email: data.email,
        password_hash: data.password,
        avatar_url: data.avatar_url,
        role: "user"
      });
  
      return response.data;
    } catch (err) {
      // 构建详细错误信息
      let errorDetails = '';
      if (err.response) {
        errorDetails = `状态码: ${err.response.status}\n`;
        if (err.response.data) {
          errorDetails += `错误详情: ${JSON.stringify(err.response.data, null, 2)}`;
        }
      }
      throw new Error(`注册失败\n${errorDetails}`.trim());
    }
  };

  const logout = () => {
    userStore.logout()
    router.push('/login')
  }

  const sendVerificationCode = async (email) => {
    try {
      await post('/auth/getEmailCode', { email })
      return true
    } catch (err) {
      console.error('Failed to send verification code:', err)
      throw err
    }
  }

  const resetPassword = async (email, code, newPassword) => {
    try {
      await post('/auth/reset-password', {
        email,
        code,
        new_password: newPassword
      })
      return true
    } catch (err) {
      console.error('Password reset failed:', err)
      throw err
    }
  }

  return {
    isLoading,
    error,
    login,
    register,
    logout,
    sendVerificationCode,
    resetPassword
  }
}