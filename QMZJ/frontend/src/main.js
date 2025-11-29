// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from "vue";
import App from "./App.vue"; // 确保 App 组件文件名后缀为 .vue
import router from "./router"; // router/index.js 中应有 export default router
import ElementUI from "element-ui";
import "element-ui/lib/theme-chalk/index.css";
import axios from "axios";
import './assets/global.css';  // 引入全局CSS样式
import './assets/font/iconfont.css'

// 云服务器部署
Vue.prototype.$baseUrl = 'http://47.98.136.180';
// 本地运行
// Vue.prototype.$baseUrl = 'http://localhost:5000';

// 全局注册 ECharts 组件（vue-echarts）
import VChart from "vue-echarts";
Vue.component('v-chart', VChart);

// 使用 ElementUI
Vue.use(ElementUI);

// 配置 axios，解决跨域请求携带凭证
Vue.prototype.$axios = axios;
axios.defaults.withCredentials = true;

// 注册 ECharts 组件（如果需要额外配置）
import { use } from "echarts/core";
import { CanvasRenderer } from "echarts/renderers";
import { GraphChart } from "echarts/charts";
import { TooltipComponent, LegendComponent } from "echarts/components";

// 注册必要的 ECharts 组件
use([
  CanvasRenderer,
  GraphChart,
  TooltipComponent,
  LegendComponent
]);

Vue.config.productionTip = false;

new Vue({
  el: "#app",
  router,
  render: h => h(App)
});
