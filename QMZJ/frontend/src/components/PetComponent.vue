<template>
  <div v-if="isVisible" class="pet-container">
    <!-- 容器用于放置宠物小精灵 -->
  </div>
</template>

<script>
import { io } from "socket.io-client";
import MarkdownIt from "markdown-it";
import axios from 'axios';

const md = new MarkdownIt();

export default {
  name: "PetComponent",
  data() {
    return {
      isVisible: true, // 控制小精灵是否显示

      socket: null, // WebSocket 连接
      conversations: [], // 存储所有对话
      activeConversationId: null, // 当前激活的对话ID
      newMessage: "", // 新消息内容
      wordsToSay: "",
      isThinking: false,
    };
  },
  watch: {
    // 监听 activeConversation.messages 数组的变化
    "activeConversation.messages": {
      handler(newVal, oldVal) {

      },
      deep: true, // 如果 messages 是一个数组或对象，需要使用 deep 选项
    },
  },
  computed: {
    // 当前激活的对话
    activeConversation() {
      return (
        this.conversations.find(
          (conv) => conv.id === this.activeConversationId
        ) || { messages: [] }
      );
    },
  },
  async mounted() {
    await this.initPet();
    try {
      // 连接 WebSocket
      this.socket = io(this.$baseUrl); // 确保 WebSocket 服务器地址正确
      this.setupSocketListeners();
      // 获取历史对话列表
      console.log('初始化对话列表');
      const response = await axios.get(this.$baseUrl+'/api/chat/pet_chat');
      this.conversations = response.data.conversations || [];

      // 遍历 conversations 数组，找到第一个 is_pet 为 true 的对话

      console.log('this.conversations: ', this.conversations);
      const petConversation = this.conversations.find(conversation => conversation.is_pet);

      console.log('petConversation:', petConversation);

      if (petConversation) {
        // 如果找到 is_pet 为 true 的对话，选择该对话的 id
        this.activeConversationId = petConversation.id;
        await this.selectConversation(this.activeConversationId);
      } else {
        // 开始新的对话
        await this.startNewConversation();
      }
    } catch (error) {
      console.error('初始化失败:', error);
      this.$message.error({ message: '初始化失败', duration: 1000 });
    }
  },
  unmounted() {
    this.destroyPet();
  },
  methods: {
    customSayWords(text) {
      // 检查是否已经存在一个对话框
      const existingDialog = document.querySelector(".custom-dialog");
      if (existingDialog) {
        document.body.removeChild(existingDialog); // 如果存在，移除旧的对话框
      }

      // 使用 marked.js 将 Markdown 转换为 HTML
      const htmlContent = this.renderMarkdown(text);

      // 创建一个新的对话框容器
      const dialog = document.createElement("div");
      dialog.className = "custom-dialog"; // 添加一个类名以便后续查找
      dialog.style.position = "fixed";
      dialog.style.top = "50%";
      dialog.style.right = "20px";
      dialog.style.transform = "translateY(-50%)";
      dialog.style.backgroundColor = "#f9f9f9"; // 更柔和的背景色
      dialog.style.padding = "20px";
      dialog.style.maxWidth = "400px";
      dialog.style.maxHeight = "600px";
      dialog.style.width = "auto";
      dialog.style.height = "auto";
      dialog.style.overflow = "auto";
      dialog.style.border = "1px solid #ddd"; // 更淡的边框颜色
      dialog.style.borderRadius = "10px"; // 更圆润的边角
      dialog.style.zIndex = "9999";
      dialog.style.boxShadow = "0 6px 12px rgba(0, 0, 0, 0.15)"; // 更强的阴影效果
      dialog.style.transition = "all 0.3s ease"; // 添加动画过渡效果
      

      // 创建关闭按钮
      const closeButton = document.createElement("span");
      closeButton.style.position = "absolute";
      closeButton.style.top = "10px";
      closeButton.style.right = "10px";
      closeButton.style.cursor = "pointer";
      closeButton.style.color = "#555"; // 更深的关闭按钮颜色
      closeButton.style.fontSize = "18px";
      closeButton.innerHTML = "×";

      // 关闭按钮点击事件
      closeButton.addEventListener("click", () => {
        dialog.style.opacity = "0"; // 动画淡出
        dialog.style.transform = "translateY(-50%) scale(0.8)"; // 缩小并淡出
        setTimeout(() => {
          document.body.removeChild(dialog); // 完全移除对话框
        }, 300); // 等待动画完成
      });

      // 创建内容区域
      const content = document.createElement("div");
      content.style.wordWrap = "break-word";
      content.style.color = "#333"; // 更深的文字颜色
      content.style.lineHeight = "1.6"; // 增加行间距
      content.innerHTML = htmlContent; // 插入转换后的 HTML 内容

      // 将关闭按钮和内容添加到对话框
      dialog.appendChild(closeButton);
      dialog.appendChild(content);

      // 将对话框添加到页面
      document.body.appendChild(dialog);

      // 对话框出现动画
      dialog.style.opacity = "0";
      dialog.style.transform = "translateY(-50%) scale(0.8)";
      setTimeout(() => {
        dialog.style.opacity = "1";
        dialog.style.transform = "translateY(-50%) scale(1)";
      }, 10);
    },
    initPet() {
      const opt = {
        drag: true,
        showChat: true,
        color: "brown",
        size: "mini",
        menu: {
          $title: "你想做什么呢？",
          和我开启对话吧: () => {
            localStorage.setItem("isChat", "true");
            this.$router.push("/chatPage");
            window.location.reload();
            // window.open("https://www.npmjs.com/package/pet2");
          },
          多久没洗澡: `(╯﹏╰）我已经有 ${Math.floor(
            (+new Date() - 1736998485780) / (1000 * 60 * 60 * 24)
          )}天没洗澡了~`,
          拍打喂食: {
            $title: "要来点什么呢？",
            小饼干: "嗷呜~ 多谢款待 >ω<",
            胡萝卜: "人家又不是小兔子 QwQ",
          },
          和我聊天吧: [
            "你想知道什么呢？",
            (val, done) => {
              // val, 输入值
              // done 关闭对话框函数
              console.log("type val: ", typeof val);
              this.newMessage = val;
              this.isThinking = true; // “AI正在思考中”提示
              pet.sayWords("AI正在思考中");

              this.sendMessage((response) => {
                this.isThinking = false; // 关闭“AI正在思考中”提示

                console.log(response);

                // 确保 response 是字符串
                if (typeof response !== 'string') {
                  response = String(response);
                }
                if (response.length > 0) {
                  this.wordsToSay = response;
                }
                else
                  this.wordsToSay = "";
                this.customSayWords(this.wordsToSay);
                // AI 回复后调用
                // pet.sayWords(this.wordsToSay);
                // pet.freeSay(response);
                // 使用自定义输出方法
                // this.customSayWords(response);
                done();
              });
            },
          ],
          隐藏小精灵: function () {
            pet.hide();
          },
        },
        words: [
          "我们一起聊天吧 ヽ(✿ﾟ▽ﾟ)ノ",
          "咦你想说什么 oAo ?",
          "o(╯□╰)o主人你今天是不是忘记吃药了！",
          "你走，我没有你这么蠢的主人╮(╯▽╰)╭",
          "不要调戏我，我生气超凶的٩(๑`^´๑)۶",
          "看什么看，没见过这么可爱的的小精灵吗？(o°ω°o)",
          "咕~~(╯﹏╰)b，铲屎的，我已经很久没洗澡了，你看着办！",
        ],
      };
      if (window.pet) {
        window.pet.init(opt);
      } else {
        console.warn("pet.js 未加载成功，请检查网络或文件路径");
      }
    },
    hidePet() {
      this.isVisible = false;
      if (window.pet) {
        window.pet.hide();
      }
    },
    showPet() {
      this.isVisible = true;
      if (window.pet) {
        window.pet.show();
      }
    },
    destroyPet() {
      if (window.pet) {
        window.pet.destroy(); // 确保调用 destroy 方法清理资源
      }
    },
    // 转换 markdown 为 HTML
    renderMarkdown(content) {
      return md.render(content);
    },
    // 开始新对话
    async startNewConversation() {
      console.log("开始新对话");
      try {
        const response = await axios.post(
          this.$baseUrl+"/api/chat/new_conversations", { is_pet: true }
        );
        const newConv = response.data;

        this.conversations.unshift({
          id: newConv.conversation_id,
          messages: [],
        });

        this.activeConversationId = newConv.conversation_id;
        // this.$message.success({ message: "已创建新对话", duration: 1000 });
      } catch (error) {
        console.error("创建聊天失败:", error);
        ElMessage.error("创建聊天失败");
      }
    },
    // 选择历史对话
    async selectConversation(id) {
      console.log('选择对话:', id);
      this.activeConversationId = id;

      const conversation = this.conversations.find(conv => conv.id === id);
      console.log('conversation:', conversation);

      // 设置加载状态
      this.$set(conversation, 'loading', true);

      if (!conversation.messages || conversation.messages.length === 0) {
        try {
          const response = await axios.post(this.$baseUrl+'/api/chat/history', null, {
            params: { conversation_id: id },
          });

          const historyMessages = response.data.history || [];

          // 数据获取完成后，再更新响应式属性
          this.$set(conversation, 'messages', historyMessages);
          console.log('historyMessages:', historyMessages);
        } catch (error) {
          console.error('获取历史记录失败:', error);
          ElMessage.error('获取历史记录失败');
        } finally {
          // 清除加载状态
          this.$set(conversation, 'loading', false);
        }
      } else {
        // 如果已经有数据，也确保加载状态为 false
        this.$set(conversation, 'loading', false);
      }
    },
    // 发送消息 (WebSocket)
    sendMessage(callback) {
      console.log("发送消息:", this.newMessage);
      if (!this.newMessage.trim()) {
        ElMessage.warning("消息内容不能为空");
        return;
      }

      if (!this.activeConversationId) {
        ElMessage.warning("请先选择或创建对话");
        return;
      }

      const userMessage = {
        role: "user",
        content: this.newMessage,
        conversation_id: this.activeConversationId,
        user_id: this.userId,
      };

      this.newMessage = "";

      // 通过 WebSocket 发送消息
      const token = localStorage.getItem("token");
      this.socket.emit("chat", { userMessage, token });

      // 保存回调函数，以便在 AI 回复后调用
      this.callback = callback;
    },

    // 监听 AI 回复
    setupSocketListeners() {
      this.socket.on("chat_response", (data) => {
        console.log("收到 AI 回复:", data);

        if (data.status === "success") {
          const conversation = this.activeConversation;

          // 确保 message 数组是响应式的，更新到页面
          conversation.messages.push({
            role: "assistant",
            content: data.response,
          });

          // 如果有回调函数，则调用它
          if (this.callback) {
            console.log("监听ai，  如果有回调函数");
            this.callback(data.response);
          }
        } else {
          ElMessage.error("AI 回复失败");
        }
      });

      this.socket.on("connect", () => {
        console.log("WebSocket 连接成功");
      });

      this.socket.on("disconnect", () => {
        console.log("WebSocket 连接断开");
      });
    },
    beforeDestroy() {
      if (this.socket) {
        this.socket.disconnect();
      }
    },
  },
};
</script>

<style scoped>
.pet-container {
  position: fixed;
  bottom: 20px;
  right: 20px;
  z-index: 9999;
}
</style>