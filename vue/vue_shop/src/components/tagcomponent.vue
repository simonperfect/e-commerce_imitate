<template>

                                    <el-input
                                        v-if="inputVisible"
                                        ref="InputRef"
                                        v-model="inputValue"
                                        class="input-tag"
                                        size="small"
                                        @keyup.enter="handleInputConfirm" 
                                        @blur="handleInputConfirm"
                                        />
                                    <el-button v-else class="button-new-tag" size="small" @click="showInput">
                                        + New Tag
                                    </el-button>
</template>



<script setup>
import {ref,nextTick} from 'vue'


const inputValue = ref('')

const inputVisible = ref(false)
const InputRef = ref(null)

const showInput = () => {
  inputVisible.value = true
  nextTick(() => {
    InputRef.value.input.focus()
  })
}

const handleInputConfirm = () => {

    emit('addTagEvent',{'inputValue':inputValue.value,'row':props.row})
    //console.log(inputValue.value)
    inputVisible.value = false
    inputValue.value = ''
}

const emit = defineEmits(['addTagEvent'])    // send the input value for View file to use
//define a reciever to revieve value from parent component  (View file)
const props = defineProps({
    row:{
        type:Object,    
        default:()=>Object
    }
})

</script>


<style scoped>

.input-tag{
    width:100px;
}

</style>