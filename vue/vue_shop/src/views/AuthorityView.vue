<template>
    <el-breadcrumb :separator-icon="ArrowRight">
        <el-breadcrumb-item :to="{ path: '/' }">Home</el-breadcrumb-item>
        <el-breadcrumb-item>authority management</el-breadcrumb-item>
        <el-breadcrumb-item>authority list</el-breadcrumb-item>

    </el-breadcrumb>
    <el-card class="box-card">
        <el-row>
            <el-button type="primary" :icon="CirclePlus">add role</el-button>
        </el-row>
        <el-row>
            <el-table :data="tableData.authorList" stripe class="table">
                <el-table-column type="expand">
                    <template #default="scope">

                        <el-row v-for="(m, i) in scope.row.menu" :key="m.id"
                            :class="['padding-l100 bottom', i === 0 ? 'top' : '']">
                            <el-col :span="5" ><el-tag class="margin-t10" closable  @close="removeMenu(scope.row,m.id)" >{{ m.name}}</el-tag></el-col>
                            <el-col :span="1"><el-icon class="margin-t15">
                                    <CaretRight />
                                </el-icon></el-col>
                            <el-col :span="15" >
                                <el-tag class="margin-t10" v-for="cm in m.children" :key="cm.id" type="success"
                                    closable @close="removeMenu(scope.row,cm.id)">{{ cm.name }}</el-tag>
                            </el-col>
                        </el-row>
                    </template>
                </el-table-column>
                <el-table-column prop="id" label="id" width="50" />
                <el-table-column prop="name" label="Name" width="150" />
                <el-table-column prop="desc" label="detail" />
                <el-table-column label="Operate">
                    <template #default="scope">
                        <el-button size="small">edit</el-button>
                        <el-button type="primary" @click="showMenuDialog(scope.row)">assign authority</el-button>
                        <el-button type="danger">delete</el-button>

                    </template>


                </el-table-column>



            </el-table>
        </el-row>
    </el-card>
    <el-dialog
        v-model="menuDialogVisible"
        title="assign authority"
        width="40%"
        :before-close="handleClose"
    >
        <el-tree show-checkbox :data="menuList" 
        :props="menuProps" @node-click="handleNodeClick"
        node-key="id" ref="treeRef" default-expand-all="true"
        />
        <template #footer>
        <div class="dialog-footer">
            <el-button @click="menuDialogVisible = false">Cancel</el-button>
            <el-button type="primary" @click="submitMenu">
            Confirm
            </el-button>
        </div>
        </template>
  </el-dialog>


</template>




<script setup>
import { ArrowRight, CaretRight, CirclePlus } from '@element-plus/icons-vue'
import { nextTick, onMounted, reactive, ref} from 'vue'
import { ElMessage, ElMessageBox, treeEmits } from 'element-plus'

import api from '@/api/index.js'


const tableData = reactive({
    authorList: []
})

onMounted(() => {       //頁面加載完直接渲染
    get_authority_list()
    getMenuList()
})

const get_authority_list = () => {
    api.get_roles().then(res => {

        tableData.authorList = res.data.data
    })
}




//  delete message box
const removeMenu = (row,mid) => {
    ElMessageBox.confirm(
        'Are you sure to delete this authority of the role?',
        'Warning',
        {
            confirmButtonText: 'Confirm',
            cancelButtonText: 'Cancel',
            type: 'warning',
        }
    )
        .then(() => {
            ElMessage({
                type: 'success',
                message: 'Delete completed',
            })
            api.del_role_menu(row.id,mid).then(res=>{
                //console.log(res)
                console.log('删除API响应:', res)
                get_authority_list()     // 重新渲染頁面
            })
        })
        .catch(() => {
            ElMessage({
                type: 'info',
                message: 'Delete canceled',
            })
        })
}

//assign authority
let menuDialogVisible = ref(false)    //message box
let menuList = reactive([])
let keyList = reactive([])
const treeRef = ref(null)
let rid = ref(null)
const menuProps={
    children:'children',     //tell the child node is in the 'children' 's name   children: { id: 2, name: '用户管理', children: [] },{ id: 3, name: '角色管理', children: [] }
    label:'name',
}

const showMenuDialog = (row)=>{
    menuDialogVisible.value = true   //open the meassage box
    //initialize 
    keyList=[]
    // get the level 1 menu
    row.menu.forEach(item => {     //if we donnot want to use forEach we can use for(const item of menus)
        //get the level 2 menu
        item.children.forEach(citem =>{
            keyList.push(citem.id)
        })
    });
    nextTick(()=>{  // Execution after current rendering Dom
        treeRef.value.setCheckedKeys(keyList)    //Set default selected node e.g. if we have management authority ,then give a tick in the boxes which is management authority
    })
    rid.value = row.id

}

const getMenuList = ()=>{
    api.get_menu().then(res=>{
        menuList = res.data.data
    })
}

const submitMenu = () =>{
    //get the selected item's id  from the message box  

     let mids=[
         treeRef.value.getCheckedKeys(),
        treeRef.value.getHalfCheckedKeys(),
    ]
    mids = mids.join(',')     // corresponding the bacjend format with , string

    api.set_menu(rid.value,{'mids':mids}).then(res=>{
        console.log(res.data)
        menuDialogVisible.value = false
        get_authority_list()
    })
    
    
}   





</script>




<style scoped>
.box-card {
    margin-top: 20px;
}

.padding-l100 {
    padding-left: 100px;
}

.top {
    border-top: 1px solid #eee
}

.bottom {
    border-bottom: 1px solid #eee;
}

.margin-t10 {
    margin: 10px;

}

.margin-t15 {
    margin-top: 15px
}
</style>