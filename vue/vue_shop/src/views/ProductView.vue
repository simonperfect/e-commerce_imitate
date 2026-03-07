<template>
    <el-breadcrumb :separator-icon="ArrowRight">
        <el-breadcrumb-item :to="{ path: '/' }">Home</el-breadcrumb-item>
        <el-breadcrumb-item>Merchandise management</el-breadcrumb-item>
        <el-breadcrumb-item>Product list</el-breadcrumb-item>
    </el-breadcrumb>
    <el-card class="box-card">
        <el-row>
            <el-col :span="10">
                <el-input v-model="productTable.searchKey" placeholder="Please input the product you want to search for:" clearable @clear="getProductList"> <!--@clear is search getProductlist by null-->
                    <template #append>
                        <el-button :icon="Search" @click="getProductList"/>
                    </template>
                </el-input>
            </el-col>
            <el-col :span="4">
                <el-button type="primary" @click="AddProduct">Add product</el-button>
            </el-col>
        </el-row>
        <el-row>
            <el-table :data="productTable.data">
                <el-table-column type="index"></el-table-column>
                <el-table-column label="Product Name" prop="name" show-overflow-tooltip></el-table-column>
                <el-table-column label="Price" prop="price" width="150"></el-table-column>
                <el-table-column label="Quantity" prop="number" width="150"></el-table-column>
                <el-table-column label="Product Status" prop="state" width="150"></el-table-column>
                <el-table-column label="Operations">
                    <template #default="scope">
                        <el-button type="primary" size="small">Edit</el-button>
                        <el-button type="danger" size="small" @click="removeProduct(scope.row)">Delete</el-button>
                </template>
                </el-table-column>
            </el-table>
        </el-row>

    </el-card>
</template>

<script setup>
import {ArrowRight,Search} from '@element-plus/icons-vue'
import api from '../api/index.js'
import { onMounted,reactive } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import AddProductView from './AddProductView.vue'
import { useRouter } from 'vue-router'


const router = useRouter()

onMounted(()=>{
    getProductList()
})

const productTable = reactive({
    data:[],
    searchKey:null     // as parameter of get_product_list 's name  it defaults null

})


const getProductList = () =>{
    api.get_product_list(productTable.searchKey).then(res=>{
        console.log(res.data.data)
        
        productTable.data = res.data.data
        })
}


const removeProduct = (row) =>{
    console.log(row)
    ElMessageBox.confirm(
    'Are you sure to delete'+row.name+'product?',
    'Delete product',
    {
      confirmButtonText: 'Confirm',
      cancelButtonText: 'Cancel',
      type: 'warning',
    }
  )
    .then(() => {
        api.delete_product(row.id).then(res=>{
            if (res.data.status==200){
                ElMessage({
                    type:'success',
                    message:res.data.msg
            })
            getProductList()
            }else{
                ElMessage({
                    type:'info',
                    message:res.data.msg
                })
            }        
        })    
        
    })
    .catch(() => {
        ElMessage({
            type: 'info',
            message: 'canceled',
        })
    })
}

const AddProduct = () =>{
    router.push('/add_product')
}

</script>


<style scoped>
.box-card{
    margin-top:20px;
}



</style>