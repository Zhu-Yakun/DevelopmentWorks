<template>
  <div class="page-home">

    <!-- <ParticleLayer /> -->

    <!-- 导航栏 -->
    <div class="navbar" v-if="showNavbar">
      <div class="navbar-container">
        <div class="nav-links">
          <router-link :to="getLink('/visualAll')" class="nav-link" @click="checkAuth('/visualAll')">智鉴图谱</router-link>
          <router-link :to="getLink('/chinaMap')" class="nav-link" @click="checkAuth('/chinaMap')">耕织地图</router-link>
          <router-link :to="getLink('/dnaTimeline')" class="nav-link"
            @click="checkAuth('/dnaTimeline')">千年回响</router-link>
          <router-link :to="getLink('/forum')" class="nav-link" @click="checkAuth('/forum')">耘集荟萃</router-link>
          <router-link v-if="!user" to="/login" class="nav-link">登录</router-link>
          <router-link v-if="user" to="/usercenter" class="nav-link">用户中心</router-link>
        </div>
      </div>
    </div>

    <!-- 多页面容器 -->
    <div @wheel="handleScroll">
      <!-- 首页 -->

      <div v-show="currentPage === 0">
        <div class="background-image"></div>
        <!-- 标题容器，包含主标题 -->
        <div class="title-wrapper">
          <div class="title-container">
            <span class="font title line1">齐民智鉴</span><br />
            <span class="font title line2">古代农学数据可视化平台</span>
          </div>
        </div>

        <!-- 描述区域，包含详细描述文本 -->
        <div class="description">
          <span class="description-text">
            《齐民智鉴——古代农学数据可视化平台》是一个将古代农学知识数字化呈现的网站。
            <br />它整合古代农业数据，以直观图表和地图形式展示古代农业生产模式、技术变迁等内容。
            <br />平台旨在方便研究者查询资料，同时让大众轻松了解古代农学智慧，助力传统文化传承与推广。
          </span>
        </div>
        <!-- 引入箭头动画组件 -->
        <ArrowAnimation class="arrow-animation" :onClick="handleArrowClick" />
      </div>

      <!-- 第二页 -->
      <div v-show="currentPage === 1">
        <div class="background-image"></div>
        <div class="text-container">
          <span class="self-center font_home pos-home" style="animation-delay: 0s">大地，是一幅画卷，</span>
          <span class="self-center font_home pos-home" style="animation-delay: 1s">绘着丰收，</span>
          <span class="self-center font_home pos-home" style="animation-delay: 2s">也绘着希望。</span>
          <span class="self-center font_home pos-home" style="animation-delay: 3s">农业，是一部史诗，</span>
          <span class="self-center font_home pos-home" style="animation-delay: 4s">它承载过去，</span>
          <span class="self-center font_home pos-home" style="animation-delay: 5s">也启迪未来。</span>
          <span class="self-center font_home pos-home" style="animation-delay: 6s">让我们一同走进，古代农学的智慧世界。</span>
        </div>
        <ArrowAnimation class="arrow-animation" :onClick="handleArrowClick" />
        <div class="footer">
          <span class="font_2">开发团队: 同济大学齐民智鉴团队</span>
          <span class="font_2">联系我们: 2252085@tongji.edu.cn</span>
        </div>
      </div>

      <div class="stripes-container" ref="stripesContainer"></div>

      <div v-show="currentPage === 2">
        <div class="overlay"></div>
        <!-- 左侧竖直标题栏 -->
        <div class="vertical-sidebar">
          <div class="sidebar-item">齐民智鉴||古代农学数据可视化平台</div>
        </div>
        <div class="vertical-block-1 slide-down">
          <router-link :to="getLink('/visualAll')" class="button-link" @click="checkAuth('/visualAll')">
            <img src="../assets/meihua.png" alt="icon" class="icon" />
            <span class="text-block">智鉴图谱</span></router-link>
        </div>
        <div class="vertical-block-2 slide-down">
          <router-link :to="getLink('/chinaMap')" class="button-link" @click="checkAuth('/chinaMap')">
            <img src="../assets/cereal.png" alt="icon" class="icon" />
            <span class="text-block">耕织地图</span>
          </router-link>
        </div>
        <div class="vertical-block-3 slide-down">
          <router-link :to="{
            name: 'chatPage',
            params: { need_reload: true }
          }" class="button-link" @click.prevent="checkAuth('/chatPage')">
            <img src="../assets/robot.png" alt="icon" class="icon-2" />
            <span class="text-block">智能问答</span>
          </router-link>
        </div>
        <div class="vertical-block-4 slide-down">
          <router-link :to="getLink('/forum')" class="button-link" @click="checkAuth('/forum')">
            <img src="../assets/star.png" alt="icon" class="icon" />
            <span class="text-block">耘集荟萃</span></router-link>
        </div>
        <div class="vertical-block-5 slide-down">
          <div class="sidebar-block-item">
            <router-link :to="{
              path: getLink('/forum'),
              query: { category: '农书' }
            }" class="button-link" @click="checkAuth('/forum')">
              <img src="../assets/nongshu.png" alt="icon" class="icon" />
              <span class="text-block">农书</span></router-link>
          </div>
        </div>
        <div class="vertical-block-6 slide-down">
          <div class="sidebar-block-item">
            <router-link :to="{
              path: getLink('/forum'),
              query: { category: '农具' }
            }" class="button-link" @click="checkAuth('/forum')">
              <img src="../assets/nongju.png" alt="icon" class="icon-3" />
              <span class="text-block">农具</span></router-link>
          </div>
        </div>
        <div class="vertical-block-7 slide-down">
          <div class="sidebar-block-item">
            <router-link :to="{
              path: getLink('/forum'),
              query: { category: '农作物' }
            }" class="button-link" @click="checkAuth('/forum')">
              <img src="../assets/cereal.png" alt="icon" class="icon" />
              <span class="text-block">农作物</span></router-link>
          </div>
        </div>
        <div class="vertical-block-8 slide-down">
          <router-link :to="getLink('/dnaTimeline')" class="button-link" @click="checkAuth('/dnaTimeline')">
            <img src="../assets/music.png" alt="icon" class="icon" />
            <span class="text-block">千年回响</span></router-link>
        </div>
        <div class="vertical-block-9 slide-down">
          <div class="sidebar-block-item">
            <router-link :to="{
              path: getLink('/forum'),
              query: { category: '农业文化' }
            }" class="button-link" @click="checkAuth('/forum')">
              <img src="../assets/cow.png" alt="icon" class="icon" />
              <span class="text-block">农业文化</span></router-link>
          </div>
        </div>
        <div class="vertical-block-10 slide-down">
          <div class="sidebar-block-item">
            <router-link :to="{
              path: getLink('/forum'),
              query: { category: '农业技术' }
            }" class="button-link" @click="checkAuth('/forum')">
              <img src="../assets/jishu.png" alt="icon" class="icon-1" />
              <span class="text-block">农业技术</span>
            </router-link>
          </div>
        </div>
        <ArrowAnimation class="arrow-animation" :onClick="handleArrowClick" />
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted, onUnmounted } from "vue";
import ArrowAnimation from "./ArrowAnimation.vue"; // 引入箭头动画组件
import PetComponent from "@/components/PetComponent.vue";
// import ParticleLayer from "@/components/ParticleLayer.vue";

export default {
  name: "Homepage", // 组件名称
  components: {
    ArrowAnimation, // 注册箭头动画组件
    PetComponent,
    // ParticleLayer,
  },
  data() {
    return {
      user: null,
      token: null,
      currentPage: 0, // 当前页数
      totalPages: 3, // 总页数
      isScrolling: false, // 是否正在滚动
      showNavbar: true, // 用于控制导航栏的显示状态
    };
  },
  mounted() {
    if(localStorage.getItem("Reload") === "true"){
      localStorage.setItem("Reload", false);
      window.location.reload();
    }
    this.$nextTick(() => {
      this.createStripes();
      window.addEventListener("resize", this.createStripes); // 监听窗口变化
    });
  },
  beforeUnmount() {
  window.removeEventListener("resize", this.createStripes);
  },
  created() {
    // console.log("Homepage created");
    const user = localStorage.getItem("user");
    const token = localStorage.getItem("token");
    if (user) {
      this.user = JSON.parse(user);
    }
    if (token) {
      this.token = token;
    }
    window.addEventListener("wheel", this.handleScroll, { passive: false }); // this.createStripes();
  },
  destroyed() {
    window.removeEventListener("wheel", this.handleScroll); // 移除监听
  },
  methods: {
    logout() {
      this.clearAuth();
      this.$router.push("/");
    },
    handleRouterClick() {
      if (!this.user) {
        this.$router.push('/login')
      } else {
        this.$router.push({
          path: '/forum'
        })
      }
    },
    checkAuth(path) {
      if (!this.user || !this.token) {
        this.clearAuth();
        this.$router.push("/login");
      } else {
        this.$router.push(path);
      }
    },
    scrollToPage(target) {
      if (target < 0 || target >= totalPages || isScrolling.value) return;

      isScrolling.value = true;
      currentPage.value = target;

      setTimeout(() => {
        isScrolling.value = false;
      }, 1000);
    },
    handleWheel(e) {
      const delta = Math.sign(e.deltaY);
      scrollToPage(currentPage.value + delta);
    },
    touchStart(e) {
      touchStartY.value = e.touches[0].clientY;
    },
    touchEnd(e) {
      const delta = touchStartY.value - e.changedTouches[0].clientY;
      if (Math.abs(delta) < 50) return;
      scrollToPage(delta > 0 ? currentPage.value + 1 : currentPage.value - 1);
    },
    handleKeyPress(e) {
      if (e.key === "ArrowDown") scrollToPage(currentPage.value + 1);
      if (e.key === "ArrowUp") scrollToPage(currentPage.value - 1);
    },

    getLink(path) {
      if (!(this.user && this.token)) {
        this.clearAuth();
      }
      return path;
    },
    clearAuth() {
      localStorage.removeItem("user");
      localStorage.removeItem("token");
      this.user = null;
      this.token = null;
    },
    handleScroll(event) {
      // 1. 检测是否按下了 Ctrl 键
      if (event.ctrlKey) {
        // 如果按下了 Ctrl 键，直接返回，不阻止默认滚动行为
        return;
      }

      // 2. 阻止默认滚动行为
      event.preventDefault();

      // 3. 防抖处理 (200ms内只能触发一次)
      if (this.isScrolling) return;
      this.isScrolling = true;
      setTimeout(() => (this.isScrolling = false), 200);

      // 4. 增加滚动幅度阈值判断
      if (Math.abs(event.deltaY) < 50) return;

      // 5. 原有逻辑
      if (event.deltaY > 0 && this.currentPage < this.totalPages - 1) {
        this.currentPage++;
        this.showNavbar = false;
        console.log("向下翻页:", this.currentPage);
      } else if (event.deltaY < 0 && this.currentPage > 0) {
        this.currentPage--;
        this.showNavbar = true;
        console.log("向上翻页:", this.currentPage);
      }
    },
    handleArrowClick() {
      if (this.currentPage < this.totalPages - 1) {
        this.currentPage++;
        this.showNavbar = false;
      }
    },
    createStripes() {
      const container = this.$refs.stripesContainer;
      if (!container) return;

      const screenWidth = window.innerWidth;
      const screenHeight = window.innerHeight;
      const stripeWidth = screenWidth * 0.05; // 设置条纹宽度
      const stripeHeight = screenHeight * 1; // 设置条纹高度
      const stripeCount = Math.ceil(screenWidth / stripeWidth);

      container.innerHTML = "";

      for (let i = 0; i < stripeCount; i++) {
        const stripe = document.createElement("div");
        stripe.className = "stripes-item";
        stripe.style.backgroundImage = `
          linear-gradient(
            45deg,
            rgba(255,255,255,0.1) 25%,
            transparent 25%,
            transparent 50%,
            rgba(255,255,255,0.1) 50%,
            rgba(255,255,255,0.1) 75%,
            transparent 75%,
            transparent
          )
        `;
        stripe.style.backgroundSize = "4px 4px";
        stripe.style.width = `${stripeWidth}px`; // 设置条纹宽度
        stripe.style.height = `${stripeHeight}px`; // 设置条纹高度
        const colors = [
          "#232836",
          "#2f423a", // 浅蓝灰
          "#6a6957", // 深灰蓝
          "#36394e", // 深棕灰
          "#563735", // 深棕
          "#4e4e5d", // 深灰棕
          "#33344b", // 深绿灰
          "#351c1b", // 深蓝
        ];
        const randomColor = colors[i % colors.length];
        stripe.style.backgroundColor = randomColor;
        container.appendChild(stripe);
      }
    },
  },
};
</script>

  <style scoped>
/* 全局重置样式 */
html, body {
  margin: 0;
  padding: 0;
  overflow-x: hidden;
  width: 100%;
  height: 100%;
  box-sizing: border-box;
}

* {
  box-sizing: inherit;
}

/* 隐藏水平滚动条 */
::-webkit-scrollbar-horizontal {
  display: none;
}

/* 手动登录按钮样式 */
.manual-login {
  position: fixed;
  top: 2%;
  right: 2%;
  z-index: 100;
  /* 确保按钮在其他元素之上 */
}

.icon {
  width: 160px;
  /* 调整图片宽度 */
  height: 120px;
  /* 调整图片高度 */
}

.icon-1 {
  width: 160px;
  /* 调整图片宽度 */
  height: 160px;
  /* 调整图片高度 */
}

.icon-2 {
  width: 120px;
  /* 调整图片宽度 */
  height: 120px;
  /* 调整图片高度 */
}

.icon-3 {
  width: 150px;
  /* 调整图片宽度 */
  height: 150px;
  /* 调整图片高度 */
}

.arrow-animation {
  position: fixed;
  bottom: 10px;
  left: 50%;
  transform: translateX(-50%);
  z-index: 1000;
}

.manual-login button {
  padding: 1% 2%;
  font-size: 1rem;
  cursor: pointer;
}

.page-home {
  position: relative;
  width: 100%;
  min-height: 100vh;
  background-color: transparent;
  overflow-x: hidden;
  padding: 0;
  margin: 0;
  box-sizing: border-box;
  /* 添加盒模型计算方式 */
}

.vertical-sidebar {
  position: fixed;
  top: 0;
  left: 5%;
  width: 5%;
  height: 100%;
  background-color: #a43c3c;
  color: white;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding-top: 20px;
  box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.3),
    -2px -2px 10px rgba(255, 255, 255, 0.1);
  z-index: 2;
}

.vertical-block-1 {
  position: fixed;
  top: 0%;
  left: 15%;
  width: 10%;
  height: 35%;
  background-color: #a75959;
  color: white;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding-top: 20px;
  box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.3),
    -2px -2px 10px rgba(255, 255, 255, 0.1);
  z-index: 2;
  transform: translateY(-100%);
  animation: slideDown-1 1s forwards;
}

.vertical-block-2 {
  position: fixed;
  top: 120%;
  left: 25%;
  width: 10%;
  height: 35%;
  background-color: #a2837f;
  color: white;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding-top: 20px;
  box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.3),
    -2px -2px 10px rgba(59, 50, 50, 0.1);
  z-index: 2;
  transform: translateY(-100%);
  animation: slideDown-2 1s forwards;
  animation-delay: 0.2s;
}

.vertical-block-3 {
  position: fixed;
  top: 0%;
  left: 35%;
  width: 10%;
  height: 35%;
  background-color: #8d93b1;
  color: white;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding-top: 20px;
  box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.3),
    -2px -2px 10px rgba(255, 255, 255, 0.1);
  z-index: 2;
  transform: translateY(-100%);
  animation: slideDown-3 1s forwards;
  animation-delay: 0.4s;
}

.vertical-block-4 {
  position: fixed;
  top: 0%;
  left: 45%;
  width: 10%;
  height: 35%;
  background-color: #88a48e;
  color: white;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding-top: 20px;
  box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.3),
    -2px -2px 10px rgba(255, 255, 255, 0.1);
  z-index: 2;
  transform: translateY(-100%);
  animation: slideDown-4 1s forwards;
  animation-delay: 0.8s;
}

.vertical-block-5 {
  position: fixed;
  top: 0%;
  left: 55%;
  width: 10%;
  height: 35%;
  background-color: #b5aa92;
  color: white;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding-top: 20px;
  box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.3),
    -2px -2px 10px rgba(255, 255, 255, 0.1);
  z-index: 2;
  transform: translateY(-100%);
  animation: slideDown-5 1s forwards;
  animation-delay: 1s;
}

.vertical-block-6 {
  position: fixed;
  top: 0%;
  left: 65%;
  width: 10%;
  height: 35%;
  background-color: #90a983;
  color: white;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding-top: 20px;
  box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.3),
    -2px -2px 10px rgba(255, 255, 255, 0.1);
  z-index: 2;
  transform: translateY(-100%);
  animation: slideDown-6 1s forwards;
  animation-delay: 1.1s;
}

.vertical-block-7 {
  position: fixed;
  top: 0%;
  left: 75%;
  width: 10%;
  height: 35%;
  background-color: rgb(165, 141, 164);
  color: white;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding-top: 20px;
  box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.3),
    -2px -2px 10px rgba(255, 255, 255, 0.1);
  z-index: 2;
  transform: translateY(-100%);
  animation: slideDown-7 1s forwards;
  animation-delay: 1.3s;
}

.vertical-block-8 {
  position: fixed;
  top: 0%;
  left: 85%;
  width: 10%;
  height: 35%;
  background-color: #89a68f;
  color: white;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding-top: 20px;
  box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.3),
    -2px -2px 10px rgba(255, 255, 255, 0.1);
  z-index: 2;
  transform: translateY(-100%);
  animation: slideDown-8 1s forwards;
  animation-delay: 1.5s;
}

.vertical-block-9 {
  position: fixed;
  top: 120%;
  left: 40%;
  width: 10%;
  height: 35%;
  background-color: #993034;
  color: white;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding-top: 20px;
  /* box-shadow: 2px 0 5px rgba(0, 0, 0, 0.1); */
  box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.3),
    -2px -2px 10px rgba(255, 255, 255, 0.1);
  z-index: 2;
  transform: translateY(-100%);
  animation: slideDown-9 1s forwards;
  animation-delay: 0.6s;
}

.vertical-block-10 {
  position: fixed;
  top: 120%;
  left: 55%;
  width: 10%;
  height: 35%;
  background-color: #48507c;
  color: white;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding-top: 20px;
  box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.3),
    -2px -2px 10px rgba(255, 255, 255, 0.1);
  z-index: 2;
  transform: translateY(-100%);
  animation: slideDown-10 1s forwards;
}

.text-block {
  display: flex;
  justify-content: center;
  align-items: center;
  white-space: nowrap;      /* 不换行 */
}

@keyframes slideDown-1 {
  to {
    transform: translateY(120%);
    /* 最终位置 */
  }
}

@keyframes slideDown-2 {
  to {
    transform: translateY(-300%);
    /* 最终位置 */
  }
}

@keyframes slideDown-3 {
  to {
    transform: translateY(100%);
    /* 最终位置 */
  }
}

@keyframes slideDown-4 {
  to {
    transform: translateY(160%);
    /* 最终位置 */
  }
}

@keyframes slideDown-5 {
  to {
    transform: translateY(180%);
    /* 最终位置 */
  }
}

@keyframes slideDown-6 {
  to {
    transform: translateY(10%);
    /* 最终位置 */
  }
}

@keyframes slideDown-7 {
  to {
    transform: translateY(100%);
    /* 最终位置 */
  }
}

@keyframes slideDown-8 {
  to {
    transform: translateY(160%);
    /* 最终位置 */
  }
}

@keyframes slideDown-9 {
  to {
    transform: translateY(-343%);
    /* 最终位置 */
  }
}

@keyframes slideDown-10 {
  to {
    transform: translateY(-310%);
    /* 最终位置 */
  }
}

.sidebar-item {
  margin: 0px 0;
  font-size: 27px;
  writing-mode: vertical-rl;
  /* 文字竖着显示 */
  text-orientation: upright;
  /* 文字直立显示 */
  cursor: pointer;
  transition: color 0.3s, transform 0.3s;
}

.sidebar-block-item {
  margin: 0px 0;
  font-size: 27px;
  cursor: pointer;
  transition: color 0.3s, transform 0.3s;
}

.sidebar-item:hover {
  color: #ffffff;
  transform: scale(1.1);
}

.page-home {
  position: relative;
  height: 100vh;
  overflow: hidden;
  width: 100vw;
  /* 使用视窗宽度 */
  max-width: 100%;
  /* 确保不超过父容器 */
}

.pages-container {
  width: 100%;
  height: 100%;
  will-change: transform;
}

.page {
  height: 100vh;
  width: 100vw;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

/* 优化动画效果 */
.fade-up-enter-active {
  transition: all 0.8s ease;
}

.fade-up-enter-from {
  opacity: 0;
  transform: translateY(20px);
}

/* 保持原有动画 */
@keyframes move {
  /* 原有关键帧保持不变 */
}

/* 响应式优化 */
@media (max-width: 600px) {
  .pages-container {
    transition-duration: 0.6s;
  }
}

/* 导航栏样式 */
.navbar {
  width: 100%;
  /* 使用百分比而非视窗单位 */
  background-color: rgba(128, 128, 128, 0.6);
  /* 设置为略微透明的灰色 */
  display: flex;
  justify-content: center;
  align-items: center;
  padding: clamp(0.5rem, 1.5vw, 2rem) 0;
  /* 响应式导航栏高度 */
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  /* 添加right:0确保宽度固定 */
  z-index: 10;
  overflow: hidden;
  /* 防止溢出 */
  box-sizing: border-box;
  /* 添加盒模型计算方式 */
}

.navbar-container {
  width: 100%;
  max-width: 1600px;
  /* 设置最大宽度，防止在超宽屏幕上过宽 */
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 0;
  /* 移除内边距，让导航项可以充分利用空间 */
  overflow: hidden;
  /* 防止溢出 */
}

.nav-links {
  display: flex;
  gap: 0;
  /* 移除gap，使用space-evenly代替 */
  flex-grow: 1;
  justify-content: space-evenly;
  /* 改为space-evenly，均匀分布并有一定的中间空间 */
  flex-wrap: wrap;
  /* 允许在窄屏幕上换行 */
  padding: 0 1.5%;
  /* 进一步减小左右内边距 */
  width: 97%;
  /* 进一步增加宽度 */
  margin: 0 auto;
  /* 水平居中 */
}

.nav-link,
.logout-button {
  color: white;
  text-decoration: none;
  font-size: clamp(1.2rem, 2.2vw, 2.8rem);
  /* 增大响应式字体大小 */
  transition: all 0.3s ease;
  /* 添加过渡效果 */
  cursor: pointer;
  /* 确保按钮样式 */
  background: none;
  border: none;
  font-family: inherit;
  /* 继承字体样式 */
  text-align: left;
  white-space: nowrap;
  /* 防止文本换行 */
  padding: 0.5rem;
  /* 增加可点击区域 */
  font-weight: 500;
  /* 增加字重，使文本更清晰 */
}

.button-link {
  color: white;
  text-decoration: none;
  font-size: 1.6rem;
  flex-direction: column;
  /* 增大字体大小 */
  transition: all 0.3s ease;
  /* 添加过渡效果 */
  cursor: pointer;
  /* 确保按钮样式 */
  background: none;
  border: none;
  font-family: inherit;
  /* 继承字体样式 */
  text-align: left;
}

/* 删除重复的样式定义 */

.nav-link:hover,
.logout-button:hover {
  transform: scale(1.2);
  /* 恢复鼠标悬停时放大效果 */
  color: rgb(48, 124, 70);
  /* 鼠标悬停时变为深绿色 */
  text-shadow: 0.3rem 0.4rem 0.3rem #1e1008a3;
  /* 恢复原来的文本阴影 */
  transition: transform 0.2s ease, color 0.2s ease, text-shadow 0.2s ease;
  /* 添加过渡效果 */
}

.poem-line {
  font-size: 1.5rem;
  margin: 0.5rem 0;
  opacity: 0;
  animation: fadeUp 0.8s forwards;
}

.page {
  width: 100%;
  height: 100%;
  overflow: auto;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: start;
  background-image: url("../../static/background.png");
  background-size: cover;
  background-position: center;
  background-attachment: fixed;
  /* z-index: 1000; */
}

/* 内容主容器样式 */
.content {
  position: relative;
  z-index: 1;
  /* 设置内容在背景图上层 */
  display: flex;
  flex-direction: column;
  /* 垂直排列子元素 */
  align-items: center;
  /* 水平居中 */
  justify-content: center;
  /* 子元素之间均匀分布 */
  margin: 0;
  /* 确保没有外边距 */
  width: 100%;
  min-height: 100vh;
  /* 内容最小高度为视口高度 */
  color: #fff;
  text-align: center;
  /* 文本居中 */
}

.content.hidden {
  opacity: 0;
}

/* 标题容器样式 */
.title-wrapper {
  position: relative;
  width: 100%;
  height: 20%;
  /* 确保容器有足够的高度 */
  margin-bottom: 0%;
  /* 调整与描述之间的距离 */
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 5%;
  /* 添加 margin-top 以向下移动标题 */
  padding: 15% 0% 12% 0%;
  /* 调整顶部内边距以适应固定导航栏 */
}

.title-container {
  position: absolute;
  text-align: center;
  line-height: 0.9;
  /* 调整行高，减小两行之间的间距 */
}

/* 标题样式 */
.title {
  font-size: 9vw;
  font-family: "hongleixingshu";
  color: #ffffff;
  text-shadow: 0.4vw 0.5vw 0.4vw #1e1008a3;
  /* 添加文本阴影 */
  margin: 0;
  /* 移除可能的外边距 */
}

.line1 {
  display: inline-block;
  text-shadow: 0.4vw 0.5vw 0.4vw #1e1008a3;
  /* 添加文本阴影 */
  /* animation: move 20s infinite; */
  font-size: 10vw;
  margin-bottom: 1%;
}

.line2 {
  display: inline-block;
  text-shadow: 0.4vw 0.5vw 0.4vw #1e1008a3;
  /* 添加文本阴影 */
  /* animation: movesmall 20s infinite; */
}

/* 描述文本样式 */
.description {
  max-width: 80%;
  font-size: 1.4rem;
  line-height: 2rem;
  text-align: center;
  color: #ffffff;
  text-shadow: 0.15rem 0.25rem 0.15rem #1e1008a3;
  /* 添加文本阴影 */
  position: absolute;
  top: 70%;
  left: 50%;
  transform: translate(-50%, -50%);
  white-space: nowrap; /* 不允许文本换行 */
}

/* 页脚样式 */
.footer {
  text-align: center;
  margin-top: 1%;
  margin-bottom: 1%;
  position: absolute;
  /* 使用绝对定位 */
  bottom: 0;
  /* 将footer固定在页面底部 */
  left: 50%;
  /* 将footer水平居中 */
  transform: translateX(-5%);
  /* 调整位置使其居中 */
  z-index: 1;
  /* 确保footer在其他元素之上 */
  width: 100%;
  /* 确保footer宽度为100% */
}

/* 公共字体样式 */
.font {
  font-family: "hongleixingshu";
}

/* 页脚文本样式，块级元素 */
.font_2 {
  display: block;
  /* 设置为块级元素以便每个项目独占一行 */
  font-size: 0.8rem;
  font-family: "HYQiHei";
  color: #ffffff;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.5);
  /* 添加文本阴影 */
  margin: 0.2rem 0;
  /* 调整每行之间的间距 */
}

/* page1 样式 */
.page1 {
  position: relative;
  width: 100%;
  height: 102vh;
  /* 覆盖整个页面 */
  background: rgba(0, 0, 0, 0.75);
  overflow: hidden;
  /* 移除多余的滚动条 */
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: space-between;
  /* 确保内容和footer之间的间距 */
  padding: 0;
  /* 确保没有内边距 */
  margin: 0;
  /* 确保没有外边距 */
  animation: changeBackground 2s 7.5s forwards;
  /* 在固定时间后将背景色改为透明 */
}

.text-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  margin-bottom: 2%;
  margin-top: 2%;
  /* 调低位置 */
  animation: fadeIn 1s ease-in-out forwards;
  position: relative;
  /* 改为相对定位，避免绝对定位影响布局 */
  z-index: 3;
  /* 确保文字在图片和背景之上 */
  opacity: 0;
}

.font_home {
  text-shadow: 0.15rem 0.25rem 0.15rem #1e1008a3;
  /* 添加文本阴影 */
  font-size: 6vh;
  font-family: "hongleixingshu";
  line-height: 9vh;
  color: #ffffff;
}

.self-center {
  align-self: center;
}

.pos-home {
  opacity: 0;
  animation: fadeIn 1s forwards;
  margin: 1% 0;
}

.image-container {
  position: absolute;
  width: 100%;
  height: 100%;
}

.image_ren {
  opacity: 0;
  z-index: 2;
  position: absolute;
  max-width: 30%;
  /* 确保图片不会太大 */
  height: auto;
}

.image_ren:nth-child(1) {
  top: 5%;
  left: 3%;
  animation: fadeInHold 1s 1s forwards, disappear 1.5s 7.5s forwards;
}

.image_ren:nth-child(2) {
  top: 15%;
  right: 13%;
  transform: scale(2.5);
  animation: fadeInHold 1s 2.5s forwards, disappear 1.5s 7.5s forwards;
}

.image_ren:nth-child(3) {
  bottom: 8%;
  left: 0%;
  transform: scale(1);
  animation: fadeInHold 1s 4s forwards, disappear 1.5s 7.5s forwards;
}

.image_ren:nth-child(4) {
  bottom: 10%;
  right: 3%;
  animation: fadeInHold 1s 5.5s forwards, disappear 1.5s 7.5s forwards;
}

/* 响应式设计 */
/* 小屏幕设备 */
@media (max-width: 600px) {
  .title {
    font-size: 3rem;
  }

  .nav-link {
    font-size: 1.1rem;
    /* 在小屏幕上的字体大小 */
    padding: 0.3rem;
  }

  .nav-links {
    gap: 0.5rem;
    /* 在小屏幕上减小间距 */
    justify-content: space-around;
  }

  .font_2 {
    font-size: 0.75rem;
  }
  
  .navbar {
    padding: 1% 0;
    /* 减小导航栏高度 */
  }
}

/* 中等屏幕设备 */
@media (min-width: 601px) and (max-width: 1024px) {
  .nav-link {
    font-size: calc(1rem + 0.6vw);
    /* 增大动态字体大小 */
  }
  
  .nav-links {
    gap: 1.5vw;
    /* 动态调整间距 */
  }
  
  .navbar {
    padding: 1.5% 0;
    /* 调整导航栏高度 */
  }
}

/* 大屏幕设备 */
@media (min-width: 1025px) and (max-width: 1600px) {
  .nav-link {
    font-size: calc(1.2rem + 0.6vw);
    /* 增大动态字体大小 */
  }
}

/* 超宽屏幕 */
@media (min-width: 1601px) {
  .navbar-container {
    max-width: 1600px;
    /* 限制最大宽度 */
  }
  
  .nav-link {
    font-size: 2.1rem;
    /* 增大固定字体大小 */
  }
  
  .nav-links {
    width: 90%;
    /* 在超宽屏幕上进一步增加宽度 */
    padding: 0 1%;
    /* 在超宽屏幕上的内边距更小 */
  }
}

@keyframes changeBackground {
  from {
    background: rgba(0, 0, 0, 0.7);
  }

  to {
    background: rgba(0, 0, 0, 0);
  }
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }

  to {
    opacity: 1;
  }
}

@keyframes fadeInHold {
  from {
    opacity: 0;
  }

  to {
    opacity: 1;
  }
}

@keyframes disappear {
  0% {
    opacity: 1;
  }

  100% {
    opacity: 0;
  }
}

@keyframes move {
  0% {
    transform: translate(0, 0);
    color: rgb(255, 255, 255);
    font-size: 10rem;
  }

  20% {
    transform: translate(12px, 0);
    color: black;
    font-size: 9.5rem;
  }

  60% {
    transform: translate(10px, -10px);
    color: rgb(248, 200, 6);
    font-size: 11rem;
  }

  80% {
    transform: translate(0, -9px);
    color: rgb(0, 0, 0);
    font-size: 9.5rem;
  }

  100% {
    transform: translate(0, 0);
    color: rgb(255, 255, 255);
    font-size: 10rem;
  }
}

@keyframes movesmall {
  0% {
    transform: translate(0, 0);
    color: rgb(255, 255, 255);
    font-size: 8rem;
  }

  20% {
    transform: translate(12px, 0);
    color: black;
    font-size: 8.5rem;
  }

  60% {
    transform: translate(10px, -10px);
    color: rgb(202, 168, 33);
    font-size: 7.5rem;
  }

  80% {
    transform: translate(0, -9px);
    color: rgb(0, 0, 0);
    font-size: 8.5rem;
  }

  100% {
    transform: translate(0, 0);
    color: rgb(255, 255, 255);
    font-size: 8rem;
  }
}

/* 基础样式 */
:root {
  /* 专业配色方案 */
  --color1: #e6f4f1;
  /* 冰霜白 */
  --color2: #c3e4e6;
  /* 薄雾蓝 */
  --color3: #9fd3d7;
  /* 浅水绿 */
  --color4: #7cb7c8;
  /* 静谧蓝 */
  --color5: #5a9fb5;
  /* 深海蓝 */
}

.stripes-container {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  /* display: grid; 条纹铺满屏幕不能使用grid */
  display: flex;
  flex-direction: row;
  grid-template-columns: repeat(auto-fit, 100px);
  /* 固定条纹宽度 */
  grid-auto-flow: dense;
  /* 密集填充模式 */
  gap: 0px;
  /* 精致间隔 */
  z-index: -2;
  pointer-events: none;
  background-color: rgb(0, 0, 0);
}

.overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.01);
  /* 半透明黑色蒙版 */
  z-index: -1;
  /* 确保蒙版在背景条纹之上 */
  pointer-events: none;
  /* 确保蒙版不影响交互 */
}
</style>
