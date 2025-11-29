<template>
    <div class="page">
        <!-- 页面其它部分，比如导航栏等 -->
        <div class="background dna-container"></div>
        <span class="text text_3 pos_2" @click="goHome">《主页</span>
        <span class="text text_2 pos">千年回响</span>

        <!-- 背景粒子层 -->
        <ParticleLayer />

        <!-- 时间线区域，独立滚动 -->
        <div class="timeline-wrapper">
            <!-- 古今箭头 -->
            <div class="timeline-arrow">
                <span class="arrow-text-l">古</span>
                <div class="arrow"></div>
                <span class="arrow-text-r">今</span>
            </div>

            <div class="timeline" ref="timelineContainer">
                <div v-for="(item, index) in dataPoints" :key="index" ref="timelineRows"
                    :class="['timeline-row', { active: activeIndex === index }]" @click="handleTimelineClick(item.id)"
                    style="cursor: pointer;">
                    <!-- 左侧卡片（古代） -->
                    <div class="timeline-card left">
                        <div class="image-wrapper">
                            <img :src="item.ancient_img" class="card-image" alt="古代图片" />
                            <div class="year-label">
                                {{ (item.ancient_year < 0 ? '公元前' + Math.abs(item.ancient_year) : item.ancient_year)
                                    + '年' }} </div>
                            </div>
                            <div class="card-content">
                                <h3>{{ item.ancient_title }}</h3>
                                <p>{{ item.ancient_description }}</p>
                            </div>
                        </div>

                        <!-- 右侧卡片（现代） -->
                        <div class="timeline-card right">
                            <div class="image-wrapper">
                                <img :src="item.modern_img" class="card-image" alt="现代图片" />
                                <div class="year-label">
                                    {{ (item.modern_year < 0 ? '公元前' + Math.abs(item.modern_year) : item.modern_year)
                                        + '年' }} </div>
                                </div>
                                <div class="card-content">
                                    <h3>{{ item.modern_title }}</h3>
                                    <p>{{ item.modern_description }}</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="bottom">© 2025 千年回响</div>
            </div>
</template>

<script>
import axios from "axios";
import ParticleLayer from "@/components/ParticleLayer.vue";

export default {
    components: {
        ParticleLayer,
    },
    data() {
        return {
            canvasWidth: window.innerWidth,
            canvasHeight: window.innerHeight,
            dataPoints: [],
            activeIndex: 0,      // 初始时选中第一个
            isScrolling: false   // 防止滚动事件连续触发
        };
    },
    async mounted() {
        if (localStorage.getItem("Reload") === "true") {
            localStorage.setItem("Reload", false);
            window.location.reload();
        }
        await this.fetchData();
        this.$nextTick(() => {
            // 确保数据加载后 DOM 渲染完成
            const container = this.$refs.timelineContainer;
            container.addEventListener("wheel", this.handleWheel, { passive: false });
        });
    },
    beforeDestroy() {
        const container = this.$refs.timelineContainer;
        if (container) {
            container.removeEventListener("wheel", this.handleWheel);
        }
    },
    methods: {
        goHome() {
            this.$router.push({ name: "homepage" });
        },
        handleTimelineClick(id) {
            this.$router.push({
                path: "/trans",
                query: { id: id },
            });
        },
        async fetchData() {
            try {
                const response = await axios.get(this.$baseUrl + "/api/timeline/get_all");
                console.log("数据获取成功", response.data); // 假设数据已按时间顺序返回
                this.dataPoints = response.data;
            } catch (error) {
                this.$message.error({ message: "数据获取失败", duration: 1000 });
            }
        },

        handleWheel(event) {
            // 阻止默认滚动
            event.preventDefault();
            if (this.isScrolling) return;

            const rows = this.$refs.timelineRows; // Vue 2 中 ref="timelineRows" 会自动收集为数组
            if (!rows || rows.length === 0) return;

            // 根据滚轮方向更新 activeIndex
            if (event.deltaY > 0) {
                // 向下滚动
                if (this.activeIndex < rows.length - 1) {
                    this.activeIndex++;
                }
            } else {
                // 向上滚动
                if (this.activeIndex > 0) {
                    this.activeIndex--;
                }
            }

            // 开始滚动前加锁，防止重复触发
            this.isScrolling = true;
            // 滚动的是 .timeline 容器
            const container = this.$refs.timelineContainer;
            const containerHeight = container.clientHeight;
            // 目标位置：容器高度的 30% 处
            const targetOffset = containerHeight * 0.05;
            const currentScroll = container.scrollTop;

            // 获取目标卡片的位置信息（相对于 viewport）
            const cardRect = rows[this.activeIndex].getBoundingClientRect();
            // 获取容器的位置信息（相对于 viewport）
            const containerRect = container.getBoundingClientRect();
            // 计算目标卡片顶部在容器内的相对位置
            const cardTopInContainer = cardRect.top - containerRect.top;
            // 我们希望该值等于 targetOffset，所以需要调整的滚动距离为：
            const targetScroll = currentScroll + (cardTopInContainer - targetOffset);

            container.scrollTo({
                top: targetScroll,
                behavior: "smooth"
            });

            // 设定滚动完毕后解除锁定（可根据实际效果调整时间）
            setTimeout(() => {
                this.isScrolling = false;
            }, 600);
        }
    }
};
</script>

<style scoped>
/* 父容器固定高度，允许横向滚动 */
.page {
    position: relative;
    width: 100%;
    height: 100vh;
    overflow: hidden;
    /* 禁止整个页面滚动 */
}

/* 背景层 */
.dna-container {
    /* position: absolute; */
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    position: fixed;
    z-index: 0;
}

.background {
    background-image: url("../../static/千年回响.jpg");
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

/* 伪元素在外层包装容器上创建连续竖线 */
.timeline-wrapper::before {
    content: "";
    position: absolute;
    top: 15%;
    bottom: 5%;
    left: 50%;
    /* 根据设计调整位置 */
    transform: translateX(-50%);
    width: 2px;
    background-color: #ccc;
    z-index: 2;
}

/* 整体的时间线容器和布局，和之前类似 */
.timeline {
    width: 100%;
    top: 10%;
    left: 0;
    right: 0;
    bottom: 0;
    margin: 50px auto;
    position: absolute;
    overflow-y: auto;
    padding: 20px;
}

/* 隐藏滚动条 */
.timeline::-webkit-scrollbar {
    display: none;
}

/* 每行 */
.timeline-row {
    display: flex;
    align-items: flex-start;
    /* 使所有子项顶部对齐 */
    justify-content: space-between;
    margin: 0 0 120px 0;
    position: relative;
    transition: all 0.5s ease;
    opacity: 0.6;
    filter: grayscale(100%);
    transform: translateY(0);
}

/* 激活状态：高亮、去灰、上移/下移等 */
.timeline-row.active {
    opacity: 1;
    filter: grayscale(0%);
    transform: translateY(30px);
}

/* 当父元素 .timeline-row 处于 active 状态时，调整 */
.timeline-row.active .timeline-card .year-label {
    top: -20px;
    /* 调整这个值，让文字下探到卡片外 */
}

/* 卡片公共样式 */
/* 卡片容器 */
.timeline-card {
    width: 25%;
    max-height: 300px;
}

/* 限制图片大小，保持一致 */
.image-wrapper {
    width: 100%;
    height: 140px;
    /* 限制卡片宽度 */
    background: #fff;
    border-radius: 20px;
    box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2);
    transition: all 0.5s ease;
    overflow: hidden;
}

/* 图片铺满整个区域 */
.card-image {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

/* 让年份文字部分溢出到卡片之外 */
.year-label {
    position: absolute;
    left: 0px;
    top: -30px;
    /* 调整这个值，让文字下探到卡片外 */
    font-size: 36px;
    font-weight: bold;
    color: #fff;
    text-shadow: 2px 2px 6px rgba(0, 0, 0, 0.5);
    /* 如果背景是深色，可换成更适合的颜色或加半透明背景 */
}

/* 针对左侧卡片的年份标签（保持左侧） */
.timeline-card.left .year-label {
    margin-left: 250px;
    /* right: auto; */
}

/* 针对右侧卡片的年份标签（靠右显示） */
.timeline-card.right .year-label {
    margin-right: 250px;
    left: auto;
}

/* 卡片内容区 */
.card-content {
    width: 120%;
    padding: 0px;
    color: rgb(0, 0, 0);
    font-size: 20px;
    font-family: "仿宋_GB2312", "FangSong", "华文仿宋", serif;
}

/* 左右对齐 */
.timeline-card.left {
    text-align: left;
    margin-left: 250px;
}

.timeline-card.right {
    text-align: left;
    margin-right: 250px;
}

/* 添加古今箭头样式 */
.timeline-arrow {
    position: absolute;
    top: 12%;
    left: 50%;
    transform: translate(-50%, -50%);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 2;
}

.arrow-text-l {
    font-size: 20px;
    font-weight: bold;
    margin-right: 20px;
    color: #ccc;
}

.arrow-text-r {
    font-size: 20px;
    font-weight: bold;
    margin-left: 20px;
    color: #ccc;
}

.arrow {
    width: 600px;
    height: 2px;
    background-color: #ccc;
    position: relative;
}

.arrow::after {
    content: '';
    position: absolute;
    top: -3px;
    right: -10px;
    width: 0;
    height: 0;
    border-top: 5px solid transparent;
    border-bottom: 5px solid transparent;
    border-left: 10px solid #ccc;
}

/* 在小屏幕时垂直布局 */
@media (max-width: 768px) {
    .timeline-row {
        flex-direction: column;
        margin: 40px 0;
    }

    .line {
        display: none;
        /* 或者改为横线 */
    }

    .timeline-card {
        width: 80%;
        max-width: none;
        text-align: center !important;
        margin: 10px 0;
    }
}
</style>