import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    redirect: '/generate'
  },
  {
    path: '/generate',
    name: 'Generate',
    component: () => import('../views/GenerateView.vue'),
    meta: { title: '生成' }
  },
  {
    path: '/styles',
    name: 'Styles',
    component: () => import('../views/StylesView.vue'),
    meta: { title: '风格效果' }
  },
  {
    path: '/tasks',
    name: 'Tasks',
    component: () => import('../views/TasksView.vue'),
    meta: { title: '任务' }
  },
  {
    path: '/profile',
    name: 'Profile',
    component: () => import('../views/ProfileView.vue'),
    meta: { title: '我的' }
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/LoginView.vue'),
    meta: { title: '登录' }
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('../views/RegisterView.vue'),
    meta: { title: '注册' }
  }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

// 路由守卫，处理页面标题和身份验证
router.beforeEach((to, from, next) => {
  // 设置页面标题
  document.title = to.meta.title ? `${to.meta.title} - Pictora` : 'Pictora'
  
  // 检查是否需要身份验证的路由
  const publicPages = ['/login', '/register']
  const authRequired = !publicPages.includes(to.path)
  const loggedIn = localStorage.getItem('token')
  
  if (authRequired && !loggedIn) {
    return next('/login')
  }
  
  next()
})

export default router