<script setup>
import Account from './components/Account.vue'
import {ref, onMounted}from 'vue'
import SideBar from './components/SideBar.vue'
import Users from './components/Users.vue'

const isLoggedIn=ref(false)
const currentTab=ref('Users')
onMounted(()=>{
  const token =localstorage.getItem('access_token')
  if (token){
    isLoggedIn.value=true
  }
})

const handleLogout=()=>{
  localStorage.removeItem('access_token')
  isLoggedIn.value=false
}
</script>

<template>
  <Account />
  <Account v-if="!isLoggedIn" @loginSuccess="handleLoginSuccess"/>

  <div v-else class="dashboard-layout">
    <SideBar @selectTab="(tab)=> currentTab=tab" @logout="handleLogout" />

    <main class="main-content">
      <Users v-if="currentTab==='Users'"/>
    </main>
  </div>
</template>

<style>
*{margin:0;
padding: 0;
box-sizing:border-box;
 }

.dashboard-layout {
  display: flex;
  height: 100vh;
  width:100vw;
  overflow:hidden;
}
.main-content {
  flex:1;
  background-color : #f1f5f9;
  overflow-y:auto ;
  padding: 30px;
}
</style>