<template>
  <v-app>
    <NavBar />
    <v-main>
      <router-view></router-view>
    </v-main>
    <FooterView />
  </v-app>
</template>

<script>
import NavBar from './components/Navbar.vue'
import FooterView from './components/Footer.vue'

export default {
  name: 'App',
  components: {
    NavBar,
    FooterView
  }
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
