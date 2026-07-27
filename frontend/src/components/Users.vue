<script setup>
import {ref,onMounted} from 'vue'

const Users =ref([])
const loading =ref(true)
const errorMessage=ref('')

const fetchUsers= async()=>{
  const token=localStorage.getItem('access_token')
}
</script>

<template>

</template>

<style scoped>

</style>