<template>
    <el-breadcrumb :separator-icon="ArrowRight">
        <el-breadcrumb-item :to="{ path: '/' }">Home</el-breadcrumb-item>
        <el-breadcrumb-item>Merchandise management</el-breadcrumb-item>
        <el-breadcrumb-item>Add product</el-breadcrumb-item>
    </el-breadcrumb>
    <el-card class="box-card">
        <el-steps  :active="active" finish-status="success" align-center>
            <el-step title="basic information" />
            <el-step title="Static state" />
            <el-step title="Dynamic state" />
            <el-step title="image upload" />
            <el-step title="Information of product" />
            <el-step title="Done" />
        </el-steps>
        <el-tabs tab-position="left" class="el-tabs">
            <el-tab-pane label="basic information">basic information</el-tab-pane>
            <el-tab-pane label="Static state">Static state</el-tab-pane>
            <el-tab-pane label="Dynamic state">Dynamic state</el-tab-pane>
            <el-tab-pane label="image upload">image upload</el-tab-pane>
            <el-tab-pane label="Information of product">Information of product</el-tab-pane>
            
        </el-tabs>


    </el-card>
</template>

<script setup>
import { ArrowRight } from '@element-plus/icons-vue';
</script>



<style scoped>
.box-card{
    margin-top:20px
}
.el-tabs{
    margin-top:20px
}
</style>