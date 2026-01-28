import axios from 'axios'

/**
 * 优化点：针对同一 baseURL（同一 FastAPI 后端），强化通用性、可维护性和健壮性
 * 保留统一 baseURL，新增通用拦截器逻辑，适配后续多个功能接口的复用需求
 */
// 创建 axios 实例（同一 FastAPI 后端，固定 baseURL，后续所有功能接口共用）
const request = axios.create({
  baseURL: 'http://10.195.157.17:8001/api', // 同一 FastAPI 后端的统一接口前缀
  timeout: 10000, // 延长超时时间（适配更多功能接口，避免短时间内超时）
  headers: {
    'Content-Type': 'application/json;charset=utf-8'
  }
})

// 【新增】请求拦截器（统一处理所有功能接口的请求前置逻辑，减少冗余）
request.interceptors.request.use(
  (config) => {
    // 1. 统一添加认证令牌（后续所有 FastAPI 功能接口都可能需要登录认证，如 JWT）
    // 示例：从本地存储获取 token，无需在每个接口请求中单独添加
    const token = localStorage.getItem('fastapi_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }

    // 2. 开发环境打印请求日志（方便调试多个功能接口的请求参数、地址）
    if (process.env.NODE_ENV === 'development') {
      console.log(`[FastAPI请求] ${config.method?.toUpperCase()} ${config.url}`, config.data || config.params)
    }

    // 3. 统一处理请求参数格式（可选，针对 FastAPI 接收参数的规范做适配）
    if (config.method === 'get' && config.data) {
      // get 请求若携带复杂数据，自动转为 params（适配 FastAPI 的查询参数接收）
      config.params = { ...config.params, ...config.data }
      delete config.data
    }

    return config
  },
  (error) => {
    // 统一捕获请求配置错误，无需在每个接口中单独处理
    console.error('请求配置失败（所有 FastAPI 接口通用）：', error.message)
    return Promise.reject(error)
  }
)

// 【优化】响应拦截器（强化容错，统一处理所有功能接口的响应结果）
request.interceptors.response.use(
  (response) => {
    // 1. 开发环境打印响应日志（方便调试多个功能接口的返回数据）
    if (process.env.NODE_ENV === 'development') {
      console.log(`[FastAPI响应] ${response.status} ${response.config.url}`, response.data)
    }

    // 2. 直接返回接口原始数据（保持和原有逻辑兼容，同时适配 FastAPI 所有功能接口的返回格式）
    // 无论后续是新闻、用户、评论接口，都直接返回核心数据，简化前端调用
    return response.data
  },
  (error) => {
    // 统一处理所有 FastAPI 接口的错误（网络错误、超时、后端状态码错误等）
    let errorMsg = 'FastAPI 接口请求失败，请稍后重试'
    if (error.code === 'ECONNABORTED') {
      errorMsg = '请求超时（接口响应过慢），请检查网络或 FastAPI 服务状态'
    } else if (error.response) {
      // 针对 FastAPI 后端返回的错误状态码，给出更精准的提示
      const { status, data } = error.response
      errorMsg = `FastAPI 接口错误 [${status}]：${data?.detail || '服务器返回异常'}` // FastAPI 错误信息通常在 detail 字段

      // 统一处理 401 未授权、403 禁止访问等通用状态码（所有功能接口共用）
      if (status === 401) {
        localStorage.removeItem('fastapi_token') // 清除无效令牌
        console.error('未授权访问，即将跳转登录页（可扩展路由跳转逻辑）')
      } else if (status === 404) {
        errorMsg = `FastAPI 接口不存在 [${status}]：${config.url}`
      }
    }

    console.error(errorMsg)
    // 统一返回拒绝状态的 Promise，方便前端每个接口单独捕获具体错误
    return Promise.reject(new Error(errorMsg))
  }
)

export default request
