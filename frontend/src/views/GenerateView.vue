<template>
  <div class="page-container">
    <div class="page-title">AI图片生成</div>
    
    <!-- 图片上传区域 -->
    <div class="card">
      <div class="upload-area" @click="triggerFileInput" v-if="!selectedImage">
        <van-icon name="photograph" size="48" />
        <p>点击上传图片</p>
      </div>
      <div class="preview-container" v-else>
        <img :src="selectedImage" class="preview-image" />
        <van-button type="danger" icon="delete" size="small" @click="removeImage" class="remove-btn">
          更换图片
        </van-button>
      </div>
      <input type="file" ref="fileInput" accept="image/*" @change="handleFileChange" hidden />
    </div>
    
    <!-- 风格效果选择 -->
    <div class="card">
      <div class="section-header">
        <span class="section-title">选择风格效果</span>
        <van-button type="primary" size="small" plain to="/styles">更多</van-button>
      </div>
      
      <div class="styles-container">
        <div 
          v-for="style in popularStyles" 
          :key="style.id" 
          class="style-item"
          :class="{ active: selectedStyle === style.id }"
          @click="selectStyle(style.id)"
        >
          <img :src="style.thumbnail" alt="风格示例" class="style-thumbnail" />
          <span class="style-name">{{ style.name }}</span>
        </div>
      </div>
    </div>
    
    <!-- 自定义提示词输入 -->
    <div class="card">
      <div class="section-header">
        <span class="section-title">自定义提示词 (可选)</span>
      </div>
      <van-field
        v-model="customPrompt"
        type="textarea"
        placeholder="输入提示词以进一步定制您的图片效果"
        rows="2"
        maxlength="100"
        show-word-limit
      />
    </div>
    
    <!-- 生成按钮 -->
    <div class="generate-btn-container">
      <van-button 
        type="primary" 
        block 
        round 
        size="large" 
        :loading="isGenerating"
        :disabled="!canGenerate"
        @click="generateImage"
      >
        {{ generateBtnText }}
      </van-button>
      
      <div class="credits-info" v-if="userStore.isLoggedIn">
        剩余积分: {{ userStore.credits }}
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { showToast, showDialog } from 'vant'
import { useUserStore } from '../stores/user'
import api from '../services/api'

const router = useRouter()
const userStore = useUserStore()

// 状态变量
const fileInput = ref(null)
const selectedImage = ref(null)
const selectedImageFile = ref(null)
const selectedStyle = ref(null)
const customPrompt = ref('')
const popularStyles = ref([])
const isGenerating = ref(false)

// 计算属性
const canGenerate = computed(() => 
  selectedImage.value && 
  selectedStyle.value && 
  userStore.credits > 0
)

const generateBtnText = computed(() => {
  if (!selectedImage.value) return '请上传图片'
  if (!selectedStyle.value) return '请选择风格'
  if (userStore.credits <= 0) return '积分不足'
  return '生成图片'
})

// 方法
function triggerFileInput() {
  fileInput.value.click()
}

function handleFileChange(event) {
  const file = event.target.files[0]
  if (!file) return
  
  // 检查文件类型
  if (!file.type.includes('image/')) {
    showToast('请上传图片文件')
    return
  }
  
  // 检查文件大小 (限制为5MB)
  if (file.size > 5 * 1024 * 1024) {
    showToast('图片大小不能超过5MB')
    return
  }
  
  selectedImageFile.value = file
  const reader = new FileReader()
  reader.onload = e => {
    selectedImage.value = e.target.result
  }
  reader.readAsDataURL(file)
}

function removeImage() {
  selectedImage.value = null
  selectedImageFile.value = null
  if (fileInput.value) {
    fileInput.value.value = ''
  }
}

function selectStyle(styleId) {
  selectedStyle.value = styleId
}

async function loadPopularStyles() {
  try {
    const styles = await api.getStyles({ popular: true, limit: 6 })
    popularStyles.value = styles
    
    // 如果有风格，默认选中第一个
    if (styles.length > 0) {
      selectedStyle.value = styles[0].id
    }
  } catch (error) {
    console.error('Failed to load styles:', error)
    showToast('加载风格失败')
  }
}

async function generateImage() {
  if (!canGenerate.value) return
  
  if (!userStore.isLoggedIn) {
    showDialog({
      title: '请先登录',
      message: '您需要登录才能生成图片',
      confirmButtonText: '去登录',
      cancelButtonText: '取消',
      showCancelButton: true,
    }).then(() => {
      router.push('/login')
    })
    return
  }
  
  if (userStore.credits <= 0) {
    showDialog({
      title: '积分不足',
      message: '您的积分不足，无法生成图片，请前往个人中心获取更多积分',
      confirmButtonText: '去充值',
      cancelButtonText: '取消',
      showCancelButton: true,
    }).then(() => {
      router.push('/profile')
    })
    return
  }
  
  try {
    isGenerating.value = true
    const task = await api.createTask(
      selectedStyle.value,
      customPrompt.value,
      selectedImageFile.value
    )
    
    showToast('任务已提交')
    router.push('/tasks')
  } catch (error) {
    console.error('生成失败:', error)
    showToast('任务提交失败，请重试')
  } finally {
    isGenerating.value = false
  }
}

// 生命周期钩子
onMounted(() => {
  loadPopularStyles()
})
</script>

<style scoped>
.upload-area {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  border: 2px dashed var(--border-color);
  border-radius: 12px;
  padding: 32px;
  cursor: pointer;
  transition: all 0.3s;
}

.upload-area:hover {
  border-color: var(--primary-color);
  background-color: rgba(115, 103, 240, 0.05);
}

.upload-area p {
  margin-top: 12px;
  color: var(--light-text);
}

.preview-container {
  position: relative;
  text-align: center;
}

.preview-image {
  max-width: 100%;
  max-height: 300px;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.remove-btn {
  position: absolute;
  top: 8px;
  right: 8px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.section-title {
  font-weight: 600;
  font-size: 16px;
}

.styles-container {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px;
  margin-bottom: 8px;
}

.style-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  cursor: pointer;
  padding: 8px;
  border-radius: 8px;
  transition: all 0.2s;
}

.style-item.active {
  background-color: rgba(115, 103, 240, 0.1);
  border: 1px solid var(--primary-color);
}

.style-thumbnail {
  width: 100%;
  aspect-ratio: 1;
  object-fit: cover;
  border-radius: 8px;
  margin-bottom: 4px;
}

.style-name {
  font-size: 12px;
  text-align: center;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  width: 100%;
}

.generate-btn-container {
  margin-top: 24px;
  margin-bottom: 16px;
}

.credits-info {
  text-align: center;
  margin-top: 12px;
  color: var(--light-text);
  font-size: 14px;
}
</style> 