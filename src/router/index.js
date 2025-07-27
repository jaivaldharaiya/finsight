// src/router/index.js

import { createRouter, createWebHistory } from 'vue-router'
import QuestionnaireView from '@/views/QuestionnaireView.vue'
import DashboardView from '@/views/DashboardView.vue'
import AgentsView from '@/views/Agents.vue'
import Intro from '@/views/Intro.vue'
import LoginView from '@/views/LoginView.vue'
import RegisterView from '@/views/RegisterView.vue'
import { useAuth } from '@/composables/auth'

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: LoginView,
    meta: { requiresAuth: false }
  },
  {
    path: '/register',
    name: 'Register',
    component: RegisterView,
    meta: { requiresAuth: false }
  },
  {
    path: '/',
    name: 'Intro',
    component: Intro,
    meta: { requiresAuth: false }
  },
  {
    path: '/Questionnaire',
    name: 'Questionnaire',
    component: QuestionnaireView,
    meta: { requiresAuth: true }
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: DashboardView,
    meta: { requiresAuth: true }
  },
  {
    path: '/Agents',
    name: 'Agents',
    component: AgentsView,
    meta: { requiresAuth: true }
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

// --- IMPROVED NAVIGATION GUARD ---
router.beforeEach((to, from, next) => {
  const { user } = useAuth();

  // If going to login/register and already logged in, redirect to dashboard
  if ((to.name === 'Login' || to.name === 'Register') && user.value) {
    next('/dashboard');
    return;
  }

  // If route requires auth and not logged in, redirect to login
  if (to.meta.requiresAuth && !user.value) {
    next('/login');
    return;
  }

  // Otherwise, allow navigation
  next();
});

export default router