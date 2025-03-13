<template>
  <div class="merchant-rating">
    <header class="header">
      <button class="back-button" @click="goBack">
        <van-icon name="arrow-left" size="18px" />
      </button>
      <span class="app-name">订单评价</span>
      <p class="subtitle">您的评价有助于商家/骑手做得更好</p>
    </header>

    <!-- 商家信息卡片 -->
    <div class="merchant-card" v-if="restaurant">
      <div class="merchant-info">
        <img :src="restaurant.image" alt="商家LOGO" class="merchant-logo" />
        <div>
          <p class="merchant-name">{{ restaurant.name }}</p>
          <p class="anonymous-checkbox">
            <input type="checkbox" id="anonymous" v-model="isAnonymous" />
            <label for="anonymous">匿名评价</label>
          </p>
        </div>
      </div>
    </div>

    <!-- 综合评价 -->
    <div class="rating-section">
      <p>综合评价</p>
      <div class="emoji-rating">
        <span
          v-for="emoji in emojis"
          :key="emoji.id"
          :class="['emoji', { selected: selectedEmoji === emoji.id }]"
          @click="selectEmoji(emoji.id)"
        >
          <img
            :src="emoji.icon"
            alt=""
            class="emoji-icon"
            :class="{ gray: selectedEmoji !== emoji.id }"
          />
        </span>
      </div>
    </div>

    <!-- 文字评价 -->
    <div class="comment-section">
      <p>您的文字评价（可选）</p>
      <textarea
        v-model="commentInfo.text"
        placeholder="请输入您的评价内容（可选）"
        class="comment-box"
      ></textarea>
    </div>

    <!-- 图片上传 -->
    <div class="upload-section">
      <p>上传图片</p>
      <div class="image-preview">
        <!-- 图片预览 -->
        <div
          v-for="(image, index) in previewImages.urls"
          :key="index"
          class="image-item"
        >
          <img :src="image" alt="预览图" class="preview-image" />
          <button class="delete-btn" @click="removeImage(index)">×</button>
        </div>
        <!-- 自定义上传框 -->
        <label class="upload-box">
          <div class="upload-plus">+</div>
          <input
            type="file"
            accept="image/*"
            multiple
            @change="onFileChange"
            class="upload-input"
          />
        </label>
      </div>
    </div>

    <!-- 对骑手的评价 -->
    <div class="delivery-rating">
      <p>您对骑手满意吗？</p>
      <div class="delivery-options">
        <button
          class="delivery-btn"
          :class="{ selected: deliverySatisfaction === false }"
          @click="setDeliverySatisfaction(false)"
        >
          😠 不满意
        </button>
        <button
          class="delivery-btn"
          :class="{ selected: deliverySatisfaction === true }"
          @click="setDeliverySatisfaction(true)"
        >
          😊 满意
        </button>
      </div>
    </div>

    <!-- 提交按钮 -->
    <div class="submit-section">
      <button
        class="submit-btn"
        :disabled="!isFormValid()"
        @click="submitComment"
      >
        提交
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import { addComment } from "@/service/comment";
import { getOrderById } from "@/service/order";
import { getRestaurantById } from "@/service/restaurantService";

const route = useRoute();
const router = useRouter();

const commentInfo = reactive({
  text: "",
  rating: 5, // 默认评分
  images: [], // 保存上传的图片文件
});

const order = reactive({
  data: {},
  loading: true,
});

const restaurant = reactive({
  name: "",
  address: "",
  phone: "",
  qr_code: "",
  description: "",
  sales: "",
  image: "",
});

const previewImages = reactive({ urls: [] }); // 用于显示评论图片的预览

const emojis = reactive([
  { id: 1, icon: "./images/angry.png", label: "很差" },
  { id: 2, icon: "./images/sad.png", label: "差" },
  { id: 3, icon: "./images/calm.png", label: "一般" },
  { id: 4, icon: "./images/happy.png", label: "满意" },
  { id: 5, icon: "./images/great.png", label: "非常满意" },
]);

const selectedEmoji = ref(null); // 用 ref 来处理单个值
const deliverySatisfaction = ref(null);
const isAnonymous = ref(false);
const MAX_FILE_SIZE = 16 * 1024 * 1024;
const selectEmoji = (emojiId) => {
  selectedEmoji.value = selectedEmoji.value === emojiId ? null : emojiId;
  commentInfo.rating = selectedEmoji.value;
};

const setDeliverySatisfaction = (value) => {
  deliverySatisfaction.value = value;
};

const isFormValid = () => {
  // 确保选中表情评分和骑手满意度
  return selectedEmoji.value !== null && deliverySatisfaction.value !== null;
};

onMounted(async () => {
  fetchOrderDetails();
  fetchRestaurantDetails();
});
/* 这里原本有个bug，只能获取与订单id号相同id的商家的信息，现在已经修改 */
const fetchOrderDetails = async () => {
  try {
    const id = route.query.id;
    if (!id) {
      throw new Error("订单ID不能为空");
    }
    const response = await getOrderById(id);
    order.data = response.data;
    console.log("商家id", order.data.restaurant_id);
    order.loading = false;

    // 确保订单详情获取成功后，再获取商家详情
    if (order.data && order.data.restaurant_id) {
      fetchRestaurantDetails(order.data.restaurant_id);
    } else {
      console.error("订单中没有商家信息");
    }
  } catch (error) {
    console.error("Error loading order details:", error);
    alert("获取订单详情失败，稍后再试");
  }
};

const fetchRestaurantDetails = async (restaurantId) => {
  try {
    if (!restaurantId) {
      throw new Error("商家ID不能为空");
    }
    const response = await getRestaurantById(restaurantId); //这里原来传的是order的id
    const data = response.data;
    Object.assign(restaurant, data);
  } catch (error) {
    console.error("Error loading restaurant details:", error);
  }
};

// 删除图片
const removeImage = (index) => {
  previewImages.urls.splice(index, 1); // 删除预览
  commentInfo.images.splice(index, 1); // 删除文件
};

// 图片上传和预览
const onFileChange = (event) => {
  const files = event.target.files;
  const allowedTypes = ["image/png", "image/jpg", "image/jpeg", "image/gif"];

  // 检查是否超出最大图片数量
  if (previewImages.urls.length + files.length > 3) {
    alert("最多只能上传 3 张图片！");
    return;
  }
  // 检查图片大小
  Array.from(files).forEach((file) => {
    if (file.size > MAX_FILE_SIZE) {
      alert("文件大小不能超过 16MB");
      return;
    }
  });
  Array.from(files).forEach((file) => {
    if (!allowedTypes.includes(file.type)) {
      alert("只能上传 png, jpg, jpeg, gif 格式的图片文件！");
      return;
    }
    const reader = new FileReader();
    reader.onload = (e) => {
      previewImages.urls.push(e.target.result); // 添加到预览
    };
    reader.readAsDataURL(file); // 读取文件为 Data URL
    commentInfo.images.push(file); // 保存文件
  });
};

const submitComment = async () => {
  if (!commentInfo.text) {
    alert("评论内容不能为空！");
    return;
  }

  try {
    const formData = new FormData();
    formData.append("order_id", route.query.id);
    formData.append("restaurant_id", order.data.restaurant_id);
    formData.append("text", commentInfo.text);
    formData.append("rating", commentInfo.rating);
    formData.append("is_anonymous", isAnonymous.value);

    commentInfo.images.forEach((image, index) => {
      formData.append("images", image);
      console.log("image id", index);
    });

    const response = await addComment(formData);

    if (response.data.message === "Comment added successfully") {
      alert("评论提交成功！");
      goBack();
    } else {
      console.log("提交失败", response);
    }
  } catch (error) {
    console.error("提交评论失败", error);
  }
};

const goBack = () => {
  router.back();
};
</script>

<style scoped>
/* 整体样式 */
.merchant-rating {
  max-width: 500px;
  margin: 20px auto;
  padding: 20px;
  background: white;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

/* 标题背景 */
/* .header {
  text-align: center;
  margin-bottom: 20px;
  background: linear-gradient(180deg, #fdf48a, #efcc0a);
  padding: 15px;
  border-radius: 5px;
  display: flex;
  flex-direction: column;
}

.header h2 {
  font-size: 18px;
  color: #333;
}

.header {
  font-size: 12px;
  color: #555;
} */

.subtitle {
  font-size: 12px;
  color: #555;
}

/* 店家信息卡片 */
.merchant-card {
  display: flex;
  align-items: center;
  padding: 15px;
  margin-bottom: 15px;
  background: #f9f9f9;
  /* 浅灰色背景 */
  border-radius: 10px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.merchant-info {
  display: flex;
  align-items: center;
}

.merchant-logo {
  width: 50px;
  height: 50px;
  border-radius: 5px;
  margin-right: 10px;
}

.merchant-name {
  font-size: 16px;
  font-weight: bold;
  color: #333;
  margin: 0;
}

/* 匿名评价部分 */
.anonymous-checkbox {
  display: flex;
  align-items: center;
  font-size: 14px;
  color: #333;
  /* 改为深灰色以提高可读性 */
  margin-top: 10px;
  /* 增加顶部间距 */
  cursor: pointer;
  /* 鼠标悬停显示指针 */
}

.anonymous-checkbox input {
  margin-right: 8px;
  /* 添加复选框和文字之间的间距 */
  width: 16px;
  height: 16px;
  cursor: pointer;
}

.anonymous-checkbox:hover {
  color: #666;
  /* 鼠标悬停时字体颜色变浅 */
  transition: color 0.3s ease;
  /* 添加平滑过渡效果 */
}

/* 综合评价 */
.rating-section p {
  font-size: 14px;
  color: #555;
  margin-bottom: 20px;
  /* 添加下方间距 */
}

.emoji-rating {
  display: flex;
  justify-content: space-around;
}

.emoji-icon {
  width: 40px;
  height: 40px;
  transition: transform 0.3s ease;
}

.emoji-icon.gray {
  filter: grayscale(100%);
  opacity: 0.5;
}

.emoji.selected .emoji-icon {
  transform: scale(1.2);
}

/* 文字评价 */
.comment-section p {
  font-size: 14px;
  color: #555;
  margin-top: 20px;
  /* 添加顶部间距 */
  margin-bottom: 20px;
  /* 添加底部间距 */
}

.comment-box {
  width: 100%;
  min-height: 80px;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 5px;
  font-size: 14px;
  resize: vertical;
}

/* 图片上传区域 */
.upload-section {
  margin: 20px 0;
}

.upload-section p {
  font-size: 14px;
  color: #555;
  margin-bottom: 10px;
}

.image-preview {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.image-item {
  position: relative;
  width: 80px;
  height: 80px;
}

.preview-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 5px;
  border: 1px solid #ddd;
}

.delete-btn {
  position: absolute;
  top: -5px;
  right: -5px;
  width: 20px;
  height: 20px;
  border: none;
  background: red;
  color: white;
  border-radius: 50%;
  cursor: pointer;
  font-size: 12px;
}

/* 自定义上传框样式 */
.upload-box {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 80px;
  height: 80px;
  border: 2px dashed #ccc;
  /* 虚线边框 */
  border-radius: 5px;
  cursor: pointer;
  text-align: center;
  transition: border-color 0.3s ease;
}

.upload-box:hover {
  border-color: #666;
  /* 悬停时边框颜色变化 */
}

.upload-plus {
  font-size: 24px;
  /* "+" 的字体大小 */
  color: #ccc;
  /* 字体颜色与边框一致 */
  line-height: 1;
}

.upload-icon {
  width: 24px;
  height: 24px;
  color: #ccc;
}

.upload-input {
  display: none;
  /* 隐藏默认文件选择按钮 */
}

/* 对骑手的评价 */
.delivery-rating p {
  margin: 20px 0 10px;
  font-size: 14px;
  color: #555;
}

.delivery-options {
  display: flex;
  justify-content: space-between;
}

.delivery-btn {
  flex: 1;
  margin: 0 5px;
  padding: 10px;
  border: none;
  border-radius: 5px;
  font-size: 14px;
  cursor: pointer;
  background: #eee;
  color: #333;
  transition: background-color 0.3s, color 0.3s;
}

.delivery-btn.selected {
  background: #efcc0a;
  color: white;
}

/* 提交按钮 */
.submit-section {
  text-align: center;
  margin-top: 20px;
}

.submit-btn {
  padding: 10px 20px;
  background: #efcc0a;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.submit-btn:disabled {
  background: #ddd;
  cursor: not-allowed;
}

.back-button {
  display: flex;
  align-items: center;
  font-size: 14px;
  color: #333;
  cursor: pointer;
  margin-bottom: 10px;
  transition: color 0.3s ease;
}

.back-button:hover {
  color: #666;
}

.back-icon {
  width: 20px;
  height: 20px;
  margin-right: 5px;
}
</style>
