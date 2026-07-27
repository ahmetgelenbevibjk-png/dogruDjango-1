<script setup>
import { ref, onMounted } from 'vue'
import Account from './components/Account.vue'
import DashboardLayout from './components/DashboardLayout.vue'

const isLoggedIn = ref(false)

onMounted(() => {
  const token = localStorage.getItem('access_token')
  if (token) {
    isLoggedIn.value = true
  }
})

const handleLoginSuccess = () => {
  isLoggedIn.value = true
}

const handleLogout = () => {
  localStorage.removeItem('access_token')
  isLoggedIn.value = false
}
</script>

<template>
  <Account v-if="!isLoggedIn" @loginSuccess="handleLoginSuccess" />
  <DashboardLayout v-else @logout="handleLogout" />
</template>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Inter', sans-serif;
}
</style>