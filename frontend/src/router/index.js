import { createRouter, createWebHistory } from 'vue-router';
import HomeView from '../views/Home.vue';
import GeneList from '../views/GeneList.vue';
import AddGene from '../views/AddGene.vue';

const routes = [
  { path: '/', name: 'Home', component: HomeView },
  { path: '/genes', name: 'GeneList', component: GeneList },
  { path: '/add-gene', name: 'AddGene', component: AddGene },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;
