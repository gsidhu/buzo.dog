<template>
    <footer class='container'>
        <hr>
        <h5>buzo.xyz</h5>
        <p>CC-BY-SA-4.0 | <a href="https://github.com/gsidhu/buzo.dog" target="_blank">GitHub</a></p>
    </footer>
</template>

<script>
export default {
    name: 'Footer',
    props: {
        msg: String
    }
}
</script>

<style scoped>
footer {
    text-align: left;
}
</style>