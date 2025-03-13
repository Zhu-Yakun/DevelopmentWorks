<template>
  <div class="restaurant-account">
    <s-header :name="'商家账号管理'" :back="'/admin'"></s-header>
    <a-button
      type="primary"
      @click="$router.push('/admin')"
      style="margin-bottom: 10px"
    >
      返回管理员主页
    </a-button>
    <div class="restaurant-account-box">
      <!-- 顶部的搜索框和添加商家按钮 -->
      <a-space style="margin-bottom: 10px">
        <a-input
          placeholder="输入商家名称进行搜索"
          v-model="searchId"
          @input="searchRestaurant"
        />
        <a-button type="primary" @click="openRestaurantModal('add')"
          >添加商家</a-button
        >
      </a-space>

      <!-- 商家列表表格 -->
      <a-table
        :columns="columns"
        :data="filteredRestaurants"
        :pagination="false"
      >
        <template #status="{ record }">
          {{ record.status }}
        </template>
        <template #qr_code="{ record }">
          <!-- 显示二维码图片 -->
          <img
            :src="record.qr_code"
            alt="二维码"
            style="max-width: 100px; max-height: 100px"
          />
        </template>
        <template #image="{ record }">
          <img
            :src="record.image"
            alt="商家图片"
            style="max-width: 100px; max-height: 100px"
          />
        </template>
        <!-- <template #description>
          ……
        </template> -->
        <template #optional="{ record }">
          <a-space>
            <a-button
              type="primary"
              @click="openRestaurantModal('edit', record)"
              >编辑</a-button
            >
            <a-button
              :status="record.status === 'normal' ? 'primary' : 'danger'"
              @click="toggleStatus(record)"
            >
              {{ record.status === "normal" ? "封禁" : "解禁" }}
            </a-button>
            <a-button status="danger" @click="removeRestaurant(record)"
              >删除</a-button
            >
          </a-space>
        </template>
      </a-table>
    </div>

    <!-- 添加/编辑商家模态框 -->
    <a-modal
      v-model:visible="restaurantModalVisible"
      :title="modalTitle"
      @cancel="closeRestaurantModal"
      @before-ok="handleConfirm"
    >
      <a-form ref="restaurantForm" :model="restaurantFormData" :rules="rules">
        <a-form-item field="image" label="商家图片">
          <input
            name = "image"
            type="file"
            @change="onImageFileChange"
            style="margin-top: 10px"
          />
          <img
            v-if="previewImage.url"
            :src="previewImage.url"
            alt="商家图片预览"
            class="image-preview"
          />
          <img
            v-else-if="
              restaurantFormData.image &&
              typeof restaurantFormData.image === 'string'
            "
            :src="restaurantFormData.image"
            alt="当前商家图片"
            class="image-preview"
          />
        </a-form-item>
        <a-form-item field="name" label="商家名称">
          <a-input name="name" v-model="restaurantFormData.name" />
        </a-form-item>


        <!-- 地址栏 -->
        <a-form-item field="address" label="地址">
          <a-input
            name="address"
            v-model="restaurantFormData.address"
            @click="showMap = true"
          />
        </a-form-item>

        <!-- 地图弹窗 -->
        <a-modal
          v-model:visible="showMap"
          title="选择商家位置"
          :width="800"
          @cancel="showMap = false"
          :footer="null"
        >
          <!-- 地图组件 -->
          <MapComponent @address-selected="handleAddressSelected" />
        </a-modal>

        <a-form-item field="phone" label="电话">
          <a-input name="phone" v-model="restaurantFormData.phone" />
        </a-form-item>
        <a-form-item field="description" label="介绍">
          <a-input name="description" v-model="restaurantFormData.description" />
        </a-form-item>
        <a-form-item field="qr_code" label="二维码信息">
          <input
            name = "qr_code"  
            type="file"
            @change="onQrCodeFileChange"
            style="margin-top: 10px"
          />
          <img
            v-if="previewQrCode.url"
            :src="previewQrCode.url"
            alt="二维码预览"
            class="image-preview"
          />
          <img
            v-else-if="
              restaurantFormData.qr_code &&
              typeof restaurantFormData.qr_code === 'string'
            "
            :src="restaurantFormData.qr_code"
            alt="当前二维码"
            class="image-preview"
          />
        </a-form-item>
      </a-form>
    </a-modal>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from "vue";
import sHeader from "@/components/SimpleHeader.vue";
import MapComponent from "@/components/MapComponent.vue";
import {
  getAllRestaurants,
  addRestaurant,
  updateRestaurant,
  deleteRestaurant,
  forbidRestaurant,
  unforbidRestaurant,
} from "@/service/restaurantService";

const rules = {
  image: [{ required: true, message: "请上传商家图片", trigger: "change" }],
  name: [{ required: true, message: "请输入商家名称", trigger: "blur" }],
  address: [{ required: true, message: "请输入地址", trigger: "blur" }],
  phone: [{ required: true, message: "请输入电话", trigger: "blur" }],
  description: [{ required: true, message: "请输入介绍", trigger: "blur" }],
  qr_code: [{ required: true, message: "请上传二维码信息", trigger: "change" }],
};

const columns = [
  { title: "ID", dataIndex: "id" },
  { title: "商家图片", slotName: "image" },
  { title: "商家名称", dataIndex: "name" },
  { title: "地址", dataIndex: "address" },
  { title: "评分", dataIndex: "rating" },
  { title: "电话", dataIndex: "phone" },
  { title: "介绍", dataIndex: "description" },
  { title: "二维码信息", slotName: "qr_code" },
  { title: "状态", slotName: "status" },
  { title: "操作", slotName: "optional" },
];

const restaurantsData = ref([]);
const filteredRestaurants = ref([]);
const searchId = ref(""); // 存储搜索的 ID
const restaurantFormData = reactive({
  image: "",
  name: "",
  address: "",
  phone: "",
  description: "",
  qr_code: "",
  lat: "",
  lng: "",
});
const restaurantModalVisible = ref(false);
const modalTitle = ref("");
const isEditMode = ref(false);

const showMap = ref(false); // 控制地图弹窗显示

const handleAddressSelected = (position) => {
  restaurantFormData.address = position.address; // 将选中的地址填入地址字段
  restaurantFormData.lat = position.lat;
  restaurantFormData.lng = position.lng;
  showMap.value = false; // 关闭地图弹窗
};

onMounted(async () => {
  // 获取商家数据（假设 API 返回商家列表）
  const data = await getAllRestaurants();
  console.log("商家列表", data);
  restaurantsData.value = data;
  filteredRestaurants.value = data; // 初始化显示所有商家
});

const searchRestaurant = () => {
  if (searchId.value) {
    filteredRestaurants.value = restaurantsData.value.filter((restaurant) =>
      restaurant.name.includes(searchId.value)
    );
  } else {
    filteredRestaurants.value = restaurantsData.value;
  }
};

/**************************** 添加/编辑商家 ****************************/
const openRestaurantModal = (mode, record = null) => {
  isEditMode.value = mode === "edit";
  modalTitle.value = isEditMode.value ? "编辑商家" : "添加商家";

  if (isEditMode.value && record) {
    Object.assign(restaurantFormData, record);
  } else {
    Object.assign(restaurantFormData, {
      image: "",
      name: "",
      address: "",
      phone: "",
      description: "",
      qr_code: "",
    });
  }

  restaurantModalVisible.value = true;
};

const closeRestaurantModal = () => {
  restaurantModalVisible.value = false;

  // 重置表单字段和预览数据
  restaurantFormData.qr_code = ""; // 清空二维码信息
  previewQrCode.url = null; // 清空二维码预览
  restaurantFormData.image = ""; // 清空商家图片
  previewImage.url = null; // 清空商家图片预览

  // 清空文件输入框的值
  const fileInputs = document.querySelectorAll('input[type="file"]');
  fileInputs.forEach(input => input.value = ""); // 清空所有的文件输入框
};

const previewQrCode = reactive({ url: null }); // 存储二维码预览的URL
const previewImage = reactive({ url: null }); // 存储商家图片预览的URL

const onQrCodeFileChange = (event) => {
  const file = event.target.files[0];
  if (file) {
    const allowedTypes = ["image/png", "image/jpg", "image/jpeg", "image/gif"];
    if (!allowedTypes.includes(file.type)) {
      alert("只能上传 png, jpg, jpeg, gif 格式的图片文件！");
      event.target.value = ""; // 清空文件选择框
      return;
    }
    restaurantFormData.qr_code = file; // 将文件赋值给 qr_code
    const reader = new FileReader();
    reader.onload = (e) => {
      previewQrCode.url = e.target.result; // 设置预览URL
    };
    reader.readAsDataURL(file); // 读取文件为 Data URL
  }
};

const onImageFileChange = (event) => {
  const file = event.target.files[0];
  if (file) {
    const allowedTypes = ["image/png", "image/jpg", "image/jpeg", "image/gif"];
    if (!allowedTypes.includes(file.type)) {
      alert("只能上传 png, jpg, jpeg, gif 格式的图片文件！");
      event.target.value = ""; // 清空文件选择框
      return;
    }
    restaurantFormData.image = file; // 将文件赋值给 image
    const reader = new FileReader();
    reader.onload = (e) => {
      previewImage.url = e.target.result; // 设置预览URL
    };
    reader.readAsDataURL(file); // 读取文件为 Data URL
  }
};

const handleConfirm = async () => {
  if (isEditMode.value) {
    const index = restaurantsData.value.findIndex(
      (item) => item.id === restaurantFormData.id
    );
    if (index !== -1) {
      const result = await updateRestaurant(
        restaurantFormData.id,
        restaurantFormData
      );
      restaurantFormData.qr_code = result.data.qr_code; // 更新二维码信息
      restaurantFormData.image = result.data.image; // 更新商家图片信息
      Object.assign(restaurantsData.value[index], restaurantFormData);
    }
  } else {
    // 所有字段不能为空
    if (
      !restaurantFormData.image ||
      !restaurantFormData.name ||
      !restaurantFormData.address ||
      !restaurantFormData.phone ||
      !restaurantFormData.description ||
      !restaurantFormData.qr_code ||
      !restaurantFormData.lat ||
      !restaurantFormData.lng
    ) {
      alert("所有字段不能为空！");
      return;
    }
    const newRestaurant = {
      id: restaurantsData.value.length + 1,
      ...restaurantFormData,
    };
    const result = await addRestaurant(newRestaurant);
    newRestaurant.id = result.data.id; // 更新商家 ID
    newRestaurant.qr_code = result.data.qr_code; // 更新二维码信息
    newRestaurant.image = result.data.image; // 更新商家图片信息
    newRestaurant.status = result.data.status; // 更新商家状态
    restaurantsData.value.push(newRestaurant);
  }
  filteredRestaurants.value = restaurantsData.value;
  closeRestaurantModal();
};

/**************************** 封禁商家 ****************************/
const toggleStatus = async (restaurant) => {
  console.log("封禁商家", restaurant);
  const index = restaurantsData.value.findIndex((r) => r.id === restaurant.id);
  if (index !== -1) {
    const currentStatus = restaurantsData.value[index].status;
    if (currentStatus === "normal") {
      restaurantsData.value[index].status = "forbid"; // 将状态更改为禁号
      await forbidRestaurant(restaurant.id);
    } else {
      restaurantsData.value[index].status = "normal"; // 如果是禁号状态，则改回正常
      await unforbidRestaurant(restaurant.id);
    }
    filteredRestaurants.value = restaurantsData.value;
  }
};

/**************************** 删除商家 ****************************/
const removeRestaurant = async (restaurant) => {
  console.log("删除商家", restaurant);
  const index = restaurantsData.value.findIndex((r) => r.id === restaurant.id);
  if (index !== -1) {
    restaurantsData.value.splice(index, 1);
    filteredRestaurants.value = restaurantsData.value;
    await deleteRestaurant(restaurant.id);
  }
};
</script>

<style lang="less" scoped>
@import "../common/style/mixin";

.restaurant-account {
  box-sizing: border-box;
  padding: 20px;

  .restaurant-account-box {
    font-size: 16px;

    a {
      color: #007fff;
    }
  }
}

.image-preview {
  width: 100px;
  height: 100px;
  margin-top: 10px;
  object-fit: cover;
  border: 2px solid #ff7f32;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}
</style>
