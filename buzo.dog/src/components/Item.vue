<template>
  <div>
    <!-- Card view -->
    <div v-if="type==='card'">
      <div class='card'>
        <!-- Article title -->
        <h5 class="card-header">
          <a v-bind:href="link.link" rel="nofollow" target="_blank" v-if="link.title != ''"><strong>{{ link.title }}</strong></a>
          <a v-bind:href="link.link" rel="nofollow" target="_blank" v-else>{{ link.link }}</a>
        </h5>
        
        <div class="card-body">
          <!-- Publication name -->
          <h6 class="card-subtitle mb-2 text-muted">
            <span v-if="link.source==='Statechery'">Stratechery</span><span v-else>{{link.source}}</span>
          </h6>
          <!-- Article description -->
          <p class="card-text">
            {{link.excerpt}}
          </p>
        </div>
        <!-- Links -->
        <div class='card-footer'>
          <!-- Link to original -->
          <a v-bind:href="link.url" rel="nofollow" target="_blank" class="btn btn-primary btn-sm mr-2" role="button">Original</a>
          <!-- Link to cached copy -->
          <a v-bind:href="'/#/cache?link=' + link.url" class="btn btn-info btn-sm mr-2" role="button">Cached</a>
          <!-- Edit -->
          <a v-if="isLoggedIn" class='btn btn-warning btn-sm' role='button' data-toggle="modal" data-target="#edit-modal" v-bind:data-serial="index" @click="callModal(index)">✏️</a>
        </div>
      </div>
    </div>

    <!-- Link view -->
    <div v-if="type==='list'">
      <strong>
          <span v-if="link.title != ''">{{ link.title }}</span>
          <span v-else>{{ link.link }}</span>
      </strong>
      <span> ({{link.source}})</span>
      &mdash;
      <a v-bind:href="link.url" rel="nofollow" target="_blank">Original</a>
      |
      <a v-bind:href="'/#/cache?link=' + link.url">Cached</a>
      <a v-if="isLoggedIn" role='button' data-toggle="modal" data-target="#edit-modal" v-bind:data-serial="index" @click="callModal(index)"> &mdash; ✏️</a>
    </div>
  </div>

</template>

<script>
export default {
  name: "Item",
  props: ["link", "index", "type"],
  components: {
  },
  data() {
    return {
      isLoggedIn: sessionStorage.getItem('isLoggedIn'),
    }
  },
  methods: {
    callModal(index) {
      this.$emit("call", index)
    }
  }
}
</script>

<style scoped>
.link:hover {
    background-color: #f7f5f5;
}
.card {
  text-align: left;
  height: 300px;
}
.card-body {
  overflow: auto;
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