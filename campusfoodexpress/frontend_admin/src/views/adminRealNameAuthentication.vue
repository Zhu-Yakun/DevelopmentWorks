<template>
    <div class="authentication-handling">
        <s-header :name="'实名认证管理'" :back="'/admin'"></s-header>
        <a-button type="primary" @click="$router.push('/admin')" style="margin-bottom: 10px">
            返回管理员主页
        </a-button>
        <div class="authentication-handling-box">
            <!-- 顶部的搜索框 -->
            <a-input placeholder="输入用户ID进行搜索" v-model="searchId" @input="searchAuthentication"
                style="margin-bottom: 20px" />

            <!-- 未处理实名认证表格 -->
            <h3>未处理实名认证</h3>
            <a-table :columns="columns" :data="filteredAuthentications" :pagination="false">
                <template #auth_image="{ record }">
                    <img :src="record.auth_image" alt="校卡照片" style="max-width: 100px;" />
                </template>
                <template #status="{ record }">
                    <p>{{ record.status }}</p> <!-- 用于调试，查看实际的 status 值 -->
                    <p v-if="record.status === 'pending'">未处理</p>
                    <p v-else-if="record.status === 'authorized'">通过</p>
                    <p v-else-if="record.status === 'unauthorized'">驳回</p>
                </template>
                <template #optional="{ record }">
                    <a-space>
                        <a-button type="primary" @click="openReplyModal(record)">处理</a-button>
                    </a-space>
                </template>
            </a-table>

            <!-- 已处理实名认证表格 -->
            <h3 style="margin-top: 30px">已处理实名认证</h3>
            <a-table :columns="processedColumns" :data="processedAuthentications" :pagination="false">
                <template #auth_image="{ record }">
                    <img :src="record.auth_image" alt="校卡照片" style="max-width: 100px;" />
                </template>
                <template #status="{ record }">
                    <p v-if="record.status === 'pending'">未处理</p>
                    <p v-else-if="record.status === 'authorized'">通过</p>
                    <p v-else-if="record.status === 'unauthorized'">驳回</p>
                </template>
                <!-- <template #optional="{ record }">
                    <a-space>
                        <a-button status="danger" @click="deleteAuthentication(record)">删除</a-button>
                    </a-space>
                </template> -->
            </a-table>
        </div>

        <!-- 处理模态框 -->
        <a-modal v-model:visible="replyModalVisible" title="处理实名认证" @cancel="replyModalVisible = false"
            @before-ok="submitAuthentication()">
            <a-form :model="replyForm">
                <a-form-item label="用户ID">
                    <p>{{ replyForm.user_id }}</p>
                </a-form-item>
                <a-form-item label="用户名">
                    <p>{{ replyForm.nike_name }}</p>
                </a-form-item>
                <a-form-item label="真实姓名">
                    <p>{{ replyForm.real_name }}</p>
                </a-form-item>
                <a-form-item label="电话号码">
                    <p>{{ replyForm.phone }}</p>
                </a-form-item>
                <a-form-item label="学号">
                    <p>{{ replyForm.id_number }}</p>
                </a-form-item>
                <a-form-item label="校卡照片">
                    <img :src="replyForm.auth_image" alt="校卡照片" style="max-width: 100px;" />
                </a-form-item>
                <a-form-item label="处理状态">
                    <a-radio-group v-model="replyForm.status">
                        <a-radio value="authorized">通过</a-radio>
                        <a-radio value="unauthorized">驳回</a-radio>
                    </a-radio-group>
                </a-form-item>
                <a-form-item label="请求日期">
                    <p>{{ replyForm.request_date }}</p>
                </a-form-item>
            </a-form>
        </a-modal>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import sHeader from '@/components/SimpleHeader.vue';
import { get_authenticate, update_authenticate } from '@/service/auth';

const columns = [
    { title: "用户ID", dataIndex: "user_id" },
    { title: "用户名", dataIndex: "nike_name" },
    { title: "真实姓名", dataIndex: "real_name" },
    { title: "电话号码", dataIndex: "phone" },
    // { title: "学校", dataIndex: "school" },// ?
    { title: "学号", dataIndex: "id_number" },
    { title: "校卡照片", slotName: "auth_image" },
    { title: "处理状态", dataIndex: "status" },
    { title: "请求日期", dataIndex: "request_date" },
    // { title: "审核日期", dataIndex: "review_date" },
    // { title: "审核人", dataIndex: "reviewed_by" },

    { title: "操作", slotName: "optional" }
];

const processedColumns = [
    { title: "用户ID", dataIndex: "user_id" },
    { title: "用户名", dataIndex: "nike_name" },
    { title: "真实姓名", dataIndex: "real_name" },
    { title: "电话号码", dataIndex: "phone" },
    // { title: "学校", dataIndex: "school" },// ?
    { title: "学号", dataIndex: "id_number" },
    { title: "校卡照片", slotName: "auth_image" },
    { title: "处理状态", dataIndex: "status" },
    { title: "请求日期", dataIndex: "request_date" },
    { title: "审核日期", dataIndex: "review_date" },
    { title: "审核人", dataIndex: "reviewed_by" },
];

const authenticationsData = ref([]);
const filteredAuthentications = ref([]);
const processedAuthentications = ref([]);
const searchId = ref('');
const replyForm = ref({
    id: '', user_id: '', nike_name: '', real_name: '', phone: '', id_number: '',
    auth_image: '', status: '', request_date: '', review_date: '', reviewed_by: ''
});

const replyModalVisible = ref(false);

console.log("Component is loading");  // 直接在 setup 中打印
onMounted(async () => {

    const data = await get_authenticate();
    console.log('实名认证数据', data);

    authenticationsData.value = data.data;
    filteredAuthentications.value = data.data.filter(auth => auth.status === 'pending');
    processedAuthentications.value = data.data.filter(auth => auth.status !== 'pending');// 未处理 通过 驳回

})

const searchAuthentication = () => {
    if (searchId.value) {
        filteredAuthentications.value = authenticationsData.value.filter(auth => auth.status === 'pending' && auth.userId.toString().includes(searchId.value));
        processedAuthentications.value = authenticationsData.value.filter(auth => auth.status !== 'pending' && auth.userId.toString().includes(searchId.value));
    } else {
        filteredAuthentications.value = authenticationsData.value.filter(auth => auth.status === 'pending');
        processedAuthentications.value = authenticationsData.value.filter(auth => auth.status !== 'pending');
    }
};

/**************************** 处理实名认证 ****************************/
const openReplyModal = (auth) => {
    replyForm.value = { ...auth };
    console.log(replyForm.value);
    replyModalVisible.value = true;
};

const submitAuthentication = async () => {
    console.log("Submitting reply form:", replyForm.value);

    if (replyForm.value.status !== 'authorized' && replyForm.value.status !== 'unauthorized') {
        alert("请选择通过或驳回");
        return;
    }

    const index = authenticationsData.value.findIndex(auth => auth.id === replyForm.value.id);
    if (index === -1) {
        alert("未找到该认证请求");
        return;
    }
    try {
        // 首先将 replyForm 发送到服务器
        const response = await update_authenticate(replyForm.value);

        if (response.status === 200) {
            console.log("更新成功");

            // 确认服务器更新成功后，再更新本地的 authenticationsData
            const newStatus = replyForm.value.status;
            if (newStatus === 'authorized' || newStatus === 'unauthorized') {
                authenticationsData.value[index].status = newStatus;
            } else {
                console.error("无效的状态:", newStatus);
                return;
            }
            // 根据更新后的状态重新过滤认证数据
            filteredAuthentications.value = authenticationsData.value.filter(auth => auth.status === 'pending');
            processedAuthentications.value = authenticationsData.value.filter(auth => auth.status !== 'pending');
            replyModalVisible.value = false;
        } else {
            console.log("更新失败，状态码:", response.status);
        }
    } catch (error) {
        console.error("更新认证时发生错误:", error);
    }
};

// /**************************** 删除已处理实名认证 ****************************/
// const deleteAuthentication = (auth) => {
//     const index = authenticationsData.value.findIndex(a => a.id === auth.id);
//     if (index !== -1) {
//         authenticationsData.value.splice(index, 1);  // 从数据中移除
//         processedAuthentications.value = authenticationsData.value.filter(auth => auth.status === '已处理');
//         // await deleteAuthenticationAPI(auth.id);  // 从数据库中删除
//     }
// };
</script>

<style lang="less" scoped>
@import '../common/style/mixin';

.authentication-handling {
    box-sizing: border-box;
    padding: 20px;

    .authentication-handling-box {
        font-size: 16px;
    }
}
</style>
