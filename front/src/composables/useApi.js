import { ref } from 'vue'
import { useUserStore } from '@/store'
import router from '@/router'

export function useApi() {
  const userStore = useUserStore()
  const BASE_URL = 'http://47.121.119.236'
  const isLoading = ref(false)
  const error = ref(null)

  const request = async (method, endpoint, data = null, options = {}) => {
    
    isLoading.value = true
    error.value = null
    
    try {
      const controller = new AbortController()
      const timeoutId = setTimeout(() => controller.abort(), 10000)
  
      // 设置请求头
      const headers = {
        ...options.headers
      }
      
      // 自动添加认证头
      if (userStore.token) {
        headers['Authorization'] = `Bearer ${userStore.token}`
      }
  
      // 处理 FormData 的特殊情况
      let body
      if (data !== null) {  // 修改这里，允许DELETE方法带body
        if (data instanceof FormData) {
          // FormData 不设置 Content-Type，让浏览器自动设置
          body = data
        } else if (data instanceof URLSearchParams) {
          headers['Content-Type'] = 'application/x-www-form-urlencoded'
          body = data.toString()
        } else {
          headers['Content-Type'] = 'application/json'
          body = JSON.stringify(data)
        }
      }
  
      const config = {
        method,
        headers,
        body,
        signal: controller.signal,
        ...options
      }
  
      const fullUrl = `${BASE_URL}${endpoint}`
      console.log('[API请求]', method, fullUrl, config)
  
      let response
      try {
        response = await fetch(fullUrl, config)
        clearTimeout(timeoutId)
      } catch (fetchError) {
        if (fetchError.name === 'AbortError') {
          throw new Error('请求超时，请检查网络连接')
        }
        throw fetchError
      }
  
      // 强制读取响应内容
      const responseText = await response.text()
      console.log('[API原始响应]', response.status, responseText)
  
      if (!response.ok) {
        let errorData
        try {
          errorData = responseText ? JSON.parse(responseText) : {}
        } catch {
          errorData = { raw: responseText }
        }
        
        // 处理未授权错误
        if (response.status === 401) {
          userStore.logout()
          router.push('/login')
        }
        
        // 构造详细的错误对象
        const error = new Error(errorData.message || `HTTP错误 ${response.status}`)
        error.status = response.status
        error.data = errorData
        
        // 特殊处理422验证错误
        if (response.status === 422) {
          const details = errorData.detail || []
          error.message = '数据验证失败: ' + 
            details.map(d => `${d.loc?.join('.')}: ${d.msg}`).join('\n')
        }
        
        throw error
      }
  
      return responseText ? JSON.parse(responseText) : {}
    } catch (err) {
      console.error('[API错误]', {
        message: err.message,
        status: err.status,
        data: err.data,
        stack: err.stack
      })
      error.value = err
      throw err
    } finally {
      isLoading.value = false
    }
  }

  // 封装常用HTTP方法
  const get = (endpoint, params = {}, options = {}) => {
    const queryString = Object.keys(params).length 
      ? '?' + new URLSearchParams(params).toString() 
      : ''
    return request('GET', endpoint + queryString, null, options)
  }

  const post = (endpoint, data, options = {}) => 
    request('POST', endpoint, data, options)

  const put = (endpoint, data, options = {}) => 
    request('PUT', endpoint, data, options)

  const del = (endpoint, data = null, options = {}) => 
    request('DELETE', endpoint, data, options)

  return {
    isLoading,
    error,
    get,
    post,
    put,
    del
  }
}