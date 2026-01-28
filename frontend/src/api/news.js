// src/api/news.js（新闻模块接口，原有功能封装）
import request from '@/utils/request'

/**
 * 获取指定分类的新闻列表（FastAPI 接口：/api/news/）
 */
export const getTopNewsList = () => {
  // 直接复用 request 实例，无需重复配置 baseURL
  return request.get('/hot-topics')
}

// 后续可新增新闻相关接口，如获取新闻详情、搜索新闻等
export const getNewsDetail = (newsId) => {
  return request.get(`/news/detail/${newsId}`)
}
