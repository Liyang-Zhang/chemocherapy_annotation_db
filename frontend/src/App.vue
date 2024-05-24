<template>
  <div id="app">
    <img alt="Vue logo" src="./assets/logo.png" />
    <HelloWorld msg="Welcome to Chemotherapy annotation db App" />
    <div v-if="chemoGenes.length">
      <h1>ChemoGene List</h1>
      <ul>
        <li v-for="gene in chemoGenes" :key="gene.id">
          <h2>{{ gene.gene_name }}</h2>
          <p>{{ gene.description }}</p>
        </li>
      </ul>
    </div>
    <div v-else>
      <p>Loading data...</p>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import HelloWorld from './components/HelloWorld.vue';

export default {
  name: 'App',
  components: {
    HelloWorld,
  },
  data() {
    return {
      chemoGenes: [],
    };
  },
  created() {
    axios
      .get('/api/Chemogene/')
      .then((response) => {
        console.log('API response:', response); // 添加调试输出
        this.chemoGenes = response.data;
      })
      .catch((error) => {
        console.error('There was an error!', error); // 添加调试输出
      });
  },
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
