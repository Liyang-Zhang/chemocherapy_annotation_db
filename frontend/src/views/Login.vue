<template>
  <div class="login">
    <h2>Login</h2>
    <form @submit.prevent="login">
      <div>
        <label for="username">Username</label>
        <input type="text" v-model="username" required class="input-field">
      </div>
      <div>
        <label for="password">Password</label>
        <input type="password" v-model="password" required class="input-field">
      </div>
      <button type="submit">Login</button>
    </form>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'UserLogin',
  data() {
    return {
      username: '',
      password: '',
    };
  },
  methods: {
    async login() {
      try {
        const response = await axios.post('/api/login/', {
          username: this.username,
          password: this.password,
        });
        localStorage.setItem('token', response.data.token);
        this.$router.push('/');
      } catch (error) {
        alert('Invalid credentials');
      }
    },
  },
};
</script>

<style scoped>
.login {
  max-width: 300px;
  margin: 100px auto;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

form div {
  margin-bottom: 10px;
}

label {
  display: block;
  margin-bottom: 5px;
}

.input-field {
  width: 100%;
  padding: 8px;
  box-sizing: border-box;
  border: 2px solid #000; /* 设置边框宽度和颜色 */
}

button {
  width: 100%;
  padding: 10px;
  background-color: #007BFF;
  border: none;
  color: white;
  border-radius: 4px;
  cursor: pointer;
}

button:hover {
  background-color: #0056b3;
}
</style>
