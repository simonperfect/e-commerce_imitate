<template>
    <div class="common-layout container">
        <el-container class="container">
            <el-header class="header">
                <div class="logo" @click="reload">
                    <img src="@/assets/pancasila.png" , alt="" @click="reload">
                    <span>E-commerce Backend Management System</span>
                </div>
                <div class="user">
                    <el-button @click="logout"> Log Out </el-button>

                </div>
            </el-header>
            <el-container>
                <el-aside class="aside">
                    <el-menu active-text-color="#ffd04b" background-color="#545c64" class="el-menu-vertical-demo"
                        default-active="2" text-color="#fff" @open="handleOpen" @close="handleClose" unique-opened router>
                        <el-sub-menu :index="index+''" v-for="(item,index) in menuList.menus"> <!-- index="1"意思是：給「每一個」生成的 el-sub-menu 都設置 index="1"， :index="index"：動態綁定循環的索引值    v-for 想像成一台智能複印機 遍歷一個一個menus的item -->
                            <template #title>
                                <el-icon>    <!-- icons --> 
                                    <!-- <User /> -->
                                    <component :is="menuList.icons[item.id]"></component>
                                </el-icon>
                                <span>{{ item.name }}</span> <!-- 將item輸出到目錄menu -->
                            </template>
                            <el-menu-item :index="childItem.path" v-for = "childItem in item.children">{{childItem.name}}  </el-menu-item>    <!-- 這個index就是url   http://localhost:8080/user_list-->
                         

                        </el-sub-menu>



                    </el-menu>
                </el-aside>
                <el-main class="main"> <router-view/></el-main>     <!-- <router-view/> 是 Vue Router 的核心组件，它的作用是显示当前路由对应的组件内容   簡單來説就是就是当前打开的抽屉去到children index.js裏面的children-->
            </el-container>
        </el-container>
    </div>

</template>

<script setup>
import { useRouter } from 'vue-router'
import api from '@/api/index.js'
import { onMounted, reactive } from 'vue'      //reactive() 会将普通对象转换为响应式对象


const router = useRouter()

const reload = ()=>{
    router.push('/')
}

const logout = () => {
    //delete session token
    sessionStorage.removeItem('token')
    //move the page to login
    router.push('/login')
}

const menuList = reactive({                //reactive() 会将普通对象转换为响应式对象
    menus: [],                     //t_menus(id,name,level,pid) values(2,'Autority',1,-1)
    
    icons:{
        '1':'User',
        '2':'Tools',
        '3':'Shop',
        '4':'Goods',
        '5':'PieChart'

    }
})


//儅dom 元素加載完 ，調用
onMounted(() => {       //生命周期 渲染的時候自動生成  而不是按按鈕生成
    get_menu()      
})





//get the menu
const get_menu = () => {
    api.get_menu().then(res => {     // 请求成功后执行 .then()     // res 是 API 响应结果   res=>{} 等價於 function(res) {
        menuList.menus = res.data.data
    })
}




</script>



<style scoped>
.header {
    background-color: #fffefe;
    box-shadow: 0 0 5px #050505;
    font-size: 20px;
    color: rgb(252, 159, 159);
    height: 50px;
    width: 100%
}

.logo {
    float: left;
    height: 50px;
    align-items: center;
    display: flex;
    justify-content: center
}

.logo img {
    width: 40px;
    height: 40px;
    margin-right: 10px
}

.user {
    float: right;
    display: flex;
    justify-content: center;
    align-items: center;
    height: 50px
}

.aside {
    width: 300px;
    background-color: #322e4f
}

.container {
    height: 100%
}

.main{
    background-color:#e6e4e4
}

</style>
