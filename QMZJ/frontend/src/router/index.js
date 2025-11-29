import Vue from "vue";
import Router from "vue-router";
import HomePage from "@/components/HomePage";
import LoginPage from "@/components/LoginPage";
import RegisterPage from "@/components/RegisterPage";
import ChatPage from "@/components/ChatPage";
import Forum from "@/components/Forum";
import UserCenter from "@/components/UserCenter";
import VisualAll from "@/components/VisualAll";
import Visual from "@/components/Visual";
import ChinaMap from "@/components/ChinaMap";
import DnaTimeline from "@/components/DnaTimeline.vue";
import trans from "@/components/trans"

import { jwtDecode } from 'jwt-decode'
import { Message } from 'element-ui';

Vue.use(Router);

const routes = [
  {
    path: "/",
    name: "homepage",
    component: HomePage,
    meta: { requiresAuth: false }
  },
  {
    path: "/login",
    name: "login",
    component: LoginPage,
    meta: { requiresAuth: false }
  },
  {
    path: "/register",
    name: "register",
    component: RegisterPage,
    meta: { requiresAuth: false }
  },
  {
    path: "/forum",
    name: "forum",
    component: Forum,
    meta: { requiresAuth: true }
  },
  {
    path: "/chatPage",
    name: "chatPage",
    component: ChatPage,
    meta: { requiresAuth: true }
  },
  {
    path: "/usercenter",
    name: "usercenter",
    component: UserCenter,
    meta: { requiresAuth: true }
  },
  {
    path: "/visualAll",
    name: "visualAll",
    component: VisualAll,
    meta: { requiresAuth: true }
  },
  {
    path: "/visual",
    name: "visual",
    component: Visual,
    meta: { requiresAuth: true }
  },
  {
    path: "/chinaMap",
    name: "chinaMap",
    component: ChinaMap,
    meta: { requiresAuth: true }
  },
  {
    path: "/dnaTimeline",
    name: "dnaTimeline",
    component: DnaTimeline,
    meta: { requiresAuth: true }
  },
  {
    path: "/trans",
    name: "trans",
    component: trans,
    meta: { requiresAuth: true }
  },
];

const router = new Router({
  mode: "hash", // 或者 history，根据需求设置
  routes,
});

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem("token");
  const user = localStorage.getItem("user");
  console.log("token: ", token);
  console.log("to.meta.requiresAuth:  ",to.meta.requiresAuth)
  if (to.meta.requiresAuth && (!token || !user)) {
    Message.warning({ message: "请先登录！", duration: 1000 });
    // alert("请先登录");
    // 如果目标路由需要登录权限且没有 token，则跳转到登录页
    next({ path: "/login" });
  }

  // 如果有token，进一步检查是否过期
  if (token) {
    try {
      const decoded = jwtDecode(token)
      const isExpired = decoded.exp < Date.now() / 1000
      if (isExpired) {
        localStorage.setItem("isLoggedIn", false);
        Message.warning({ message: "登录已过期，请重新登录", duration: 1000 });
        localStorage.removeItem('token')
        next({
          path: '/login',
          // query: { redirect: to.fullPath }
        })
        return
      }
    } catch (error) {
      console.error('Token解析失败:', error)
      localStorage.removeItem('token')
      next('/login')
      return
    }
  }

  if (to.path !== '/chatPage' && from.path === '/chatPage' || to.path === '/chatPage' && from.path !== '/chatPage') {
    localStorage.setItem("Reload", true);
  }

  next();
});

export default router;