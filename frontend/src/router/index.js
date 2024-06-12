import { createRouter, createWebHistory } from 'vue-router';
import HomeView from '../views/Home.vue';
import GeneList from '../views/GeneList.vue';
import AddGene from '../views/AddGene.vue';
import UploadExcel from '../components/UploadExcel.vue';
import UserLogin from '../views/Login.vue'

const routes = [
  { path: '/', name: 'Home', component: HomeView, meta: { requiresAuth: true } },
  { path: '/genes', name: 'GeneList', component: GeneList, meta: { requiresAuth: true } },
  { path: '/add-gene', name: 'AddGene', component: AddGene, meta: { requiresAuth: true } },
  { path: '/upload-excel', name: 'UploadExcel', component: UploadExcel, meta: { requiresAuth: true } },
  { path: '/login', name: 'UserLogin', component: UserLogin },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

router.beforeEach((to, from, next) => {
  const loggedIn = !!localStorage.getItem('token');
  if (to.matched.some(record => record.meta.requiresAuth) && !loggedIn) {
    next('/login');
  } else {
    next();
  }
});

export default router;
