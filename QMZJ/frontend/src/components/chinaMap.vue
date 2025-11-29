<template>
  <div class="flex-col justify-start relative page">

    <div class="background"></div>
    <span class="text text_3 pos_2" @click="goHome">《主页</span>
    <span class="text text_2 pos">耕织地图</span>

    <!-- 背景粒子层 -->
    <ParticleLayer />

    <!-- 内容区 -->
    <div class="box content-wrapper">
      <!-- 左侧图表区域：上下排列 -->
      <div class="left-charts-container">
        <div id="categoryChart" class="chart"></div>
        <div id="regionChart" class="chart"></div>
      </div>

      <!-- 中间地图及控制器 -->
      <div id="mapContainer" class="map-container">

        <!-- 搜索框 -->
        <div class="search-box">
          <el-input ref="searchInput" v-model="searchQuery" placeholder="搜索古代农学数据" @keyup.enter.native="searchData"
            clearable>
            <el-button slot="append" icon="el-icon-search" @click="searchData"></el-button>
          </el-input>
        </div>

        <div id="mapChart" class="chart"></div>

        <button class="backBtn" @click="back()" v-show="isSecondLevelMap">返回上级</button>

        <!-- 分类过滤器 -->
        <div class="filter">
          <select v-model="selectedCategory" @change="filterData">
            <option value="">全部</option>
            <option value="农具">农具</option>
            <option value="农书">农书</option>
            <option value="农作物">农作物</option>
            <option value="农业技术">农业技术</option>
            <option value="农业文化">农业文化</option>
          </select>
        </div>
      </div>

      <!-- 右侧图表区域 -->
      <div class="right-charts-container">
        <div id="subcategoryChart" class="chart"></div>
        <!-- 新增详情展示面板，使用 ElScrollbar 包裹文字部分 -->
        <div id="detailPanel" class="detail-panel">
          <h3 class="small-title">田园诗话</h3>
          <div class="detail-content" v-if="randomEntry">
            <p v-if="randomEntry.name"><strong>名称：</strong>{{ randomEntry.name }}</p>
            <p v-if="randomEntry.alias"><strong>别称：</strong>{{ randomEntry.alias }}</p>

            <p v-if="randomEntry.category"><strong>类别：</strong>{{ randomEntry.category }}</p>
            <p v-if="randomEntry.sub_category"><strong>子类别：</strong>{{ randomEntry.sub_category }}</p>
            <p v-if="randomEntry.location"><strong>地点：</strong>{{ randomEntry.location }}</p>
            <!-- 农具 -->
            <p v-if="randomEntry.period"><strong>出现时期：</strong>{{ randomEntry.period }}</p>
            <p v-if="randomEntry.creator"><strong>>创作者：</strong>{{ randomEntry.creator }}</p>
            <p v-if="randomEntry.main_usage"><strong>主要用途：</strong>{{ randomEntry.main_usage }}</p>
            <p v-if="randomEntry.significance"><strong>意义：</strong>{{ randomEntry.significance }}</p>

            <!-- 农书 -->
            <p v-if="randomEntry.publish_date"><strong>出版日期或成书时期：</strong>{{ randomEntry.publish_date }}</p>

            <!-- 农作物 -->
            <p v-if="randomEntry.origin"><strong>出现时期：</strong>{{ randomEntry.origin }}</p>
            <p v-if="randomEntry.nutri_value"><strong>营养价值：</strong>{{ randomEntry.nutri_value }}</p>
            <p v-if="randomEntry.econo_value"><strong>经济价值：</strong>{{ randomEntry.econo_value }}</p>
            <p v-if="randomEntry.grow_env"><strong>生长环境：</strong>{{ randomEntry.grow_env }}</p>
            <p v-if="randomEntry.plant_area"><strong>种植地带：</strong>{{ randomEntry.plant_area }}</p>

            <!-- 农业文化 -->
            <p v-if="randomEntry.widespread"><strong>文化传播：</strong>{{ randomEntry.widespread }}</p>

            <p v-if="randomEntry.description"><strong>描述：</strong>{{ randomEntry.description }}</p>
            <p v-if="randomEntry.ancient_reference"><strong>古籍引用：</strong>{{ randomEntry.ancient_reference }}</p>
          </div>
          <div v-else>
            <p>暂无数据</p>
          </div>
          <button class="refreshBtn" @click="selectRandomEntry">换一条</button>
        </div>
      </div>
    </div>

    <div>审图号：GS（2024）0650号</div>
     <a href="https://cloudcenter.tianditu.gov.cn/administrativeDivision" target="_blank" style="z-index: 100; position: relative;">数据来源：国家地理信息公共服务平台</a>
    <!-- 底部区域 -->
    <div class="bottom">© 2025 耕织地图</div>
  </div>
</template>

<script>
import cityMap from "@/js/china-main-city-map.js";
import * as echarts from "echarts";
import axios from "axios";
import ParticleLayer from "@/components/ParticleLayer.vue";
// import this.registerAndsetOption from '@/js/echarts-map'
// 声明一个变量用于存储所有数据
let globalAllData = [];

//中国地图（第一级地图）的ID、Name、Json数据
var chinaId = 100000;
var chinaName = "china";
var mapJson = null;

//记录父级ID、Name
var mapStack = [];
var parentId = null;
var parentName = null;

// ECharts实例
var myChart = null;
var categoryChart = null; // 显示各大类数据统计（柱状图）
var subcategoryChart = null; // 显示当前大类下各子类别占比（饼图）
var regionChart = null; // 显示区域分布（饼图）

// 标注点数据，category 字段代表大类
var MarkDatas = [];

// 定义大类及对应的所有子类
const categoryData = {
  "农具": [],
  "农书": [],
  "农作物": [],
  "农业技术": [],
  "农业文化": []
};

export default {
  name: "chinaMap",
  props: {
    msg: String,
  },
  components: {
    ParticleLayer,
  },

  data() {
    return {
      searchQuery: "",
      selectedCategory: "",
      isSecondLevelMap: false,
      randomEntry: null,
    }
  },

  async mounted() {
    if (localStorage.getItem("Reload") === "true") {
      localStorage.setItem("Reload", false);
      window.location.reload();
    }
    try {
      parentId = chinaId;
      parentName = chinaName;
      myChart = echarts.init(document.getElementById("mapChart"));
      categoryChart = echarts.init(document.getElementById("categoryChart"));
      subcategoryChart = echarts.init(document.getElementById("subcategoryChart"));
      regionChart = echarts.init(document.getElementById("regionChart"));
      await this.loadAllData(); // 加载并保存所有数据到 globalAllData
      await this.initMapChart("mapChart");
      this.initcategoryChart();
      this.initsubcategoryChart();
      this.initRegionChart();
      this.selectRandomEntry();
    } catch (error) {
      this.$message.error({ message: '初始化失败', duration: 1000 });
    }
  },

  methods: {
    goHome() {
      this.$router.push({ name: "homepage" });
    },

    // Search function triggered by the enter key or search button
    searchData() {
      const query = this.searchQuery.trim();
      if (query === '') {
        this.$message.warning({ message: '请输入要检索的数据', duration: 1000 });
        return;
      }
      const searchResult = globalAllData.find((item) =>
        item.name.includes(query) || item.location.includes(query)
      );

      if (searchResult) {
        // Jump to the second-level map for the searched data point
        console.log("searchResult.location: ", searchResult.location);

        let cityId = null;
        let province_ = null;
        const provinces = Object.keys(cityMap);
        provinces.forEach(province => {
          if (searchResult.location.includes(province)) {
            cityId = cityMap[province]; // 根据省份名称查找对应的 cityId
            province_ = province;
          }
        });

        console.log("cityId: ", cityId);
        // const cityId = cityMap[searchResult.location];
        if (cityId) {
          axios.get("./static/json/map/" + cityId + ".json")
            .then((response) => {
              mapJson = response.data;
              this.updateMapData(province_);
              this.isSecondLevelMap = province_ !== "china";
              this.registerAndsetOption(myChart, cityId, province_, mapJson, true);
              parentId = cityId;
              parentName = province_;
              console.log("parentName: ", parentName);
              this.highlightDataPoint(searchResult);
              this.initcategoryChart();
              this.initsubcategoryChart();
              this.initRegionChart();
            });

        }
      } else {
        this.$message.warning({ message: '未找到匹配的数据点', duration: 1000 });
      }
      this.searchQuery = '';
    },

    // Highlight the selected data point on the map
    highlightDataPoint(dataPoint) {
      const matchedData = {
        name: dataPoint.name,
        value: [dataPoint.lng, dataPoint.lat],
        category: dataPoint.category,
        sub_category: dataPoint.sub_category,
        location: dataPoint.location,
        dataValue: 1, // You can modify this as per your data structure
      };

      myChart.setOption({
        series: [{ // highlighted matchedData
          type: "scatter",
          coordinateSystem: "geo",
          data: [matchedData],
          symbolSize: 15,
          itemStyle: {
            color: "#FF6347", // Highlight color for the selected point
            borderColor: "#ffffff",
            borderWidth: 3,
            borderColor: "#fff",
          },
          label: {
            backgroundColor: 'rgba(250,250,250,0.6)', // 半透明黑色背景
            borderRadius: 6,
            padding: [4, 6], // [上下, 左右]
            show: true,
            formatter: "{b}",
            position: "top",
            // position: "right",
            fontFamily: "FangSong",
            fontWeight: "bold",
            fontSize: 30,
            // 浅红色
            color: "#FF6347",
          }
        }, {
          // Keep other points with the original label style
          type: "scatter",
          coordinateSystem: "geo",
          data: globalAllData.filter(item => item.name !== dataPoint.name).map(item => ({
            name: item.name,
            value: [item.lng, item.lat],
          })),
          symbolSize: 6,
          itemStyle: {
            color: "#ffffff",       // 点颜色
            borderColor: "#ffffff",
            borderWidth: 1,
            shadowBlur: 4,         // 增加点的可视性
            shadowColor: "#fff"
          },
          label: {
            formatter: function (params) {
              const name = params.name || "";
              return name.length > 8 ? name.slice(0, 8) + "…" : name;
            },
            position: "top",
            // position: "right",
            show: this.isSecondLevelMap,
            fontFamily: "FangSong",
            fontWeight: 'bold',
            fontSize: 20
          }
        }],
      });
    },

    /* 返回上一级地图 */
    async back() {
      console.log("mapStack: ", mapStack);
      if (mapStack.length != 0) {
        var map = mapStack.pop();
        parentId = map.mapId;
        parentName = map.mapName;// "china "
        this.isSecondLevelMap = parentName !== "china";

        const response = await axios.get("./static/json/map/" + parentId + ".json", {});
        mapJson = response.data;

        // 先更新散点数据（基于初始全局数据或过滤条件）
        if (parentName === "china") {
          this.updateMapData();
        } else {
          this.updateMapData(parentName);
        }
        this.registerAndsetOption(myChart, parentId, parentName, mapJson, false);
        this.initcategoryChart();
        this.initsubcategoryChart();
        this.initRegionChart();
      }
      else {
        this.$message.warning({ message: '地图已经是最上级', duration: 1000 });
      }
    },

    // 初始化左侧柱状图：统计各大类数据总量
    initcategoryChart() {
      console.log("init left chart");
      let stats = {};
      // 初始化所有大类统计项为0
      Object.keys(categoryData).forEach(cat => {
        stats[cat] = 0;
      });
      // 遍历所有标注点，累加对应大类的 dataValue
      MarkDatas.forEach(item => {
        if (stats[item.category] !== undefined) {
          stats[item.category] += item.dataValue;
        }
      });
      // 统一颜色，选择柔和的冷色调蓝色
      const barColor = 'rgb(123,191,221)'

      const option = {
        title: {
          text: this.selectedCategory + '数据统计',
          left: 'center',
          textStyle: { fontSize: 24, fontWeight: 'bold', color: '#333', fontFamily: "hongleixingshu" } // 改进标题样式
        },
        tooltip: {
          trigger: 'item',
          textStyle: { fontFamily: "FangSong" }
        },
        xAxis: {
          data: Object.keys(stats),
          axisLabel: { fontSize: 11, color: '#333', fontFamily: "FangSong" },
          axisLine: { lineStyle: { color: '#ccc' } },
          axisTick: { show: false } // 隐藏x轴刻度线
        },
        yAxis: {
          axisLabel: { fontSize: 12, color: '#333', fontFamily: "FangSong" },
          axisLine: { lineStyle: { color: '#ccc' } },
        },
        series: [{
          name: '数量',
          type: 'bar',
          data: Object.values(stats),
          itemStyle: {
            color: barColor,  // 柱子的颜色
            borderRadius: [10, 10, 0, 0], // 为柱子设置圆角
            borderWidth: 2,  // 增加边框宽度
            borderColor: '#fff',  // 边框颜色为白色
          },
          animationType: 'scale', // 添加缩放动画效果
          animationEasing: 'elasticOut', // 弹性动画
          animationDelay: (idx) => idx * 100 // 动画延迟
        }]
      };
      categoryChart.setOption(option);
    },

    // 初始化右侧饼图：展示当前选中大类中各子类别占比
    initsubcategoryChart() {
      console.log("init right chart");
      let data = [];
      let noData = false; // 标识是否所有数据均为0

      if (this.selectedCategory) {
        // console.log("selectedCategory: ", this.selectedCategory);
        // 获取选中大类对应的所有子类别
        const subCats = categoryData[this.selectedCategory] || [];
        // 初始化各子类别统计数据
        let subStats = {};
        subCats.forEach(sub => {
          subStats[sub] = 0;
        });
        // 遍历标注点，统计属于当前大类中各子类别的数量
        MarkDatas.forEach(item => {
          if (item.category === this.selectedCategory && subStats[item.sub_category] !== undefined) {
            subStats[item.sub_category] += item.dataValue;
          }
        });
        // 如果所有统计结果都为0，则标识无数据
        if (Object.values(subStats).every(v => v === 0)) {
          noData = true;
        } else {
          data = Object.keys(subStats).map(sub => ({
            value: subStats[sub],
            name: sub
          }));
        }
      } else {
        console.log("no selectedCategory");
        let total = 0;
        let catStats = {};
        Object.keys(categoryData).forEach(cat => {
          catStats[cat] = 0;
        });
        MarkDatas.forEach(item => {
          if (catStats[item.category] !== undefined) {
            catStats[item.category] += item.dataValue;
            total += item.dataValue;
          }
        });
        // 如果总数为0，则标识无数据
        if (total === 0) {
          noData = true;
        } else {
          data = Object.keys(catStats).map(cat => ({
            value: catStats[cat],
            name: cat
          }));
        }
      }

      let option = null;
      if (noData) {
        option = {
          title: {
            text: '暂无数据',
            left: 'center',
            textStyle: { fontSize: 24, fontWeight: 'bold', color: '#333', fontFamily: "hongleixingshu" } // 改进标题样式
          },
          tooltip: {
            trigger: 'item',
            textStyle: { fontFamily: "FangSong" }
          },
          series: [{
            name: '比例',
            type: 'pie',
            radius: '50%',
            data: []
          }]
        };
      } else {
        option = {
          title: {
            text: this.selectedCategory + '类别比例',
            left: 'center',
            textStyle: { fontSize: 24, fontWeight: 'bold', color: '#333', fontFamily: "hongleixingshu" } // 改进标题样式
          },
          tooltip: {
            trigger: 'item',
            textStyle: { fontFamily: "FangSong" }
          },
          legend: { orient: 'vertical', left: 'left', textStyle: { color: '#555', fontSize: 14, fontFamily: "FangSong" } },
          series: [{
            name: '比例',
            type: 'pie',
            radius: ['30%', '60%'],  // 增加环形图的样式
            data: data,
            label: { show: false, },
            itemStyle: {
              borderColor: '#fff',
              borderWidth: 2,  // 增加边框宽度
              shadowBlur: 10,
              shadowOffsetX: 2,
              shadowOffsetY: 2,
              shadowColor: 'rgba(0, 0, 0, 0.1)'  // 增加图表的阴影效果
            },
            emphasis: {
              itemStyle: {
                shadowBlur: 15,
                shadowOffsetX: 0,
                shadowOffsetY: 0,
                shadowColor: 'rgba(0, 0, 0, 0.5)',
                // borderColor: '#333',
                borderWidth: 3
              }
            },
            animationType: 'scale', // 添加动画效果
            animationEasing: 'elasticOut',
            animationDelay: (idx) => idx * 100,
            color: [
              'rgba(100, 40, 40, 0.4)',
              'rgba(20, 109, 53, 0.4)',
              'rgba(10, 44, 70, 0.4)',
              'rgba(140, 140, 0, 0.4)',
              'rgba(140, 80, 100, 0.4)',
            ]
          }]
        };
      }
      subcategoryChart.setOption(option);

      // 添加点击事件，点击某个省份时更新地图数据（只显示该省的数据）
      subcategoryChart.off("click"); // 移除之前的 click 事件绑定
      subcategoryChart.on("click", (param) => {
        console.log("点击了类别：", param.name);
        if (!Object.keys(categoryData).includes(param.name)) {
          this.$message.warning({ message: '该类别暂无子类', duration: 1000 });
          return;
        }
        this.selectedCategory = param.name;
        this.filterData();
      });
    },

    // 定义区域分布饼图的初始化方法
    initRegionChart() {
      console.log("init region chart");
      // 获取当前地图的所有省份名称（mapJson 已加载）
      const provinces = mapJson && mapJson.features
        ? mapJson.features.map(f => f.properties.name).filter(name => name !== "")
        : [];

      // console.log("当前地图的所有省份名称:",provinces);

      // 初始化各省统计数据为0
      let regionStats = {};
      provinces.forEach(province => {
        regionStats[province] = 0;
      });

      // 遍历 MarkDatas，累计每个数据项中 dataValue 到对应省份（采用 substring 包含判断）
      let noData = true; // 标识是否所有数据均为0
      MarkDatas.forEach(item => {
        if (item.location) {
          // console.log("item.location: ", item.location);
          // 遍历所有省份名称，若 item.location 包含该省份名，则累加数据
          provinces.forEach(province => {
            if (item.location.includes(province)) {
              regionStats[province] += item.dataValue;
              noData = false;
            }
          });
        }
      });

      // 构造 ECharts 饼图数据格式
      const data = Object.keys(regionStats).map(province => ({
        name: province,
        value: regionStats[province]
      }));

      // 构造饼图 option
      let option = null;
      if (noData) {
        option = {
          title: {
            text: '暂无数据',
            left: 'center',
            textStyle: { fontSize: 24, fontWeight: 'bold', color: '#333', fontFamily: "hongleixingshu" } // 改进标题样式
          },
          tooltip: {
            trigger: 'item',
            textStyle: { fontFamily: "FangSong" }
          },
          series: [{
            name: '区域分布',
            type: 'pie',
            radius: '50%',
            data: []
          }]
        };
      } else {
        option = {
          title: {
            text: parentName === "china" ? '中国' + '区域分布' : parentName + '区域分布',
            left: 'center',
            textStyle: { fontSize: 24, fontWeight: 'bold', color: '#333', fontFamily: "hongleixingshu" } // 调整标题样式
          },
          tooltip: {
            trigger: 'item',
            textStyle: { fontFamily: "FangSong" }
          },
          legend: { show: false },
          series: [{
            name: '区域分布',
            type: 'pie',
            radius: ['25%', '50%'],  // 增加环形图的样式
            data: data,
            label: {
              formatter: '{b}',
              show: true,  // 显示每个省份的标签
              position: 'outside', // 将标签放在图外
              textStyle: { fontSize: 16, color: '#333', fontFamily: "FangSong" } // 调整标题样式
            },
            itemStyle: {
              borderColor: '#fff',
              borderWidth: 2,  // 增加边框宽度
              shadowBlur: 15,  // 强化阴影
              shadowOffsetX: 3,
              shadowOffsetY: 3,
              shadowColor: 'rgba(0, 0, 0, 0.2)',
              fontFamily: "FangSong"
            },
            emphasis: {
              itemStyle: {
                shadowBlur: 20,
                shadowOffsetX: 0,
                shadowOffsetY: 0,
                shadowColor: 'rgba(0, 0, 0, 0.4)',
                borderWidth: 3,
                fontFamily: "FangSong"
              }
            },
            animationType: 'scale', // 添加动画效果
            animationEasing: 'elasticOut',
            animationDelay: (idx) => idx * 100, // 动画延迟
            color: [
              'rgba(100, 40, 40, 0.4)',
              'rgba(20, 109, 53, 0.4)',
              'rgba(10, 44, 70, 0.4)',
              'rgba(140, 140, 0, 0.4)',
              'rgba(84, 48, 60, 0.4)',
              'rgba(45, 86, 153, 0.4)',
              'rgba(74, 117, 57, 0.4)',
              'rgba(56, 76, 153, 0.4)',
              'rgba(49, 115, 153, 0.4)',
              'rgba(82, 59, 153, 0.4)',
              'rgba(69, 105, 148, 0.4)',
              'rgba(84, 97, 28, 0.4)',
              'rgba(72, 137, 95, 0.4)',
              'rgba(101, 153, 94, 0.4)',
              'rgba(68, 83, 153, 0.4)',
              'rgba(133, 141, 151, 0.4)',
              'rgba(117, 133, 104, 0.4)',
              'rgba(151, 133, 122, 0.4)',
              'rgba(153, 138, 92, 0.4)',
              'rgba(129, 111, 145, 0.4)',
              'rgba(119, 135, 147, 0.4)',
              'rgba(125, 135, 113, 0.4)',
              'rgba(120, 108, 86, 0.4)',
              'rgba(127, 142, 136, 0.4)',
              'rgba(140, 126, 153, 0.4)'
            ]
          }]
        };
      }
      regionChart.setOption(option);

      // 添加点击事件，点击某个省份时更新地图数据（只显示该省的数据）
      regionChart.off("click"); // 移除之前的 click 事件绑定
      regionChart.on("click", (param) => {
        console.log("点击了省份：", param.name);
        const cityId = cityMap[param.name];
        if (cityId) {
          axios.get("./static/json/map/" + cityId + ".json")
            .then((response) => {
              mapJson = response.data;
              this.updateMapData(param.name);
              this.isSecondLevelMap = param.name !== "china";
              this.registerAndsetOption(myChart, cityId, param.name, mapJson, true);
              parentId = cityId;
              parentName = param.name;
              // console.log("parentName: ", parentName);
              this.initcategoryChart();
              this.initsubcategoryChart();
              this.initRegionChart();
            });
        }
      });
    },

    // 随机选择一条数据，用于展示详细信息
    selectRandomEntry() {
      if (globalAllData && globalAllData.length > 0) {
        const idx = Math.floor(Math.random() * globalAllData.length);
        const point = globalAllData[idx];
        // 格式化数据为 randomEntry
        this.randomEntry = {
          name: point.name,
          alias: point.alias,

          category: point.category,
          sub_category: point.sub_category,
          location: point.location,

          period: point.period,
          creator: point.creator,
          main_usage: point.main_usage,
          significance: point.significance,

          publish_date: point.publish_date,

          origin: point.origin,
          nutri_value: point.nutri_value,
          econo_value: point.econo_value,
          grow_env: point.grow_env,
          plant_area: point.plant_area,

          widespread: point.widespread,

          description: point.description,
          ancient_reference: point.ancient_reference,
        };
        // this.$message.success({ message: '数据', duration: 1000 });
      } else {
        this.randomEntry = null;
        this.$message.error({ message: '暂无数据展示', duration: 1000 });
      }
    },

    // 加载所有数据
    async loadAllData() {
      try {
        // 获取后端标注点数据
        const res = await axios.get(this.$baseUrl + "/api/map/markersAll");
        const mapPoints = res.data;
        const NongJu = mapPoints["NongJu"];
        const NongShu = mapPoints["NongShu"];
        const NongZhuoWu = mapPoints["NongZuoWu"];
        const NongYeJiShu = mapPoints["NongYeJiShu"];
        const NongYeWenHua = mapPoints["NongYeWenHua"];
        globalAllData = [].concat(NongJu, NongShu, NongZhuoWu, NongYeJiShu, NongYeWenHua);
        categoryData["农具"] = NongJu.map(item => item.sub_category);
        categoryData["农书"] = NongShu.map(item => item.sub_category);
        categoryData["农作物"] = NongZhuoWu.map(item => item.sub_category);
        categoryData["农业技术"] = NongYeJiShu.map(item => item.sub_category);
        categoryData["农业文化"] = NongYeWenHua.map(item => item.sub_category);
      } catch (error) {
        this.$message.error({ message: '数据加载失败', duration: 1000 });
      }
    },

    // 更新地图数据，只更新数据部分，不重新加载地图底图，可选参数 province，当传入时，仅更新该省的数据
    async updateMapData(province = "") {
      console.log("updateMapData start");
      // 如果有过滤条件，基于全局数据进行过滤；否则，直接使用全局数据
      let allData = this.selectedCategory
        ? globalAllData.filter(item => item.category === this.selectedCategory)
        : globalAllData;

      // console.log('globalAllData: ', globalAllData);

      // 如果传入了省份名称，则进一步过滤出该省的数据
      if (province) {
        allData = allData.filter(item => item.location && item.location.includes(province));
      }

      // 将数据转换为 MarkDatas 格式
      MarkDatas = allData.map(point => ({
        name: point.name,
        value: [point.lng, point.lat],
        category: point.category,
        sub_category: point.sub_category,
        location: point.location,
        dataValue: 1  // 这里默认每个标注点为1，实际可替换为真实数据
      }));
      // console.log("MarkDatas: ", MarkDatas);

      // 更新散点系列数据，不重新加载地图底图
      myChart.setOption({
        series: [{
          type: "scatter",
          coordinateSystem: "geo",
          data: MarkDatas,
          symbolSize: 8,
          itemStyle: { color: "#ffffff" },
          label: {
            // formatter: "{b}",
            formatter: function (params) {
              const name = params.name || "";
              return name.length > 8 ? name.slice(0, 8) + "…" : name;
            },
            position: "top",
            // position: "right",
            show: this.isSecondLevelMap
          }
        }]
      });
    },

    // 原有的 initMapChart 方法，只需在首次加载时调用
    async initMapChart(divid) {
      const response = await axios.get("./static/json/map/" + parentId + ".json", {});
      // console.log('parentId: ',parentId);
      mapJson = response.data;
      console.log("初始化：", response.data);

      // 先更新散点数据（基于初始全局数据或过滤条件）
      await this.updateMapData();
      this.registerAndsetOption(myChart, parentId, parentName, mapJson, false);

      // 地图渲染完成后设置焦点
      this.$nextTick(() => {
        const inputEl = this.$refs.searchInput.$el.querySelector('input');
        if (inputEl) inputEl.focus();
      });

      // 添加地图点击事件
      myChart.off("click"); // 移除之前的 click 事件绑定
      myChart.on("click", (param) => {
        if (param.seriesType === "map") {
          const cityId = cityMap[param.name];
          if (cityId) {
            axios.get("./static/json/map/" + cityId + ".json")
              .then((response) => {
                mapJson = response.data;
                this.updateMapData(param.name);
                this.isSecondLevelMap = param.name !== "china";
                this.registerAndsetOption(myChart, cityId, param.name, mapJson, true);
                parentId = cityId;
                parentName = param.name;
                // console.log("parentName", parentName)
                this.initcategoryChart();
                this.initsubcategoryChart();
                this.initRegionChart();
              });
          }
        }
        else if (param.seriesType === "scatter") {
          this.$router.push({
            path: "/visual",
            query: { name: param.data.name, category: param.data.category },
          });
        }
      });
    },

    // 地图配置方法，增加 visualMap 实现颜色映射，flag为1，表示需要将当前地图ID和Name存入mapStack
    registerAndsetOption(myChart, id, name, mapJson, flag) {
      echarts.registerMap(name, mapJson);
      let mapData = initMapData(mapJson);
      myChart.setOption({
        backgroundColor: "transparent",
        visualMap: {
          min: 0,
          max: 10, // 这个值需要根据实际数据进行调整
          left: "left",
          top: "bottom",
          text: ['高', '低'],
          calculable: true,
          inRange: {
            color: ['#e0f3f8', '#0868ac']
          },
        },
        geo: [
          {
            map: name, // 地图类型
            roam: false, // 是否允许缩放和平移
            layoutCenter: ['50%', '50%'],
            layoutSize: '100%',
            label: {
              show: false, // 各个省市县的名字
              fontFamily: "FangSong",
              color: '#333',
              fontSize: 16
            },
            itemStyle: {
              // 每块的样式
              normal: {
                borderColor: "#1dc199",
                borderWidth: 1,
              },
            },
            emphasis: {
              itemStyle: {
                show: false,
                color: '#fff',
                areaColor: 'rgba(0,254,233,0.6)',
              },
            },
          },
          // 重影
          {
            type: 'map',
            map: name,
            zlevel: -1,
            // aspectScale: 1,
            layoutCenter: ['50%', '50.5%'],
            layoutSize: '100%',
            roam: false,
            silent: true,
            itemStyle: {
              borderWidth: 1,
              borderColor: 'rgba(58,149,253,0.8)',
              shadowColor: 'rgba(172, 122, 255,0.5)',
              shadowOffsetY: 5,
              shadowBlur: 15,
              areaColor: 'rgba(5,21,35,0.1)',
            },
          },
          {
            type: 'map',
            map: name,
            zlevel: -2,
            // aspectScale: 1,
            layoutCenter: ['50%', '51%'],
            layoutSize: '100%',
            roam: false,
            silent: true,
            itemStyle: {
              borderWidth: 1,
              borderColor: 'rgba(58,149,253,0.6)',
              shadowColor: 'rgba(65, 214, 255,0.6)',
              shadowOffsetY: 5,
              shadowBlur: 15,
              areaColor: 'rgba(5,21,35,0.1)',
            },
          },
          {
            type: 'map',
            map: name,
            zlevel: -3,
            // aspectScale: 1,
            layoutCenter: ['50%', '51.5%'],
            layoutSize: '100%',
            roam: false,
            silent: true,
            itemStyle: {
              borderWidth: 5,
              borderColor: 'rgba(58,149,253,0.4)',
              shadowColor: 'rgba(29, 111, 165,1)',
              shadowOffsetY: 15,
              shadowBlur: 10,
              areaColor: 'rgba(5,21,35,0.1)',
            },
          },
          {
            type: 'map',
            map: name,
            zlevel: -4,
            // aspectScale: 1,
            layoutCenter: ['50%', '52%'],
            layoutSize: '100%',
            roam: false,
            silent: true,
            itemStyle: {
              borderWidth: 5,
              borderColor: 'rgba(5,9,57,0.8)',
              shadowColor: 'rgba(29,111,165, 0.8)',
              shadowOffsetY: 15,
              shadowBlur: 10,
              areaColor: 'rgba(5,21,35,0.1)',
            },
          },
        ],
        series: [
          {
            type: "map",
            map: name,
            geoIndex: 0, // 关联到 geo 配置
            zoom: 1.25,
            data: mapData,
          },
          {
            type: "scatter",
            coordinateSystem: "geo",
            data: MarkDatas,
            symbolSize: 6,
            itemStyle: {
              color: "#ffffff",       // 点颜色
              borderColor: "#ffffff",
              borderWidth: 1,
              shadowBlur: 4,         // 增加点的可视性
              shadowColor: "#fff"
            },
            label: {
              formatter: function (params) {
                const name = params.name || "";
                return name.length > 8 ? name.slice(0, 8) + "…" : name;
              },
              // formatter: "{b}",
              position: "top",
              show: this.isSecondLevelMap,
              fontFamily: "FangSong",
              fontWeight: 'bold',
              fontSize: 20
            },
            emphasis: {
              label: {
                backgroundColor: 'rgba(250,250,250,0.6)', // 半透明黑色背景
                borderRadius: 6,
                padding: [4, 6], // [上下, 左右]
                formatter: "{b}",
                position: "top",
                // position: "right",
                color: "#FF6347",// 184 155 159
                show: true, // 若非第二级地图则悬浮时显示
                fontFamily: "FangSong",
                fontWeight: 'bold',
                fontSize: 24,
              }
            }
          }
        ]
      });

      if (flag) {
        // console.log("add mapStack: ", mapStack);
        mapStack.push({ mapId: parentId, mapName: parentName });
        parentId = id;
        parentName = name;
      }
    },

    // 分类过滤事件，仅更新数据，不重新加载地图底图
    async filterData() {
      await this.updateMapData();
      this.registerAndsetOption(myChart, parentId, parentName, mapJson, false);
      this.isSecondLevelMap = parentName !== "china";
      this.initcategoryChart();
      this.initsubcategoryChart();
      this.initRegionChart();
    }
  }
};

// 构造地图区域数据，根据 MarkDatas 中数据的 location 对每个省进行统计，location 表示省份或具体地点
function initMapData(mapJson) {
  var mapData = [];
  // 遍历地图中每个区域（通常为省份）
  for (var i = 0; i < mapJson.features.length; i++) {
    var provinceName = mapJson.features[i].properties.name;
    // 累加所有 MarkDatas 中 location 为 provinceName 的数据值
    var sum = 0;
    for (var j = 0; j < MarkDatas.length; j++) {
      if (MarkDatas[j].location.includes(provinceName)) {
        // console.log("provinceName: ", provinceName, "MarkDatas[j]: ", MarkDatas[j]);
        sum += MarkDatas[j].dataValue;
      }
    }
    mapData.push({
      name: provinceName,
      value: sum, // 若没有数据则为 0
      itemStyle: {
        normal: {
          areaColor: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: "lightgreen" },
            { offset: 1, color: "darkgreen" }
          ]),
        },
      },
    });
  }
  return mapData;
}
</script>

<style scoped>
>>>.el-input__inner {
  caret-color: #000 !important;
  color: #000 !important;
}

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

.background {
  background-image: url("../../static/耕织地图.jpg");
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
  width: 90vw;
  height: 90vh;
  margin: 0 auto;
  border-radius: 20px;
  transition: var(--transition);
  overflow: hidden;
}

/* .content-wrapper:hover {
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.12);
  transform: translateY(-2px);
  border-radius: 20px;
} */

/* 包装容器 */
.left-charts-container,
.right-charts-container {
  position: relative;
  width: 25%;
  height: 700px;
  /* background: rgba(255, 255, 255, 0.92); */
  /* border: 1px solid #ddd; */
}

.map-container {
  position: relative;
  width: 48%;
  height: 700px;
  /* background-color: rgba(255, 255, 255, 0.52); */
  /* border: 1px solid #ddd; */
}

/* 分别为左、中、右区域设置尺寸 */
#regionChart,
#categoryChart,
#subcategoryChart,
#detailPanel {
  height: 50%;
}


#mapChart {
  height: 100%;
}

/* 图表容器 */
.chart {
  width: 100%;
  height: 100%;
  z-index: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  /* background-color: rgba(255, 255, 255, 0.92); */
  /* border: 1px solid #ddd; */
}

/* 搜索框 */
.search-box {
  width: 80%;
  margin: 0 auto;
}

.search-box .el-input {
  width: 100%;
}

/* 返回按钮 */
.backBtn {
  position: absolute;
  top: 10%;
  left: 10px;
  z-index: 10;
  background-color: rgba(0, 0, 0, 0.6);
  border: none;
  color: #ffffff;
  font-family: hongleixingshu;
  cursor: pointer;
  padding: 5px 10px;
  border-radius: 3px;
}

/* 分类过滤器 */
.filter {
  position: absolute;
  top: 10%;
  right: 10px;
  z-index: 10;
  background-color: rgba(0, 0, 0, 0.6);
  padding: 5px;
  border-radius: 3px;
}

/* 详情展示面板 */
.small-title {

  font-size: 24px;
  font-weight: bold;
  color: #333;
  font-family: "hongleixingshu";
  /* font-family: "仿宋_GB2312", "FangSong", "华文仿宋", serif; */
}

.detail-panel {
  /* background-color: rgba(255, 255, 255, 0.92); */
  /* border: 1px solid #ddd; */
  padding: 10px;
  border-radius: 5px;
  /* box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1); */
  font-family: "仿宋_GB2312", "FangSong", "华文仿宋", serif;
}

.detail-panel h3 {
  margin-top: 0;
  text-align: center;
  color: #333;
}

.detail-content {
  height: 70%;
  overflow-y: auto;
  font-size: 18px;
  /* padding: 5px; */
}

.detail-content::-webkit-scrollbar {
  display: none;
}

.refreshBtn {
  margin-top: 10px;
  width: 50%;
  height: 40px;
  padding: 12px;
  border: none;
  background-color: rgba(169, 169, 169, 0.5);
  /* 半透明的灰色背景 */
  color: #333;
  /* 深灰色字体 */
  font-size: 20px;
  font-weight: bold;
  border-radius: 5px;
  /* 圆角 */
  cursor: pointer;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  /* 轻微阴影 */
  transition: all 0.3s ease;
  /* 平滑过渡动画 */
  font-family: "hongleixingshu";
  font-family: "仿宋_GB2312", "FangSong", "华文仿宋", serif;
}

.refreshBtn:hover {
  background-color: rgba(169, 169, 169, 0.5);
  /* 悬停时增加透明度 */
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2);
  /* 悬停时增加阴影 */
}

.refreshBtn:active {
  background-color: rgba(169, 169, 169, 0.7);
  /* 点击时背景更深 */
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  /* 点击时减小阴影 */
}

/* 底部区域 */
</style>
