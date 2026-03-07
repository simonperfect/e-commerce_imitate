<template>
    <!--要顯示主體内容-->
    <div class="main">
        <div class="login">
            <div class="logo">
                <img src="../assets/pancasila.png" ,alt="">
            </div>
            <el-form :model="user" class="user_form" :rules="userRules" ref="userFormRef">

                <el-form-item prop="name">
                    <el-input v-model="user.name" placeholder="Username" :prefix-icon="User"></el-input>
                    <!--placeholder is 提示文字-->
                </el-form-item>
                <el-form-item prop="pwd">
                    <el-input v-model="user.pwd" placeholder="Password" :prefix-icon="Lock" show-password></el-input>
                </el-form-item>

                <el-form-item class="butns">
                    <el-button type="primary" @click="submitForm(userFormRef)">Submit</el-button>
                    <el-button type="success" @click="resetForm(userFormRef)">Reset</el-button>


                </el-form-item>

            </el-form>
        </div>

    </div>



</template>


<script setup>
// setup 代表vue3方式-->
import { ref } from 'vue'
import { Lock, User } from '@element-plus/icons-vue'    //引入圖標
import { ElMessage } from 'element-plus'
import api from '@/api/index.js'    //引入api   @ means root folder src
import{useRouter} from 'vue-router'      //用來「跳轉頁面」的工具！    vue内部的引用方法

const user = ref({
    name: '',    //初始化值
    pwd: ''
})

const userRules = ref({    //ref()  应该是用于创建响应式变量
    name: [
        { required: true, message: 'Username is required', trigger: 'blur' },
        { min: 3, max: 10, message: 'length should be 3 to 10', trigger: 'blur' }
    ],
    pwd: [
        { required: true, message: 'Password is required', trigger: 'blur' }

    ]
})


const router = useRouter()   //獲取路由對象




//userFormRef  reset the form
const userFormRef = ref(null)     //创建一个响应式引用（ref），初始值为 null  引用上面ref='userFormRef'對象  

const resetForm = () => {     // formRef這是參數，名字由你決定   ()=>{}箭頭函數  相當於function(){}
    userFormRef.value?.resetFields();       // 直接reset 兩個form的資料
}

const submitForm = (formRef) => {
    formRef.validate((valid) => {
        if (valid) {
            console.log('subimit validate!')
            api.login(user.value).then(res=>{
                //根據響應的結果處理
                if (res.data.status==200){
                    ElMessage({                      //錯誤彈窗
                    message: res.data.msg,
                    type: 'success'
                    })
                    //把登錄成功後獲得的 token（身份令牌）暫時保存到瀏覽器裡
                    sessionStorage.setItem('token',res.data.data.token)     //token是key   res.data.token是token的value
                    //登錄成功后，跳轉到首頁
                    router.push('/')     //  '/'跳轉主頁
                }else{
                    ElMessage.warning({message: res.data.msg})
                }
                
            })
        }
        else {
            console.log('error submit!')
            return false;
        }
    })
}

</script>




<style scoped>
/* scoped 代表只作用在本组件内 */
.main {
    width: 100%;
    height: 100%;
    background-color: rgba(64, 4, 4, 1);
    display: flex;
    /* flexable box    操作main的内容的位置*/
    justify-content: center;
    /* 將内容水平置中 */
    align-items: center;
    /* 將内容垂直置中 */

}

.login {
    width: 450px;
    height: 300px;
    background-color: white;
    border-radius: 10px;
}

.logo {
    width: 150px;
    border: 1px solid white;
    margin: 0 auto;
    /* 水平置中 */
    margin-top: -60px;
    padding: 5px;
    border-radius: 5px;
    box-shadow: 0 0 10px #858383ff
}

img {
    width: 100%;
    height: 100%;

}

.user_form {
    padding: 20px;

}

.butns {
    display: flex;
    justify-content: space-between;
    /* 按鈕之間的距離拉開 */
}

.butns .el-button {
    flex: 1;
    /* 按鈕平均空間分配*/
}
</style>
