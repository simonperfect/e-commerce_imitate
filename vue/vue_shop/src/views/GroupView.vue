<template>
    <el-breadcrumb :separator-icon="ArrowRight">
        <el-breadcrumb-item :to="{ path: '/' }">Home</el-breadcrumb-item>
        <el-breadcrumb-item :to="{ path: '/groups' }">Merchandise management</el-breadcrumb-item>
        <el-breadcrumb-item>Category list</el-breadcrumb-item>
    </el-breadcrumb>
    <el-card class="box-card">
        <el-row>
            <el-button type="primary" :icon="CirclePlus" @click="addCateDialog">Add Category</el-button>

        </el-row>
        <el-row>
            <el-table :data="tableData.data" style="width: 100%; margin-bottom: 20px" row-key="id" border>

                <el-table-column prop="id" label="ID" sortable />
                <el-table-column prop="name" label="Category name" sortable />
                <el-table-column prop="level" label="Categroy level" sortable>
                    <template #default="scope">
                        <el-tag v-if="scope.row.level == 1" type="success">level 1</el-tag>
                        <el-tag v-else-if="scope.row.level == 2" type="primary">level 2</el-tag>
                        <el-tag v-else-if="scope.row.level == 3" type="warning">level 3</el-tag>
                    </template>
                </el-table-column>
                <el-table-column label="operation" sortable>
                    <template #default="scope">
                        <el-button type="primary" size="small" :icon="Edit">edit</el-button>
                        <el-button type="danger" size="small" :icon="Delete" @click="del(scope.row)">delete</el-button>
                    </template>
                </el-table-column>
            </el-table>
        </el-row>
        <!--add category-->
        <el-dialog v-model="addDialogVisable" title="add category">
            <el-form :model="addForm" :rulse="addRules" ref="addFormRef">
                <el-form-item label="Category name" prop="name"> <!--prop is for later rules-->
                    <el-input v-model="addForm.name"></el-input>
                </el-form-item>
                <el-form-item label="parents node" prop="pid">
                    <el-cascader v-model="value" 
                        :options="options.data" 
                        :props="props" 
                        @change="handleChange"
                        separator=" > " 
                        style="width: 500px;"
                        clearable/>
                </el-form-item>
                <el-button type="primary" @click="addCate">confirm</el-button>
                <el-button  @click="addDialogVisable = false">cancel</el-button>
            </el-form>
        </el-dialog>
    </el-card>
</template>


<script setup>
import { ArrowRight, CirclePlus } from '@element-plus/icons-vue'
import { reactive, onMounted, ref } from 'vue'
import { Delete, Edit } from '@element-plus/icons-vue'
import api from '@/api/index.js'


const tableData = reactive({
    data: []
})
onMounted(() => {
    get_category()
    get_options()
})

const get_category = () => {
    api.get_category(3).then(res => {
        tableData.data = res.data.data
        console.log(tableData.data)
    })
}

//-------------------------------add category---------------------------------
let addDialogVisable = ref(false)
const value = ref([])
let addRules = reactive({
    name: [
        { required: true, message: 'please input the category name', trigger: 'blur' }
    ],

})
const addCateDialog = () => {
    addDialogVisable.value = true
}

const addForm = reactive({
    name: '',
    pid: 0,
    level:1
})

const props = {
  expandTrigger: 'hover' ,
  label:'name',
  value:'id',
  checkStrictly:true,     //means that we can independtly select any node no matter it is parent of children node
}

const handleChange = (value) => {
    if (value){
        if (value.length==1){   
            addForm.pid = value[0]     //value[0] is the pid of level one
            addForm.level=2             // set level two is because we want to add a node in this node so the added node is in level two
        }
        else if (value.length==2){
            addForm.pid = value[1]
            addForm.level=3
        }
        
    }else{
        addForm.pid=0
        addForm.level=1
    }
    console.log(addForm)


}
const options = reactive({   //add message box 's data
    data:[]
})

const get_options = () =>{
    api.get_category(2).then(res=>{
        options.data = res.data.data
    })
}


//              confirm
const addCate = ()=>{
    api.add_category(addForm).then(res=>{
        console.log(res.data)
        addDialogVisable.value=false
        get_category()
        get_options()

    })
}
</script>


<style scoped>
.box-card {
    margin-top: 20px;
}
</style>