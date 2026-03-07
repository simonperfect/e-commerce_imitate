<template>

    <el-breadcrumb :separator-icon="ArrowRight">
        <el-breadcrumb-item :to="{ path: '/' }">Home</el-breadcrumb-item>
        <el-breadcrumb-item>authority management</el-breadcrumb-item>
        <el-breadcrumb-item>authority list</el-breadcrumb-item>

    </el-breadcrumb>
    <el-card class="box-card">
        <el-row>
            <el-table :data="table_data.menuList" stripe class="table">
                <el-table-column prop="id" label="id" width="50" />
                <el-table-column prop="name" label="Name" />
                <el-table-column prop="path" label="Path" />
                <el-table-column prop="level" label="Level" >
                    <template #default="scope">
                        <el-tag v-if="scope.row.level == 1">Tag1 </el-tag>   <!--scope 是一个对象，包含了当前行的数据 scope.row 是數據-->
                        <el-tag v-else type="success">Tag2 </el-tag>

                    </template>


                </el-table-column>
                
                

            </el-table>
        </el-row>
    </el-card>
</template>


<script setup>
import { ArrowRight, } from '@element-plus/icons-vue';
import { reactive,onMounted } from 'vue'
import api from '@/api/index.js'

const table_data = reactive({
    menuList: [   
        {
            'id': 1,
            'name': 'Authority',
            'path': '/menu',
            'level': 1
        },
        {
            'id': 2,
            'name': 'Authority list',
            'path': '/menu/list',
            'level': 2
        }

    ],

})

// after loaded use get_menu_list
onMounted(() => {
    get_menu_list()
})

const get_menu_list = ()=>{
    api.get_menu_list().then(res=>{
        table_data.menuList = res.data.data
    })

}

</script>

<style scoped>
.box-card {
    margin-top: 20px;
}
</style>
