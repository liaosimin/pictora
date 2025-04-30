import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api from '../services/api'

export const useUserStore = defineStore('user', () => {
  // 状态
  const user = ref(null)
  const token = ref(localStorage.getItem('token') || '')
  const loading = ref(false)
  const error = ref(null)
  
  // 计算属性
  const isLoggedIn = computed(() => !!token.value)
  const isVip = computed(() => user.value?.is_vip || false)
  const credits = computed(() => user.value?.credits || 0)
  
  // 动作
  async function login(username, password) {
    loading.value = true
    error.value = null
    
    try {
      const response = await api.login(username, password)
      token.value = response.access_token
      localStorage.setItem('token', response.access_token)
      await fetchUserProfile()
      return true
    } catch (err) {
      error.value = err.response?.data?.detail || '登录失败'
      return false
    } finally {
      loading.value = false
    }
  }
  
  async function register(username, password, email) {
    loading.value = true
    error.value = null
    
    try {
      await api.register(username, password, email)
      return true
    } catch (err) {
      error.value = err.response?.data?.detail || '注册失败'
      return false
    } finally {
      loading.value = false
    }
  }
  
  async function fetchUserProfile() {
    if (!token.value) return
    
    loading.value = true
    error.value = null
    
    try {
      user.value = await api.getUserProfile()
    } catch (err) {
      error.value = err.response?.data?.detail || '获取用户信息失败'
      logout()
    } finally {
      loading.value = false
    }
  }
  
  async function subscribeVip() {
    loading.value = true
    error.value = null
    
    try {
      const response = await api.subscribeVip()
      await fetchUserProfile()
      return response
    } catch (err) {
      error.value = err.response?.data?.detail || 'VIP订阅失败'
      return false
    } finally {
      loading.value = false
    }
  }
  
  function logout() {
    user.value = null
    token.value = ''
    localStorage.removeItem('token')
  }
  
  return {
    user,
    token,
    loading,
    error,
    isLoggedIn,
    isVip,
    credits,
    login,
    register,
    fetchUserProfile,
    subscribeVip,
    logout
  }
})