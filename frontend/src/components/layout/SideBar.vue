<script setup>
// Artık router kullanıldığı için props ve emit'lere gerek kalmadı.
</script>

<template>
  <aside class="sidebar">
    <div class="sidebar-menu">

      <!-- Users Sekmesi (Router Link) -->
      <router-link to="/" class="menu-item" active-class="active">
        <svg class="menu-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
          <circle cx="9" cy="7" r="4"></circle>
          <path d="M23 21v-2a4 4 0 0 0-3-3.87"></path>
          <path d="M16 3.13a4 4 0 0 1 0 7.75"></path>
        </svg>
        <span>{{ $t('nav.users') }}</span>
      </router-link>

      <!-- Todos Sekmesi (Router Link) -->
      <router-link to="/todos" class="menu-item" active-class="active">
        <svg class="menu-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"></path>
          <rect x="8" y="2" width="8" height="4" rx="1" ry="1"></rect>
          <path d="m9 14 2 2 4-4"></path>
        </svg>
        <span>{{ $t('nav.todos') }}</span>
      </router-link>

      <router-link to="/posts" class="menu-item" active-class="active">
        <svg class="menu-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
          <polyline points="14 2 14 8 20 8"></polyline>
          <line x1="16" y1="13" x2="8" y2="13"></line>
          <line x1="16" y1="17" x2="8" y2="17"></line>
        </svg>
        <span>{{ $t('nav.posts') }}</span>
      </router-link>

      <!-- Albums Sekmesi -->
      <router-link to="/albums" class="menu-item" active-class="active">
        <svg class="menu-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>
          <circle cx="8.5" cy="8.5" r="1.5"></circle>
          <polyline points="21 15 16 10 5 21"></polyline>
        </svg>
        <span>{{ $t('nav.albums') }}</span>
      </router-link>

    </div>
  </aside>
</template>

<style scoped>
.sidebar {
  width: 240px;
  background-color: #ffffff;
  border-right: 1px solid #e2e8f0;
  display: flex;
  flex-direction: column;
  height: calc(100vh - 60px); /* Navbar payı düşüldü */
  padding-top: 20px;
}

.sidebar-menu {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.menu-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 20px;
  text-decoration: none;
  cursor: pointer;
  color: var(--text-muted, #64748b); /* Koyu/Açık temaya göre otomatik uyarlanır */
  font-size: 15px;
  font-weight: 500;
  position: relative;
  transition: all 0.2s ease;
}

.menu-item:hover {
  background-color: var(--bg-main, #f8fafc);
  color: var(--text-main, #1e293b);
}

.menu-item.active {
  background-color: var(--bg-main, #f1f5f9);
  color: #7c3aed;
  font-weight: 600;
}
.menu-item.active::before {
  content: '';
  position: absolute;
  left: 0;
  top: 50%;
  transform: translateY(-50%);
  width: 4px;
  height: 28px;
  background-color: #7c3aed;
  border-top-right-radius: 4px;
  border-bottom-right-radius: 4px;
}

.menu-icon {
  width: 20px;
  height: 20px;
  color: inherit;
  pointer-events: none;
}
</style>