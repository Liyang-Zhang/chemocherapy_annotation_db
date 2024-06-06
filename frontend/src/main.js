import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import vuetify from './plugins/vuetify';
import { loadFonts } from './plugins/webfontloader';
import axios from 'axios';
import VueCookies from 'vue-cookies';

loadFonts();

const app = createApp(App);

app.use(VueCookies, { expire: '7d' });  // 配置 cookies 过期时间

// Manually parse document.cookie to get CSRF token
function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
  return null;
}
const csrfToken = getCookie('csrftoken');

if (csrfToken) {
  axios.defaults.headers.common['X-CSRFToken'] = csrfToken;
} else {
  console.error('CSRF token is null or undefined!');
}

app.config.globalProperties.$axios = axios;

app.use(router)
   .use(vuetify)
   .mount('#app');
