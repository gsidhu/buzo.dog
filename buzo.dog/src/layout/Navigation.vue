<template>
  <div id="nav" class='py-2 mx-auto' @click='login()'>
    <router-link to="/">Home</router-link> |
    <router-link to="/about">About</router-link> |
    <router-link to="/add">Add</router-link>
  </div>
</template>

<script>

export default {
    name: 'Navigation',
    data: function() {
      return {
        allow: 0,
      };
    },
    components: {
    },
    methods: {
      login() {
        this.allow = this.allow + 1
        if (this.allow === 5) {
          console.log(this.allow)
          sessionStorage.setItem('isLoggedIn', true);
        }
      }
    }
}
</script>

<style scoped>
#nav {
  font-size: x-large;
  background-color: #eeeeee60;
  border: 1px dotted #ddd;
  width: 300px;
}

#nav a {
  font-weight: bold;
  color: #2c3e50;
}

#nav a.router-link-exact-active {
  color: #42b983;
}
</style>