<template>
  <div class="flex-col justify-start items-center relative page">
    <div class="background-image"></div>
    <span class="text text_3 pos_2" @click="goHome">《主页</span>
    <span class="text text_2 pos">用户中心</span>

    <div class="box content-wrapper">
      <div class="sidebar">
        <ul>
          <li><a @click="showSection('comments')">历史评论</a></li>
          <li><a @click="showSection('changePassword')">修改密码</a></li>
          <li><a @click="showSection('feedback')">使用反馈</a></li>
          <li><a @click="logout" class="logout-link">登出</a></li>
        </ul>
      </div>
      <div class="main">
        <div v-show="currentSection === 'comments'" class="section">
          <h2>历史评论</h2>
          <p style="font-size: 20px" v-if="comments.length === 0">暂无评论。</p>
          <ul class="comments-list">
            <li v-for="comment in comments" :key="comment.id" class="comment-item">
              <p class="comment-text">{{ comment.content }}</p>
              <div class="comment-footer">
                <span class="comment-date">时间:
                  {{ new Date(comment.create_time).toLocaleString() }}</span>
                <span class="comment-likes">点赞: {{ comment.likes }}</span>
              </div>
            </li>
          </ul>
        </div>
        <div v-show="currentSection === 'changePassword'" class="section">
          <h2>修改密码</h2>
          <form @submit.prevent="changePassword">
            <label class="form-label" for="oldPassword">旧密码：</label>
            <input type="password" v-model="oldPassword" id="oldPassword" /><br />
            <label class="form-label" for="newPassword">新密码：</label>
            <input type="password" v-model="newPassword" id="newPassword" /><br />
            <label class="form-label" for="confirmPassword">确认新密码：</label>
            <input type="password" v-model="confirmPassword" id="confirmPassword" /><br />
            <button class="form-label" type="submit">提交</button>
          </form>
        </div>
        <div v-show="currentSection === 'feedback'" class="section">
          <h2>使用反馈</h2>
          <form @submit.prevent="sendFeedback">
            <label class="form-label" for="rating">评价：</label>
            <select v-model="rating" id="rating">
              <option value="1">1 分</option>
              <option value="2">2 分</option>
              <option value="3">3 分</option>
              <option value="4">4 分</option>
              <option value="5">5 分</option>
            </select><br />
            <label class="form-label" for="feedbackType">反馈类型：</label>
            <select v-model="feedbackType" id="feedbackType">
              <option value="建议">建议</option>
              <option value="错误反馈">错误反馈</option>
              <option value="咨询">咨询</option>
              <option value="其他">其他</option>
            </select><br />
            <label class="form-label" for="feedbackContent">反馈内容：</label>
            <textarea v-model="feedbackContent" id="feedbackContent"></textarea><br />
            <label class="form-label" for="contact">联系方式：</label>
            <input type="text" v-model="contact" id="contact" /><br />
            <button class="form-label" type="submit">发送反馈</button>
          </form>
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
      currentSection: "comments",
      oldPassword: "",
      newPassword: "",
      confirmPassword: "",
      rating: "",
      feedbackType: "",
      feedbackContent: "",
      contact: "",
      user: JSON.parse(localStorage.getItem("user")) || null,
      comments: [],
    };
  },
  created() {
    if(localStorage.getItem("Reload") === "true"){
      localStorage.setItem("Reload", false);
      window.location.reload();
    }
    this.fetchComments();
  },
  methods: {
    goHome() {
      this.$router.push({ name: "homepage" });
    },
    async fetchComments() {
      if (!this.user) {
        this.$router.push("/login");
        return;
      }
      try {
        const response = await axios.get(
          this.$baseUrl + "/api/usercenter/usercomments"
        );
        this.comments = response.data;
        console.log(this.comments);
      } catch (error) {
        console.error(error);
      }
    },
    async logout() {
      try {
        const response = await axios.get(this.$baseUrl + "/api/logout");
        if (response.status === 200) {
          localStorage.removeItem("user");
          localStorage.setItem("isLoggedIn", "false");
          this.user = null;

          this.$router.push("/");
          window.location.reload();
          alert("您已登出");
          // this.$message.success({ message: '您已登出', duration: 1000 });
        }
      } catch (error) {
        if (error.response && error.response.status === 401) {
          this.$router.push({ path: "/login" });
        } else {
          console.error(error);
          this.$message.error({ message: "登出失败", duration: 1000 });
        }
      }
    },
    showSection(section) {
      this.currentSection = section;
    },
    async changePassword() {
      if (
        this.oldPassword === "" ||
        this.newPassword === "" ||
        this.confirmPassword === ""
      ) {
        this.$message.warning({ message: "所有位置不能为空", duration: 1000 });
        return;
      }
      if (this.oldPassword === this.newPassword) {
        this.$message.warning({
          message: "新密码不能与旧密码相同",
          duration: 1000,
        });
        return;
      }
      if (this.newPassword !== this.confirmPassword) {
        this.$message.warning({
          message: "新密码和确认新密码不一致",
          duration: 1000,
        });
        return;
      }
      try {
        const response = await axios.post(
          this.$baseUrl + "/api/usercenter/updatePwd",
          {
            oldPassword: this.oldPassword,
            newPassword: this.newPassword,
          }
        );
        if (response.status === 200) {
          this.$message.success({ message: "密码修改成功", duration: 1000 });
        }
      } catch (error) {
        this.$message.error({ message: "密码修改失败", duration: 1000 });
        console.error(error);
        if (error.response && error.response.status === 401) {
          console.error(error);
          this.$message.error({ message: "密码修改失败", duration: 1000 });
        } else {
          console.error(error);
          this.$message.error({ message: "密码修改失败", duration: 1000 });
        }
      }
    },
    async sendFeedback() {
      try {
        const response = await axios.post(
          this.$baseUrl + "/api/usercenter/feedback",
          {
            rating: this.rating,
            feedback_type: this.feedbackType,
            feedback_content: this.feedbackContent,
            contact: this.contact,
          }
        );
        if (response.status === 200) {
          this.$message.success({ message: "反馈发送成功", duration: 1000 });
        }
      } catch (error) {
        if (error.response && error.response.status === 401) {
          this.$router.push({ path: "/login" });
        } else {
          console.error(error);
          this.$message.error({ message: "反馈发送失败", duration: 1000 });
        }
      }
    },
  },
};
</script>

<style scoped>
.page {
  position: relative;
  width: 100%;
  height: 100vh;
  /* background-color: #f4e9d8; */
  overflow: hidden;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.box {
  position: relative;
  top: 5%;
  display: flex;
  justify-content: center;
  /* align-items: center; */
}

.content-wrapper {
  width: 90vw;
  height: 80vh;
  margin: 0 auto;
  transition: var(--transition);
  overflow: hidden;

  position: relative;
  display: flex;
  flex-direction: row;
  color: #333;
  text-align: left;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  background: rgba(255, 255, 255, 0.5);
  border-radius: 10px;
}

.sidebar {
  width: 20%;
  padding: 1rem;
  background: rgba(212, 181, 157, 0.5);
  /* 原色#d4b59d转为RGBA并设置透明度 */
  border-right: 1px solid #ccc;
  display: flex;
  flex-direction: column;
}

.sidebar ul {
  list-style-type: none;
  padding: 0;
}

.sidebar li {
  margin-bottom: 1em;
}

.sidebar a {
  text-decoration: none;
  color: #5a4636;
  /* 深棕色文字 */
  background: #e8d4c0;
  /* 浅土黄色背景 */
  display: block;
  padding: 0.75em;
  border: 1px solid #ccc;
  border-radius: 4px;
  text-align: center;
  transition: background-color 0.3s, color 0.3s, transform 0.3s;
}

.sidebar a:hover {
  background-color: #c8a689;
  /* 稍深土黄色 */
  color: #ffffff;
  /* 白色文字 */
  transform: translateY(-5px);
}

.sidebar button {
  width: 100%;
  padding: 0.75em;
  border: 1px solid #ccc;
  background-color: rgba(249, 249, 249, 0.5);
  /* 原色#f9f9f9转为RGBA，alpha=0.5 */
  color: #333;
  border-radius: 4px;
  cursor: pointer;
  text-align: center;
  transition: background-color 0.3s, color 0.3s;
}

.sidebar button:hover {
  background-color: #e9e9e9;
}

.main {
  flex-grow: 1;
  padding: 2rem;
  background: rgba(249, 240, 227, 0.5);
}

.section {
  display: block;
}

.section h2 {
  margin-top: 0;
  margin-bottom: 0;
  font-size: 30px;
  color: #5a4636;
}

form {
  display: flex;
  flex-direction: column;
}

form label {
  margin-top: 1em;
  font-size: 20px;
  font-weight: bold;
}

.form-label {
  color: #5a4636;
  margin-top: 1em;
  font-size: 20px;
  font-family: "hongleixingshu";
}

form input,
form textarea,
form select {
  margin-top: 0.5em;
  padding: 0.5em;
  border-radius: 4px;
  background: #f9f0e3;
  /* 浅土黄色 */
  border: 1px solid #d4b59d;
  /* 中等土黄色边框 */
}

input:focus {
  caret-color: black;
  outline: none;
  /* 去掉聚焦时的边框 */
  /* 去掉聚焦时的边框 */
}

form button {
  margin-top: 1em;
  padding: 0.5em;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s;
  background-color: #d4b59d;
  /* 中等土黄色 */
  color: #5a4636;
  /* 深棕色文字 */
}

form button:hover {
  background-color: #c8a689;
}

/* 添加首页链接的样式 */
.home-link {
  position: absolute;
  top: 2rem;
  left: 3rem;
}

.home-link .link {
  color: #5a4636;
  /* 颜色使用白色 */
  font-size: 2rem;
  /* 增大字体大小 */
  font-family: "hongleixingshu";
  /* 使用"hongleixingshu"字体 */
  text-decoration: none;
}

.home-link .link:hover {
  color: #ffffff;
  /* 白色 */
  text-decoration: underline;
}

/* 自定义滚动条样式 */
::-webkit-scrollbar {
  width: 12px;
}

::-webkit-scrollbar-track {
  background: #f9f0e3;
  border-radius: 10px;
}

::-webkit-scrollbar-thumb {
  background: #d4b59d;
  border-radius: 10px;
}

::-webkit-scrollbar-thumb:hover {
  background: #c8a689;
}

.comments-section {
  padding: 1rem;
}

.comments-list {
  max-height: 700px;
  /* height: 100%; */
  /* 固定高度 */
  overflow-y: auto;
  /* 添加滚动条 */
  /* margin: 20px 0; */
  list-style: none;
  /* border: 1px solid #d4b59d; */
  border-radius: 8px;
}

.comment-item {
  background: #f9f0e3;
  /* 浅土黄色 */
  border: 1px solid #e8d4c0;
  /* 浅土黄色边框 */
  border-radius: 8px;
  margin-bottom: 1rem;
  padding: 1rem;
  transition: background-color 0.3s;
}

.comment-item:hover {
  background-color: #e8d4c0;
}

.comment-text {
  margin: 0;
  font-size: 1rem;
  color: #5a4636;
  line-height: 1.5;
  word-wrap: break-word;
  /* 强制换行 */
}

.comment-footer {
  display: flex;
  justify-content: space-between;
  margin-top: 0.5rem;
  font-size: 0.9rem;
  color: #7a6656;
}
</style>
