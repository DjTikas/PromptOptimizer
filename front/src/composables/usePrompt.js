import { ref } from 'vue'
import { useApi } from './useApi'

export function usePrompt() {
  const { get, post, put, delete: del, isLoading, error } = useApi()

  // 提示词相关操作
  const fetchPrompts = async (folderId = null) => {
    try {
      const endpoint = folderId 
        ? `/manage/folders/${folderId}/prompts`
        : '/manage/prompts'
      return await get(endpoint)
    } catch (err) {
      console.error('Failed to fetch prompts:', err)
      throw err
    }
  }

  const createPrompt = async (promptData) => {
    try {
      return await post('/manage/prompts', promptData)
    } catch (err) {
      console.error('Failed to create prompt:', err)
      throw err
    }
  }

  const updatePrompt = async (promptId, promptData) => {
    try {
      return await put(`/manage/prompts/${promptId}`, promptData)
    } catch (err) {
      console.error('Failed to update prompt:', err)
      throw err
    }
  }

  const movePrompt = async (folderId, { prompt_ids, move = true }) => {
    try {
      // 确保folderId是数字类型
      const numericFolderId = Number(folderId)
      if (isNaN(numericFolderId)) {
        throw new Error('folderId必须是有效的数字')
      }
      
      return await post(`/manage/folders/${folderId}/prompts`, {
        prompt_ids,
        move
      })
    } catch (err) {
      console.error('Failed to move prompt:', err)
      throw err
    }
  }

  // 修改删除提示词方法支持批量
  const deletePrompt = async (promptIds) => {
    try {
      if (Array.isArray(promptIds)) {
        return await del('/manage/prompts', { data: promptIds })
      }
      return await del(`/manage/prompts/${promptIds}`)
    } catch (err) {
      console.error('Failed to delete prompt:', err)
      throw err
    }
  }

  // 收藏夹相关操作
  const fetchFolders = async () => {
    try {
      return await get('/manage/folders')
    } catch (err) {
      console.error('Failed to fetch folders:', err)
      throw err
    }
  }

  const createFolder = async (folderName) => {
    try {
      const response = await post('/manage/folders', { folder_name: folderName })
      return { success: true, data: response }
    } catch (err) {
      if (err.response?.data?.detail?.some(e => e.type === 'value_error.folder_exists')) {
        return { success: false, error: '文件夹名称已存在' }
      }
      console.error('Failed to create folder:', err)
      throw err
    }
  }

  const updateFolder = async (folderId, folderName) => {
    try {
      return await put(`/manage/folders/${folderId}`, { folder_name: folderName })
    } catch (err) {
      console.error('Failed to update folder:', err)
      throw err
    }
  }

  const deleteFolder = async (folderId) => {
    try {
      return await del(`/manage/folders/${folderId}`)
    } catch (err) {
      console.error('Failed to delete folder:', err)
      throw err
    }
  }

  // 提示词优化
  const optimizePrompt = async (originalPrompt, config) => {
    try {
      return await post('/optimize/optimize', {
        original_prompt: originalPrompt,
        config
      })
    } catch (err) {
      console.error('Failed to optimize prompt:', err)
      throw err
    }
  }

  const testPrompt = async (prompt, config) => {
    try {
      return await post('/optimize/test', {
        prompt,
        config
      })
    } catch (err) {
      console.error('Failed to test prompt:', err)
      throw err
    }
  }

  return {
    isLoading,
    error,
    fetchPrompts,
    createPrompt,
    updatePrompt,
    deletePrompt,
    fetchFolders,
    createFolder,
    updateFolder,
    deleteFolder,
    optimizePrompt,
    testPrompt,
    movePrompt
  }
}