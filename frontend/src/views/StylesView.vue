<template>
  <div class="page-container">
    <van-nav-bar
      title="风格效果"
      left-arrow
      @click-left="$router.go(-1)"
    />
    
    <!-- 筛选条件 -->
    <div class="filter-container">
      <van-tabs v-model:active="activeTab" sticky animated swipeable>
        <van-tab title="推荐">
          <div class="tab-content">
            <style-grid :styles="filteredStyles" @select="selectStyle" />
          </div>
        </van-tab>
        <van-tab title="热门">
          <div class="tab-content">
            <style-grid :styles="filteredStyles" @select="selectStyle" />
          </div>
        </van-tab>
        <van-tab title="最近使用">
          <div class="tab-content">
            <style-grid :styles="filteredStyles" @select="selectStyle" />
          </div>
        </van-tab>
        <van-tab title="全部">
          <div class="tab-content">
            <van-dropdown-menu>
              <van-dropdown-item v-model="categoryFilter" :options="categoryOptions" />
            </van-dropdown-menu>
            <style-grid :styles="filteredStyles" @select="selectStyle" />
          </div>
        </van-tab>
      </van-tabs>
    </div>
    
    <!-- 底部按钮 -->
    <div class="footer-actions" v-if="selectedStyleId">
      <van-button type="primary" block round @click="confirmSelection">
        确认选择
      </van-button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { showToast, showLoadingToast, closeToast } from 'vant'
import api from '../services/api'

// 自定义组件
const StyleGrid = defineComponent({
  name: 'StyleGrid',
  props: {
    styles: {
      type: Array,
      required: true
    }
  },
  setup(props, { emit }) {
    const selectedId = ref(null)
    
    const selectStyle = (styleId) => {
      selectedId.value = styleId
      emit('select', styleId)
    }
    
    return {
      selectedId,
      selectStyle
    }
  },
  template: `
    <div class="styles-grid">
      <div 
        v-for="style in styles" 
        :key="style.id" 
        class="style-item"
        :class="{ active: selectedId === style.id }"
        @click="selectStyle(style.id)"
      >
        <img :src="style.thumbnail" alt="风格示例" class="style-thumbnail" />
        <div class="style-info">
          <span class="style-name">{{ style.name }}</span>
          <span class="style-usage" v-if="style.usage_count">已被使用 {{ style.usage_count }} 次</span>
        </div>
      </div>
      <div v-if="styles.length === 0" class="empty-state">
        <van-empty description="暂无风格效果" />
      </div>
    </div>
  `
})

// 主组件逻辑
const router = useRouter()

// 状态变量
const styles = ref([])
const activeTab = ref(0)
const categoryFilter = ref('all')
const categoryOptions = ref([
  { text: '全部分类', value: 'all' },
  { text: '写实风格', value: 'realistic' },
  { text: '卡通风格', value: 'cartoon' },
  { text: '艺术风格', value: 'artistic' },
  { text: '像素风格', value: 'pixel' },
])
const selectedStyleId = ref(null)

// 计算属性
const filteredStyles = computed(() => {
  let result = [...styles.value]
  
  // 根据tab筛选
  switch (activeTab.value) {
    case 0: // 推荐
      result = result.filter(s => s.is_recommended)
      break
    case 1: // 热门
      result = result.sort((a, b) => b.usage_count - a.usage_count)
      break
    case 2: // 最近使用
      result = result.filter(s => s.recently_used)
      break
    case 3: // 全部 (含分类筛选)
      if (categoryFilter.value !== 'all') {
        result = result.filter(s => s.category === categoryFilter.value)
      }
      break
  }
  
  return result
})

// 方法
async function fetchStyles() {
  const loading = showLoadingToast({
    message: '加载中...',
    forbidClick: true,
  })
  
  try {
    const response = await api.getStyles()
    styles.value = response
  } catch (error) {
    console.error('Failed to load styles:', error)
    showToast('加载风格失败')
  } finally {
    closeToast()
  }
}

function selectStyle(styleId) {
  selectedStyleId.value = styleId
}

function confirmSelection() {
  if (!selectedStyleId.value) {
    showToast('请选择风格')
    return
  }
  
  // 将选择的风格ID传回到上一页
  router.push({
    path: '/generate',
    query: { styleId: selectedStyleId.value }
  })
}

// 生命周期钩子
onMounted(() => {
  fetchStyles()
  
  // 从URL参数获取预选风格
  const query = router.currentRoute.value.query
  if (query.styleId) {
    selectedStyleId.value = query.styleId
  }
})

// 监听数据变化
watch(() => activeTab.value, () => {
  // 当切换tab时重置分类筛选
  if (activeTab.value !== 3) {
    categoryFilter.value = 'all'
  }
})
</script>

<style scoped>
.filter-container {
  margin-bottom: 16px;
}

.tab-content {
  padding: 16px 0;
}

.styles-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
  padding: 0 16px;
}

.style-item {
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: all 0.2s;
  cursor: pointer;
}

.style-item.active {
  box-shadow: 0 0 0 2px var(--primary-color);
}

.style-thumbnail {
  width: 100%;
  aspect-ratio: 3/4;
  object-fit: cover;
}

.style-info {
  padding: 8px 12px;
}

.style-name {
  font-weight: 600;
  display: block;
  margin-bottom: 4px;
}

.style-usage {
  font-size: 12px;
  color: var(--light-text);
}

.footer-actions {
  position: sticky;
  bottom: 0;
  padding: 16px;
  background-color: #fff;
  box-shadow: 0 -2px 10px rgba(0, 0, 0, 0.05);
}

.empty-state {
  grid-column: span 2;
  padding: 32px 0;
}
</style>

<script>
import { defineComponent } from 'vue'
</script> 