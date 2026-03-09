<template>
    <el-breadcrumb :separator-icon="ArrowRight">
        <el-breadcrumb-item :to="{ path: '/' }">Home</el-breadcrumb-item>
        <el-breadcrumb-item>Merchandise management</el-breadcrumb-item>
        <el-breadcrumb-item>Add product</el-breadcrumb-item>
    </el-breadcrumb>
    <el-card class="box-card">
        <el-alert title="Enter infomation of the product you want to add below" type="info" center show-icon />
        <el-steps  :active="active-0" finish-status="success" align-center>
            <el-step title="basic information" />
            <el-step title="Static state" />
            <el-step title="Dynamic state" />
            <el-step title="image upload" />
            <el-step title="Information of product" />
            <el-step title="Done" />
        </el-steps>
        <el-tabs tab-position="left" class="el-tabs" v-model="active">   <!--v-model accomplishes the binding with el-steps when tab pane go to the second the el-steps will go to second pleace too-->
            <el-form :model="addForm" ref="addFormRef" :rules="addFormRules">
                <el-tab-pane label="basic information" :name="0">   <!-- name attribute is the default is ordinal number of the tab-pane in the sequence, e.g. the second default tab-pane is '1' a layer won't fall to first pane-->
                    <el-form-item label="name" prop="name">
                        <el-input v-model="addForm.name" />
                    </el-form-item>
                    <el-form-item label="price" prop="price">
                        <el-input v-model="addForm.price" />
                    </el-form-item>
                    <el-form-item label="inventory" prop="number"> 
                        <el-input v-model="addForm.number" />
                    </el-form-item>
                    <el-form-item label="Product weight" prop="weight">
                        <el-input v-model="addForm.weight" />
                    </el-form-item>
                    <el-form-item label="Category">     <!--v-model針對 options.selectID 做雙向綁定 options is the content of menu / props is the menu intruction :tell you how to read menu :the dishes name and id  / v-model is the customer order: Tells waiter: write my order on this 'options.selectID 賬單 -->
                        <el-cascader  
                            :options="options.data"      
                            :props="props" 
                            separator=" > " 
                            style="width: 500px;"
                            clearable
                            v-model="options.selectID"     
                            @change="changeSelect"
                            class="cascader"  />

                    </el-form-item>
                </el-tab-pane>  
                <el-tab-pane label="Static state" :name="1">Static state</el-tab-pane>
                <el-tab-pane label="Dynamic state" :name="2">Dynamic state</el-tab-pane>
                <el-tab-pane label="image upload" :name="3">image upload</el-tab-pane>
                <el-tab-pane label="Information of product" :name="4">Information of product</el-tab-pane>
            </el-form>
        </el-tabs>


    </el-card>
</template>




<script setup>
import { ArrowRight } from '@element-plus/icons-vue';
import {ref,reactive,onMounted} from 'vue'
import api from '../api/index.js'

const active = ref(0)     //0 is a int because the name attribute of el-tab-pane is a number {:name"0"} if it is a string the el-steps won't work

const addForm = reactive({
    name:'',
    price:'',
    number:'',
    weight:'',

})

const addFormRules = reactive({
    name:[
        {required:true,message:'Please input the name of product',trigger:'blur'},
        {min:2,max:10,message:'Length should be 2 to 10', trigger:'blur'}
    ],
    price:[
        {required:true,message:'Please input the price of product',trigger:'blur'},
        {type:'number',message:'Price should be a number',trigger:'blur'}
    ],
    number:[
        {required:true,message:'Please input the inventory of product',trigger:'blur'},
        {type:'number',message:'Inventory should be a number',trigger:'blur'}
    ],
    weight:[
        {required:true,message:'Please input the weight of product',trigger:'blur'},
        {type:'number',message:'Weight should be a number',trigger:'blur'}
    ]
})

//object of the form
const addFormRef = ref(null)    //null is the initial placeholder


//create cascader options ==> for data scource
const options = reactive({
    data:[],
    selectID:null
})

//get the data from backend and assign it to options.data
onMounted(()=>{
    get_category()
})

const get_category = () =>{
    api.get_category(3).then(res=>{
        options.data = res.data.data
    })
}


const props = {               // 設定資料欄位與元件屬性的對應關係（如 value、label、children）
    expandTrigger:'hover',          
    label:'name',          //base on the id and show the name
    value:'id',      // the id  is come from backend data
}

//Method triggered when the selected item changes.

const changeSelect = (value) =>{
     console.log(value)
}
</script>



<style scoped>
.box-card{
    margin-top:20px
}
.el-tabs{
    margin-top:20px
}
.cascader{
    width:500px
}

</style>