import { createRouter, createWebHistory } from 'vue-router'
import Users from '../modules/users/pages/Users.vue'
import Todos from '../modules/Todos/pages/Todos.vue'
import Profile from '../modules/Profile/pages/Profile.vue'
import Posts from '../modules/Posts/pages/Posts.vue'
import Albums from '../modules/Albums/pages/Albums.vue'
import UserDetails from '../modules/usersDetail/pages/UserDetails.vue';const routes = [
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
  },
 {
    path: '/user/:id',
    name: 'UserDetails',
    component: () => import('../modules/usersDetail/pages/UserDetails.vue')
  }

]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router