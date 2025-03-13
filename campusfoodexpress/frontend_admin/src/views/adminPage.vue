<template>
    <div class="user-box">
        <s-header :name="'我的'"></s-header>
        <div class="user-info">
            <div class="info">
                <img :src="state.user.avatar" alt="User Avatar" />
                <div class="user-desc">
                    <span>账号：{{ state.user.phone }}</span>
                    <span>账号类型：{{ state.user.role }}</span>
                </div>
            </div>
        </div>
        <div class="function-list">
            <div class="function-item" @click="goTo('/userAcount')">
                <font-awesome-icon icon="user" class="function-icon" />
                <span>用户账号</span>
            </div>
            <div class="function-item" @click="goTo('/restaurantAcount')">
                <font-awesome-icon icon="user-tie" class="function-icon" />
                <span>商家账号</span>
            </div>
            <div class="function-item" @click="goTo('/realNameAuthentication')">
                <font-awesome-icon icon="chart-bar" class="function-icon" />
                <span>实名审批</span>
            </div>
            <div class="function-item" @click="goTo('/reportHandlinig')">
                <font-awesome-icon icon="circle-exclamation" class="function-icon" />
                <span>举报处理</span>
            </div>
            <div class="function-item" @click="goTo('/comment')">
                <font-awesome-icon icon="comment" class="function-icon" />
                <span>查看评论</span>
            </div>
        </div>
        <div class="logout-button">
            <a-button status="danger" @click="logout">退出登录</a-button>
        </div>
    </div>
</template>

<script setup>
import { reactive, onMounted } from 'vue'
// import navBar from '@/components/NavBar.vue'
import sHeader from '@/components/SimpleHeader.vue'
import { getAdminInfo, adminLogout } from '@/service/admin'
import { useRouter } from 'vue-router'
const router = useRouter()
const state = reactive({
    user: {},
    loading: false
})
console.log("Component is loading");  // 直接在 setup 中打印
onMounted(async () => {
    const response = await getAdminInfo();
    /*const data = {
        "nickName": "13281598205",
        "loginName": "13281598205",
        "introduceSign": "随新所欲，蜂富多彩",
        "type": "管理员"
    }*/

    state.user = response.data
    state.loading = true

    console.log(state.user.nickname)

})

const goTo = (r, query) => {
    router.push({ path: r, query: query || {} })
}

const logout = async () => {
    const response = await adminLogout()
    if (response.status === 200) {
        localStorage.removeItem('token')
        router.push('/login')
    }
    else {
        console.log(response)
    }
}
</script>

<style lang="less" scoped>
@import '../common/style/mixin';

.user-box {
    .user-header {
        position: fixed;
        top: 0;
        left: 0;
        z-index: 10000;
        .fj();
        .wh(100%, 44px);
        line-height: 44px;
        padding: 0 10px;
        .boxSizing();
        color: #252525;
        background: #fff;
        border-bottom: 1px solid #dcdcdc;

        .user-name {
            font-size: 14px;
        }
    }

    .user-info {
        width: 94%;
        margin: 10px auto;
        height: 140px;
        background: linear-gradient(90deg, #FFD700, #FEE200); //@primary,#51c7c7
        box-shadow: 0 2px 5px #F47C3C; //#269090
        border-radius: 6px;
        overflow: hidden;

        .info {
            position: relative;
            display: flex;
            width: 100%;
            height: 100%;
            padding: 25px 20px;
            .boxSizing();

            img {
                .wh(60px, 60px);
                border-radius: 50%;
                margin-top: 4px;
            }

            .user-desc {
                display: flex;
                flex-direction: column;
                margin-left: 10px;
                line-height: 20px;
                font-size: 14px;
                color: #fff;

                span {
                    color: #fff;
                    font-size: 14px;
                    padding: 2px 0;
                }
            }
        }
    }

    .function-list {
        padding: 3%;
        background-color: #f8f8f8;
        margin-top: 20px;

        .function-item {
            display: flex;
            align-items: center;
            padding: 10px 0;
            border-bottom: 1px solid #e0e0e0;
            cursor: pointer;

            &:last-child {
                border-bottom: none;
            }

            .function-icon {
                font-size: 24px;
                color: #007bff;
                margin-right: 2%;
                /* 增加图标和文本之间的间距 */
            }

            span {
                font-size: 14px;
                color: #333;
                flex: 1;
                /* 使文本左对齐 */
            }
        }
    }

    .logout-button {
        display: flex;
        justify-content: center;
        margin-top: 20px;
        padding-bottom: 20px;
    }
}
</style>