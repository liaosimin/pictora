# Pictora Frontend

Pictora是一个基于AI的图片生成应用，允许用户上传图片并应用各种风格效果来创建新的图像。

## 技术栈

- Vue 3 (组合式API + script setup)
- Vite
- Vue Router
- Pinia (状态管理)
- Vant UI (移动端组件库)
- Axios (HTTP请求)

## 项目设置

### 安装依赖

```bash
npm install
```

### 启动开发服务器

```bash
npm run dev
```

### 构建生产版本

```bash
npm run build
```

### 预览生产构建

```bash
npm run preview
```

## 项目结构

- `src/assets`: 静态资源文件
- `src/components`: 可复用组件
- `src/router`: 路由配置
- `src/services`: API服务
- `src/stores`: Pinia状态仓库
- `src/views`: 页面视图组件
- `src/App.vue`: 根组件
- `src/main.js`: 应用入口

## 需要优先完成的功能

1. 完善登录和注册功能
2. 实现图片上传和风格选择
3. 增加任务管理，包括状态跟踪、预览和下载
4. 优化VIP系统和积分管理

## 后端API

后端API运行在 `http://localhost:8000`，包含以下主要功能：

- 用户认证和管理
- 风格效果管理
- 图片生成任务处理
- VIP和积分系统
