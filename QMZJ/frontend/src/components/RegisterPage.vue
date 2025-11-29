<template>
  <div class="register-page">
    <!-- 添加跳转回首页的选项 -->
    <div class="home-link">
      <router-link to="/" class="font link">《首页</router-link>
    </div>
    <div class="background-image"></div>
    <div class="register-container">
      <h2>注册</h2>
      <form @submit.prevent="register">
        <div class="input-group">
          <label v-if="usernameLabelVisible" for="username">用户名</label>
          <input type="text" id="username" name="username" v-model="username" autocomplete="off"
            @focus="hideLabel('username')" @blur="showLabel('username')" />
        </div>
        <div class="input-group">
          <label v-if="accountLabelVisible" for="account">手机号</label>
          <input type="text" id="account" name="account" v-model="account" autocomplete="off"
            @focus="hideLabel('account')" @blur="showLabel('account')" />
        </div>
        <div class="input-group">
          <label v-if="passwordLabelVisible" for="password">密码</label>
          <input type="password" id="password" name="password" v-model="password" autocomplete="off"
            @focus="hideLabel('password')" @blur="showLabel('password')" />
        </div>
        <div class="input-group">
          <label v-if="confirmPasswordLabelVisible" for="confirm-password">确认密码</label>
          <input type="password" id="confirm-password" name="confirm-password" v-model="confirmPassword"
            autocomplete="off" @focus="hideLabel('confirmPassword')" @blur="showLabel('confirmPassword')" />
        </div>
        <button type="submit" class="register-button">立即注册</button>
      </form>
      <div class="login-link">
        <span>已有账号？</span>
        <router-link to="/login" class="font link">立即登录</router-link>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  components: {},
  props: {},
  name: "Register",
  data() {
    return {
      username: "",
      account: "",
      password: "",
      confirmPassword: "",
      usernameLabelVisible: true,
      accountLabelVisible: true,
      passwordLabelVisible: true,
      confirmPasswordLabelVisible: true,
    };
  },
  methods: {
    hideLabel(field) {
      this[`${field}LabelVisible`] = false;
    },
    showLabel(field) {
      if (!this[field]) {
        this[`${field}LabelVisible`] = true;
      }
    },
    async register() {
      if (this.password !== this.confirmPassword) {
        this.$message.error({ message: "密码和确认密码不匹配！", duration: 1000 });
        return;
      }
      try {
        // 发送登录请求
        // 使用v-model绑定的数据
        const response = await axios.post(
          this.$baseUrl+"/api/register",
          {
            username: this.username,
            account: this.account,
            password: this.password,
          }
        );
        if (response.status === 201) {
          // 登录成功，可以进行路由跳转或其他操作
          if (this.$route.path !== "/login") {
            this.$router.push("/login");
          }
        }
      } catch (error) {
        // 错误处理，例如网络错误提示
        if (error.response) {
          if (error.response.status === 400) {
            this.$message.error({ message: "缺少必要字段！", duration: 1000 });
          } else if (error.response.status === 409) {
            this.$message.error({ message: "该手机号已注册！", duration: 1000 });
          } else {
            this.$message.error({ message: "注册失败，请稍后再试", duration: 1000 });
          }
        } else {
          console.error("注册请求失败:", error);
          this.$message.error({ message: "注册请求失败，请稍后再试", duration: 1000 });
        }
      }
    },
  },
};
</script>

<style scoped>
/* 页面样式 */
.register-page {
  position: relative;
  width: 100%;
  height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: transparent;
  overflow: hidden;
}

/* 添加首页链接的样式 */
.home-link {
  position: absolute;
  top: 2rem;
  left: 3rem;
}

.home-link .link {
  color: #ffffff;
  /* 颜色使用白色 */
  font-size: 2rem;
  /* 增大字体大小 */
  font-family: "hongleixingshu";
  /* 使用"hongleixingshu"字体 */
  text-decoration: none;
}

.home-link .link:hover {
  text-decoration: underline;
}

/* 注册容器样式 */
.register-container {
  position: relative;
  width: 350px;
  padding: 2rem;
  background-color: rgba(255, 255, 255, 0.3);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
  /* 更明显的悬空阴影效果 */
  border-radius: 0;
  /* 边界改为直角 */
  text-align: center;
  /* background-image: url("../../static/01-登录-背景图.png"); */
  /* 背景纸纹理 */
  background-size: cover;
  border: none;
  /* 取消边框 */
}

/* 注册标题样式 */
.register-container h2 {
  font-family: "hongleixingshu";
  /* 字体 */
  font-size: 3rem;
  color: #5b4636;
  /* 字体颜色 */
  font-weight: 550;
  /* 调整字体粗细 */
  margin-bottom: 1rem;
}

.input-group {
  margin-bottom: 0.1rem;
  /* 减少输入框之间的距离 */
  position: relative;
  background: url("../../static/03-账号密码框.png") no-repeat center center;
  /* 确保背景图居中对齐 */
  background-size: contain;
  /* 确保背景图完整显示 */
  display: flex;
  /* 使用 Flexbox 布局 */
  justify-content: flex-start;
  /* 左对齐 */
  align-items: center;
  /* 垂直居中对齐 */
  padding: 1rem 2rem;
  /* 添加内边距以确保输入框不贴边 */
}

label {
  font-size: 1.6rem;
  color: #5b4636;
  /* 字体颜色 */
  font-family: "hongleixingshu";
  /* 字体 */
  position: absolute;
  top: 50%;
  left: 0.8rem;
  /* 调整左边距 */
  transform: translateY(-35%);
  /* 使标签垂直居中 */
  pointer-events: none;
  /* 使标签不可点击 */
  z-index: 1;
  /* 确保标签在输入框上层 */
}

input {
  width: 20rem;
  /* 增大输入框的宽度 */
  border: none;
  padding: 1.2rem 2rem;
  /* 调整内边距 */
  font-size: 1.3rem;
  font-family: "hongleixingshu";
  /* 字体 */
  background: transparent;
  /* 背景透明 */
  color: #5b4636;
  /* 字体颜色 */
  border-radius: 0;
  /* 边界改为直角 */
  z-index: 2;
  /* 确保输入框在标签上层 */
  padding-left: 2rem;
  /* 调整左侧内边距以确保输入文本与标签对齐 */
  transform: translate(-1.8rem, 0.4rem);
  /* 向左和向下调整位置 */
}

input:-webkit-autofill {
  -webkit-box-shadow: 0 0 0 1000px transparent inset !important;
  box-shadow: 0 0 0 1000px transparent inset !important;
  -webkit-text-fill-color: #000 !important;
  /* 确保文本颜色正常 */
}

input:focus {
  caret-color: black;
  outline: none;
  /* 去掉聚焦时的边框 */
  /* 去掉聚焦时的边框 */
}

/* 注册按钮样式 */
.register-button {
  width: 90%;
  padding: 1.7rem;
  background: url("../../static/03-立即登录框.png") no-repeat center;
  background-size: cover;
  color: #5b4636;
  /* 字体颜色 */
  border: none;
  border-radius: 0;
  /* 边界改为直角 */
  font-size: 1.6rem;
  cursor: pointer;
  transition: background-color 0.3s ease;
  font-family: "hongleixingshu";
  /* 字体 */
  font-weight: 400;
  /* 调整字体粗细 */
  margin-bottom: 0.5rem;
}

.register-button:hover {
  background-color: rgba(0, 0, 0, 0.1);
  /* 按钮悬停时略微变暗 */
}

/* 登录链接样式 */
.login-link {
  margin-top: 1rem;
  font-size: 0.9rem;
  font-family: "HYQiHei";
  /* 修改字体为 "HYQiHei" */
}

.login-link a {
  color: #5b4636;
  /* 字体颜色 */
  text-decoration: none;
  font-weight: bold;
}

.login-link a:hover {
  text-decoration: underline;
}
</style>
