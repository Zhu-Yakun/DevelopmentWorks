<template>
  <div class="flex-col justify-start relative page">
    <div class="background"></div>
    <!-- <div class="overlay"></div> -->
    <span class="text text_3 pos_2" @click="goHome">《主页</span>
    <span class="text text_2 pos">智鉴图谱</span>

    <!-- 背景粒子层 -->
    <ParticleLayer />

    <div class="box content-wrapper">

      <!-- 选择栏 -->
      <div class="select-bar">
        <button v-for="item in itemList" :key="item" @click="selectItemHandler(item)"
          :class="{ active: selectItem === item }">
          {{ mapTable[item] }}
        </button>
      </div>

      <!-- 搜索栏 -->
      <!-- <div class="search-bar"> -->
      <!-- <input type="text" v-model="searchKeyword" placeholder="搜索节点..." @keyup.enter="searchNode" -->
      <!-- class="search-input" /> -->
      <!-- <button @click="searchNode" class="search-btn">搜索</button> -->
      <!-- </div> -->

      <div id="guanxi" ref="guanxi"></div>
    </div>

    <div class="bottom">© 2025 智鉴图谱</div>
  </div>
</template>

<script>
import axios from "axios";
import * as echarts from "echarts";
import ParticleLayer from "@/components/ParticleLayer.vue";
export default {
  name: "visualALL",
  props: {
    msg: String,
  },
  components: {
    ParticleLayer,
  },
  data() {
    return {
      myChart: null,
      baseURL: this.$baseUrl + "/api",
      originalFontSize: 18,
      loading: true,
      searchKeyword: "", // 搜索关键词
      // 选择栏相关数据
      selectItem: "NongJu",
      itemList: ["NongJu", "NongShu", "NongZuoWu", "NongYeJiShu", "NongYeWenHua",],
      mapTable: {
        NongJu: "农具",
        NongShu: "农书",
        NongZuoWu: "农作物",
        NongYeJiShu: "农业技术",
        NongYeWenHua: "农业文化",
      },
      // 各模块数据
      itemArr: {
        NongJu: ["农具", "整地农具", "播种农具", "中耕农具", "灌溉农具", "收获农具", "运输农具", "加工农具", "称量农具", "其他农具",],
        NongShu: ["农书", "综合类", "种植类", "畜牧类", "农具类", "水利类", "蚕桑类", "茶叶类", "治蝗类", "其他农书"],
        NongZuoWu: ["农作物", "谷类作物", "豆类植物", "薯类作物", "油料作物", "蔬菜作物", "果类", "饲料作物", "药用作物", "其他作物",],
        NongYeJiShu: ["农业技术", "耕作技术", "山地水利", "发酵技术", "种植技术", "存储技术", "加工技术", "育种技术", "土壤改良技术", "防灾技术"],
        NongYeWenHua: ["农业文化", "生态智慧", "水利工程", "农业系统", "丝绸之路", "特色林果", "农耕民俗", "农业经济", "古训"],
      },
      keyWords: ["农具", "农书", "农作物", "农业技术", "农业文化"],
      reservedWords: [
        "农具", "整地农具", "播种农具", "中耕农具", "灌溉农具", "收获农具", "运输农具", "加工农具", "称量农具", "其他农具",
        "农书", "综合类", "种植类", "畜牧类", "农具类", "水利类", "蚕桑类", "茶叶类", "治蝗类", "其他农书",
        "农作物", "谷类作物", "豆类植物", "薯类作物", "油料作物", "蔬菜作物", "果类", "饲料作物", "药用作物", "其他作物",
        "农业技术", "耕作技术", "山地水利", "发酵技术", "种植技术", "存储技术", "加工技术", "育种技术", "土壤改良技术", "防灾技术",
        "农业文化", "生态智慧", "水利工程", "农业系统", "丝绸之路", "特色林果", "农耕民俗", "农业经济", "古训",
      ],
      textColorArr: [
        "#B81A35", "#D77F66", "#483D8B", "#FFD700", "#000000",
        "#8B0000", "#8B0111", "#887657", "#4682B4", "#32CD32",
      ],

      itemStyleArr: [
        "rgba(106, 91, 109, 0.8)",
        "rgba(215, 127, 102, 0.8)",
        "rgba(106, 91, 109, 0.8)",
        "rgba(255, 215, 0, 0.8)",
        "rgba(226, 162, 172, 0.8)",
        "rgba(32, 104, 100, 0.8)",
        "rgba(188, 212, 231, 0.8)",
        "rgba(190, 202, 183, 0.8)",
        "rgba(70, 130, 180, 0.8)",
        "rgba(50, 205, 50, 0.8)",
      ],
      allDatas: {
        NongJu: [],
        NongShu: [],
        NongZuoWu: [],
        NongYeJiShu: [],
        NongYeWenHua: [],
      },
      // ECharts 配置，legend.data 与 series[0].categories 将在 updateChartOptions 中根据 selectItem 动态生成
      option: {
        animationDurationUpdate: 1500,
        animationEasingUpdate: "quinticInOut",
        legend: {
          orient: "vertical",
          right: 80, // legend 距离右侧80像素
          y: "center",
          show: true,
          data: [],
          textStyle: {
            fontSize: 25,
            fontFamily: "hongleixingshu,Microsoft YaHei, Arial",
            // fontFamily: "FangSong",
          },
        },
        series: [
          {
            type: "graph",
            layout: "force",
            symbolSize: 120,
            edgeSymbol: ["circle", "arrow"],
            edgeSymbolSize: [5, 6],
            scaleLimit: {
              min: 0.1,
              max: 0.3,
            },
            emphasis: {
              itemStyle: {
                shadowBlur: 20,
                shadowColor: "rgba(0, 0, 0, 0.8)",
                scale: true,
              },
              label: {
                show: true,
                fontSize: 25,
              },
            },
            edgeLabel: {
              normal: {
                show: true,
                textStyle: {
                  fontSize: 10,
                  fontFamily: "FangSong",
                  fontWeight: 'bold',
                },
                formatter: "{c}",
                color: "#887657",
                opacity: 0.3,
              },
            },
            force: {
              repulsion: 5500,
              gravity: 0.1,
              edgeLength: [550, 600],
            },
            focusNodeAdjacency: true,
            draggable: true,
            roam: true,
            categories: [],
            label: {
              normal: {
                show: true,
                //backgroundColor: 'rgba(50,50,50,0.3)', // 半透明黑色背景
                borderRadius: 6,
                padding: [4, 6], // [上下, 左右]
                textStyle: {
                  fontSize: 20,
                  fontFamily: "KaiTi",
                  color: "rgba(0, 0, 0, 0.7)",
                  fontWeight: '550',
                  // shadowColor: "rgba(0, 0, 0, 0.8)",  // 阴影颜色
                  // shadowBlur: 2,           // 阴影模糊程度
                  // shadowOffsetX: 2,        // 阴影水平偏移
                  // shadowOffsetY: 2         // 阴影垂直偏移
                  // textShadowColor: "rgba(0, 0, 0, 0.8)",
                  // textBorderColor: "rgba(0, 0, 0, 0.9)",
                  // textBorderWidth: 1.2,
                },
              },
            },
            tooltip: {
              formatter(node) {
                if (!node.value) {
                  return node.data.name;
                } else {
                  return `${node.data.name}:${node.data.showNum}`;
                }
              },
            },
            lineStyle: {
              normal: {
                opacity: 0.3,
                width: 2,
                curveness: 0.3,
                color: "#887657",
              },
            },
            nodes: [],
            links: [],
          },
        ],
      },
    };
  },
  mounted() {
    if (localStorage.getItem("Reload") === "true") {
      localStorage.setItem("Reload", false);
      window.location.reload();
    }
    // 初始化时先根据默认 selectItem 更新 legend 和 categories
    this.updateChartOptions();

    this.myChart = echarts.init(this.$refs.guanxi);
    // this.myChart.showLoading();
    window.addEventListener("resize", this.myChart.resize);

    // 监听图例点击事件
    this.myChart.on("legendselectchanged", (params) => {
      const selected = params.selected;

      // 确保 keyWords 中的类别始终显示
      this.keyWords.forEach((keyword) => {
        selected[keyword] = true; // 强制设置为 true
      });

      // 更新图表配置
      this.myChart.setOption({
        legend: {
          selected,
        },
      });
    });

    axios
      .get("/qa/all_relations_by_cate", {
        baseURL: this.baseURL,
      })
      .then((response) => {
        Object.keys(this.allDatas).forEach((key) => {
          if (response.data.hasOwnProperty(key)) {
            this.allDatas[key] = response.data[key];
          }
        });
        const { data, links } = this.allDatas[this.selectItem];
        if (Array.isArray(data) && Array.isArray(links)) {
          this.option.series[0].nodes = data.map((node, idx) => {
            node.id = idx;
            node.x = node.x || null;
            node.y = node.y || null;
            return node;
          });
          this.option.series[0].links = links;
          this.myChart.setOption(this.option, true);
        } else {
          console.error("Invalid response format:", response.data);
        }
      })
      .catch((error) => {
        if (error.response && error.response.status === 401) {
          this.$router.push({ path: "/login" });
        }
        console.error("Error fetching data:", error);
      })
      .finally(() => {
        this.myChart.hideLoading();
      });
    this.loading = false;

    this.myChart.on("click", this.handleNodeClick);
    this.myChart.on("dataZoom", this.handleZoom);
  },
  methods: {
    searchNode() {
      const keyword = this.searchKeyword.trim();
      if (!keyword) return;

      // 确保 this.option.series[0].data 已经初始化并且是一个数组
      if (!Array.isArray(this.option.series[0].nodes)) {
        console.error("nodes data is not available");
        return;
      }

      // 查找节点
      const node = this.option.series[0].nodes.find(
        (node) => node.name === keyword
      );

      console.log(node);

      if (!node) {
        this.$message.error({ message: '未找到该结点', duration: 1000 });
        return;
      }

      // 计算容器中心坐标
      const containerWidth = this.$refs.guanxi.clientWidth;
      const containerHeight = this.$refs.guanxi.clientHeight;
      const centerX = containerWidth / 2;
      const centerY = containerHeight / 2;

      // 将目标结点的坐标设置为中心坐标
      node.x = centerX;
      node.y = centerY;

      console.log(node.name);

      // 更新图表
      this.myChart.setOption(this.option, true);

      // 高亮显示结点
      this.myChart.dispatchAction({
        type: "highlight",
        seriesIndex: 0,
        name: keyword,
      });
    },
    // 根据当前 selectItem 更新 legend.data 和 series.categories
    updateChartOptions() {
      const items = this.itemArr[this.selectItem] || [];
      // 取 items 与 textColorArr、itemStyleArr 三者的最小长度，防止数组长度不一致
      const len = Math.min(
        items.length,
        this.textColorArr.length,
        this.itemStyleArr.length
      );
      const newLegendData = [];
      const newCategories = [];
      for (let i = 0; i < len; i++) {
        newLegendData.push({
          name: items[i],
          icon: "circle",
          textStyle: { color: this.textColorArr[i] },
        });
        newCategories.push({
          name: items[i],
          itemStyle: { color: this.itemStyleArr[i] },
        });
      }
      this.option.legend.data = newLegendData;
      this.option.series[0].categories = newCategories;

      // 根据当前 selectItem 更新 nodes 和 links
      const currentData = this.allDatas[this.selectItem];
      if (
        currentData &&
        Array.isArray(currentData.data) &&
        Array.isArray(currentData.links) &&
        currentData.data.length > 0
      ) {
        // 更新 nodes 和 links
        this.option.series[0].nodes = currentData.data.map((node, idx) => {
          node.id = idx;
          node.x = node.x || null;
          node.y = node.y || null;
          return node;
        });
        this.option.series[0].links = currentData.links;
        this.myChart.setOption(this.option, true);
      } else {
        if (!this.loading) {
          // 清空图表数据
          this.option.series[0].nodes = [];
          this.option.series[0].links = [];
          // 提示用户数据为空
          this.$message.error({
            message: "当前数据为空！",
            duration: 1000,
            offset: 50,
          });
        }
      }

      if (this.myChart) {
        this.myChart.setOption(this.option, true);
      }
    },
    // 点击选择栏按钮，更新 selectItem 并更新图表选项
    selectItemHandler(item) {
      this.selectItem = item;
      this.updateChartOptions();
    },
    handleNodeClick(params) {
      if (params.dataType === "node") {
        console.log("Clicked node:", params.data.name);
        // 检查 params.data.name 是否在 reservedWords 中
        if (!this.reservedWords.includes(params.data.name)) {
          this.$router.push({
            path: "/visual",
            query: {
              name: params.data.name,
              category: this.mapTable[this.selectItem],
            },
          });
        } else {
          console.log("This node is reserved, no redirection");
        }
      }
    },
    goHome() {
      this.$router.push({ name: "homepage" });
    },
    handleZoom(params) {
      const zoomRatio = params.batch[0].end / params.batch[0].start;
      const newFontSize = this.originalFontSize * zoomRatio;
      this.myChart.setOption({
        series: [
          {
            label: {
              normal: {
                textStyle: {
                  fontSize: newFontSize,
                },
              },
            },
            edgeLabel: {
              normal: {
                textStyle: {
                  fontSize: newFontSize,
                },
              },
            },
          },
        ],
      });
    },
  },
  beforeDestroy() {
    window.removeEventListener("resize", this.myChart.resize);
    this.myChart.off("click", this.handleNodeClick);
    this.myChart.off("dataZoom", this.handleZoom);
    this.myChart.dispose();
  },
};
</script>

<style scoped>
/* 整体页面 */
.page {
  position: relative;
  width: 100%;
  height: 100%;
  background-color: #ffffff;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.overlay {
  position: absolute;
  inset: 0;
  background: rgba(0, 0, 0, 0.1);
  /* 黑色透明层 */
  z-index: 0;
}

.background {
  background-image: url("../../static/智鉴图谱.jpg");
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  opacity: 0.5;
}

/* 内容区域：采用水平布局 */
.box {
  position: relative;
  top: 15%;
  display: flex;
  justify-content: center;
}

/* 透明内容框样式 */
.content-wrapper {
  width: 100vw;
  height: 80vh;
  margin: 0 auto;
  transition: var(--transition);
  overflow: hidden;
}

.left-bar {
  width: 120px;
  height: 100vh;
  background-color: #887657;
  opacity: 0.9;
  position: fixed;
  left: 0;
  top: 0;
  display: flex;
  flex-direction: column;
  justify-content: start;
  align-items: center;
  border-right: 1px solid #ddd;
  z-index: 2;
  padding-top: 10px;
}

.vertical-text {
  writing-mode: vertical-lr;
  font-size: 45px;
  /* font-family: hongleixingshu, "Microsoft YaHei", Arial, sans-serif; */
  text-align: center;
  margin-top: 20px;
  font-weight: bold;
  color: aliceblue;
}

/* 新增搜索栏样式 */
.search-bar {
  position: fixed;
  top: 1%;
  left: 1%;
  /* width: calc(100vw - 120px); */
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 10px;
  z-index: 3;
  padding: 10px;
}

.search-input {
  padding: 8px 16px;
  font-size: 16px;
  width: 300px;
  border-radius: 20px;
  border: 1px solid #ccc;
  outline: none;
  transition: border 0.3s;
  caret-color: black;
  outline: none;
  /* 去掉聚焦时的边框 */
}

.search-input:focus {
  border-color: #916634;
}

.search-btn {
  padding: 8px 16px;
  font-size: 16px;
  background-color: #916634;
  color: white;
  border: none;
  border-radius: 20px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.search-btn:hover {
  background-color: #a77c47;
}

/* 改进后的选择栏样式 */
.select-bar {
  position: fixed;
  bottom: 3%;
  left: 2%;
  width: 120px;
  /* 左侧栏宽度 */
  display: flex;
  flex-direction: column;
  /* 按钮竖排 */
  justify-content: center;
  align-items: center;
  /* 居中对齐按钮 */
  gap: 20px;
  /* 按钮间距 */
  z-index: 3;
  font-family: "仿宋_GB2312", "FangSong", "华文仿宋", serif;
}

/* 按钮样式改进，柔和背景 */
.select-bar button {
  padding: 12px 24px;
  font-size: 16px;
  width: 100%;
  /* 按钮宽度充满左侧栏 */
  background-color: rgba(145, 102, 52, 0.2);
  /* 柔和的背景色 */
  color: #333;
  /* 按钮文字颜色 */
  border: none;
  /* 去掉边框 */
  border-radius: 30px;
  /* 圆角按钮，增加柔和感 */
  cursor: pointer;
  transition: all 0.3s ease;
  /* 平滑的过渡动画 */
  font-weight: 600;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  /* 轻微阴影效果 */
}

/* 按钮悬停效果 */
.select-bar button:hover {
  background-color: rgba(145, 102, 52, 0.3);
  /* 悬停时增加背景透明度 */
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2);
  /* 增加阴影 */
  transform: scale(1.05);
  /* 鼠标悬停时稍微放大 */
}

/* 激活按钮的样式 */
.select-bar button.active {
  background-color: #916634;
  color: #fff;
  transform: scale(1.05);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

#guanxi {
  width: 100%;
  height: 100%;
}

html,
body,
#app {
  width: 100%;
  height: 100%;
  margin: 0;
  padding: 0;
}
</style>
