import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Home.vue'
import VueMeta from 'vue-meta'

Vue.use(VueRouter)
Vue.use(VueMeta)

const routes = [
{
  path: '/',
  name: 'Home',
  component: Home
},
{
  path: '/about',
  name: 'About',
  // route level code-splitting
  // this generates a separate chunk (about.[hash].js) for this route
  // which is lazy-loaded when the route is visited.
  component: () => import(/* webpackChunkName: "about" */ '../views/About.vue')
},
{
  path: '/scroll',
  name: 'Scroll',
  component: () => import(/* webpackChunkName: "scroll" */ '../views/Scroll.vue')
},
{
  path: '/cache',
  name: 'Cache',
  component: () => import(/* webpackChunkName: "cache" */ '../views/Cache.vue')
},
{
  path: '/edit',
  name: 'Edit',
  component: () => import(/* webpackChunkName: "edit" */ '../components/Edit.vue')
},
{
  path: '/add',
  name: 'Add',
  component: () => import(/* webpackChunkName: "add" */ '../views/Add.vue')
}
// {
//   path: '/login',
//   name: 'Login',
//   component: () => import(/* webpackChunkName: "login" */ '../components/Login.vue')
// }
]

const router = new VueRouter({
  routes
})

export default router
