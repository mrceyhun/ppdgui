import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: "/",
      name: "Home",
      component: () => import('../views/HomeView.vue'),
      meta: {
        requiresAuth: true
      }
    },
  ]
})
router.beforeEach((to, from, next) => {
  next()
})


export default router
