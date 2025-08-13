import { createRouter, createWebHistory } from 'vue-router'


import Welcome from '@/pages/Welcome.vue'
import Login from '@/pages/Login.vue'
import Register from '@/pages/Register.vue'
import ForgotPassword from '@/pages/ForgotPassword.vue'
import Catalog from '@/pages/Catalog.vue'
import Dashboard from '@/pages/Dashboard.vue'
import ItemPage from '@/pages/ItemPage.vue'
import Cart from '@/pages/Cart.vue'
import Categories from '@/pages/Categories.vue'


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'Welcome',
      component: Welcome,
      meta: {
      title: 'ShadcnVue',
      description: 'Welcome to ShadcnVue Project',
    },
    },
    {
      path: '/cart',
      name: 'Cart',
      component: Cart,
      meta: {
      title: 'Shopping Cart',
      description: 'Shopping cart',
    },
    },
    {
      path: '/login',
      name: 'Login',
      component: Login,
      meta: {
      title: 'Login - ShadcnVue',
      description: 'Login to your account in ShadcnVue Project',
    },
    },
    {
      path: '/register',
      name: 'Register',
      component: Register,
        meta: {
      title: 'Register - ShadcnVue',
      description: 'Register your account in ShadcnVue Project',
    },
    },
    {
      path: '/forgot-password',
      name: 'ForgotPassword',
      component: ForgotPassword,
        meta: {
      title: 'Forgot Password - ShadcnVue',
      description: 'Reset your password and regain access to your account',
    },
    },
    {
      path: '/catalog',
      name: 'Catalog',
      component: Catalog,
      meta: {
      title: 'Catalog - ShadcnVue',
      description: 'Catalog',
    },
    },
    {
      path: '/dashboard',
      name: 'Dashboard',
      component: Dashboard,
      meta: {
      title: 'Dashboard - ShadcnVue',
      description: 'Your personel dashboard in ShadcnVue',
    },
    },
    {
    path: "/item/:id",
    name: "item",
    component: ItemPage,
    
  },
    {
    path: "/categories",
    name: "Categories",
    component: Categories,
    meta: {
      title: 'Categories - ShadcnVue',
      description: 'Browse categories and choose a game for boost.',
    },
    
  }
  ],
})

export default router