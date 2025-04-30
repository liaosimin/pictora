import axios from 'axios'

const API_URL = 'http://localhost:8000'

// 创建axios实例
const apiClient = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 请求拦截器，添加认证令牌
apiClient.interceptors.request.use(config => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// API服务
const api = {
  // 用户认证
  login: async (username, password) => {
    const response = await apiClient.post('/users/login', { username, password })
    return response.data
  },
  
  register: async (username, password, email) => {
    const response = await apiClient.post('/users/register', { username, password, email })
    return response.data
  },
  
  getUserProfile: async () => {
    const response = await apiClient.get('/users/me')
    return response.data
  },
  
  // 风格效果
  getStyles: async (params = {}) => {
    const response = await apiClient.get('/styles', { params })
    return response.data
  },
  
  // 任务管理
  createTask: async (styleId, customPrompt, file) => {
    const formData = new FormData()
    formData.append('file', file)
    formData.append('style_id', styleId)
    if (customPrompt) {
      formData.append('custom_prompt', customPrompt)
    }
    
    const response = await apiClient.post('/tasks', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
    return response.data
  },
  
  getTasks: async (status) => {
    const params = status ? { status } : {}
    const response = await apiClient.get('/tasks', { params })
    return response.data
  },
  
  getTask: async (taskId) => {
    const response = await apiClient.get(`/tasks/${taskId}`)
    return response.data
  },
  
  retryTask: async (taskId) => {
    const response = await apiClient.post(`/tasks/${taskId}/retry`)
    return response.data
  },
  
  // VIP订阅
  subscribeVip: async () => {
    const response = await apiClient.post('/vip/subscribe')
    return response.data
  }
}

export default api