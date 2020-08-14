<template>
    <div class='card'>
        <!-- <img class="card-img-top" v-bind:src="link.image" alt="Card image cap"> -->
        <a class='card-body' v-bind:href="link.link" rel="nofollow" target="_blank" v-if="link.title != ''">{{ link.title }}</a>
        <a class='card-body' v-bind:href="link.link" rel="nofollow" target="_blank" v-else>{{ link.link }}</a>

        <p class='card-footer'>
            {{link.description}} <br/>
            <span v-if="link.source==='Statechery'">&mdash; Stratechery</span><span v-else>&mdash; {{link.source}}</span> <a v-bind:href="'/#/cache?id=' + link._id">(cached)</a>
        </p>
    </div>
</template>

<script>
export default {
  name: "Item",
  props: ["link"],
  data() {
    return {
      links: []
    }
  }
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

.card-img-top {
    width: 100%;
    height: 10vw;
    object-fit: cover;
}
</style>