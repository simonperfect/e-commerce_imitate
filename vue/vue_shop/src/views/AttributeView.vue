<template>
    <el-breadcrumb :separator-icon="ArrowRight">
        <el-breadcrumb-item :to="{ path: '/' }">Home</el-breadcrumb-item>
        <el-breadcrumb-item>Merchandise management</el-breadcrumb-item>
        <el-breadcrumb-item>Attribute list</el-breadcrumb-item>
    </el-breadcrumb>
    <el-card class="box-card"> <!-- select category box-->
        <el-alert title="must select the last level" type="warning" />
        <div>
            <span class="attr_title">select category</span>
            <el-cascader  
                :options="options.data" 
                :props="props" 
                separator=" > " style="width: 500px;"
                clearable
                class="cascader"
                v-model="options.selectID"
                @change="changeSelect" />    <!--when  we change the selection -->

        </div>
        <div>
            <el-tabs v-model="activeName" class="demo-tabs"  @tab-click="handleClick">    <!-- v-model is binding with the tab when we click dynamic tag ,the value of activeName will be dynamic-->
                <el-tab-pane label="Static" name="static">         <!--static tag-->
                    <el-button type="primary"  :disabled="isButtonVisible" @click="addDialogVisible=true">Add attribute</el-button>
                    <el-table :data="attrData.static">
                        <el-table-column type="index"></el-table-column>
                        <el-table-column label="Attribute Name" prop="name"></el-table-column>
                        <el-table-column label="operations">
                            <template #default="scope">
                                <el-button type="primary" size="small">Edit</el-button>
                                <el-button type="danger" size="small">Delete</el-button>
                            </template>
                        </el-table-column>
                    </el-table>
                </el-tab-pane>

                <el-tab-pane label="Dynamic" name="dynamic">        <!--dynamic tag--> 
                    <el-button type="primary"  :disabled="isButtonVisible" @click="addDialogVisible=true">Add attribute</el-button>            
                    <el-table :data="attrData.dynamic" row-key="id">
                        <el-table-column type="expand">
                                  <template #default="scope">
                                    <el-tag class='e-tag' v-for="(item,index) in scope.row.val.split(',')" closable @close="closeTag(scope.row.id,scope.row.val,index)">{{ item.trim() }}</el-tag>
                                    <!--the button to add the tag is in the components file  所有输入框共享同一个引用 when we input content in one tag box the other tag box wil also have the same content so we need to create a independent component file-->
                                    <tagcomponent @addTagEvent="getTagValue" :row="scope.row"/>
                                
                            </template>
                        </el-table-column>
                        <el-table-column type="index"></el-table-column>
                        <el-table-column label="Attribute Name" prop="name"></el-table-column>
                        <el-table-column label="operations">
                            <template #default="scope">
                                <el-button type="primary" size="small">Edit</el-button>
                                <el-button type="danger" size="small">Delete</el-button>
                            </template>
                        </el-table-column>
                    </el-table></el-tab-pane>
            </el-tabs>
        </div>
    </el-card>

    <el-dialog      
    :title="dialogTitle"
    width="30%"
    v-model="addDialogVisible"
    :before-close="addDialogClose"
    >                        <!---the message box of adding attibute-->

        <el-form :model="addForm" label-width="80px" :rules="addRules" ref="addRef">
            <el-form-item label="Attribute name" label-width="150px" prop="name">  <!-- this prop name work as a reference for addRules to verify-->
                 <el-input v-model="addForm.name"></el-input>
            </el-form-item>
            <el-form-item>
                <el-button type="primary" @click="addAttr">Confirm</el-button>
                <el-button type="danger" @click="addDialogVisible=false">Cancel</el-button>
            </el-form-item>

        </el-form>
    </el-dialog>
</template>

<script setup>
import { ArrowRight, CirclePlus } from '@element-plus/icons-vue'
import { reactive, onMounted, ref, computed, nextTick} from 'vue'
import api from '../api/index.js'
import { ElMessage } from 'element-plus'

const options = reactive({
    data: [],
    selectID:null
})

const props = {
    expandTrigger: 'hover',
    label: 'name',
    value: 'id',

}

onMounted(() => {
    get_category()
})


const get_category = () => {
    api.get_category(3).then(res => {
        options.data = res.data.data

    })
}


    //tags    
 const attrData = reactive({
    static:[],
    dynamic:[]
})
   
const handleClick = (tab, event) => {

    if (tab.props.name == 'static'){
        dialogTitle.value = 'Add static attribute'
    }else if (tab.props.name == 'dynamic'){
        dialogTitle.value = 'Add dynamic attribute'
    }


    if (options.selectID){
        if (options.selectID.length == 3){
            let select_key = options.selectID[2]     //output the level 3 category id 
            let _type = tab.props.name        //output static or dynamic
            if (_type == 'static' && flag.static == false){
                return
            }
            if(_type ==  'dynamic' && flag.dynamic == false){
                return
            }
         
            
            if (_type=='static'){
                api.get_attr_by_category(select_key,_type).then(res=>{
                attrData.static = res.data.data
                flag.static = false
                })
            }else if(_type == 'dynamic'){
                api.get_attr_by_category(select_key,_type).then(res=>{
                    attrData.dynamic = res.data.data
                    flag.dynamic = false
                })
            }

        }
    }

}


const activeName = ref('static')

const flag = reactive({     // to judge whether the status can be got
    static:false,     // it means that static cannot be got
    dynamic:false     //it means that dynamic cannot be got 
})

const changeSelect = (value) =>{
    if (value){
        if(value.length == 3){
            let select_key = value[2]     //value[2] is level 3 category id 
            let _type = activeName.value  
            //set static can be got
            flag.static = true   
            flag.dynamic = true
            if (_type=='static'){
                api.get_attr_by_category(select_key,_type).then(res=>{
                    attrData.static = res.data.data
                    // set static cannot be got   it means that we do not need to get static again
                    flag.static = false
                })
            }else if(_type == 'dynamic'){
                api.get_attr_by_category(select_key,_type).then(res=>{
                    attrData.dynamic = res.data.data
                    flag.dynamic = false

                })
            }
      
        
        }
        else{
            attrData.static = []
            attrData.dynamic = []
        }
    }
    else{        //if we clear the selection box then the data table will be cleared
        attrData.static = []
        attrData.dynamic =[]
    }


}
 

//add attribute message box
const addForm = reactive({
    name:'',
})

const addDialogVisible = ref(false)


const dialogTitle = ref('Add static attribute')

//rules
const addRules = reactive({
    name:[
        {required:true,message:'please input the attribute name',trigger:'blur'}
    ]
})

const addRef = ref(null)

const addDialogClose = () =>{
    addRef.value.resetFields()   //reset the form 
    addDialogVisible.value = false
    
}

const addAttr=()=>{
    
   

    let params={
        "name":addForm.name,
        "_type":activeName.value,
        "cid":options.selectID[2]
    }
    api.add_attribute(params).then(res=>{
        
        let select_key = options.selectID[2]
        let _type = activeName.value
        if (_type=='static'){
            api.get_attr_by_category(select_key,_type).then(res=>{
                attrData.static = res.data.data
                // set static cannot be got   it means that we do not need to get static again
                flag.static = false
            })
        }else if(_type == 'dynamic'){
            api.get_attr_by_category(select_key,_type).then(res=>{
                attrData.dynamic = res.data.data
                flag.dynamic = false

            })
        }        
        addDialogClose()
    })
}

let isButtonVisible = computed(()=>{
    if (options.selectID){
        if (options.selectID.length == 3){
            return false
        }
    }
    return true 
})

//tag input
// all the tag input code is in component file
import tagcomponent from '@/components/tagcomponent.vue'


const getTagValue = (val) =>{  // revieve the value from tag components
    
    // add the new input to the original value  because we need to keep the original value
    let valArray = []
    
    if (val.row.val) {
        if (typeof val.row.val === 'string') {
            valArray = val.row.val.split(',').map(item => item.trim()).filter(item => item)
        } else if (Array.isArray(val.row.val)) {
            valArray = [...val.row.val]
        }
    }
    
    if (val.inputValue && !valArray.includes(val.inputValue)) {
        valArray.push(val.inputValue)
        
        const newValString = valArray.join(",")
        
        // ⭐ 创建新对象替换原对象（强制响应式）
        const rowIndex = attrData.dynamic.findIndex(row => row.id === val.row.id)
        if (rowIndex !== -1) {
            attrData.dynamic[rowIndex] = {
                ...attrData.dynamic[rowIndex],
                val: newValString
            }
        
        }
    }
    
    let params = {
        '_type': activeName.value,
        'val': valArray.join(",")  // 将数组转换回字符串
    }
    api.update_attr_value(val.row.id,params).then(res=>{
        ElMessage({
            type:'success',
            message:res.data.msg
       })
    })
}



//close tag
const closeTag = (id,tagList,index) =>{

       
    console.log('删除标签:', { id, tagList, index })
    
    // 1. change string to array
    let tagArray = []
    if (tagList) {
        tagArray = tagList.split(',').map(item => item.trim()).filter(item => item)
    }
    
    // 2. delete the tag by index   we need to use splice that only can used in array
    if (index >= 0 && index < tagArray.length) {
        tagArray.splice(index, 1)
    }
    
    // 3. change array back
    const newTagList = tagArray.join(',')  
    console.log('新的标签字符串:', newTagList)
    
    // 4. update the local data immediately （这样界面会立即刷新）
    const rowIndex = attrData.dynamic.findIndex(row => row.id === id)
    if (rowIndex !== -1) {
        // create a new object 
        attrData.dynamic[rowIndex] = {
            ...attrData.dynamic[rowIndex],    //show all the original properties
            val: newTagList              //just change the val property
        }
    }    

    let params = {
        "val": newTagList
    }
    api.update_attr_value(id,params).then(res=>{
        ElMessage({
            type:'success',
            message:res.data.msg
        })
    })
}

</script>




<style scoped>
.box-card {
    margin-top: 20px;
}

.attr_title {
    margin-right: 10px
}

.demo-tabs>.el-tabs__content {
    padding: 32px;
    color: #6b778c;
    font-size: 32px;
    font-weight: 600;
}
.e-tag{
    margin:5px;
}

</style>