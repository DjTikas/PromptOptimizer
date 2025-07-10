module.exports = {
  root: true,
  env: {
    node: true
  },
  // 只保留最核心的 Vue 3 规则
  extends: ['plugin:vue/vue3-essential'], 
  parserOptions: {
    ecmaVersion: 2020
  },
  rules: {
    // 关闭所有非必要的规则
    'vue/multi-word-component-names': 'off',  // 允许单单词组件名
    'no-unused-vars': 'warn',                // 未使用变量改为警告
    'no-console': 'off',                     // 允许 console.log
    'no-debugger': 'off'                     // 允许 debugger
  }
}