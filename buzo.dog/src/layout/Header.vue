<template>
    <header>
        <router-link to="/">
            <img alt="Buzo logo" src="../assets/buzo.png">
            <h1>Buzo.Dog</h1>
        </router-link>
        <p @click='login()'>{{ msg }}</p>
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
img {
    width: 10%;
}
a, a:hover,
a:visited {
    color: inherit;
    text-decoration: none;
}
</style>