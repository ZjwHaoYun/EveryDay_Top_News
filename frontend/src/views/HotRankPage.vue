<template>
  <div class="hot-rank-page">
    <!-- 引入Header组件 -->
    <HotRankHeader 
      :current-time="currentTime"
      :is-loading="isLoading"
      @refresh="refreshHotRank"
    />

    <!-- 热榜卡片容器 -->
    <div class="card-container" v-loading="isLoading" element-loading-text="正在加载热榜...">
      <!-- 无数据提示 -->
      <div class="empty-tip" v-if="!isLoading && Object.keys(hotData).length === 0">
        <el-icon><Warning /></el-icon>
        <span>暂无热点数据，点击刷新重试</span>
      </div>

      <!-- 各平台热榜卡片 -->
      <el-card
        v-for="(platformData, platform) in hotData"
        :key="platform"
        class="hot-card"
        shadow="hover"
      >
        <!-- 卡片头部（仅保留Logo+平台名+热榜标签） -->
        <template #header>
          <div class="card-header">
            <!-- 左侧：Logo + 平台名 -->
            <div class="header-left">
              <img 
                class="platform-logo"
                :src="platformLogoMap[platform] || defaultLogo"
                :alt="platform"
                width="20"
                height="20"
              >
              <span class="platform-name">{{ platform }}</span>
            </div>
            <!-- 右侧：热榜标签 -->
            <div class="header-right">
              <span class="hot-tag">热榜</span>
            </div>
          </div>
        </template>

        <!-- 卡片主体：热榜列表 + 底部信息（更新时间+刷新按钮） -->
        <div class="card-body">
          <!-- 热榜列表 -->
          <div class="hot-list">
            <div
              v-for="(item, index) in platformData"
              :key="item.hot_url || index"
              class="hot-item"
              @click="goToHotDetail(item)"
            >
              <!-- 排名序号（顶部对齐） -->
              <span 
                class="rank-num" 
                :class="{
                  first: index === 0,
                  second: index === 1,
                  third: index === 2
                }"
              >
                {{ index + 1 }}
              </span>
              
              <!-- 标题容器（支持换行） -->
              <div class="label-container">
                <!-- 热点标题（完整显示+自动换行） -->
                <span class="hot-label">{{ item.hot_label }}</span>
              </div>
              
              <!-- 热度值（顶部对齐） -->
              <span class="hot-value" v-if="item.hot_value && item.hot_value !== '0'">
                {{ item.hot_value }}
              </span>
            </div>
          </div>

          <!-- 卡片底部：更新时间 + 刷新按钮（放到列表最下面） -->
          <div class="card-footer">
            <span class="update-time">{{ updateTimeText }}</span>
            <el-button 
              icon="Refresh" 
              text 
              size="small"
              @click="refreshSinglePlatform(platform)"
              class="card-refresh-btn"
            ></el-button>
          </div>
        </div>
      </el-card>
    </div>
  </div>
</template>

<script setup>
// （script代码与之前完全一致，无修改）
import { ref, onMounted, onUnmounted } from 'vue'
import axios from 'axios'
import { ElCard, ElIcon, ElMessage } from 'element-plus'
import { Warning } from '@element-plus/icons-vue'
import {getTopNewsList } from "@/api/news"
// 引入Header组件
import HotRankHeader from '@/components/HotRankHeader.vue'

// 响应式数据
const hotData = ref({})
const currentTime = ref('')
const isLoading = ref(false)
const updateTimeText = ref('刚刚更新')
const lastRefreshTime = ref(Date.now())

// 平台Logo映射
const platformLogoMap = ref({
  澎湃新闻: '/logo/pengpaixinwen.png',
  今日头条: '/logo/toutiao.png',
  微博: '/logo/微博.svg',
  知乎: '/logo/zhihu.png',
  抖音: '/logo/抖音.svg',
  百度: '/logo/baidu.png',
  B站: '/logo/B站.svg',
  csdn: "/logo/csdn.png",
  第一财经:"/logo/diyicaijing.png",
  白鲸出海:"/logo/baijingchuhai.png",
  掘金:"/logo/juejin.png",
  acfun:"/logo/acfun.png"
})

// 默认Logo
const defaultLogo = `<svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M12 2C6.48 2 2 6.48 2 12C2 17.52 6.48 22 12 22C17.52 22 22 17.52 22 12C22 6.48 17.52 2 12 2ZM12 20C7.59 20 4 16.41 4 12C4 7.59 7.59 4 12 4C16.41 4 20 7.59 20 12C20 16.41 16.41 20 12 20Z" fill="#666"/><path d="M14 10H10V14H14V10Z" fill="white"/></svg>`

// 时间差格式化函数
const formatTimeAgo = (targetTime) => {
  const now = Date.now()
  const diffMs = now - targetTime
  const diffSeconds = Math.floor(diffMs / 1000)

  if (diffSeconds < 60) {
    return '刚刚更新'
  } else if (diffSeconds < 3600) {
    const minutes = Math.floor(diffSeconds / 60)
    return `${minutes}分钟前更新`
  } else if (diffSeconds < 86400) {
    const hours = Math.floor(diffSeconds / 3600)
    const minutes = Math.floor((diffSeconds % 3600) / 60)
    return `${hours}小时${minutes}分钟前更新`
  } else {
    const date = new Date(targetTime)
    return `${date.getFullYear()}-${(date.getMonth()+1).toString().padStart(2, '0')}-${date.getDate().toString().padStart(2, '0')} 更新`
  }
}

// 定时器变量
let timeTimer = null
let updateTextTimer = null
let scheduleTimer = null
const REFRESH_TIMES = [[8, 0], [12, 0], [18, 0]]

// 计算下一次刷新延迟
const getNextRefreshDelay = () => {
  const now = new Date()
  const nowTime = now.getTime()
  const today = new Date(now.getFullYear(), now.getMonth(), now.getDate())
  let minDelay = Infinity

  REFRESH_TIMES.forEach(([hour, minute]) => {
    const targetTime = new Date(today)
    targetTime.setHours(hour, minute, 0, 0)
    let targetTimestamp = targetTime.getTime()
    let delay = targetTimestamp - nowTime
    if (delay < 0) {
      targetTimestamp += 86400000
      delay = targetTimestamp - nowTime
    }
    if (delay < minDelay) minDelay = delay
  })
  return minDelay
}

// 定时刷新
const scheduleDailyRefresh = async () => {
  await refreshHotRank()
  const delay = getNextRefreshDelay()
  scheduleTimer = setTimeout(() => scheduleDailyRefresh(), delay)
}

// 初始化页面
onMounted(() => {
  updateCurrentTime()
  timeTimer = setInterval(updateCurrentTime, 1000)
  refreshHotRank()
  scheduleDailyRefresh()
  updateTextTimer = setInterval(() => {
    if (lastRefreshTime.value) updateTimeText.value = formatTimeAgo(lastRefreshTime.value)
  }, 1000)
})

// 卸载清理
onUnmounted(() => {
  clearInterval(timeTimer)
  clearInterval(updateTextTimer)
  clearTimeout(scheduleTimer)
})

// 更新当前时间
const updateCurrentTime = () => {
  currentTime.value = new Date().toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
    hour12: false
  }).replace(/\//g, '-')
}

// 刷新全部热榜
const refreshHotRank = async () => {
  try {
    isLoading.value = true
    updateTimeText.value = '加载中...'
    const res = await getTopNewsList()
    hotData.value = res.data.hot_topics
    lastRefreshTime.value = Date.now()
    updateTimeText.value = formatTimeAgo(lastRefreshTime.value)
    ElMessage.success('热榜刷新成功')
  } catch (err) {
    console.error('获取热榜失败:', err)
    ElMessage.error('加载热榜失败，请稍后重试')
    updateTimeText.value = '更新失败'
  } finally {
    isLoading.value = false
  }
}

// 刷新单个平台
const refreshSinglePlatform = async (platform) => {
  ElMessage.info(`正在刷新${platform}热榜...`)
}

// 跳转详情
const goToHotDetail = (item) => {
  if (item.hot_url) window.open(item.hot_url, '_blank', 'noopener noreferrer')
  else ElMessage.warning('该热点暂无链接')
}
</script>

<style scoped>
/* 页面整体样式 */
.hot-rank-page {
  max-width: 1200px;
  margin: 24px auto;
  padding: 0 20px;
  width: 100%;
  box-sizing: border-box;
  font-family: "Microsoft YaHei", sans-serif;
}

/* 卡片容器 */
.card-container {
  display: grid;
  grid-template-columns: repeat(3, minmax(280px, 1fr));
  gap: 20px;
  max-width: 920px;
  margin: 0 auto;
}

/* 无数据提示 */
.empty-tip {
  grid-column: 1 / -1;
  text-align: center;
  padding: 60px 0;
  color: #909399;
  font-size: 16px;
  el-icon {
    font-size: 32px;
    margin-bottom: 12px;
    display: block;
    color: #c0c4cc;
  }
}

/* 热榜卡片 */
.hot-card {
  height: 100%;
  border-radius: 8px;
  --el-card-header-padding: 12px 16px;
  --el-card-body-padding: 0 16px 12px; /* 调整body内边距，底部留空间 */
}

/* 卡片头部（简化） */
.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0;
}
.header-left {
  display: flex;
  align-items: center;
}
.platform-logo {
  margin-right: 8px;
  display: flex;
  align-items: center;
}
.platform-name {
  font-size: 16px;
  font-weight: 600;
  color: #333;
}
.header-right {
  display: flex;
  align-items: center;
}
.hot-tag {
  padding: 2px 6px;
  background: #f5f7fa;
  border-radius: 4px;
  font-size: 12px;
  color: #666;
}

/* 卡片主体（包含列表+底部） */
.card-body {
  display: flex;
  flex-direction: column;
  height: 100%;
}

/* 热榜列表 */
.hot-list {
  flex: 1; /* 列表占满剩余空间 */
  margin-top: 8px;
  max-height: 280px; /* 调整高度，适配换行后的标题 */
  overflow-y: auto;
  overflow-x: hidden;
  scrollbar-width: thin;
  padding-right: 4px;
}
.hot-list::-webkit-scrollbar {
  width: 4px;
}
.hot-list::-webkit-scrollbar-thumb {
  background-color: #e5e7eb;
  border-radius: 2px;
}
.hot-list::-webkit-scrollbar-thumb:hover {
  background-color: #d1d5db;
}

/* 热榜项（核心：顶部对齐，适配换行） */
.hot-item {
  display: flex;
  align-items: flex-start; /* 改为顶部对齐，避免换行后错位 */
  justify-content: space-between;
  padding: 10px 0;
  cursor: pointer;
  transition: background-color 0.2s ease;
  border-bottom: 1px solid #f5f7fa;
  width: 100%;
  &:last-child {
    border-bottom: none;
  }
  &:hover {
    background-color: #f8f9fa;
    border-radius: 4px;
  }
}

/* 排名序号（顶部对齐+微调位置） */
.rank-num {
  display: inline-block;
  width: 24px;
  height: 24px;
  line-height: 24px;
  text-align: center;
  font-size: 14px;
  border-radius: 50%;
  margin-right: 12px;
  font-weight: 500;
  flex-shrink: 0; /* 固定宽度不挤压 */
  margin-top: 2px; /* 微调位置，和标题顶部对齐 */
}
.rank-num.first {
  background-color: #fef0f0;
  color: #f56c6c;
}
.rank-num.second {
  background-color: #fdf6ec;
  color: #e6a23c;
}
.rank-num.third {
  background-color: #f0f9eb;
  color: #87d068;
}
.rank-num {
  background-color: #f5f7fa;
  color: #666;
}

/* 标题容器（支持换行，占满剩余宽度） */
.label-container {
  flex: 1; /* 占满剩余宽度 */
  margin-right: 8px;
}

/* 热点标题（完整显示+自动换行） */
.hot-label {
  font-size: 14px;
  color: #333;
  line-height: 1.4; /* 调整行高，提升多行可读性 */
  word-wrap: break-word; /* 自动换行（中文/英文单词） */
  word-break: break-all; /* 强制换行（连续数字/字母） */
  padding: 2px 0;
}

/* 热度值（顶部对齐+微调位置） */
.hot-value {
  font-size: 12px;
  color: #909399;
  white-space: nowrap; /* 热度值仍单行 */
  flex-shrink: 0; /* 固定宽度不挤压 */
  margin-left: 8px;
  margin-top: 2px; /* 微调位置，和标题顶部对齐 */
}

/* 卡片底部（更新时间+刷新按钮） */
.card-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-top: 8px;
  padding-top: 8px;
  border-top: 1px solid #f5f7fa; /* 加分割线区分列表 */
  font-size: 12px;
}
.update-time {
  color: #909399;
}
.card-refresh-btn {
  color: #909399;
  &:hover {
    color: #666;
  }
}

/* 响应式适配 */
@media (max-width: 1000px) {
  .card-container {
    grid-template-columns: repeat(2, 1fr);
    max-width: 600px;
  }
}
@media (max-width: 600px) {
  .card-container {
    grid-template-columns: 1fr;
    max-width: 100%;
  }
  .hot-rank-page {
    padding: 0 15px;
  }
}
</style>
