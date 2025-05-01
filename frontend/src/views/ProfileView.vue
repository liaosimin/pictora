<template>
  <div class="page-container">
    <div class="page-title">个人中心</div>
    
    <!-- 用户信息卡片 -->
    <div class="card user-card">
      <div class="user-info">
        <van-image
          class="avatar"
          round
          width="80"
          height="80"
          :src="userStore.user?.avatar || defaultAvatar"
        />
        <div class="user-details">
          <h2 class="username">{{ userStore.user?.username || '加载中...' }}</h2>
          <div class="user-status">
            <van-tag type="primary" v-if="userStore.isVip">VIP会员</van-tag>
            <van-tag type="warning" v-else>免费用户</van-tag>
          </div>
        </div>
      </div>
    </div>
    
    <!-- 积分信息 -->
    <div class="card credits-card">
      <div class="credits-info">
        <div class="credits-header">
          <span class="section-title">积分余额</span>
          <van-button size="small" plain type="primary" @click="showCreditsInfo">
            积分说明
          </van-button>
        </div>
        
        <div class="credits-display">
          <span class="credits-value">{{ userStore.credits }}</span>
          <span class="credits-label">可用积分</span>
        </div>
        
        <div class="credits-progress" v-if="!userStore.isVip">
          <van-progress
            :percentage="Math.min(100, (userStore.credits / 100) * 100)"
            :show-pivot="false"
            color="#7367f0"
          />
          <div class="credits-usage">
            <span>剩余可用</span>
            <span>{{ userStore.credits }}/100</span>
          </div>
        </div>
      </div>
    </div>
    
    <!-- VIP会员卡片 -->
    <div class="card vip-card" :class="{ 'is-vip': userStore.isVip }">
      <div class="vip-header">
        <div class="vip-title">
          <van-icon name="gem-o" size="20" />
          <span>VIP会员</span>
        </div>
        <div class="vip-status">
          {{ userStore.isVip ? '已开通' : '未开通' }}
        </div>
      </div>
      
      <div class="vip-content">
        <div class="vip-benefits">
          <div class="benefit-item">
            <van-icon name="gold-coin-o" />
            <span>每月赠送 500 积分</span>
          </div>
          <div class="benefit-item">
            <van-icon name="fire-o" />
            <span>优先处理生成任务</span>
          </div>
          <div class="benefit-item">
            <van-icon name="new-o" />
            <span>抢先体验新功能</span>
          </div>
        </div>
        
        <van-button 
          type="primary" 
          block 
          class="vip-button"
          :loading="subscribing"
          @click="handleVipAction"
        >
          {{ userStore.isVip ? '续费会员' : '立即开通' }}
        </van-button>
      </div>
    </div>
    
    <!-- 设置列表 -->
    <div class="card">
      <van-cell-group inset>
        <van-cell title="账号与安全" is-link to="/account-security" />
        <van-cell title="消息通知" is-link to="/notifications" />
        <van-cell title="关于我们" is-link to="/about" />
        <van-cell title="帮助中心" is-link to="/help" />
      </van-cell-group>
    </div>
    
    <!-- 退出登录按钮 -->
    <div class="logout-container">
      <van-button 
        type="danger" 
        block 
        plain
        @click="confirmLogout"
      >
        退出登录
      </van-button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { showToast, showDialog } from 'vant'
import { useUserStore } from '../stores/user'

const router = useRouter()
const userStore = useUserStore()
const subscribing = ref(false)
const defaultAvatar = 'https://fastly.jsdelivr.net/npm/@vant/assets/cat.jpeg' // 默认头像

// 方法
function showCreditsInfo() {
  showDialog({
    title: '积分说明',
    message: `
      积分是生成AI图片的必要条件，每生成一张图片将消耗1积分。
      
      免费用户初始赠送10积分，每日可领取1积分。
      
      VIP会员每月自动发放500积分，积分不清零。
    `,
    confirmButtonText: '我知道了'
  })
}

async function handleVipAction() {
  if (subscribing.value) return
  
  try {
    subscribing.value = true
    
    if (!userStore.isVip) {
      // 模拟支付流程
      const confirmed = await showDialog({
        title: 'VIP会员订阅',
        message: '开通VIP会员，每月仅需￥30元，享受更多优质服务',
        showCancelButton: true,
        confirmButtonText: '确认支付',
        cancelButtonText: '取消'
      })
      
      if (confirmed) {
        await userStore.subscribeVip()
        showToast('恭喜您，已成功开通VIP会员')
      }
    } else {
      // 续费逻辑
      const confirmed = await showDialog({
        title: 'VIP会员续费',
        message: '续费VIP会员，继续享受会员权益',
        showCancelButton: true,
        confirmButtonText: '确认续费',
        cancelButtonText: '取消'
      })
      
      if (confirmed) {
        await userStore.subscribeVip()
        showToast('续费成功，感谢您的支持')
      }
    }
  } catch (error) {
    console.error('VIP订阅失败:', error)
    showToast('操作失败，请重试')
  } finally {
    subscribing.value = false
  }
}

function confirmLogout() {
  showDialog({
    title: '确认退出',
    message: '确定要退出登录吗？',
    showCancelButton: true,
    confirmButtonText: '确认',
    cancelButtonText: '取消'
  }).then(() => {
    userStore.logout()
    router.push('/login')
  })
}
</script>

<style scoped>
.user-card {
  margin-bottom: 20px;
}

.user-info {
  display: flex;
  align-items: center;
}

.avatar {
  border: 3px solid #fff;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.user-details {
  margin-left: 20px;
}

.username {
  margin: 0 0 8px 0;
  font-size: 20px;
}

.credits-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.credits-display {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 16px;
}

.credits-value {
  font-size: 36px;
  font-weight: bold;
  color: var(--primary-color);
}

.credits-label {
  font-size: 14px;
  color: var(--light-text);
  margin-top: 4px;
}

.credits-usage {
  display: flex;
  justify-content: space-between;
  font-size: 12px;
  color: var(--light-text);
  margin-top: 4px;
}

.vip-card {
  background-color: #f8f8f8;
  border: 1px solid var(--border-color);
  margin-bottom: 20px;
}

.vip-card.is-vip {
  background: linear-gradient(135deg, #7367f0 0%, #9e95f5 100%);
  color: white;
}

.vip-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.vip-title {
  display: flex;
  align-items: center;
  font-weight: 600;
  font-size: 18px;
}

.vip-title .van-icon {
  margin-right: 8px;
}

.vip-content {
  margin-top: 16px;
}

.vip-benefits {
  margin-bottom: 20px;
}

.benefit-item {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
}

.benefit-item .van-icon {
  margin-right: 8px;
}

.vip-button {
  background-color: var(--primary-color);
  border: none;
}

.is-vip .vip-button {
  background-color: white !important;
  color: var(--primary-color) !important;
}

.logout-container {
  margin-top: 32px;
  margin-bottom: 16px;
}
</style> 