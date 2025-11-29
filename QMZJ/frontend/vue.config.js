module.exports = {
  transpileDependencies: true,
  publicPath: './',  // 确保使用相对路径加载资源
  transpileDependencies: [
    'vuetify',
  ],
  devServer: {
    proxy: {
      '/': {                              // 用于前端开发的接口请求抽象地址
        changeOrigin: true,               // 允许跨域
        target: this.$baseUrl+'/'         // 后端接收请求的地址
      },
    }
  }
}