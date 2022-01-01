import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: Home
  },

  {
    path: '/trip/:slug',
    name: 'trip',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "trip" */ '../views/Question.vue'),
    props:true
  },
  {
    path: "/todo/:uuid",
    name: "todo-editor",
    component: () =>
      import(/* webpackChunkName: "todo-editor" */ "../views/TodoEditor.vue"),
    props: true
  },
  {
    // the ? sign makes the slug parameter optional
    path: "/ask/:slug?",
    name: "trip-editor",
    component: () =>
      import(/* webpackChunkName: "trip-editor" */ "../views/TripEditor.vue"),
    props: true
  },
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
