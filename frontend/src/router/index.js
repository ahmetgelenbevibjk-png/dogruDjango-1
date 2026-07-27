import { createRouter, createWebHistory } from 'vue-router'
import Users from '../components/Users.vue'
import Todos from '../components/Todos.vue'
import Profile from '../components/Profile.vue'
import Posts from '../components/Posts.vue'
import Albums from '../components/Albums.vue'
const routes = [
  {
    path: '/',
    name: 'users',
    component: Users
  },
  {
    path: '/todos',
    name: 'todos',
    component: Todos
  },
  {
    path: '/Profile',
    name: 'Profile',
    component: Profile
  },
    {
    path: '/Posts',
    name: 'Posts',
    component: Posts
  },
  {
    path: '/Albums',
    name: 'Albums',
    component: Albums
  }

]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router