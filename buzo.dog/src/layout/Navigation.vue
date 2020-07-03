<template>
    <div>
        <div id="nav" class='py-2 mx-auto'>
            <router-link to="/">Home</router-link> |
            <router-link to="/about">About</router-link>
        </div>

        <!-- <AddLink /> -->
    </div>
</template>

<script>
// import AddLink from '../components/AddLink';

export default {
    name: 'Navigation',
    components: {
        // AddLink
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