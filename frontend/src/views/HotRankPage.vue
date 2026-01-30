<template>
  <div class="hot-rank-page">
    <HotRankHeader 
      :current-time="currentTime"
      :lunar-date="lunarDate" 
      :is-loading="isLoading"
      @refresh="refreshHotRank"
    />

    <div class="card-container" v-loading="isLoading" element-loading-text="正在加载热榜...">
      <div class="empty-tip" v-if="!isLoading && Object.keys(hotData).length === 0">
        <el-icon><Warning /></el-icon>
        <span>暂无热点数据，点击刷新重试</span>
      </div>

      <el-card
        v-for="(platformData, platform) in hotData"
        :key="platform"
        class="hot-card"
        shadow="hover"
        :body-style="{ padding: '0' }"
      >
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
            <!-- 右侧：热榜标签（匹配参考图样式） -->
            <div class="hot-tag-wrapper">
              <span 
                class="hot-tag"
                :class="tagClassMap[platformHotTagMap[platform] || '热榜']"
              >
                {{ platformHotTagMap[platform] || '热榜' }}
              </span>
            </div>
          </div>
        </template>

        <div class="card-body">
          <div class="hot-list">
            <div
              v-for="(item, index) in platformData"
              :key="item.hot_url || index"
              class="hot-item"
              @click="goToHotDetail(item)"
            >
              <!-- 排名序号 -->
              <span 
                class="rank-num"
                :class="{
                  'rank-1': index === 0,
                  'rank-2': index === 1,
                  'rank-3': index === 2,
                  'rank-other': index >= 3
                }"
              >{{ index + 1 }}</span>

              <div class="label-container">
                <span 
                  class="hot-item-tag"
                  :class="itemTagClassMap[item.hot_tag]"
                  v-if="item.hot_tag"
                >{{ item.hot_tag }}</span>
                <span class="hot-label">{{ item.hot_label }}</span>
              </div>

              <span class="hot-value" v-if="item.hot_value && item.hot_value !== '0'">{{ item.hot_value }}</span>
            </div>
          </div>
          <!-- 卡片底部更新信息 + 刷新图标 -->
          <div class="card-footer" :class="{ 'footer-loading': platformLoading[platform] }">
            <span class="update-time">{{ formatTimeAgo(platformUpdateTime[platform]) }}</span>
            <el-icon 
              class="refresh-icon" 
              @click.stop="refreshSinglePlatform(platform)"
              :loading="platformLoading[platform]"
            >
              <Refresh />
            </el-icon>
          </div>
        </div>
      </el-card>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { ElCard, ElIcon, ElMessage } from 'element-plus'
import { Warning, Refresh } from '@element-plus/icons-vue'
import { getTopNewsList } from "@/api/news"
import HotRankHeader from '@/components/HotRankHeader.vue'
import { Lunar, Solar } from 'lunar-javascript'

// 响应式数据
const hotData = ref({})
const currentTime = ref('')
const isLoading = ref(false)
const lunarDate = ref('')
const lastRefreshTime = ref(Date.now())
// 各平台单独刷新时间 + 单独加载状态
const platformUpdateTime = ref({})
const platformLoading = ref({})

// 平台Logo映射
const platformLogoMap = ref({
  微博: '/logo/微博.svg',
  小红书: '/logo/xiaohongshu.png',
  B站: '/logo/B站.svg',
  抖音: '/logo/抖音.svg',
  澎湃新闻: '/logo/pengpaixinwen.png',
  今日头条: '/logo/toutiao.png',
  知乎: '/logo/zhihu.png',
  百度: '/logo/baidu.png',
  csdn: "/logo/csdn.png",
  第一财经:"/logo/diyicaijing.png",
  白鲸出海:"/logo/baijingchuhai.png",
  掘金:"/logo/juejin.png",
  acfun:"/logo/acfun.png",
  豆瓣电影: "/logo/douban-movie.png",
  懂车帝: "/logo/dongchedi.png"
})

// 平台热榜标签映射
const platformHotTagMap = ref({
  微博: '热搜榜',
  小红书: '实时热榜',
  B站: '热门榜',
  抖音: '热点榜'
})

// 卡片右上角标签样式映射
const tagClassMap = ref({
  '热搜榜': 'tag-green',
  '实时热榜': 'tag-red',
  '热门榜': 'tag-green',
  '热点榜': 'tag-orange',
  '热榜': 'tag-green'
})

// 新闻项标签样式映射
const itemTagClassMap = ref({
  '新': 'tag-item-red',
  '热': 'tag-item-orange',
  '爆': 'tag-item-yellow'
})

// 默认平台Logo（svg）
const defaultLogo = `<svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M12 2C6.48 2 2 6.48 2 12C2 17.52 6.48 22 12 22C17.52 22 22 17.52 22 12C22 6.48 17.52 2 12 2ZM12 20C7.59 20 4 16.41 4 12C4 7.59 7.59 4 12 4C16.41 4 20 7.59 20 12C20 16.41 16.41 20 12 20Z" fill="#666"/><path d="M14 10H10V14H14V10Z" fill="white"/></svg>`

// 农历日期
const getLunarDate = () => {
  const today = new Date()
  const solar = Solar.fromYmd(today.getFullYear(), today.getMonth() + 1, today.getDate())
  const lunar = solar.getLunar()
  const monthNum = lunar.getMonth()
  const dayNum = lunar.getDay()

  const monthNames = ["", "正月", "二月", "三月", "四月", "五月", "六月",
                      "七月", "八月", "九月", "十月", "冬月", "腊月"]
  const dayNames = ["", "初一", "初二", "初三", "初四", "初五", "初六", "初七", "初八", "初九", "初十",
                    "十一", "十二", "十三", "十四", "十五", "十六", "十七", "十八", "十九", "二十",
                    "廿一", "廿二", "廿三", "廿四", "廿五", "廿六", "廿七", "廿八", "廿九", "三十"]

  return `${today.getFullYear()}年 ${monthNames[monthNum] || ''}${dayNames[dayNum] || ''}`
}

// 定时刷新
let timeTimer = null
let scheduleTimer = null
const REFRESH_TIMES = [[8, 0], [12, 0], [18, 0]]

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

const scheduleDailyRefresh = async () => {
  await refreshHotRank()
  const delay = getNextRefreshDelay()
  scheduleTimer = setTimeout(() => scheduleDailyRefresh(), delay)
}

onMounted(() => {
  updateCurrentTime()
  lunarDate.value = getLunarDate()
  timeTimer = setInterval(updateCurrentTime, 1000)
  //refreshHotRank()
  scheduleDailyRefresh() //仅保留这一行，负责初始化+定时
})

onUnmounted(() => {
  clearInterval(timeTimer)
  clearTimeout(scheduleTimer)
})

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
  lunarDate.value = getLunarDate()
}

// 替换为你提供的 时间差格式化函数
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

// 批量刷新所有平台
const refreshHotRank = async () => {
  try {
    isLoading.value = true
    const res = await getTopNewsList()
    hotData.value = res.data.hot_topics
    lastRefreshTime.value = Date.now()
    // 批量更新各平台刷新时间
    Object.keys(res.data.hot_topics).forEach(platform => {
      platformUpdateTime.value[platform] = Date.now()
    })
    ElMessage.success('热榜刷新成功')
  } catch (err) {
    console.error('获取热榜失败:', err)
    ElMessage.error('加载热榜失败，请稍后重试')
  } finally {
    isLoading.value = false
  }
}

// 单独刷新某个平台热榜
const refreshSinglePlatform = async (platform) => {
  try {
    platformLoading.value[platform] = true
    // 若有单平台接口，可替换为专属接口，此处临时调用批量接口提取数据
    const res = await getTopNewsList()
    if (res.data.hot_topics[platform]) {
      hotData.value[platform] = res.data.hot_topics[platform]
      platformUpdateTime.value[platform] = Date.now()
      ElMessage.success(`${platform}热榜刷新成功`)
    } else {
      ElMessage.warning(`${platform}暂无热榜数据`)
    }
  } catch (err) {
    console.error(`${platform}刷新失败:`, err)
    ElMessage.error(`${platform}热榜刷新失败，请稍后重试`)
  } finally {
    platformLoading.value[platform] = false
  }
}

const goToHotDetail = (item) => {
  if (item.hot_url) window.open(item.hot_url, '_blank', 'noopener noreferrer')
  else ElMessage.warning('该热点暂无链接')
}
</script>

<style scoped>
/* 全局字体 */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  font-family: "Microsoft YaHei UI", "Microsoft YaHei", "微软雅黑", sans-serif !important;
}

.hot-rank-page {
  margin: 24px auto;
  padding: 0 20px;
  width: 100%;
}

.card-container {
  display: grid;
  grid-template-columns: repeat(4, minmax(240px, 1fr));
  gap: 20px;
  margin: 0 auto;
}

.empty-tip {
  grid-column: 1 / -1;
  text-align: center;
  padding: 60px 0;
  color: #909399;
  font-size: 16px;
}
.empty-tip el-icon {
  font-size: 32px;
  margin-bottom: 12px;
  display: block;
  color: #c0c4cc;
}

.hot-card {
  height: 100%;
  border-radius: 4px;
  --el-card-header-padding: 8px 12px;
  box-shadow: 0 1px 2px rgba(0,0,0,0.08);
  border: 1px solid #f5f7fa;
}

/* 卡片头部：平台名与热榜标签对齐 */
.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0;
}
.header-left {
  display: flex;
  align-items: center;
  gap: 6px;
}
.platform-logo {
  width: 20px;
  height: 20px;
}
.platform-name {
  font-size: 15px;
  color: #333;
  font-weight: 500;
}

/* 热榜标签：匹配参考图（绿色圆形图标+文字） */
.hot-tag-wrapper {
  display: flex;
  align-items: center;
  gap: 4px;
}
.hot-tag {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 2px 6px;
  font-size: 12px;
  color: #87d068;
  background-color: #f0f9eb;
  border-radius: 10px;
}
/* 标签前置圆形图标（通过伪元素实现） */
.hot-tag::before {
  content: "";
  display: inline-block;
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background-color: #87d068;
}
/* 不同标签颜色（可选） */
.tag-red {
  color: #f56c6c;
  background-color: #fff1f0;
}
.tag-red::before {
  background-color: #f56c6c;
}
.tag-orange {
  color: #e6a23c;
  background-color: #fff7e6;
}
.tag-orange::before {
  background-color: #e6a23c;
}

/* 排名序号 */
.rank-num {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 20px;
  height: 20px;
  font-size: 12px;
  font-weight: 700;
  margin-right: 8px;
  color: white;
  border-radius: 2px;
}
.rank-1 { background-color: #f56c6c; }
.rank-2 { background-color: #e6a23c; }
.rank-3 { background-color: #67c23a; }
.rank-other {
  background-color: #f5f7fa;
  color: #606266;
}

/* === 关键修改：移除固定高度，使用 flex 自动填充 === */
.card-body { 
  padding: 0;
  display: flex;
  flex-direction: column;
  /* 删除 height: calc(100% - 36px); */
}

.hot-list {
  flex: 1; /* 占满剩余空间 */
  overflow-y: auto;
  overflow-x: hidden;
  scrollbar-width: thin;
  max-height: 260px; /* 保留最大高度限制 */
}
.hot-list::-webkit-scrollbar { width: 3px; }
.hot-list::-webkit-scrollbar-thumb {
  background-color: #e5e7eb;
  border-radius: 2px;
}

.hot-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 8px 12px;
  cursor: pointer;
  border-bottom: 1px solid #f5f7fa;
  width: 100%;
}
.hot-item:last-child { border-bottom: none; }
.hot-item:hover {
  background-color: #f8f9fa;
  border-radius: 4px;
}

.label-container {
  flex: 1;
  margin-right: 8px;
  display: flex;
  align-items: center;
  gap: 6px;
}

.hot-item-tag {
  padding: 0 3px;
  font-size: 12px;
  color: white;
  border-radius: 2px;
}
.tag-item-red { background-color: #f56c6c; }
.tag-item-orange { background-color: #e6a23c; }
.tag-item-yellow { background-color: #fadb14; color: #333; }

.hot-label {
  font-size: 13px;
  color: #333;
  line-height: 1.3;
  word-wrap: break-word;
  word-break: break-all;
}

.hot-value {
  font-size: 12px;
  color: #909399;
  white-space: nowrap;
  flex-shrink: 0;
}

/* === 关键修改：底部自动吸附，不占额外空间 === */
.card-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 6px 12px;
  font-size: 12px;
  color: #909399;
  border-top: 1px solid #f5f7fa;
  background-color: #fafbfc;
  /* 移除圆角（避免与 card-body 冲突） */
  border-bottom-left-radius: 0;
  border-bottom-right-radius: 0;
  /* 关键：自动推到底部 */
  margin-top: auto;
  /* 固定高度确保一致性 */
  height: 32px;
}
/* 刷新图标样式 */
.refresh-icon {
  cursor: pointer;
  font-size: 14px;
  transition: color 0.2s;
}
.refresh-icon:hover {
  color: #409eff;
}
/* 加载状态下底部样式微调 */
.footer-loading .refresh-icon {
  color: #409eff;
}

/* 响应式 */
@media (max-width: 1199px) {
  .card-container { grid-template-columns: repeat(3, minmax(240px, 1fr)); }
}
@media (max-width: 991px) {
  .card-container { grid-template-columns: repeat(2, minmax(240px, 1fr)); }
}
@media (max-width: 600px) {
  .card-container { grid-template-columns: 1fr; }
  .hot-rank-page { padding: 0 15px; }
  .hot-list { max-height: 240px; }
  .card-footer { 
    padding: 4px 10px; 
    font-size: 11px; 
    height: 28px; /* 适配小屏 */
  }
  .refresh-icon { font-size: 13px; }
}
</style>
