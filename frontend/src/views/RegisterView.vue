<template>
  <div class="auth-container">
    <div class="auth-card">
      <div class="logo-container">
        <img src="../assets/logo.svg" alt="Pictora Logo" class="logo" />
        <h1 class="brand-name">PICTORA</h1>
      </div>
      
      <h2 class="auth-title">注册账号</h2>
      
      <van-form @submit="handleRegister">
        <van-cell-group inset>
          <van-field
            v-model="username"
            name="username"
            label="用户名"
            placeholder="请输入用户名"
            :rules="[{ required: true, message: '请输入用户名' }]"
          />
          <van-field
            v-model="email"
            name="email"
            label="邮箱"
            placeholder="请输入邮箱"
            :rules="[
              { required: true, message: '请输入邮箱' },
              { pattern: emailPattern, message: '请输入有效的邮箱地址' }
            ]"
          />
          <van-field
            v-model="password"
            type="password"
            name="password"
            label="密码"
            placeholder="请输入密码"
            :rules="[
              { required: true, message: '请输入密码' },
              { min: 6, message: '密码至少6个字符' }
            ]"
          />
          <van-field
            v-model="confirmPassword"
            type="password"
            name="confirmPassword"
            label="确认密码"
            placeholder="请再次输入密码"
            :rules="[
              { required: true, message: '请确认密码' },
              { validator: validatePasswordMatch, message: '两次密码不一致' }
            ]"
          />
        </van-cell-group>
        
        <div class="agreement">
          <van-checkbox v-model="agreement" shape="square">
            <span>我已阅读并同意</span>
            <a href="#" @click.prevent="showTerms">《用户协议》</a>
            <span>和</span>
            <a href="#" @click.prevent="showPrivacy">《隐私政策》</a>
          </van-checkbox>
        </div>
        
        <div class="form-actions">
          <van-button
            round
            block
            type="primary"
            native-type="submit"
            :loading="userStore.loading"
            :disabled="!agreement"
          >
            注册
          </van-button>
        </div>
      </van-form>
      
      <div class="auth-footer">
        <p>已有账号?</p>
        <router-link to="/login" class="login-link">立即登录</router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { showToast, showDialog } from 'vant'
import { useUserStore } from '../stores/user'

const router = useRouter()
const userStore = useUserStore()

// 表单数据
const username = ref('')
const email = ref('')
const password = ref('')
const confirmPassword = ref('')
const agreement = ref(false)
const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/

// 验证两次密码是否一致
function validatePasswordMatch() {
  return password.value === confirmPassword.value
}

// 显示用户协议
function showTerms() {
  showDialog({
    title: '用户协议',
    message: '这是Pictora的用户协议内容，包含用户使用本服务需遵守的条款和条件...',
    confirmButtonText: '我知道了'
  })
}

// 显示隐私政策
function showPrivacy() {
  showDialog({
    title: '隐私政策',
    message: '这是Pictora的隐私政策内容，详细说明了我们如何收集、使用和保护您的个人信息...',
    confirmButtonText: '我知道了'
  })
}

// 提交注册
async function handleRegister() {
  if (!agreement.value) {
    showToast('请先阅读并同意用户协议和隐私政策')
    return
  }
  
  try {
    const success = await userStore.register(username.value, password.value, email.value)
    
    if (success) {
      showToast('注册成功')
      router.replace('/login')
    } else {
      showToast('注册失败: ' + userStore.error)
    }
  } catch (error) {
    console.error('Register error:', error)
    showToast('注册失败，请重试')
  }
}
</script>

<style scoped>
.auth-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  padding: 20px;
  background-color: var(--background-color);
}

.auth-card {
  width: 100%;
  max-width: 400px;
  background-color: white;
  border-radius: 16px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
  padding: 32px 24px;
}

.logo-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 24px;
}

.logo {
  width: 80px;
  height: 80px;
  margin-bottom: 12px;
}

.brand-name {
  font-size: 24px;
  font-weight: 700;
  color: var(--primary-color);
  letter-spacing: 1px;
}

.auth-title {
  font-size: 20px;
  font-weight: 600;
  color: var(--text-color);
  text-align: center;
  margin-bottom: 24px;
}

.agreement {
  margin: 16px 0;
  padding: 0 16px;
}

.agreement a {
  color: var(--primary-color);
  text-decoration: none;
}

.form-actions {
  margin-top: 24px;
  margin-bottom: 24px;
}

.auth-footer {
  text-align: center;
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 8px;
  color: var(--light-text);
}

.login-link {
  color: var(--primary-color);
  text-decoration: none;
  font-weight: 600;
}
</style> 