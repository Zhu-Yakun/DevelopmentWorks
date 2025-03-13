<template>
  <div class="container">
    <!-- 标头 -->
    <header class="app-header">
      <h1>校园食运通 - 管理员登录</h1>
    </header>

    <div class="login">
      <!-- 登录界面 -->
      <div class="login-body">
        <form @submit.prevent="onSubmit">
          <!-- 登录表单 -->
          <div class="form-group">
            <label for="username">账号 (手机号)</label>
            <input
              v-model="state.username"
              type="text"
              id="username"
              placeholder="请输入账号"
              required
            />
          </div>
          <div class="form-group">
            <label for="password">密码</label>
            <input
              v-model="state.password"
              type="password"
              id="password"
              placeholder="请输入密码"
              required
            />
          </div>
          <div class="form-actions">
            <button type="submit" class="btn-submit">登录</button>
          </div>
          <!-- 使用自定义模态框显示消息 -->
          <div v-if="modalMessage" class="modal">
            <div class="modal-content">
              <h3>提示</h3>
              <p class="modal-text">{{ modalMessage }}</p>
              <button @click="closeModal">关闭</button>
            </div>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref } from "vue";
import { useRouter } from "vue-router";
import { login } from "@/service/register-login"; // 后端登录接口

const router = useRouter();

const state = reactive({
  username: "",
  password: "",
  role: "admin", // 强制角色为管理员
});

const modalMessage = ref("");

const onSubmit = async () => {
  if (!state.username || !state.password) {
    modalMessage.value = "请填写账号和密码";
    return;
  }

  try {
    // 调用后端登录接口
    const response = await login({
      loginName: state.username,
      password: state.password,
      role: state.role,
    });

    if (response.data.token && response.data.role === "admin") {
      // 登录成功
      localStorage.setItem("token", response.data.token);
      router.push("/admin"); // 登录成功后跳转到管理员页面
    } else {
      modalMessage.value = "登录失败：账号或密码不匹配";
    }
  } catch (error) {
    modalMessage.value = "登录失败：账号或密码不匹配";
  }
};

const closeModal = () => {
  modalMessage.value = "";
};
</script>

<style scoped>
/* 保持现有的样式，或根据需要进行调整 */
.container {
  position: relative;
  width: 100%;
  height: 100vh;
  background-image: url("../static/images/img_bg_2.jpg");
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.app-header {
  text-align: center;
  margin-top: 20px;
}

.app-header h1 {
  font-size: 36px;
  color: white;
  font-weight: bold;
}

.login {
  margin-top: 20px;
  width: 400px;
  padding: 20px;
  background-color: #fff;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.form-group {
  margin-bottom: 15px;
  width: 100%;
}

.form-group input {
  width: 100%;
  padding: 12px;
  font-size: 16px;
  border: 1px solid #ddd;
  border-radius: 5px;
}

.form-actions {
  margin-top: 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.btn-submit {
  background-color: #fee200;
  color: white;
  padding: 10px;
  border: none;
  border-radius: 5px;
  width: 80%;
  cursor: pointer;
  font-size: 16px;
}

.btn-submit:hover {
  background-color: #f47c3c;
}

.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal-content {
  background-color: #fff;
  padding: 30px;
  border-radius: 10px;
  width: 80%;
  max-width: 600px;
  max-height: 70vh; /* 限制模态框高度 */
  overflow-y: auto; /* 超出时显示滚动条 */
  text-align: left;
}

.modal-content h3 {
  margin-bottom: 15px;
  font-size: 24px; /* 调整标题字体大小 */
  color: #f47c3c;
  text-align: center;
}

.modal-content p {
  font-size: 18px; /* 增大文字大小 */
  color: #333;
  line-height: 1.6;
}

.modal-content button {
  background-color: #f47c3c;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 5px;
  cursor: pointer;
  font-size: 16px;
  margin-top: 20px;
  display: block;
  margin-left: auto;
  margin-right: auto;
}
</style>
