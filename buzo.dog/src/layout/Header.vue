<template>
    <header>
        <router-link to="/">
            <img alt="Buzo logo" src="../assets/buzo.png">
            <h1>Buzo.Dog</h1>
        </router-link>
        <p>{{ msg }}</p>
    </header>
</template>

<script>
export default {
    name: 'Header',
    props: {
    },
    data() {
        return {
            msg: "My personal reader.",
            allow: 0
        }
    }
}
</script>

<style scoped>
img {
    width: 10%;
}
a, a:hover,
a:visited {
    color: inherit;
    text-decoration: none;
}
</style>