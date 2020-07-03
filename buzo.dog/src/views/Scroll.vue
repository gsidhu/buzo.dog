<template>
  <div id="app" class='container'>
      <Publications v-bind:pubs="pubs" />
      <button class='btn btn-light' v-on:click="scrollUp()">go up</button>
  </div>
</template>

<script>
import Publications from '../components/Publications';

// import axios from 'axios';
import $ from 'jquery';

export default {
  name: 'Scroll',
  components: {
    Publications
  },
  data() {
    return {
      pubs: [{"id": 0, "title": 'All'},
      {"id": 1, "title": 'Random'},
      {"id": 2, "title": 'Pinboard'},
      {"id": 3, "title": 'Reddit Subs'},
      {"id": 4, "title": "Reddit threads"},
      {"id": 5, "title": 'Brain Pickings'},
      {"id": 6, "title": 'Aeon'},
      {"id": 7, "title": 'Wikipedia'},
      {"id": 8, "title": 'Vox'},]
    }
  },
  created() {
    // code for pulling publications from API
      // axios.get('https://api.buzo.dog/api/v1/resources/links?count=10')
      //   .then( response => this.links = response.data)
      //   .catch( err => console.log(err));
  },
  methods: {
    scrollUp() {
      $([document.documentElement, document.body]).animate({
              scrollTop: $("#links").offset().top
        }, 1000);
    }
  }
}

</script>

<style>

</style>
