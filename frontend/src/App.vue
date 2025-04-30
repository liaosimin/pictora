<template>
  <div class="app-container">
    <!-- 主内容区域 -->
    <div class="content-area">
      <router-view v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </div>
    
    <!-- 底部导航栏 -->
    <van-tabbar v-model="activeTab" route v-if="showTabbar">
      <van-tabbar-item to="/generate" icon="photo-o">生成</van-tabbar-item>
      <van-tabbar-item to="/tasks" icon="orders-o">任务</van-tabbar-item>
      <van-tabbar-item to="/profile" icon="user-o">我的</van-tabbar-item>
    </van-tabbar>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useUserStore } from './stores/user'

// 获取用户状态
const userStore = useUserStore()
const route = useRoute()

// 当前激活的标签页
const activeTab = ref(0)

// 计算是否显示底部导航栏
const showTabbar = computed(() => {
  const noTabbarRoutes = ['/login', '/register']
  return !noTabbarRoutes.includes(route.path) && userStore.isLoggedIn
})

// 组件挂载时获取用户信息
onMounted(async () => {
  if (userStore.isLoggedIn) {
    await userStore.fetchUserProfile()
  }
})
</script>

<style>
/* 全局样式 */
:root {
  --primary-color: #7367f0;
  --secondary-color: #9e95f5;
  --success-color: #28c76f;
  --info-color: #00cfe8;
  --warning-color: #ff9f43;
  --danger-color: #ea5455;
  --background-color: #f8f7fa;
  --text-color: #4b4b4b;
  --light-text: #6e6b7b;
  --border-color: #ebe9f1;
}

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html, body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: var(--text-color);
  background-color: var(--background-color);
  height: 100%;
  width: 100%;
}

#app {
  height: 100%;
  width: 100%;
}

.app-container {
  display: flex;
  flex-direction: column;
  height: 100%;
  width: 100%;
  max-width: 500px;
  margin: 0 auto;
  background-color: #fff;
  position: relative;
}

.content-area {
  flex: 1;
  overflow-y: auto;
  padding-bottom: 50px;
}

/* 页面过渡动画 */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* 通用样式类 */
.page-container {
  padding: 16px;
}

.page-title {
  font-size: 20px;
  font-weight: 600;
  margin-bottom: 16px;
  color: var(--primary-color);
}

.card {
  background-color: #fff;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  padding: 16px;
  margin-bottom: 16px;
}

.btn-primary {
  background-color: var(--primary-color);
  color: white;
  border: none;
  border-radius: 8px;
  padding: 12px 20px;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.3s;
}

.btn-primary:hover {
  background-color: var(--secondary-color);
}

.text-center {
  text-align: center;
}

.mt-16 {
  margin-top: 16px;
}

.mb-16 {
  margin-bottom: 16px;
}
</style>
