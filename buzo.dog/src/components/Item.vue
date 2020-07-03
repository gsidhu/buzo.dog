<template>

    <div class='card'>
        <!-- <img v-bind:src="link.image" class='card-title'/> -->
        <a class='card-body link' v-bind:href="link.link" rel="nofollow" target="_blank" v-if="link.title != ''">
        {{ link.title }}
        </a>
        <a class='card-body link' v-bind:href="link.link" rel="nofollow" target="_blank" v-else>
            {{ link.link }}
        </a>
        <p class='card-footer'>
            {{link.description}}
        </p>
    </div>
    <!-- <p class=''>
        {{ link.source}}
    </p> -->

</template>

<script>
export default {
    name: "Item",
    props: ["link"]
}
</script>

<style scoped>
.link:hover {
    background-color: #f7f5f5;
}

.card-footer {
    text-align: left;
    margin-bottom: 0;
}
</style>