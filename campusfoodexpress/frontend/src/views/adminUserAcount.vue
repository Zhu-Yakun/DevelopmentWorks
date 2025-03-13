<template>
    <div class="user-account">
        <s-header :name="'用户账号管理'" :back="'/admin'"></s-header>
        <a-button type="primary" @click="$router.push('/admin')" style="margin-bottom: 10px">
            返回管理员主页
        </a-button>

        <div class="user-account-box">
            <!-- 顶部的搜索框和添加用户按钮 -->
            <a-space style="margin-bottom: 10px">
                <a-input placeholder="输入用户账号进行搜索" v-model="searchId" @input="searchUser" />
            </a-space>

            <!-- 用户列表表格 -->
            <a-table :columns="columns" :data="filteredUsers" :pagination="false">
                <template #status="{ record }">
                    {{ record.status }}
                </template>
                <template #avatar="{ record }">
                    <img :src="record.avatar" alt="头像" style="max-width: 100px; max-height: 100px;" />
                </template>
                <template #optional="{ record }">
                    <a-space>
                        <!-- <a-button type="primary" @click="openEditUser(record)">编辑</a-button> -->
                        <a-button :status="record.status === 'normal' ? 'primary' : 'danger'"
                            @click="toggleBan(record)">
                            {{ record.status === 'normal' ? '封禁' : '解禁' }}
                        </a-button>
                        <a-button status="danger" @click="removeUser(record)">删除</a-button>
                    </a-space>
                </template>
            </a-table>
        </div>

        <!-- 编辑用户模态框 -->
        <!-- <a-modal v-model:visible="editUserVisible" title="编辑用户" @cancel="editUserVisible = false" @before-ok="editUser">
            <a-form :model="editUserForm">
                <a-form-item field="nickname" label="昵称">
                    <a-input v-model="editUserForm.nickname" />
                </a-form-item>
                <a-form-item field="phone" label="账号">
                    <a-input v-model="editUserForm.phone" />
                </a-form-item>
                <a-form-item field="bio" label="签名">
                    <a-input v-model="editUserForm.bio" />
                </a-form-item>
                <a-form-item field="status" label="状态">
                    <a-select v-model="editUserForm.status" placeholder="请选择状态">
                        <a-option v-for="option in statusOptions" :key="option" :value="option">{{ option
                            }}</a-option>
                    </a-select>
                </a-form-item>
            </a-form>
        </a-modal> -->

    </div>
</template>

<script setup>
// import { ref, reactive, onMounted } from 'vue';
import { ref, onMounted } from 'vue';
import sHeader from '@/components/SimpleHeader.vue'
// import { getUser, updateUser, banUser, unbanUser, deleteUser } from '@/service/admin';
import { getUser, banUser, unbanUser, deleteUser } from '@/service/admin';

const columns = [
    { title: "ID", dataIndex: "id" },
    { title: "头像", slotName: "avatar" },
    { title: "昵称", dataIndex: "nickname" },
    { title: "账号", dataIndex: "phone" },
    { title: "签名", dataIndex: "bio" },
    { title: "状态", slotName: "status" },
    { title: "操作", slotName: "optional" }
];

const usersData = ref([]);
const filteredUsers = ref([]);
const searchId = ref('');  // 存储搜索的 ID
// const statusOptions = ref(['normal', 'forbid']);
// const editUserForm = reactive({});
// const editUserVisible = ref(false);

onMounted(async () => {
    // 获取用户数据（假设 API 返回用户列表）
    const { data } = await getUser();
    usersData.value = data;
    filteredUsers.value = data;  // 初始化显示所有用户
});

const searchUser = () => {
    // 如果 searchId 不为空，则根据 ID 过滤用户
    if (searchId.value) {
        filteredUsers.value = usersData.value.filter(user => user.phone.includes(searchId.value));
    } else {
        filteredUsers.value = usersData.value;
    }
};

/**************************** 修改用户 ****************************/
// const openEditUser = (user) => {
//     editUserForm.id = user.id;
//     editUserForm.nickname = user.nickname;
//     editUserForm.phone = user.phone;
//     editUserForm.bio = user.bio;
//     editUserVisible.value = true;
//     console.log('编辑用户可见', editUserForm);
// };

// const editUser = async () => {
//     await updateUser(editUserForm);
//     console.log('编辑用户', editUserForm);
//     editUserVisible.value = false;
//     const index = usersData.value.findIndex(user => user.id === editUserForm.id);
//     if (index !== -1) {
//         usersData.value[index] = { ...editUserForm };
//     }
//     filteredUsers.value = usersData.value;
// };

/**************************** 封禁用户 ****************************/
const toggleBan = async (user) => {
    console.log('封禁用户', user);
    const index = usersData.value.findIndex(u => u.id === user.id);
    if (index !== -1) {
        const currentStatus = usersData.value[index].status;
        if (currentStatus === 'normal') {
            usersData.value[index].status = 'forbided';  // 将状态更改为禁号
            await banUser(user.id);  // TODO
        } else {
            usersData.value[index].status = 'normal';  // 如果是禁号状态，则改回正常
            await unbanUser(user.id);  // TODO
        }
        filteredUsers.value = usersData.value;
    }
};

/**************************** 删除用户 ****************************/
const removeUser = async (user) => {
    console.log('删除用户', user);
    const index = usersData.value.findIndex(u => u.id === user.id);
    if (index !== -1) {
        usersData.value.splice(index, 1);
        filteredUsers.value = usersData.value;
        await deleteUser(user.id);  // TODO
    }
};

</script>


<style lang="less" scoped>
@import '../common/style/mixin';

.user-account {
    box-sizing: border-box;
    padding: 20px;

    .user-account-box {
        font-size: 16px;

        a {
            color: #007fff;
        }
    }
}
</style>