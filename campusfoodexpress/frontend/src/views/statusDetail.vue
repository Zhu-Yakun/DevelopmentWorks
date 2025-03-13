<template>
  <div class="whole-page">
    <header class="header">
      <button class="back-button" @click="goBack">
        <van-icon name="arrow-left" size="18px" />
      </button>
    </header>

    <div class="status-detail">
      <div class="status-card">
        <h2>用户状态详情</h2>

        <!-- 选择状态 -->
        <div class="status-selection">
          <h3>选择状态</h3>
          <select v-model="selectedStatus">
            <option v-for="(status, index) in statusList" :key="index" :value="index">
              {{ status }}
            </option>
          </select>
          <input v-model="customStatusText" type="text" placeholder="输入自定义状态文字" />
        </div>

        <!-- 操作按钮 -->
        <div class="button-group">
          <button class='button' @click="handleCreateStatus" :disabled="hasActiveStatus">创建状态</button>
          <button class='button' @click="handleUpdateStatus" :disabled="!hasActiveStatus">修改状态</button>
          <button class='button' @click="handleEndStatus" :disabled="!hasActiveStatus">结束状态</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { createStatus, updateStatus, endStatus, checkActiveStatus, getStatus } from '@/service/userStatus';

export default {
  name: 'UserStatusDetail',
  data() {
    return {
      id: '',
      statusList: ['😋在干饭', '😢饿饿', '🥣等饭吃'],
      selectedStatus: null,
      customStatusText: '',
      hasActiveStatus: false,
    };
  },
  computed: {
    currentStatus() {
      return this.hasActiveStatus
        ? this.statusList[this.selectedStatus] || '未知状态'
        : '无活动状态';
    },
  },
  async created() {
    await this.checkAndFetchCurrentStatus();
  },
  methods: {
    goBack() {
      this.$router.back();
    },
    async checkAndFetchCurrentStatus() {
      try {
        const checkResponse = await checkActiveStatus();
        this.hasActiveStatus = checkResponse.has_status;

        if (this.hasActiveStatus) {
          const statusResponse = await getStatus();
          this.id = statusResponse.status.id;
          const statusId = statusResponse?.status?.status_id;
          this.customStatusText = statusResponse.status.content;

          if (statusId !== undefined && statusId < this.statusList.length) {
            this.selectedStatus = statusId;
          } else {
            this.selectedStatus = null;
          }
        } else {
          this.selectedStatus = null;
        }
      } catch (error) {
        console.error('获取当前状态失败:', error);
        this.hasActiveStatus = false;
        this.selectedStatus = null;
      }
    },
    async handleCreateStatus() {
      try {
        const selectedContent = this.customStatusText || this.statusList[this.selectedStatus];
        if (this.selectedStatus == null) {
          alert('请选择状态');
          return;
        }
        await createStatus(this.selectedStatus, selectedContent);
        alert('创建状态成功！');
        await this.checkAndFetchCurrentStatus();
      } catch (error) {
        console.error('创建状态失败:', error);
        alert(`创建状态失败：${error.message}`);
      }
    },
    async handleUpdateStatus() {
      try {
        const selectedContent = this.customStatusText || this.statusList[this.selectedStatus];
        await updateStatus(this.id, this.selectedStatus, selectedContent);
        alert('修改状态成功！');
        this.customStatusText = '';
        await this.checkAndFetchCurrentStatus();
      } catch (error) {
        console.error('修改状态失败:', error);
        alert(`修改状态失败：${error.message}`);
      }
    },
    async handleEndStatus() {
      try {
        await endStatus(this.id);
        alert('结束状态成功！');
        this.customStatusText = '';
        this.selectedStatus = null;
        await this.checkAndFetchCurrentStatus();
      } catch (error) {
        console.error('结束状态失败:', error);
        alert(`结束状态失败：${error.message}`);
      }
    },
  },
};
</script>

<style scoped>
.status-detail {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
}

.status-card {
  width: 100%;
  max-width: 400px;
  padding: 20px;
  background: #fff;
  border-radius: 15px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  text-align: center;
}

h2 {
  margin-bottom: 20px;
}

.status-selection select,
.status-selection input {
  width: 100%;
  padding: 10px;
  margin-bottom: 15px;
  border: 1px solid #ddd;
  border-radius: 10px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.button-group {
  display: flex;
  justify-content: space-between;
}

.button {
  flex: 1;
  background: linear-gradient(to right, #ff9966, #ff5e62);
  color: #fff;
  padding: 10px;
  margin: 5px;
  border: none;
  border-radius: 10px;
  font-size: 16px;
  cursor: pointer;
  transition: transform 0.2s;
}

.button:disabled {
  background: #ccc;
  cursor: not-allowed;
}
</style>
