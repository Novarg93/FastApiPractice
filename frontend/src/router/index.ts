import { createRouter, createWebHistory } from 'vue-router'

import { useAuthStore } from '@/stores/auth'
import Welcome from '@/pages/Welcome.vue'
import Login from '@/pages/Login.vue'
import Register from '@/pages/Register.vue'
import ForgotPassword from '@/pages/ForgotPassword.vue'
import Catalog from '@/pages/Catalog.vue'
import Dashboard from '@/pages/Dashboard.vue'
import ItemPage from '@/pages/ItemPage.vue'
import Cart from '@/pages/Cart.vue'
import Categories from '@/pages/Categories.vue'
import Settings from '@/pages/Settings.vue'
import Checkout from '@/pages/Checkout.vue'
import OrderSuccess from '@/pages/OrderSuccess.vue'

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
      meta: { guestOnly: true,
      title: 'Login - ShadcnVue',
      description: 'Login to your account in ShadcnVue Project',
    },
    },
    {
      path: '/register',
      name: 'Register',
      component: Register,
        meta: { guestOnly: true,
      title: 'Register - ShadcnVue',
      description: 'Register your account in ShadcnVue Project',
    },
    },
    {
      path: '/forgot-password',
      name: 'ForgotPassword',
      component: ForgotPassword,
        meta: { guestOnly: true,
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
      meta: { requiresAuth: true,
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
    
  },
    {
    path: "/settings",
    name: "Settings",
    component: Settings,
    meta: { requiresAuth: true,
      title: 'Setting - ShadcnVue',
      description: 'Change your password or delete account.',
    },
  },
  {
    path: "/checkout", 
    name:"Checkout", 
    component: Checkout,
    meta: { requiresAuth: true,
      title: 'Checkout - ShadcnVue',
      description: 'Checkout page for payment provide',
    },
  },
  {
  path: '/success',
  name: 'PaymentSuccess',
  component: OrderSuccess,
  meta: { requiresAuth: true, title: 'Payment success' },
}
  ],
})

  router.beforeEach(async (to) => {
  const auth = useAuthStore()

  // 1) Синк токена из storage
  if (!auth.token) {
    const t = localStorage.getItem('access_token') ?? sessionStorage.getItem('access_token')
    if (t) auth.$patch({ token: t })
  }

  // 2) Подтянуть профиль, если нужно
  if (auth.token && !auth.user && !auth.loading) {
    try { await auth.fetchMe() } catch {/* проглотим: 401 обработаем ниже правилом */}
  }

  // 3) Правила
  if (to.meta?.guestOnly && auth.isAuthenticated) {
    return { path: '/dashboard' }
  }

  if (to.meta?.requiresAuth && !auth.isAuthenticated) {
    return { path: '/login', query: { redirect: to.fullPath } }
  }

  // иначе — пропуск
})

export default router