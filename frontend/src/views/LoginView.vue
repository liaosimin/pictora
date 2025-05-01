<template>
  <div class="auth-container">
    <div class="auth-card">
      <div class="logo-container">
        <img src="../assets/logo.png" alt="Pictora Logo" class="logo" />
        <h1 class="brand-name">PICTORA</h1>
      </div>
      
      <h2 class="auth-title">登录账号</h2>
      
      <van-form @submit="handleLogin">
        <van-cell-group inset>
          <van-field
            v-model="username"
            name="username"
            label="用户名"
            placeholder="请输入用户名"
            :rules="[{ required: true, message: '请输入用户名' }]"
          />
          <van-field
            v-model="password"
            type="password"
            name="password"
            label="密码"
            placeholder="请输入密码"
            :rules="[{ required: true, message: '请输入密码' }]"
          />
        </van-cell-group>
        
        <div class="forgot-password">
          <router-link to="/forget-password">忘记密码?</router-link>
        </div>
        
        <div class="form-actions">
          <van-button
            round
            block
            type="primary"
            native-type="submit"
            :loading="userStore.loading"
          >
            登录
          </van-button>
        </div>
      </van-form>
      
      <div class="auth-footer">
        <p>还没有账号?</p>
        <router-link to="/register" class="register-link">立即注册</router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { showToast } from 'vant'
import { useUserStore } from '../stores/user'

const router = useRouter()
const userStore = useUserStore()

// 表单数据
const username = ref('')
const password = ref('')

// 提交登录
async function handleLogin() {
  try {
    const success = await userStore.login(username.value, password.value)
    
    if (success) {
      showToast('登录成功')
      router.replace('/generate')
    } else {
      showToast('登录失败: ' + userStore.error)
    }
  } catch (error) {
    console.error('Login error:', error)
    showToast('登录失败，请重试')
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

.forgot-password {
  text-align: right;
  margin: 12px 0;
  font-size: 14px;
}

.forgot-password a {
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

.register-link {
  color: var(--primary-color);
  text-decoration: none;
  font-weight: 600;
}
</style> 