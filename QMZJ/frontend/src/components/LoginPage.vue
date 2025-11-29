<template>
  <div class="login-page">
    <!-- 添加跳转回首页的选项 -->
    <div class="home-link">
      <router-link to="/" class="font link">《首页</router-link>
    </div>
    <div class="background-image"></div>
    <div class="login-container">
      <h2>登录</h2>
      <form @submit.prevent="login">
        <div class="input-group">
          <label v-if="accountLabelVisible" for="account">手机号</label>
          <input type="text" id="account" name="account" v-model="account" @focus="hideLabel('account')"
            @blur="showLabel('account')" autocomplete="off" />
        </div>
        <div class="input-group">
          <label v-if="passwordLabelVisible" for="password">密码</label>
          <input type="password" id="password" name="password" v-model="password" @focus="hideLabel('password')"
            @blur="showLabel('password')" autocomplete="off" />
        </div>
        <button type="submit" class="login-button">立即登录</button>
      </form>
      <div class="register-link">
        <span>没有账号？</span>
        <router-link to="/register" class="font link">立即注册</router-link>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  components: {},
  props: {},
  name: "Login",
  data() {
    return {
      account: "",
      password: "",
      accountLabelVisible: true,
      passwordLabelVisible: true,
    };
  },
  mounted() {
    if (this.$route.query.redirect) {
      window.location.reload();
    }
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
    async login() {
      try {
        // 发送登录请求
        // 使用v-model绑定的数据
        const response = await axios.post(this.$baseUrl+"/api/login", {
          account: this.account,
          password: this.password,
        });
        if (response.status === 200) {
          // 使用输入的 account 作为用户信息存储
          const user = { account: this.account };
          localStorage.setItem("user", JSON.stringify(user));
          localStorage.setItem("token", response.data.access_token);

          localStorage.setItem("isLoggedIn", "true");
          localStorage.setItem("isChat", "false");
          localStorage.setItem("Reload", "false");

          // this.$router.push("/");
          this.$router.replace({
            path: this.$route.query.redirect || '/'
          })

          window.location.reload();
          this.$message.success({ message: "登录成功！", duration: 1000 });
        } else {
          this.$message.error({ message: "登录失败，请检查您的账号和密码！", duration: 1000 });
        }
      } catch (error) {
        // 第一个Promise rejection
        if (error.response.status === 401) {
          this.$message.error({ message: "账号不存在或密码错误！", duration: 1000 });
        }
        // 第二个Promise rejection
        else if (error.response.status === 400) {
          this.$message.error({ message: "请填写账号和密码！", duration: 1000 });
        }
        // 处理其他类型的错误
        else {
          console.error("Error:", error);
          this.$message.error({ message: "发生了一个错误，请稍后重试！", duration: 1000 });
        }
      }
    },
  },
};
</script>

<style scoped>
/* 页面样式 */
.login-page {
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

/* 登录容器样式 */
.login-container {
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
  /* background-image: url("../../static/bgColor.png"); */
  /* 背景纸纹理 */
  background-size: cover;
  border: none;
  /* 取消边框 */
}

/* 登录标题样式 */
.login-container h2 {
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
  margin-bottom: 2rem;
  /* 增加输入框之间的距离 */
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
  padding: 1.2rem 2rem;
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
  transform: translateY(-25%);
  /* 使标签垂直居中 */
  pointer-events: none;
  /* 使标签不可点击 */
  z-index: 1;
  /* 确保标签在输入框上层 */
}

input:-webkit-autofill {
  -webkit-box-shadow: 0 0 0 1000px transparent inset !important;
  box-shadow: 0 0 0 1000px transparent inset !important;
  -webkit-text-fill-color: #000 !important;
  /* 确保文本颜色正常 */
}

input {
  width: 16rem;
  /* 设置具体宽度值来增加长度 */
  /* 计算宽度以确保输入框适应容器 */
  border: none;
  padding: 1.2rem 2rem;
  /* 调整内边距 */
  font-size: 1.5rem;
  font-family: "hongleixingshu";
  /* 字体 */
  background: transparent;
  /* 背景透明 */
  /* color: #5b4636; */
  /* 字体颜色 */
  border-radius: 0;
  /* 边界改为直角 */
  z-index: 2;
  /* 确保输入框在标签上层 */
  padding-left: 2rem;
  /* 调整左侧内边距以确保输入文本与标签对齐 */
  transform: translate(-2.9rem, 0.5rem);
  /* 向左和向下调整位置 */
  /* background-color: aqua; */
  caret-color: auto;
}

input:focus {
  caret-color: black;
  outline: none;
  /* 去掉聚焦时的边框 */
  /* 去掉聚焦时的边框 */
}

/* 登录按钮样式 */
.login-button {
  width: 100%;
  padding: 1.75rem;
  background: url("../../static/03-立即登录框.png") no-repeat center;
  background-size: cover;
  color: #5b4636;
  /* 字体颜色 */
  border: none;
  border-radius: 0;
  /* 边界改为直角 */
  font-size: 2rem;
  cursor: pointer;
  transition: background-color 0.3s ease;
  font-family: "hongleixingshu";
  /* 字体 */
  font-weight: 400;
  /* 调整字体粗细 */
  margin-bottom: 1rem;
}

.login-button:hover {
  background-color: rgba(0, 0, 0, 0.1);
  /* 按钮悬停时略微变暗 */
}

/* 注册链接样式 */
.register-link {
  margin-top: 1rem;
  font-size: 0.9rem;
  font-family: "HYQiHei";
  /* 修改字体为 "HYQiHei" */
}

.register-link a {
  color: #5b4636;
  /* 字体颜色 */
  text-decoration: none;
  font-weight: bold;
}

.register-link a:hover {
  text-decoration: underline;
}
</style>
