<template>
  <v-app-bar app>
    <v-spacer></v-spacer>
    <v-toolbar-title class="toolbar-title">Chemo Gene Annotation Database</v-toolbar-title>
    <v-spacer></v-spacer>
    <v-btn color="primary" @click="logout">Logout</v-btn>
  </v-app-bar>
</template>

<script>
export default {
  name: "NavBar",
  methods: {
    logout() {
      this.$axios.post('/api/logout/')
        .then(() => {
          localStorage.removeItem('token');
          this.$router.push('/login');
        })
        .catch(error => {
          console.error('There was an error logging out!', error);
          localStorage.removeItem('token');  // 即使后端失败，也移除本地token
          this.$router.push('/login');
        });
    }
  }
}
</script>

<style scoped>
.v-toolbar-title {
  text-align: center;
  width: 100%;
}
.v-btn {
  position: absolute;
  right: 20px;
}
</style>
