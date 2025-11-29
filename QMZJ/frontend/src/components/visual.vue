<template>
  <div class="flex-col justify-start relative page">
    <div class="background"></div>
    <span class="text text_3 pos_2" @click="goBack">《返回</span>
    <span class="text text_2 pos">{{ this.$route.query.name }}</span>

    <!-- 主体内容 -->
    <div class="box content-wrapper">

      <div class="top-section">
        <div class="left-column">
          <img :src="pictureSrc" class="project-picture" />
        </div>

        <div class="right-column">
          <div id="guanxi" ref="guanxi" class="graph-container"></div>
        </div>
      </div>

      <!-- 简介 -->
      <div class="introduction-section">
        <h3 class="title">简介</h3>

        <div class="introduction-content"></div>
        <div v-for="(item, index) in filteredResults" :key="index">
          <h4 class="item-title">{{ formatTitle(item.key) }}</h4>
          <p class="item-description">{{ item.value || "N/A" }}</p>
        </div>
      </div>

      <!-- 评论区域 -->
      <div class="comments-section">
        <h3 class="title">用户评论</h3>
        <div class="search-group">
          <!-- <input type="text" placeholder="搜索评论内容..." v-model="searchQuery" @keyup.enter="searchComments"
            class="comment-search" /> -->
        </div>
        <div class="new-comment">
          <input type="text" v-model="newComment" placeholder="发布评论..." @keyup.enter="postComment"
            class="comment-input" />
          <button class="submit-button" @click="postComment">提交</button>
        </div>
        <div class="comments-list">
          <div v-for="comment in filteredComments" :key="comment.id" class="comment-item">
            <img :src="comment.avatar" class="comment-avatar" />
            <div class="comment-content">
              <span class="comment-author">{{ comment.username }}</span>
              <p class="comment-text">{{ comment.text }}</p>
              <div class="comment-footer">
                <span class="comment-time">{{ formatTime(comment.create_time) }}</span>
                <button class="like-button" @click="toggleLike(comment)">
                  👍 {{ comment.likes || 0 }}
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import * as echarts from "echarts";

export default {
  data() {
    return {
      myChart: null,
      pictureSrc: "",
      baseURL: this.$baseUrl + "/api",
      results: {
        NongJu: {},
        NongShu: {},
        NongZuoWu: {},
        NongYeJiShu: {},
        NongYeWenHua: {},
      },
      profile: [],
      option: {
        grid: {
          left: "3%",
          right: "4%",
          bottom: "3%",
          containLabel: true,
        },
        title: {
          textStyle: {
            fontWeight: "lighter",
          },
        },
        backgroundColor: "rgba(255, 255, 255, 0.8)",
        animationDurationUpdate: 1500,
        animationEasingUpdate: "quinticInOut",
        legend: {
          x: "center",
          y: 10,
          show: false,
          data: [
            { name: "农具", icon: "circle", textStyle: { color: "#B81A35" } },
            {
              name: "耕作工具",
              icon: "circle",
              textStyle: { color: "#D77F66" },
            },
            {
              name: "播种工具",
              icon: "circle",
              textStyle: { color: "#483D8B" },
            },
            {
              name: "灌溉工具",
              icon: "circle",
              textStyle: { color: "#FFD700" },
            },
            {
              name: "收获工具",
              icon: "circle",
              textStyle: { color: "#000000" },
            },
            {
              name: "加工工具",
              icon: "circle",
              textStyle: { color: "#8B0000" },
            },
            {
              name: "运输工具",
              icon: "circle",
              textStyle: { color: "#8B0111" },
            },
            {
              name: "其他辅助工具",
              icon: "circle",
              textStyle: { color: "#887657" },
            },
          ],
          textStyle: {
            color: "#000000",
            fontSize: 30,
            fontFamily: "hongleixingshu,Microsoft YaHei, Arial",
          },
        },
        series: [
          {
            type: "graph",
            layout: "force",
            symbolSize: 100,
            edgeSymbol: ["circle", "arrow"],
            edgeSymbolSize: [2, 4],
            edgeLabel: {
              normal: {
                show: true,
                textStyle: {
                  fontSize: 15,
                  fontFamily:
                    "hongleixingshu,Microsoft YaHei, Arial, sans-serif",
                },
                formatter: "{c}",
              },
            },
            force: {
              repulsion: 1500,
              edgeLength: [100, 300],
            },
            focusNodeAdjacency: true,
            draggable: true,
            roam: true,
            scaleLimit: { min: 0.5, max: 2 },
            categories: [
              { name: "农具", itemStyle: { color: "rgba(106, 91, 109, 0.8)" } },
              {
                name: "耕作工具",
                itemStyle: { color: "rgba(215,127,102, 0.8)" },
              },
              {
                name: "播种工具",
                itemStyle: { color: "rgba(106, 91, 109, 0.8)" },
              },
              {
                name: "灌溉工具",
                itemStyle: { color: "rgba(255,215,0, 0.8)" },
              },
              {
                name: "收获工具",
                itemStyle: { color: "rgba(226,162,172, 0.8)" },
              },
              {
                name: "加工工具",
                itemStyle: { color: "rgba(32,104,100, 0.8)" },
              },
              {
                name: "运输工具",
                itemStyle: { color: "rgba(188,212,231, 0.8)" },
              },
              {
                name: "其他辅助工具",
                itemStyle: { color: "rgba(190,202,183, 0.8)" },
              },
            ],
            label: {
              normal: {
                show: true,
                textStyle: {
                  fontSize: 25,
                  fontFamily:
                    "hongleixingshu,Microsoft YaHei, Arial, sans-serif",
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
                opacity: 1,
                width: 2,
                curveness: 0.3,
                color: "#000000",
              },
            },
            itemStyle: {
              opacity: 0.98, // 设置节点透明度
            },
            nodes: [],
            links: [],
          },
        ],
      },
      // 原有数据保持不变...
      user: null, // 添加用户信息初始化
      comments: [],
      newComment: "",
      searchQuery: "",
      currentItem: {
        name: this.$route.query.name,
        category: this.$route.query.category,
      },
    };
  },
  async mounted() {
    if (localStorage.getItem("Reload") === "true") {
      localStorage.setItem("Reload", false);
      window.location.reload();
    }
    const characterName = this.$route.query.name;
    const cate = this.$route.query.category;
    this.myChart = echarts.init(this.$refs.guanxi);
    this.myChart.showLoading();
    window.addEventListener("resize", this.myChart.resize);

    try {
      const response = await axios.get("/qa/search_name", {
        params: {
          name: characterName,
          model_param: cate,
        },
        baseURL: this.baseURL,
      });

      const { data, links } = response.data[0];
      this.profile = response.data[1];

      // TODO 这里修改了后端发送的数据格式，准备返回字典
      console.log("this.profile: ", this.profile);
      // console.log("this.profile[category]", this.profile["category"]);
      // console.log("this.$route.query.category", this.$route.query.category);
      const picture = response.data[2];
      if (Array.isArray(data) && Array.isArray(links)) {
        this.option.series[0].nodes = data.map((node, idx) => {
          node.id = idx;
          return node;
        });

        // 动态根据 category 设置结果
        const categoryMap = {
          "农书": "NongShu",
          "农具": "NongJu",
          "农作物": "NongZuoWu",
          "农业技术": "NongYeJiShu",
          "农业文化": "NongYeWenHua",
        };

        const categoryKey = categoryMap[this.profile["category"]];
        if (categoryKey) {
          this.results[categoryKey] = {};

          // 遍历 profile 对象的键，检查键是否存在，如果存在则赋值
          Object.keys(this.profile).forEach(key => {
            if (this.profile[key] && this.profile[key] !== "") {
              this.results[categoryKey][key] = this.profile[key];
            }
          });
        }

        this.option.series[0].nodes = data.map((node, idx) => {
          node.id = idx;
          return node;
        });

        console.log("results: ", this.results);
        this.option.series[0].links = links;
        this.myChart.setOption(this.option, true);
        this.pictureSrc = `data:image/jpg;base64,${picture}`;
        // document.getElementById("picture").style.display = "block";
      } else {
        console.error("Invalid response format:", response.data);
      }
    } catch (error) {
      if (error.response && error.response.status === 401) {
        this.$router.push({ path: "/login" });
      }
      console.error("Error fetching data:", error);
    }

    this.myChart.on("click", this.handleNodeClick);

    this.myChart.hideLoading();
    this.fetchComments(); // 在mounted末尾添加
  },
  computed: {
    filteredResults() {
      const category = this.currentItem.category;
      const category_map = {
        "农书": "NongShu",
        "农具": "NongJu",
        "农作物": "NongZuoWu",
        "农业技术": "NongYeJiShu",
        "农业文化": "NongYeWenHua",
      };
      const categoryKey = category_map[category];

      const result = Object.entries(this.results[categoryKey] || {})
        .filter(([key, value]) => this.formatTitle(key)) // Only include keys with a valid title
        .map(([key, value]) => ({ key, value })); // Return an array of objects with 'key' and 'value'

      console.log("filteredResults: ", result);
      return result
    },

    filteredComments() {
      if (!this.searchQuery) {
        return this.comments;
      }
      const query = this.searchQuery.toLowerCase();
      return this.comments.filter(
        (comment) =>
          comment.text.toLowerCase().includes(query) ||
          comment.username.toLowerCase().includes(query)
      );
    },
  },

  methods: {
    formatTitle(key) {
      console.log("key: ", key);
      const mapping = {
        sub_category: "次级类型",
        description: "描述",
        publish_date: "出版日期",
        location: "地点",
        significance: "意义",
        author: "作者",
        main_usage: "主要用途",
        ancient_reference: "古籍记载",
        period: "朝代时期",
        region: "使用地区",
        creator: "发明者",
        alias: "别称",
        origin: "原产地",
        nutri_value: "营养价值",
        econo_value: "经济价值",
        grow_env: "生长环境",
        plant_area: "种植地带",
        widespread: "文化传播"
      };
      return mapping[key];  // 如果没有映射则返回原key
    },

    async handleNodeClick(params) {
      const characterName = params.name;
      try {
        const response = await axios.get("/qa/get_profile", {
          params: {
            character_name: characterName,
          },
          baseURL: this.baseURL,
        });

        const [profile, picture] = response.data;

        this.profile = profile;
        this.pictureSrc = `data:image/jpg;base64,${picture}`;
        document.getElementById("picture").style.display = "block";

        // 更新 this.results
        this.results = [
          {
            time: this.profile[0] || "N/A",
            author: this.profile[1] || "N/A",
            position: this.profile[2] || "N/A",
            mainUsage: this.profile[3] || "N/A",
            alias: this.profile[4] || "N/A",
            significance: this.profile[5] || "N/A",
            ancientRecords: this.profile[6] || "N/A",
            id: 0, // Assuming there's only one result
          },
        ];
      } catch (error) {
        console.error("Error fetching profile:", error);
      }
    },

    goBack() {
      this.$router.go(-1);
    },

    async fetchComments() {
      try {
        const response = await axios.get("/forum/commentsByItem", {
          params: {
            name: this.currentItem.name,
            category: this.currentItem.category,
          },
          baseURL: this.baseURL,
        });
        // 确保返回数据结构正确
        this.comments = response.data.comments.map((c) => ({
          ...c,
          username: c.username || "匿名用户", // 添加默认用户名
          avatar: c.avatar || "../../static/profile.png", // 默认头像
        }));
      } catch (error) {
        console.error("获取评论失败:", error);
      }
    },

    async postComment() {
      if (this.newComment.trim()) {
        try {
          await axios.post(
            "/forum/writeComments",
            {
              text: this.newComment,
              name: this.currentItem.name,
              category: this.currentItem.category,
            },
            { baseURL: this.baseURL }
          );
          this.newComment = "";
          await this.fetchComments();
        } catch (error) {
          console.error("发布评论失败:", error);
        }
      }
    },

    async toggleLike(comment) {
      try {
        await axios.post(
          "/forum/likeComments",
          {
            id: comment.id,
          },
          { baseURL: this.baseURL }
        );
        comment.likes++;
      } catch (error) {
        console.error("点赞失败:", error);
      }
    },

    formatTime(time) {
      return new Date(time).toLocaleString();
    },
  },
};
</script>

<style scoped>
.page {
  position: relative;
  width: 100%;
  height: 100%;
  background-color: #ffffff;
  display: flex;
  flex-direction: column;
}

/* 背景 */
.background {
  background-image: url("../../static/耘集荟萃.jpg");
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

/* 内容区域：使用flex布局并且允许换行 */
.box {
  position: relative;
  top: 15%;
  justify-content: center;
  flex-direction: column;
}

/* 透明内容框样式 */
.content-wrapper {
  width: 80vw;
  height: 80vh;
  margin: 0 auto;
  border-radius: 20px;
  transition: var(--transition);
  overflow-x: hidden;
  overflow-y: auto;
  /* background-color: rgba(255, 255, 255, 0.3); */
}

/* 隐藏滚动条 */
.content-wrapper::-webkit-scrollbar {
  display: none;
}

/* 顶部部分：图片+图表 */
.top-section {
  display: flex;
  width: 100%;
  height: 40vh;
  /* margin-top: 900px; */
  overflow: visible;
  padding: 20px;
  border-radius: 8px;
  margin-bottom: 20px;
}

.introduction-section,
.comments-section {
  /* background-color: rgba(255, 255, 255, 0.3); */
  padding: 20px;
  border-radius: 8px;
  /* box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); */
  margin: 0px 20px 10px 20px;
  text-align: left;
}

/* 左栏图片部分 */
.left-column {
  width: 50%;
  height: 100%;
  padding: 0px;
  overflow: hidden;
  /* 隐藏超出容器的图片部分 */
}

.project-picture {
  width: 100%;
  height: 100%;
  object-fit: contain;
  /* 保持图片比例且完整显示 */
  background-color: white;
}

/* 右栏图表部分 */
.right-column {
  width: 50%;
  height: 100%;
  padding: 0px;
  border-radius: 8px;
}

.graph-container {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.title {
  font-size: 30px;
  color: #333333;
  /* margin-bottom: 10px; */
  font-family: "仿宋_GB2312", "FangSong", "华文仿宋", serif;
  font-weight: bold;
}

.introduction-content {
  display: flex;
  flex-direction: column;
}

.item-title {
  font-size: 24px;
  color: #916634;
  margin-bottom: 1px;
  font-family: "仿宋_GB2312", "FangSong", "华文仿宋", serif;
  font-weight: bold;
}

.item-description {
  /* text-align: left; */
  font-size: 22px;
  color: #666666;
  margin-top: 5px;
  line-height: 1.4;
  font-family: "仿宋_GB2312", "FangSong", "华文仿宋", serif;
}

/* 评论区块 */
.comment-search {
  width: 100%;
  padding: 10px;
  border: 1px solid #d4b886;
  border-radius: 5px;
  font-size: 14px;
}

.comment-item {
  display: flex;
  margin-bottom: 15px;
  padding: 15px;
  background-color: rgba(255, 255, 255, 0.6);
  border-radius: 8px;
  font-family: "仿宋_GB2312", "FangSong", "华文仿宋", serif;
}

.comment-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  margin-right: 15px;
}

.comment-content {
  flex: 1;
}

.comment-author {
  font-weight: bold;
}

.comment-text {
  font-size: 20px;
  margin: 10px 0;
  color: #666666;
}

.comment-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.comment-time {
  font-size: 16px;
  color: #666666;
}

.like-button {
  background-color: #916634;
  color: white;
  border: none;
  padding: 5px 10px;
  border-radius: 5px;
  cursor: pointer;
}

.like-button:hover {
  background-color: #7a542b;
}

.new-comment {
  display: flex;
  gap: 10px;
  margin-top: 20px;
  margin-bottom: 20px;
}

.comment-input {
  flex: 1;
  padding: 10px;
  background-color: rgba(255, 255, 255, 0.6);
  border-radius: 5px;
  font-size: 14px;
}

.submit-button {
  background-color: #916634;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 5px;
  cursor: pointer;
}

.submit-button:hover {
  background-color: #7a542b;
}
</style>
