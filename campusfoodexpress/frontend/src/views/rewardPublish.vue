<template>
  <div id="reward-publish">
    <!-- 顶部导航栏 -->
    <div class="header">
      <button class="back-button" @click="goBack">
        <van-icon name="arrow-left" size="24px" />
      </button>
      <h1>发布悬赏订单</h1>
    </div>

    <form @submit.prevent="submitReward">
      <!-- 商家选择 -->
      <div class="form-group">
        <label for="merchant">商家名称</label>
        <select v-model="selectedMerchant">
          <option v-for="merchant in merchants" :key="merchant.id" :value="merchant">
            {{ merchant.name }}
          </option>
        </select>
      </div>

      <!-- 取餐和送达时间 -->
      <div class="form-group">
        <label for="pickup-time">预计取餐时间</label>
        <input type="datetime-local" v-model="pickupTime" required />

        <label for="delivery-time">希望送达时间</label>
        <input type="datetime-local" v-model="deliveryTime" required />
      </div>

      <!-- 收货地址 -->
      <div class="form-group">
        <label for="delivery-address">收货地址</label>
        <div class="address-selector" @click="openAddressModal">
          <span>{{ selectedAddress ? `${selectedAddress.location} - ${selectedAddress.name} - ${selectedAddress.phone}`
            :
            '请选择收货地址' }}</span>
        </div>
      </div>

      <!-- 悬赏金额 -->
      <div class="form-group">
        <label for="reward-amount">悬赏金额 (元)</label>
        <input v-model.number="rewardAmount" type="number" step="1" placeholder="请输入悬赏金额" required />
      </div>

      <!-- 外卖员手机号 -->
      <div class="form-group">
        <label for="courier-phone">外卖员手机号 (可选)</label>
        <input v-model="courierPhone" type="text" placeholder="请输入外卖员手机号" />
      </div>

      <!-- 备注 -->
      <div class="form-group">
        <label for="note">备注 (可选)</label>
        <textarea v-model="note" placeholder="请输入备注信息"></textarea>
      </div>

      <!-- 提交按钮 -->
      <button type="submit">提交悬赏订单</button>
    </form>

    <!-- 地址选择弹出框 -->
    <div v-if="showAddressModal" class="address-modal-overlay" @click="closeAddressModal">
      <div class="address-modal" @click.stop>
        <div class="address-modal-content">
          <!-- 添加左侧返回按钮 -->
          <button class="modal-back-button" @click="closeAddressModal">‹</button>
          <h2>选择收货地址</h2>
          <div v-for="address in addressHistory" :key="address.id" class="address-item" @click="selectAddress(address)">
            <span class="tag">{{ address.tag }}</span>
            <div class="address-info">
              <p class="address-text">{{ `${address.location} - ${address.name}${address.gender} - ${address.phone}` }}
              </p>
            </div>
          </div>
          <button class="add-address-button" @click="navigateToAddAddress">新增收货地址</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import { addOrder, getAddresses } from "@/service/order.js"; // 导入订单创建函数
import { getAllRestaurants } from "@/service/restaurantService.js"; // 导入获取所有商家信息的函数

export default {
  setup() {
    const router = useRouter();

    // 数据状态
    const merchants = ref([]);
    const addressHistory = ref([
      // { id: 1, tag: "学校", name: "牛先生", gender: "先生", address: "同济大学(嘉定校区)-通达馆门口", phone: "19839693796" },
      // { id: 2, tag: "外卖柜", name: "牛先生", gender: "先生", address: "嘉实·同济接待中心门口美团外卖柜", phone: "19839693796" },
      // { id: 3, tag: "家", name: "牛先生", gender: "先生", address: "同济大学东门美团外卖柜", phone: "19839693796" },
    ]);

    const selectedMerchant = ref(null);
    const pickupTime = ref("");
    const deliveryTime = ref("");
    const selectedAddress = ref(null);
    const rewardAmount = ref(0);
    const courierPhone = ref("");
    const note = ref("");
    const showAddressModal = ref(false);

    // 获取所有商家的信息
    const fetchAllMerchants = async () => {
      try {
        const response = await getAllRestaurants();
        merchants.value = response;
      } catch (error) {
        console.error("获取商家信息失败:", error);
        alert("获取商家信息失败，请稍后重试。");
      }
    };

    onMounted(() => {
      fetchAllMerchants(); // 页面加载时调用以获取商家信息
    });

    const openAddressModal = () => {
      fetchAllAddresses(); // 打开弹窗时调用以获取地址信息
      showAddressModal.value = true;

    };

    const closeAddressModal = () => {
      showAddressModal.value = false;
    };

    const selectAddress = (address) => {
      selectedAddress.value = address;
      closeAddressModal();
    };

    const navigateToAddAddress = () => {
      router.push({ name: "addAddress" });
    };

    // 获取所有地址
    const fetchAllAddresses = async () => {
      try {
        // 调用获取地址的 API
        const response = await getAddresses();
        addressHistory.value = response.data.addresses;
        console.log("获取地址信息成功：", addressHistory.value);//,response.data
      } catch (error) {
        console.error("获取地址信息失败：", error.response ? error.response : error.message);
        alert("获取地址信息失败，请稍后重试。");
      }
    };

    // 提交悬赏订单
    const submitReward = async () => {
      // 校验时间
      const currentTime = new Date();
      const pickupDateTime = new Date(pickupTime.value);
      const deliveryDateTime = new Date(deliveryTime.value);
      console.log("当前时间：", currentTime);

      if (pickupDateTime <= currentTime) {
        alert("预计取餐时间必须晚于当前时间");
        return;
      }
      if (deliveryDateTime <= pickupDateTime) {
        alert("希望送达时间必须晚于预计取餐时间");
        return;
      }
      if (!selectedMerchant.value) {
        alert("请选择商家");
        return;
      }
      if(rewardAmount.value < 0){
        alert("您是希望别人付费给您配送吗😨");
        return;
      }
      try {
        const orderData = {
          restaurant_id: selectedMerchant.value.id, // 商家ID
          phone: selectedAddress.value ? selectedAddress.value.phone : "",
          gender: selectedAddress.value ? selectedAddress.value.gender : "", // 从收货地址中获取性别
          delivery_person_id: null, // 默认为空
          order_date: new Date(), // 当前时间
          expected_pickup_time: pickupDateTime, // 预计取餐时间
          desired_delivery_time: deliveryDateTime, // 希望送达时间
          status: 'Created', // 初始化状态为 空闲中
          delivery_fee: rewardAmount.value,
          remarks: note.value,
          address: selectedAddress.value ? selectedAddress.value.location : "", // 按格式设置地址信息
        };

        // 调用添加订单的 API
        const response = await addOrder(orderData);
        alert("悬赏订单已提交！");

        // 打印返回的数据以供调试
        console.log("悬赏订单数据：", response);

        goBack(); // 成功提交后返回上一级页面
      } catch (error) {
        console.error("提交悬赏订单失败：", error.response ? error.response : error.message);
        alert("提交悬赏订单失败，请稍后重试。");
      }
    };

    const goBack = () => {
      router.push('/foodOrder');
    };

    return {
      merchants,
      addressHistory,
      selectedMerchant,
      pickupTime,
      deliveryTime,
      selectedAddress,
      rewardAmount,
      courierPhone,
      note,
      showAddressModal,
      openAddressModal,
      closeAddressModal,
      selectAddress,
      navigateToAddAddress,
      submitReward,
      goBack,
    };
  },
};
</script>

<style scoped>
#reward-publish {
  font-family: Arial, sans-serif;
  background-color: #f8f4ec;
  /* 页面下方区域的浅色背景 */
  color: #333;
  min-height: 100vh;
  /* max-width: 500px;  控制页面宽度 */
  margin: 0px auto;
  border-radius: 10px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  padding-bottom: 20px;
}

.header {
  height: 100px;
  background: linear-gradient(to bottom, #f9e8a0, #f8f4ec);
  /* 渐变背景 */
  border-top-left-radius: 8px;
  border-top-right-radius: 8px;
}

.header h1 {
  flex-grow: 1;
  text-align: center;
  font-size: 25px;
  /* 增加字体大小 */
  font-weight: bold;
  /* 加粗字体 */
  color: #333;
  padding-top: 35px;
}


h1 {
  flex-grow: 1;
  text-align: center;
  font-size: 18px;
  margin: 0;
}

.form-group {
  margin: 20px 15px;
  /* 增加边距 */
  background-color: #ffffff;
  padding: 15px 20px;
  border-radius: 8px;
  box-shadow: 0px 2px 5px rgba(0, 0, 0, 0.1);
  /* 卡片样式 */
}

.form-group label {
  font-weight: bold;
  color: #666;
  display: block;
  margin-bottom: 5px;
}

input,
select,
textarea {
  width: 100%;
  padding: 10px;
  font-size: 14px;
  border: 1px solid #ccc;
  border-radius: 4px;
  margin-top: 5px;
  background-color: #fdfdfd;
}

.address-selector {
  background-color: #f9f9f9;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
  cursor: pointer;
}

/* 黑色遮罩层 */
.address-modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.7);
  /* 半透明黑色遮罩 */
  display: flex;
  justify-content: center;
  align-items: flex-end;
  /* 使弹窗出现在底部 */
  z-index: 1000;
}

/* 地址选择弹窗 */
.address-modal {
  background: #fff;
  border-top-left-radius: 15px;
  border-top-right-radius: 15px;
  max-height: 70vh;
  overflow-y: auto;
  width: 100%;
  max-width: 100%;
  /* 和主区域一致的宽度 */
  margin: 0 auto;
  /* 居中对齐 */
  box-shadow: 0px -4px 15px rgba(0, 0, 0, 0.4);
  /* 阴影效果 */
  z-index: 1001;
}

/* 添加返回按钮样式 */
.modal-back-button {
  position: absolute;
  left: 15px;
  top: 15px;
  background: none;
  border: none;
  font-size: 24px;
  color: #333;
  cursor: pointer;
  z-index: 1002;
  /* 增加z-index以确保按钮在最上层 */
}

/* 弹出框内容样式 */
.address-modal-content {
  padding-top: 15px;
  text-align: center;
}

.address-modal-content h2 {
  font-size: 16px;
  margin-bottom: 20px;
}

.address-item {
  padding: 10px;
  display: flex;
  align-items: center;
  border-bottom: 1px solid #f0f0f0;
  cursor: pointer;
}

.tag {
  background-color: #f1c40f;
  color: #fff;
  border-radius: 4px;
  padding: 2px 5px;
  font-size: 12px;
  margin-right: 10px;
  flex-shrink: 0;
  /* 固定宽度标签 */
}

.address-info {
  flex-grow: 1;
  text-align: left;
}

.address-text,
.address-details {
  margin: 0;
  font-size: 14px;
  color: #333;
}

.add-address-button {
  display: block;
  width: 90%;
  /* 设置按钮宽度为 90% */
  padding: 10px;
  text-align: center;
  background: #ffcc00;
  color: #fff;
  border: none;
  border-radius: 4px;
  margin: 10px auto 20px;
  /* 增加底部下边距 */
  box-shadow: 0px 2px 5px rgba(0, 0, 0, 0.1);
}
</style>