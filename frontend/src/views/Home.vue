// src/views/Home.vue
<template>
  <v-container>
    <v-row>
      <v-col cols="12" class="text-center">
        <v-img
          src="@/assets/logo.png"
          max-width="200"
          class="mb-5"
        ></v-img>
        <h1>Welcome to the ChemoGene Annotation Database</h1>
        <p class="text-subtitle-1">Manage and annotate your chemo-related gene data easily and efficiently.</p>
        <v-btn color="primary" @click="goToGeneList">View Gene List</v-btn>
        <v-btn color="secondary" @click="goToAddGene">Add New Gene</v-btn>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  name: 'HomeView', // 修改组件名称为多单词
  methods: {
    goToGeneList() {
      this.$router.push({ name: 'GeneList' });
    },
    goToAddGene() {
      this.$router.push({ name: 'AddGene' });
    }
  }
}
</script>

<style scoped>
h1 {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  color: #2c3e50;
}
</style>
