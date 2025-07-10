<template>
  <div class="app-container">
    <header class="app-header">
      <div class="header-left">
        <router-link to="/profile" class="user-info">
          <Avatar :src="userStore.avatar" size="small" />
          <span v-if="userStore.isLoggedIn">{{ userStore.username }}</span>
          <span v-else>未登录</span>
        </router-link>
      </div>
      <nav class="header-nav">
        <router-link to="/">首页</router-link>
        <router-link to="/optimize">提示词优化</router-link>
        <router-link to="/favorites">收藏夹</router-link>
        <router-link to="/api">API管理</router-link>
      </nav>
    </header>
    
    <main class="app-main">
      <router-view v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </main>
    
    <!-- 新增通知组件 -->
    <Notification ref="notification" />
    <LoginModal v-if="showLoginModal" @close="showLoginModal = false" />
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue' // 确保导入生命周期钩子
import { useRouter } from 'vue-router'
import { useUserStore } from '@/store'
import Avatar from '@/components/common/Avatar.vue'
import LoginModal from '@/components/common/LoginModal.vue'
import Notification from '@/components/common/Notification.vue' // 新增导入

const router = useRouter()
const userStore = useUserStore()
const showLoginModal = ref(false)
const notification = ref(null) // 新增通知引用

// 全局挂载通知方法
onMounted(() => {
  window.$notify = {
    success: (msg) => notification.value.add(msg, 'success'),
    error: (msg) => notification.value.add(msg, 'error'),
    info: (msg) => notification.value.add(msg, 'info'),
    warning: (msg) => notification.value.add(msg, 'warning')
  }
})

// 检查需要登录的路由
const authRequiredRoutes = ['/optimize', '/favorites', '/api']

const unwatch = router.beforeEach((to) => {
  if (authRequiredRoutes.includes(to.path)) {
    if (!userStore.isLoggedIn) {
      showLoginModal.value = true
      return false
    }
  }
})

// 组件卸载时取消监听
onUnmounted(() => {
  unwatch()
})
</script>

<style scoped>
.app-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.app-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 2rem;
  background-color: #fff;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  position: sticky;
  top: 0;
  z-index: 100;
}

.header-left {
  display: flex;
  align-items: center;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  text-decoration: none;
  color: inherit;
}

.header-nav {
  display: flex;
  gap: 2rem;
}

.header-nav a {
  text-decoration: none;
  color: #333;
  font-weight: 500;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  transition: all 0.2s;
}

.header-nav a:hover {
  background-color: #f0f0f0;
}

.header-nav a.router-link-active {
  color: #4f46e5;
  background-color: #eef2ff;
}

.app-main {
  flex: 1;
  padding: 2rem;
  background-color: #f9fafb;
}

/* 路由过渡动画 */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>