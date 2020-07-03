<template>
    <div class='col-sm mx-auto my-4'>
        <h3 id='title'>Source: {{title}}</h3>
        <div v-bind:key="link._id" v-for="link in links" class="links-div my-2">
            <Item v-bind:link="link" />
        </div>
    </div>
</template>

<script>
import Item from './Item'; 
// eslint-disable-line no-unused-vars
export default {
    name: "Links",
    components: {
        Item
    },
    props: ["links", "title"]
}
</script>

<style scoped>
</style>