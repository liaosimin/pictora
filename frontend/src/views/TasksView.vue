<template>
  <div class="page-container">
    <div class="page-title">任务管理</div>
    
    <!-- 任务状态Tab -->
    <van-tabs v-model:active="activeTab" sticky animated>
      <van-tab title="进行中">
        <task-list :tasks="processingTasks" @retry="retryTask" />
      </van-tab>
      <van-tab title="已完成">
        <task-list :tasks="completedTasks" @preview="previewImage" @download="downloadImage" />
      </van-tab>
      <van-tab title="失败">
        <task-list :tasks="failedTasks" @retry="retryTask" />
      </van-tab>
    </van-tabs>
    
    <!-- 图片预览弹窗 -->
    <van-image-preview
      v-model:show="previewVisible"
      :images="[currentPreviewUrl]"
      :close-on-popstate="true"
      :show-index="false"
      @close="closePreview"
    >
      <template #cover>
        <div class="preview-action-bar">
          <van-button type="primary" icon="down" @click="downloadImage(currentPreviewTask)">
            下载图片
          </van-button>
        </div>
      </template>
    </van-image-preview>
  </div>
</template>

<script setup>
import { defineComponent, ref, computed, onMounted } from 'vue'
import { showToast, showLoadingToast, closeToast } from 'vant'
import api from '../services/api'

// 任务列表组件
const TaskList = defineComponent({
  name: 'TaskList',
  props: {
    tasks: {
      type: Array,
      required: true
    }
  },
  setup(props, { emit }) {
    const formatDate = (dateString) => {
      const date = new Date(dateString)
      return new Intl.DateTimeFormat('zh-CN', {
        month: 'short',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit'
      }).format(date)
    }
    
    const retryTask = (task) => {
      emit('retry', task)
    }
    
    const previewImage = (task) => {
      emit('preview', task)
    }
    
    const downloadImage = (task) => {
      emit('download', task)
    }
    
    return {
      formatDate,
      retryTask,
      previewImage,
      downloadImage
    }
  },
  template: `
    <div class="task-list">
      <template v-if="tasks.length > 0">
        <div v-for="task in tasks" :key="task.id" class="task-item">
          <div class="task-left">
            <img :src="task.input_image_url" class="task-thumbnail" />
          </div>
          <div class="task-content">
            <div class="task-header">
              <div class="task-title">任务 #{{ task.id.substring(0, 6) }}</div>
              <div class="task-time">{{ formatDate(task.created_at) }}</div>
            </div>
            
            <template v-if="task.status === 'processing'">
              <van-progress 
                :percentage="task.progress || 0" 
                :show-pivot="true" 
                color="#7367f0"
              />
            </template>
            
            <template v-else-if="task.status === 'completed'">
              <div class="task-result">
                <img v-if="task.output_image_url" :src="task.output_image_url" class="result-thumbnail" />
              </div>
              <div class="task-actions">
                <van-button 
                  type="primary" 
                  size="small" 
                  plain 
                  @click="previewImage(task)"
                >
                  预览
                </van-button>
                <van-button 
                  type="primary" 
                  size="small" 
                  @click="downloadImage(task)"
                >
                  下载
                </van-button>
              </div>
            </template>
            
            <template v-else-if="task.status === 'failed'">
              <div class="task-error">
                <van-icon name="warning-o" color="#ea5455" />
                <span>{{ task.error_message || '生成失败' }}</span>
              </div>
              <div class="task-actions">
                <van-button 
                  type="danger" 
                  size="small" 
                  plain 
                  @click="retryTask(task)"
                >
                  重试
                </van-button>
              </div>
            </template>
          </div>
        </div>
      </template>
      
      <template v-else>
        <van-empty description="暂无任务" />
      </template>
    </div>
  `
})

// 主组件逻辑
const activeTab = ref(0)
const tasks = ref([])
const previewVisible = ref(false)
const currentPreviewTask = ref(null)
const currentPreviewUrl = ref('')
const refreshInterval = ref(null)

// 计算属性
const processingTasks = computed(() => 
  tasks.value.filter(task => task.status === 'processing')
)

const completedTasks = computed(() => 
  tasks.value.filter(task => task.status === 'completed')
)

const failedTasks = computed(() => 
  tasks.value.filter(task => task.status === 'failed')
)

// 方法
async function fetchTasks() {
  try {
    const response = await api.getTasks()
    tasks.value = response
  } catch (error) {
    console.error('Failed to load tasks:', error)
    showToast('加载任务失败')
  }
}

async function retryTask(task) {
  const loading = showLoadingToast({
    message: '正在重试...',
    forbidClick: true,
  })
  
  try {
    await api.retryTask(task.id)
    await fetchTasks()
    showToast('重试成功')
  } catch (error) {
    console.error('Failed to retry task:', error)
    showToast('重试失败')
  } finally {
    closeToast()
  }
}

function previewImage(task) {
  currentPreviewTask.value = task
  currentPreviewUrl.value = task.output_image_url
  previewVisible.value = true
}

function closePreview() {
  previewVisible.value = false
  currentPreviewTask.value = null
  currentPreviewUrl.value = ''
}

async function downloadImage(task) {
  if (!task || !task.output_image_url) {
    showToast('图片不可用')
    return
  }
  
  try {
    const a = document.createElement('a')
    a.href = task.output_image_url
    a.download = `pictora-${task.id}.png`
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
  } catch (error) {
    console.error('Failed to download image:', error)
    showToast('下载失败，请重试')
  }
}

function setupRefreshInterval() {
  // 如果有处理中的任务，每5秒刷新一次
  if (processingTasks.value.length > 0) {
    if (!refreshInterval.value) {
      refreshInterval.value = setInterval(fetchTasks, 5000)
    }
  } else {
    clearRefreshInterval()
  }
}

function clearRefreshInterval() {
  if (refreshInterval.value) {
    clearInterval(refreshInterval.value)
    refreshInterval.value = null
  }
}

// 生命周期钩子
onMounted(async () => {
  await fetchTasks()
  setupRefreshInterval()
})

// 监听数据变化
watch(() => processingTasks.value.length, (newVal, oldVal) => {
  if (newVal !== oldVal) {
    setupRefreshInterval()
  }
})

onBeforeUnmount(() => {
  clearRefreshInterval()
})
</script>

<style scoped>
.task-list {
  padding: 16px;
}

.task-item {
  display: flex;
  background-color: #fff;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  margin-bottom: 16px;
  overflow: hidden;
}

.task-left {
  width: 80px;
  flex-shrink: 0;
}

.task-thumbnail {
  width: 80px;
  height: 80px;
  object-fit: cover;
}

.task-content {
  flex: 1;
  padding: 12px;
  display: flex;
  flex-direction: column;
}

.task-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 8px;
}

.task-title {
  font-weight: 600;
}

.task-time {
  font-size: 12px;
  color: var(--light-text);
}

.task-result {
  margin: 8px 0;
  display: flex;
  justify-content: center;
}

.result-thumbnail {
  height: 120px;
  max-width: 100%;
  object-fit: contain;
  border-radius: 8px;
}

.task-actions {
  display: flex;
  justify-content: flex-end;
  gap: 8px;
  margin-top: 8px;
}

.task-error {
  display: flex;
  align-items: center;
  gap: 8px;
  color: var(--danger-color);
  margin: 8px 0;
}

.preview-action-bar {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  display: flex;
  justify-content: center;
  padding: 16px;
  background: rgba(0, 0, 0, 0.5);
}
</style>

<script>
import { defineComponent, watch, onBeforeUnmount } from 'vue'
</script> 