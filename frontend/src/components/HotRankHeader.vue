<template>
  <div class="hot-rank-header">
    <!-- 左侧Logo+标题 -->
    <div class="header-left">
      <!-- 红色图标（替换原ElIcon） -->
      <img 
        class="header-logo" 
        src="/ico/favicon.png"  
        alt="今日热榜"
        width="44"
        height="44"
      >
      <div class="title-group">
        <h1 class="main-title">今日热榜</h1>
        <p class="sub-title">汇聚全网热点，热门尽览无余</p>
      </div>
    </div>

    <!-- 中间时间 -->
    <div class="header-middle">
      <p class="current-time">{{ currentTime }}</p>
      <p class="weekday">{{ getWeekday() }}</p>
    </div>

    <!-- 右侧工具 -->
    <div class="header-right">
      <el-button 
        icon="Refresh" 
        text 
        @click="handleRefresh" 
        :loading="isLoading"
        class="refresh-btn"
      >刷新</el-button>
    </div>
  </div>
</template>

<script setup>
import { defineProps, defineEmits, ref, onMounted, onUnmounted } from 'vue'
import { ElButton } from 'element-plus'
import { Refresh } from '@element-plus/icons-vue'

// 接收外部传入的参数
const props = defineProps({
  currentTime: {
    type: String,
    required: true
  },
  isLoading: {
    type: Boolean,
    default: false
  }
})

// 触发刷新事件
const emit = defineEmits(['refresh'])
const handleRefresh = () => {
  emit('refresh')
}

// 计算当前星期几
const getWeekday = () => {
  const weekList = ['周日', '周一', '周二', '周三', '周四', '周五', '周六']
  return weekList[new Date().getDay()]
}
</script>

<style scoped>
.hot-rank-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 0;
  margin-bottom: 24px;
  border-bottom: 1px solid #e5e7eb;
  width: 100%;
  font-family: "Microsoft YaHei", sans-serif;
}

/* 左侧Logo+标题 */
.header-left {
  display: flex;
  align-items: center;
  gap: 12px;
}
.header-logo {
  border-radius: 4px; /* 可选：让图标更圆润 */
}
.title-group {
  display: flex;
  flex-direction: column;
  gap: 2px;
}
.main-title {
  font-size: 20px;
  font-weight: 700;
  color: #333;
  margin: 0;
}
.sub-title {
  font-size: 12px;
  color: #909399;
  margin: 0;
}

/* 中间时间 */
.header-middle {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 2px;
  color: #666;
}
.current-time {
  font-size: 14px;
  margin: 0;
}
.weekday {
  font-size: 12px;
  margin: 0;
}

/* 右侧刷新按钮 */
.header-right {
  display: flex;
  align-items: center;
}
.refresh-btn {
  color: #666;
  &:hover {
    color: #f56c6c;
  }
}
</style>
