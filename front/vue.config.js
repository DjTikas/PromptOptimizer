module.exports = {
  devServer: {
    proxy: {
      '/api': {
        target: 'http://47.121.119.236',
        changeOrigin: true,
        pathRewrite: {
          '^/api': ''
        }
      }
    }
  },
  configureWebpack: {
    plugins: [
      new (require('webpack').DefinePlugin)({
        // 显式定义 Vue 的特性标志
        __VUE_PROD_HYDRATION_MISMATCH_DETAILS__: JSON.stringify(false),
      }),
    ],
  },
  css: {
    loaderOptions: {
      scss: {
        additionalData: `@import "@/styles/variables.scss";`
      }
    }
  }
}