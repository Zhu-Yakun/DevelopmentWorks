<template>
  <div class="shell">
    <div class="background"></div>
    <span class="text text_3 pos_2" @click="handleBack">《返回</span>
    <span class="text text_2 pos">岁月史书</span>

    <!-- 背景粒子层 -->
    <ParticleLayer />

    <div class="shell_body">
      <div class="button">
        <div class="prev" @click="prev">
          <i class="iconfont icon-backward_filled"></i>
        </div>
        <div class="next" @click="next">
          <i class="iconfont icon-forward_filled"></i>
        </div>
      </div>
      <div class="shell_slider" :style="{ transform: sliderTransform }">
        <div v-for="(item, index) in items" :key="index" class="item"
          :class="{ 'item--active': currentIndex === index }" :style="itemStyle">
          <div class="frame">

            <div class="box front">
              <!-- ✅ 独立图层：仅作为背景使用 -->
              <div class="box front img-layer" :style="{ backgroundImage: `url(${getImgUrl(item.img)})` }"></div>

              <!-- 黑色遮罩层 -->
              <div class="overlay"></div>

              <h1>{{ item.year < 0 ? "公元前" + Math.abs(item.year) : item.year }}年</h1>
                  <h2>{{ item.title }}</h2>
                  <span>{{ item.description }}</span>
            </div>
            <!-- 
            <div class="box front img" :style="{ backgroundImage: `url(${getImgUrl(item.img)})` }">
              <h1>
                {{
                  (item.year < 0 ? "公元前" + Math.abs(item.year) : item.year) + "年" }} </h1>
                  <h2>{{ item.title }}</h2>
                  <span>{{ item.description }}</span>
            </div> -->
            <div class="box left img" :style="{ backgroundImage: `url(${getImgUrl(item.img)})` }"></div>
            <div class="box right img" :style="{ backgroundImage: `url(${getImgUrl(item.img)})` }"></div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import ParticleLayer from "@/components/ParticleLayer.vue";

export default {
  data() {
    return {
      originalBackground: "",
      currentIndex: 0,
      itemWidth: 0,
      itemHeight: 0,
      margin: 20,
      interval: null,
      intervalTime: 3000,
      items: [],
      defaultImage: this.$baseUrl + "/static/KnowledgePair/default.jpg",
      isScrolling: false, // 防止滚动事件连续触发
    };
  },
  components: {
    ParticleLayer,
  },
  computed: {
    itemStyle() {
      return {
        width: `${this.itemWidth - this.margin * 2}px`,
        height: `${this.itemHeight}px`,
        margin: `0 ${this.margin}px`,
      };
    },
    sliderTransform() {
      return `translate3d(${this.currentIndex * -this.itemWidth + // 当前卡片偏移
        window.innerWidth / 2 - // 视口居中
        this.itemWidth / 2 // 卡片自身居中
        }px, 0, 0)`;
    },
  },
  async mounted() {
    if (localStorage.getItem("Reload") === "true") {
      localStorage.setItem("Reload", false);
      window.location.reload();
    }
    // 保存进入时的背景状态
    this.originalBackground = document.body.style.backgroundImage;
    const { data } = await axios.get(
      this.$baseUrl + "/api/timeline/get_by_id",
      {
        params: { record_id: this.$route.query.id },
      }
    );
    // 构建符合要求的items数组
    this.items = [
      // 古代知识作为第一项
      {
        title: data.data.ancient_title,
        description: data.data.ancient_description,
        year: data.data.ancient_year,
        img: data.data.ancient_img,
      },
      // 列表项展开
      ...data.data.list_items.map((item) => ({
        title: item.title,
        description: item.description,
        year: item.year,
        img: item.img,
      })),
      // 现代理论作为最后一项
      {
        title: data.data.modern_title,
        description: data.data.modern_description,
        year: data.data.modern_year,
        img: data.data.modern_img,
      },
    ];
    this.init();
    window.addEventListener("resize", this.handleResize);

    // 添加鼠标滚轮事件监听
    window.addEventListener("wheel", this.handleWheel, { passive: false });

    // 在mounted函数末尾添加
    this.$nextTick(() => {
      const firstItem = this.items[0];
      if (firstItem) {
        // document.body.style.backgroundImage = `url(${this.getImgUrl(
        //   firstItem.img
        // )})`;
      }
    });
  },
  beforeDestroy() {
    // 恢复原始背景
    document.body.style.backgroundImage = this.originalBackground;
    clearInterval(this.interval);
    window.removeEventListener("resize", this.handleResize);

    // 移除鼠标滚轮事件监听
    window.removeEventListener("wheel", this.handleWheel);
  },
  methods: {
    getImgUrl(relativePath) {
      // 基础路径配置
      const basePath =
        process.env.NODE_ENV === "development" ? this.$baseUrl + "/" : "/";

      // 处理空值和默认路径
      if (!relativePath) return `${basePath}KnowledgePair/default.jpg`;

      // 移除可能存在的多余static前缀
      // const cleanPath = relativePath.replace(/^static\//, '');

      return `${relativePath}`;
    },
    handleWheel(event) {
      // 阻止默认滚动
      event.preventDefault();
      if (this.isScrolling) return;

      // 开始滚动前加锁，防止重复触发
      this.isScrolling = true;

      // 根据滚轮方向更新 activeIndex
      if (event.deltaY > 0) {
        // 向下滚动
        this.next();
      } else {
        // 向上滚动
        this.prev();
      }
      // 设定滚动完毕后解除锁定（可根据实际效果调整时间）
      setTimeout(() => {
        this.isScrolling = false;
      }, 400);
    },
    init() {
      this.move(0);
      this.handleResize();
      this.startTimer();
    },
    handleBack() {
      // 这里添加具体的返回逻辑，例如：
      this.$router.go(-1);
      //   console.log("返回按钮被点击");
    },
    handleResize() {
      this.itemWidth = Math.max(window.innerWidth * 0.2, 275);
      this.itemHeight = window.innerHeight * 0.5;

      // 修正容器总宽度（增加一个卡片宽度作为缓冲）
      this.$el.querySelector(".shell_slider").style.width = `${this.itemWidth * (this.items.length + 1)
        }px`;
    },
    updateFrameTransforms() {
      this.$nextTick(() => {
        const items = this.$el.querySelectorAll(".item");
        items.forEach((item, i) => {
          const frame = item.querySelector(".frame");
          if (i === this.currentIndex) {
            frame.style.transform = "perspective(1200px)";
          } else {
            const rotate = i < this.currentIndex ? 40 : -40;
            frame.style.transform = `perspective(1200px) rotateY(${rotate}deg)`;
          }
        });
      });
    },
    move(index) {
      if (index < 0) index = this.items.length - 1;
      if (index >= this.items.length) index = 0;
      this.currentIndex = index;

      this.updateFrameTransforms();

      // 更新背景图逻辑
      const frontBox = this.$el.querySelector(
        `.item:nth-child(${index + 1}) .front`
      );
      if (frontBox) {
        // document.body.style.backgroundImage = frontBox.style.backgroundImage;
      }
    },
    prev() {
      this.move(this.currentIndex - 1);
      this.startTimer();
    },
    next() {
      this.move(this.currentIndex + 1);
      this.startTimer();
    },
    startTimer() {
      clearInterval(this.interval);
      this.interval = setInterval(() => {
        this.move(this.currentIndex + 1);
      }, this.intervalTime);
    },
  },
};
</script>

<style scoped>
.home-link .link {
  color: #ffffff;
  /* 颜色使用白色 */
  font-size: 2rem;
  /* 增大字体大小 */
  font-family: "hongleixingshu";
  text-decoration: none;
}

.background {
  background-image: url("../../static/千年回响.jpg");
  background-repeat: no-repeat;
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  /* 淡化背景 */
  opacity: 0.6;
}

.text {
  z-index: 99999;
  text-shadow:
    0.31rem 0.31rem 0.31rem #1e1008a3,
    -0.3px -0.3px 0 #1e1008a3,
    0.3px -0.3px 0 #1e1008a3,
    -0.3px 0.3px 0 #1e1008a3,
    0.3px 0.3px 0 #1e1008a3;
}

.text_3 {
  color: #ffffff;
  font-size: 3rem;
  font-family: "hongleixingshu";
  line-height: 2.16rem;
}

.pos_2 {
  position: absolute;
  left: 3.76rem;
  top: 3.27rem;
  cursor: pointer;
}

.text_2 {
  color: #ffffff;
  font-size: 4.3rem;
  font-family: "hongleixingshu";
  line-height: 3.3rem;
}

.pos {
  position: absolute;
  left: 50%;
  top: 1.99rem;
  transform: translateX(-50%);
}

/* 保持与原生HTML完全一致的样式 */
* {
  padding: 0;
  margin: 0;
}

html,
body {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-size: cover;
  overflow: hidden;
  transition: background-image 0.7s ease-in-out;
}

.shell {
  position: relative;
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
  height: 100%;
  box-sizing: border-box;
  background: rgba(99, 99, 99, 0.9);
}

.button {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 350px;
  position: absolute;
  left: 50%;
  transform: translateX(-50%);
  bottom: 1%;
}

.prev,
.next {
  transition: transform 0.25s ease;
  z-index: 99999;
  bottom: 5px;
}

.prev i,
.next i {
  font-size: 60px;
  color: #fff;
  cursor: pointer;
}

/* 添加透视容器 */
.shell_body {
  perspective: 1000px;
  width: 100%;
  height: 100%;
  padding: 20px 0 150px 0;
  overflow: hidden;
}

.shell_slider {
  top: 20%;
  position: relative;
  transition: transform 1s ease-in-out;
  background: transparent;
}

.item {
  position: relative;
  float: left;
  transition: all 1s ease-in-out;
}

.item--active {
  z-index: 10;
}

.frame {
  position: relative;
  width: 100%;
  height: 100%;
  transition: transform 1s ease-in-out;
  transform-style: preserve-3d;
}

.frame:after {
  content: "";
  position: absolute;
  bottom: -16%;
  width: 100%;
  height: 60px;
  background: #ffffff1c;
  box-shadow: 0px 0px 15px 5px #ffffff1c;
  transform: rotateX(90deg) translate3d(0px, -20px, 0px);
}

.box {
  display: flex;
  flex-direction: column;
  align-items: center;
  position: absolute;
  width: 100%;
  height: 100%;
  border: 4px solid #fff;
  perspective: 1000px;
  transform-style: preserve-3d;
  justify-content: flex-start !important;
  /* 顶部对齐 */
  padding-top: 8% !important;
  /* 增加顶部间距 */
}

.box h1,
.box h2,
.box span {
  color: #fff;
  transform: translateZ(20px);
  font-family: "hongleixingshu";
  text-shadow:
    0.31rem 0.31rem 0.31rem #000000a3,
    -0.5px -0.5px 0 #000000a3,
    0.5px -0.5px 0 #000000a3,
    -0.5px 0.3px 0 #000000a3,
    0.5px 0.5px 0 #000000a3;
}

.box h1 {
  font-size: 3vw !important;
  /* 响应式字体 */
  line-height: 1.2;
  margin: 0 0 2vh !important;
  /* 增加下间距 */
  /* text-shadow: 0 0 10px #333; */
}

.box h2 {
  font-size: 1.6vw !important;
  /* 响应式字体 */
  line-height: 1.2;
  margin: 0 0 2vh !important;
  /* 增加下间距 */
  /* text-shadow: 0 0 10px #333; */
  /* 深色阴影 */
}

.box span {
  font-size: 1.0vw !important;
  position: absolute;
  bottom: 20px;
  padding: 0 25px;
  /* text-shadow: 0 0 10px #333; */
  /* 深色阴影 */
  font-family: "仿宋_GB2312", "FangSong", "华文仿宋", serif;
  font-weight: bold;
  text-align: left;
}

.front,
.left,
.right {
  box-shadow: 0 0 50px rgba(255, 255, 255, 0.8);
  filter: hue-rotate(-20deg) saturate(120%);
  /* box-shadow: 0 0 50px #ffffff; */
  background-size: cover;
}

.right,
.left {
  top: 0;
  width: 60px;
  backface-visibility: hidden;
}

.left {
  left: 0;
  border-left-width: 5px;
  transform: translate3d(1px, 0, -60px) rotateY(-90deg);
  transform-origin: 0%;
}

.right {
  right: 0;
  border-right-width: 5px;
  transform: translate3d(-1px, 0, -60px) rotateY(90deg);
  transform-origin: 100%;
}

.img-layer {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-size: cover;
  background-position: center;
  opacity: 0.6;
  /* 只背景图透明 */
  z-index: -1;
  /* 放到底层，不影响 h1 h2 span */
  pointer-events: none;
  /* 不拦截鼠标事件 */
}


.overlay {
  position: absolute;
  inset: 0;
  background: rgba(0, 0, 0, 0.2);
  /* 黑色透明层 */
  z-index: -1;
}

.img {
  opacity: 0.5;
  z-index: -1;
}
</style>