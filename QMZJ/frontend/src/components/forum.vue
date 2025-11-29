<template>
  <div class="flex-col justify-start items-center relative page">
    <!-- 添加背景图 -->
    <div class="background"></div>

    <!-- 返回主页按钮 -->
    <span class="text text_3 pos_2" @click="goHome">《主页</span>

    <!-- 标题 -->
    <span class="text text_2 pos">耘集荟萃</span>
    <div class="content-wrapper">
      <!-- 简介段落 -->
      <!-- <p class="description">
        显示各类农业数据，包括农具、农书、农作物、农业技术和农业文化。
      </p> -->

      <!-- 筛选条件区域 -->
      <div class="filter-section">
        <!-- 类别选择 -->
        <div class="filter-group">
          <label>一级类别：</label>
          <select v-model="selectedCategory" @change="resetSubCategory">
            <option value="">全部</option>
            <option v-for="category in categories" :key="category" :value="category">
              {{ category }}
            </option>
          </select>
        </div>

        <!-- 二级类别选择 -->
        <div class="filter-group">
          <label>二级类别：</label>
          <select v-model="selectedSubCategory" :disabled="!selectedCategory">
            <option value="">全部</option>
            <option v-for="subCat in filteredSubCategories" :key="subCat" :value="subCat">
              {{ subCat }}
            </option>
          </select>
        </div>

        <!-- 搜索框 -->
        <div class="filter-group">
          <label>搜索框：</label>
          <input 
            type="text" 
            placeholder="输入关键词搜索..." 
            v-model="searchQuery"
            class="search-input"
          />
        </div>
      </div>

      <!-- 项目列表 -->
      <div class="section-projects">
        <div class="project-item" v-for="item in filteredItems" :key="item.id" @click="handleItemClick(item)">
          <div class="project-header">
            <span class="project-name">{{ item.name }}</span>
            <span class="project-type">{{ item.category }} · {{ item.sub_category }}</span>
          </div>
          <div class="project-details">
            <span class="project-period">时期：{{ getPeriod(item) }}</span>
          </div>
          <div class="project-details">
            <span class="project-location">地区：{{ item.location }}</span>
          </div>
          <p class="project-description" v-if="item.description">
            🔖描述：{{ item.description }}
          </p>
          <p class="project-description" v-if="item.main_usage">
            🎯主要用途：{{ item.main_usage }}
          </p>
          <p class="project-description" v-if="item.nutri_value">
            🧀营养价值：{{ item.nutri_value }}
          </p>
          <p class="project-description" v-if="item.econo_value">
            💰经济价值：{{ item.econo_value }}
          </p>
          <p class="project-description" v-if="item.grow_env">
            🌾生长环境：{{ item.grow_env }}
          </p>
          <p class="project-description" v-if="item.widespread">
            🌏文化传播：{{ item.widespread }}
          </p>
          <p class="project-description" v-if="item.significance">
            😀意义：{{ item.significance }}
          </p>
          <div class="project-footer">
            <span class="project-alias" v-if="item.alias">别称：{{ item.alias }}</span>

            <span class="project-alias" v-if="item.creator">创作者：{{ item.creator }}</span>
            <span class="project-alias" v-if="item.author">作者：{{ item.author }}</span>

            <span class="project-reference" v-if="item.ancient_reference">古籍记载：{{ item.ancient_reference }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      selectedCategory: this.$route.query.category ? this.$route.query.category : "", // 默认全部
      selectedSubCategory: "", // 选中的二级类别
      searchQuery: "", // 搜索关键词
      items: [], // 合并后的所有数据
    };
  },
  computed: {
    // 从合并后的数据中提取所有可用主类别
    categories() {
      return [...new Set(this.items.map((item) => item.category))];
    },
    // 根据选中的主类别筛选出所有二级类别
    filteredSubCategories() {
      if (!this.selectedCategory) return [];
      return [
        ...new Set(
          this.items
            .filter((item) => item.category === this.selectedCategory)
            .map((item) => item.sub_category)
        ),
      ];
    },
    // 综合过滤：按类别、二级类别和关键词进行过滤
    filteredItems() {
      console.log("在filteredItems函数中");
      return this.items.filter((item) => {
        const categoryMatch =
          !this.selectedCategory || item.category === this.selectedCategory;
        const subCategoryMatch =
          !this.selectedSubCategory ||
          item.sub_category === this.selectedSubCategory;
        const searchMatch =
          !this.searchQuery.trim() ||
          Object.values(item).some((value) =>
            String(value).toLowerCase().includes(this.searchQuery.toLowerCase())
          );
        return categoryMatch && subCategoryMatch && searchMatch;
      });
    },
  },
  methods: {
    // 新增返回主页方法
    goHome() {
      this.$router.push({ name: "homepage" });
    },
    resetSubCategory() {
      this.selectedSubCategory = "";
    },
    getPeriod(item) {
      // 时期
      return item.period || item.publish_date || item.origin;
    },
    handleSearch() {
      this.searchQuery = this.tempSearch;
    },
    fetchData() {
      axios
        .get(this.$baseUrl + "/api/search/searchAll")
        .then((response) => {
          // 将接口返回的数据（各模型数据）合并为一个数组
          let merged = [];
          for (let key in response.data) {
            if (response.data.hasOwnProperty(key)) {
              merged = merged.concat(response.data[key]);
            }
          }
          this.items = merged;
        })
        .catch((error) => {
          this.$message.error({ message: "数据获取失败", duration: 1000 });
        });
    },
    // 点击条目后跳转
    handleItemClick(item) {
      this.$router.push({
        path: "/visual",
        query: { name: item.name, category: item.category },
      });
      window.location.reload();
    },
  },
  mounted() {
    console.log("category", this.$route.query.category);
    if(localStorage.getItem("Reload") === "true"){
      localStorage.setItem("Reload", false);
      window.location.reload();
    }
    this.fetchData();
  },
};
</script>

<style scoped>
.page {
  position: relative;
  height: 100vh;
  overflow: hidden;
  padding: 0;
  display: flex;
  flex-direction: column;
}

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

.content-wrapper {
  width: 90vw;
  padding: 2rem;
  margin: 0 auto;
  /* background: rgba(255, 255, 255, 0.52); */
  border-radius: 20px;
  backdrop-filter: blur(2px);
  /* box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08); */
  transition: var(--transition);
  overflow: hidden;
  margin-top: 5%;
}

/* .content-wrapper:hover {
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.12);
  transform: translateY(-2px);
  border-radius: 20px;
} */

.description {
  color: var(--text-light);
  text-align: center;
  margin: 1.5rem 0;
  font-size: 2rem;
  opacity: 0.9;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

.project-footer {
  margin-top: 0rem;
  padding-top: 0rem;
  border-top: 1px solid rgba(90, 164, 135, 0.1);
  display: grid;
  gap: 0.5rem;
  font-family: inherit;
}

.project-alias {
  font-size: 1.1rem;
  color: var(--secondary);
  display: flex;
  align-items: center;
}

.project-alias::before {
  content: "•";
  color: var(--accent);
  margin-right: 0.5rem;
}

.project-reference {
  font-family: "楷体_GB2312", "KaiTi", "华文楷体", cursive;
  font-size: 1em;
  font-style: italic;
  color: var(--secondary);
  padding: 0.5rem;
  background: rgba(255, 159, 77, 0.05);
  border-left: 2px solid var(--accent);
}

/* 设计变量 */
:root {
  --orange-bg: rgba(255, 159, 77, 0.08);
  --orange-border: rgba(255, 159, 77, 0.12);
  --orange-shadow: 0 2px 12px rgba(255, 159, 77, 0.1);
  --shadow-green: 0 2px 12px rgba(90, 164, 135, 0.1);
  --shadow-green-hover: 0 4px 20px rgba(90, 164, 135, 0.15),
    0 2px 6px rgba(90, 164, 135, 0.1);
  --primary: #2b8c6e;
  --secondary: #5aa487;
  --accent: #ff9f4d;
  --text-main: #2d3439;
  --text-light: #f8f9fa;
  --surface: rgba(255, 255, 255, 0.96);
  --border-radius: 12px;
  --shadow-sm: 0 2px 8px rgba(0, 0, 0, 0.08);
  --shadow-md: 0 4px 16px rgba(0, 0, 0, 0.12);
  --transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
}

/* 
.horizontal-text::after {
  content: "";
  position: absolute;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 120px;
  height: 3px;
  background: linear-gradient(90deg, var(--accent), var(--secondary));
} */

/* 筛选区域 */
.filter-section {
  display: grid;
  gap: 1.5rem;
  max-width: 1200px;
  margin: 0 auto;
  padding: 1rem;
  background: var(--surface);
  border-radius: var(--border-radius);
  box-shadow: var(--shadow-sm);
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
}

.filter-group select,
.search-input {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid rgba(0, 0, 0, 0.1);
  border-radius: 8px;
  background: white;
  transition: var(--transition);
  caret-color: auto;
}

.filter-group select:focus,
.search-input:focus {
  outline: none;
  border-color: var(--accent);
  box-shadow: 0 0 0 3px rgba(255, 159, 77, 0.2);
}

/* 项目列表 */
.section-projects {
  font-family: "仿宋_GB2312", "FangSong", "华文仿宋", serif;
  font-size: 16px;
  line-height: 1.8;
  display: grid;
  gap: 1.5rem;
  max-width: 1200px;
  width: 90%;
  height: 80vh;
  margin: 0 auto;
  padding: 2rem 0;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  /* max-height: 60vh; */
  /* 启用滚动 */
  overflow-y: auto;
  overflow-x: hidden;
}

/* 隐藏滚动条 */
.section-projects::-webkit-scrollbar {
  display: none;
}

.project-item {
  background: rgba(255, 159, 77, 0.08);
  /* 半透明橙色背景 */
  border-radius: var(--border-radius);
  border: 1px solid rgba(255, 159, 77, 0.12);
  /* 橙色边框 */
  box-shadow: 0 2px 12px rgba(255, 159, 77, 0.1);
  transition: var(--transition);
  cursor: pointer;
  backdrop-filter: blur(2px);
  line-height: 1.6;
  display: grid;
  gap: 1.0rem;
  margin: 0 auto;
  padding: 3rem 1.5rem;
}

.project-item:hover {
  transform: translateY(-4px);
  background: rgba(255, 159, 77, 0.12);
  /* 悬浮加深透明度 */
  box-shadow: 0 4px 20px rgba(255, 159, 77, 0.15),
    0 2px 8px rgba(255, 159, 77, 0.1);
  border-color: rgba(255, 159, 77, 0.2);
}

.project-item:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-md);
}

/* 文字排版 */
.project-name {
  font-size: 1.8rem;
  font-weight: 600;
  color: var(--primary);
  font-family: "方正小标宋_GBK", "SimSun", serif;
  letter-spacing: 0.05em;
  border-left: 3px solid var(--accent);
  padding-left: 0.75rem;
}

.project-details {
  display: flex;
  gap: 1rem;
  margin: 0rem 0;
  color: var(--text-main);
  font-size: 1em;
  font-family: inherit;
}

.project-description {
  color: var(--text-main);
  line-height: 0.6;
  margin: 0rem 0;
  padding: 0.7rem;
  background: rgba(90, 164, 135, 0.03);
  border-radius: 8px;
  font-family: inherit;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

/* 响应式处理 */
@media (max-width: 768px) {
  .horizontal-text {
    font-size: 2rem;
  }

  .filter-section {
    grid-template-columns: 1fr;
    margin: 1rem;
  }

  .section-projects {
    font-size: 15px;
    line-height: 0.6;
    grid-template-columns: 1fr;
  }

  .content-wrapper {
    padding: 0 1rem;
  }

  .project-footer {
    grid-template-columns: 1fr;
  }
}
</style>