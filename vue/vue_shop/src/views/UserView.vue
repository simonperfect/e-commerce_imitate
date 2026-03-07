<!-- 
裝修店面（組件創建）→ setup()

擺放貨架（模板渲染）→ template

正式開門營業（掛載完成）→ onMounted() ← 這時候才開始接待客人！

客人進店購物（獲取數據）→ get_user_list() 

-->




<template>

    <el-breadcrumb :separator-icon="ArrowRight">
        <el-breadcrumb-item :to="{ path: '/' }">Home</el-breadcrumb-item>
        <el-breadcrumb-item>Guests management</el-breadcrumb-item>
        <el-breadcrumb-item>Guests list</el-breadcrumb-item>

    </el-breadcrumb>

    <el-card class="box-card">
        <el-row :gutter="20">
            <el-col :span="8">
                <el-input v-model="user_data.queryName" style="max-width: 600px" placeholder="Search"
                    class="input-with-select">


                    <template #append>
                        <el-button :icon="Search" @click="searchuser" />
                    </template>
                </el-input>
            </el-col>
            <el-col :span="2">
                <el-button type="primary" :icon="CirclePlus" @click="addDialogFormVisible = true"> add user </el-button>
            </el-col>

        </el-row>

        <el-row>
            <el-table :data="user_data.tableData" stripe class="table">
                <el-table-column prop="id" label="id" width="50" />
                <el-table-column prop="name" label="Name" width="150" />
                <el-table-column prop="nick_name" label="nick_name" width="120" />
                <el-table-column prop="phone" label="phone" />
                <el-table-column prop="email" label="email" />
                <el-table-column prop="role_name" label="Role" />
                

                <el-table-column label="Operations">
                    <template #default="scope">
                        <el-button size="small" @click="handleEdit(scope.$index, scope.row)">
                            Edit
                        </el-button>

                        <el-button size="small" type="danger" @click="handleDelete(scope.$index, scope.row)">
                            Delete
                        </el-button>
                        <el-button size="small" type="success" @click="handlReset(scope.$index, scope.row)">
                            Reset
                        </el-button>
                    </template>
                </el-table-column>

            </el-table>
        </el-row>


        <el-pagination v-model:current-page="user_data.pageNum" v-model:page-size="user_data.pageSize"
            :page-sizes="pageSizes" :small="small" :disabled="disabled" :background="background"
            layout="total, sizes, prev, pager, next, jumper" :total="user_data.total" @size-change="handleSizeChange"
            @current-change="handleCurrentChange" class="table" />

    </el-card>

    <!-- 增加用戶對話框 -->


    <el-dialog v-model="addDialogFormVisible" title="Add users" width="500" :before-close="addFormrest">
        <el-form :model="user_form" :rules="user_rules" ref="addFromRef">
            <el-form-item label=" name:" :label-width="formLabelWidth" prop="name">
                <el-input v-model="user_form.name" autocomplete="off" />
            </el-form-item>

            <el-form-item label=" password:" :label-width="formLabelWidth" prop="pwd">
                <el-input v-model="user_form.pwd" autocomplete="off" />
            </el-form-item>
            <el-form-item label="password confirm:" :label-width="formLabelWidth" prop="real_pwd">
                <el-input v-model="user_form.real_pwd" autocomplete="off" />
            </el-form-item>

            <el-form-item label=" nick_name:" :label-width="formLabelWidth" prop="nick_name">
                <el-input v-model="user_form.nick_name" autocomplete="off" />
            </el-form-item>

            <el-form-item label=" phone:" :label-width="formLabelWidth" prop="phone">
                <el-input v-model="user_form.phone" autocomplete="off" />
            </el-form-item>

            <el-form-item label="email:" :label-width="formLabelWidth" prop="email">
                <el-input v-model="user_form.email" autocomplete="off" />
            </el-form-item>
            <el-form-item label="role:" :label-width="formLabelWidth" prop="role_id">
                <el-select v-model="user_form.role_id" placeholder="please select your role">
                    <el-option :label="r.name" :value="r.id" v-for="r in roles" :key="r.id"/>
                    
                </el-select>
            </el-form-item>



        </el-form>
        <template #footer>
            <div class="dialog-footer">
                <el-button @click="addFormrest">Cancel</el-button>
                <el-button type="primary" @click="addUser()">
                    Confirm
                </el-button>
            </div>
        </template>
    </el-dialog>



<!-- edit users-->
<el-dialog v-model="editDialogFormVisible" title="Edit users" width="500">
        <el-form :model="edit_form"  ref="editFormRef">
            <el-form-item label=" name:" :label-width="formLabelWidth" prop="name">
                <el-input v-model="edit_form.name" autocomplete="off" disabled/>
            </el-form-item>

            <el-form-item label=" nick_name:" :label-width="formLabelWidth" prop="nick_name">
                <el-input v-model="edit_form.nick_name" autocomplete="off" />
            </el-form-item>

            <el-form-item label=" phone:" :label-width="formLabelWidth" prop="phone">
                <el-input v-model="edit_form.phone" autocomplete="off" />
            </el-form-item>

            <el-form-item label="email:" :label-width="formLabelWidth" prop="email">
                <el-input v-model="edit_form.email" autocomplete="off" />
            </el-form-item>

            <el-form-item label="role:" :label-width="formLabelWidth" prop="role_id">
                <el-select v-model="edit_form.role_id" placeholder="please select your role">
                    <el-option :label="r.name" :value="r.id" v-for="r in roles" :key="r.id"/>
                    
                </el-select>
            </el-form-item>


        </el-form>
        <template #footer>
            <div class="dialog-footer">
                <el-button @click="editDialogFormVisible=false">Cancel</el-button>
                <el-button type="primary" @click="editUser()">
                    Confirm
                </el-button>
            </div>
        </template>
    </el-dialog>    



<!-- delete users-->
<el-dialog v-model="deleteDialogFormVisible" title="Delete users" width="500">
        
        <span>Are you sure delete this user: {{remove_user.name}}, nick_name: {{remove_user.nick_name}}?</span>
        
        <template #footer>
            <div class="dialog-footer">
                <el-button @click="deleteDialogFormVisible=false">Cancel</el-button>
                <el-button type="primary" @click="deleteUser(editFormRef)">
                    Confirm
                </el-button>
            </div>
        </template>
    </el-dialog>    

<!-- reset password-->
<el-dialog v-model="resetDialogFormVisible" title="reset password" width="500">
        
        <span>Are you sure to reset password: {{reset_user.name}}, nick_name: {{reset_user.nick_name}}?</span>
        
        <template #footer>
            <div class="dialog-footer">
                <el-button @click="resetDialogFormVisible=false">Cancel</el-button>
                <el-button type="primary" @click="resetPassword(editFormRef)">
                    Confirm
                </el-button>
            </div>
        </template>
    </el-dialog>    


</template>


<script setup>
import { onMounted, reactive, ref } from 'vue'
import { ArrowRight, Search, CirclePlus } from '@element-plus/icons-vue'
import api from '@/api/index.js'
import { ElMessage } from 'element-plus'



const user_data = reactive({
    tableData: [],
    total: 10,
    pageNum: 1,
    pageSize: 3,
    queryName: '',
})


/*
 點擊輸入框 → 獲得焦點（focus）
2. 開始輸入文字 → 輸入中...
3. 點擊其他地方 → 失去焦點（blur）← trigger: 'blur' 在這裡觸發！
*/





let pageSizes = ref([1, 2, 5, 10, 100])
const small = ref(false)
const background = ref(false)
const disabled = ref(false)

const addDialogFormVisible = ref(false)

const formLabelWidth = '160px'

const addFromRef = ref(null)

const user_form = reactive({
    name: null,
    pwd: null,
    real_pwd: null,
    nick_name: null,
    phone: null,
    email: null,
    role_id:null


})


onMounted(() => {

    get_user_list()
    //get_authority_list()
})

const get_user_list = () => {
    let params = {
        'pnum': user_data.pageNum,
        'psize': user_data.pageSize,
        'name': user_data.queryName,

    }
    api.get_user_list({ params }).then(res => {
        //update user list data
        user_data.tableData = res.data.data.data
        //update 分頁數據
        user_data.total = res.data.data.total
    })
}


const handleSizeChange = (val) => {
    //update page size
    user_data.pageSize = val
    //重新獲取用戶列表數據
    get_user_list()
}
const handleCurrentChange = (val) => {
    //update the page of display
    user_data.pageNum = val
    get_user_list()
}

const searchuser = () => {
    //返回第一頁
    user_data.pageNum = 1

    get_user_list()
}



//定義驗證h確認密碼的規則  check real_pwd是否等於pwd
const validatePass2 = (rule, value, callback) => {
    if (value === '') {
        callback(new Error('please input the password '))
    } else if (value !== user_form.pwd) {
        callback(new Error("the two passwords is not same!"))
    } else {
        callback()
    }
}

const validatorPhone = (rule, value, callback) => {
    if (value == '') {
        callback(new Error('please input the phone number'))
    }
    else if (!/^1[3456789]\d{9}$/.test(value)) {
        callback(new Error('the format of the phone number is wrong'))
    }
    else {
        callback()
    }
}


const validatorEmail = (rule, value, callback) => {
    if (value == '') {
        callback(new Error('please input the email'))
    }
    else if (!/^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/i.test(value))    //   a\.b只匹配: a.b
    {
        callback(new Error('the format of the email is wrong'))
    }
    else {
        callback()
    }
}


//校驗用戶表單數據  
const user_rules = reactive({
    name: [
        { required: true, message: 'please input the name', trigger: 'blur' },
        { min: 3, max: 5, message: 'it should be between three and five', trigger: 'blur' }
    ],
    pwd: [
        { required: true, message: 'please input the password', trigger: 'blur' },
        { min: 3, max: 5, message: 'it should be between three and five', trigger: 'blur' }
    ],
    real_pwd: [
        { required: true, message: 'please ensure the password', trigger: 'blur' },
        { validator: validatePass2, trigger: 'blur' }

    ],
    nick_name: [
        { required: true, message: 'please input the nick name', trigger: 'blur' },
        { min: 1, max: 5, message: 'it should be between one and five', trigger: 'blur' }
    ],
    phone: [
        { validator: validatorPhone, trigger: 'blur' }
    ],
    email: [
        { validator: validatorEmail, trigger: 'blur' }
    ],
})

//reset the form   只關心：重置表單 + 關閉對話框
const addFormrest = () => {     // formRef這是參數，名字由你決定   ()=>{}箭頭函數  相當於function(){}
    addFromRef.value.resetFields();       // 直接reset 兩個form的資料
    //close chat box
    addDialogFormVisible.value = false
}

const addUser = () => {     //關心：驗證 + 提交數據 + 處理響應

    addFromRef.value.validate((valid) => {          //validate() 就是 觸發（trigger）所有 rule 驗證 的方法。
        if (valid) {
            console.log('subimit validate!')

            api.add_user(user_form).then(res => {
                //根據響應的結果處理
                if (res.data.status == 200) {
                    ElMessage({                      //錯誤彈窗
                        message: res.data.msg,
                        type: 'success'
                    })
                    //reset the box that means close the table box
                    addFormrest()
                    //重新獲取數據
                    get_user_list()

                } else {
                    ElMessage.warning({ message: res.data.msg })
                }

            })
        }
        else {
            console.log('error submit!')
            return false;
        }
    })
}



//edit user
const editDialogFormVisible = ref(false)
const editFormRef =  ref(null)
let userID = ref(0)

let edit_form = reactive({     //let 是變量  const是常量不允許修改
    id:null,
    name: null,
    nick_name: null,
    phone: null,
    email: null,
    role_id:null,

})

const handleEdit =(index,row) => {
    //show the edit box 
    editDialogFormVisible.value = true
    
    api.get_user_by_id(row.id).then(res=>{
        // show the original data in the edit box
        edit_form.name = res.data.data.name,
        edit_form.nick_name = res.data.data.nick_name,
        edit_form.phone = res.data.data.phone,
        edit_form.email = res.data.data.email
        edit_form.role_id = res.data.data.role_id
    })
    userID.value = row.id
    //edit_form = row
    
}


const editUser = (editform) =>{
    
    api.edit_user(userID.value,edit_form).then(res=>{
        if(res.status == 200){
            ElMessage({
                message:res.data.msg,
                type:'success',
            })
            editDialogFormVisible.value = false
            get_user_list()
        }
        else{
            ElMessage.warning(res.data.msg)
        }
    }
    )
}


//delete user'

const deleteDialogFormVisible = ref(false)

let remove_user = reactive({
    id:null,
    name:null,
    nick_name:null,
})

const handleDelete = (index,row) =>{
    remove_user.id= row.id
    remove_user.name = row.name
    remove_user.nick_name = row.nick_name
    deleteDialogFormVisible.value = true

}

const deleteUser = ()=>{
    //request the user's api which need to be deleted 
    api.delete_user(remove_user.id).then(res=>{
        if(res.status == 200){
            ElMessage({
                message:res.data.msg,
                type:'success',
            })
        deleteDialogFormVisible.value = false   //close the windows
        get_user_list()   //reload the page
        }
        else{
            ElMessage.warning(res.data.msg)
        }

    })
}



//reset password
const resetDialogFormVisible = ref(false)

let reset_user = reactive({
    id:null,
    name: null,
    nick_name: null,
     
})

const handlReset = (index,row)=>{
    resetDialogFormVisible.value = true
    reset_user.id = row.id
    reset_user.name = row.name
    reset_user.nick_name = row.nick_name

}

const resetPassword = ()=>{
    api.reset_user_password(reset_user.id).then(res=>{
        if(res.status == 200){
            ElMessage({
                message:res.data.msg,
                type:'success' // this is color
            })
            resetDialogFormVisible.value = false,
            get_user_list()
        }else{
            ElMessage.warning(res.data.msg)
        }
    })
}

// get the role 

onMounted(()=>{
    get_authority_list()
})
let roles = ref([])
const get_authority_list = () =>{
    api.get_roles().then(res=>{
        roles = res.data.data
    })
    
}


</script>


<style scoped>
.box-card {
    margin-top: 20px;
}

.table {
    margin-top: 10px
}
</style>
