import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { useApi } from '@/composables/useApi'
import { useRouter } from 'vue-router'

export const useUserStore = defineStore('user', () => {
  const userId = ref(null)
  const email = ref('')
  const username = ref('未登录用户')
  const avatar = ref('')
  const token = ref(null)
  const isLoggedIn = computed(() => !!token.value)

  const router = useRouter() // 新增：引入router
  const { get, post } = useApi() // 修改：新增post方法

  // 原有状态...
  const avatarTimestamp = ref(Date.now()) // 新增：头像时间戳
  
  // 新增计算属性
  const avatarWithTimestamp = computed(() => {
    return avatar.value ? `${avatar.value}?t=${avatarTimestamp.value}` : ''
  })

  // 新增方法
  const updateAvatar = async (newAvatarUrl) => {
    avatar.value = newAvatarUrl
    refreshAvatar()
    
    try {
      //await post('/user/update-avatar', { avatar_url: newAvatarUrl })
    } catch (err) {
      console.error('头像更新失败:', err)
      throw err
    }
  }

  // 新增方法
  const refreshAvatar = () => {
    avatarTimestamp.value = Date.now()
  }


  const login = async (userData) => {
    if (!userData?.token) {
      throw new Error('缺少访问令牌')
    }

    // 先设置token确保后续请求可用
    token.value = userData.token
    
    // 获取完整用户信息
    try {
      const userInfo = await get('/auth/me', {}, {
        headers: {
          Authorization: `Bearer ${userData.token}`
        }
      })

      userId.value = userInfo.user_id
      email.value = userInfo.email
      username.value = userInfo.username || userInfo.email.split('@')[0]
      avatar.value = userInfo.avatar_url
      
      return userInfo
    } catch (err) {
      // 获取用户信息失败时回滚
      logout()
      throw err
    }
  }

  const logout = () => {
    userId.value = null
    email.value = ''
    username.value = '未登录用户'
    avatar.value = ''
    token.value = null
    resetUserState()
    router.push('/login') // 新增：登出后跳转
  }

  // 新增方法
  const resetUserState = () => {
    userId.value = null
    email.value = ''
    username.value = '未登录用户'
    avatar.value = ''
    token.value = null
    avatarTimestamp.value = Date.now() // 重置时间戳
  }

  const fetchUserInfo = async () => {
    if (!token.value) {
      throw new Error('未登录')
    }
    
    try {
      return await get('/auth/me', {}, {
        headers: {
          Authorization: `Bearer ${token.value}`
        }
      })
    } catch (err) {
      logout()
      throw err
    }
  }

  return {
    userId,
    email,
    username,
    avatar,
    token,
    isLoggedIn,
    login,
    logout,
    fetchUserInfo,
    avatarTimestamp, // 新增
    avatarWithTimestamp, // 新增
    updateAvatar, // 新增
    refreshAvatar, // 新增
    resetUserState // 新增
  }
}, {
  persist: {
    key: 'prompt-community-user',
    paths: ['userId', 'email', 'username', 'avatar', 'token'],
    serializer: {
      serialize: JSON.stringify,
      deserialize: JSON.parse
    }
  }
})

export const usePromptStore = defineStore('prompt', () => {
  const currentFolderId = ref(null)
  const searchQuery = ref('')
  const searchMode = ref('AND')
  const selectedTags = ref([])

  return {
    currentFolderId,
    searchQuery,
    searchMode,
    selectedTags
  }
})