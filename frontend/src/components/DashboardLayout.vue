<script setup>
import SideBar from './SideBar.vue'
import Navbar from './Navbar.vue'

const emit = defineEmits(['logout'])
</script>

<template>
  <div class="dashboard-container">
    <!-- Üst Sabit Navbar -->
    <Navbar @logout="$emit('logout')" />

    <div class="dashboard-body">
      <SideBar />

      <main class="main-content">
        <router-view />
      </main>
    </div>
  </div>
</template>

<style scoped>
.dashboard-container {
  display: flex;
  flex-direction: column;
  height: 100vh;
  width: 100vw;
  overflow: hidden;
}

.dashboard-body {
  display: flex;
  flex: 1;
  height: calc(100vh - 60px);
}

.main-content {
  flex: 1;
  background-color: #f1f5f9;
  overflow-y: auto;
  padding: 30px;
}
</style>