<template>
  <main class='container'>
    <Publications v-bind:pubs="pubs" :cats="cats" />
  </main>
</template>

<script>
import Publications from '../components/Publications';
// import axios from 'axios';
// import $ from 'jquery';

export default {
  name: 'Scroll',
  components: {
    Publications
  },
  data() {
    return {
      cats: [{"title": 'All'},
      // {"title": 'Recent'},
      {"title": 'Favourites'}],
      pubs: [
        {"title": 'Aeon'},
        {"title": 'Psyche'},
        {"title": 'Fifty Two'},
        {"title": 'Palladium'},
        {"title": "fs blog"},
        {"title": "Alex Danco"},
        {"title": "Drew Devault"},
        {"title": "Margins"},
        {"title": "Ava"},
        {"title": "Seminar"},
        {"title": "Stratechery"},
        {"title": "Mark Manson"},
        {"title": 'The Marginalian'},
        {"title": "Other"},
      ]
    }
  },
  created() {
    document.getElementsByTagName('title')[0].textContent = "Browse | buzo.xyz" 
    // code for pulling publications from API
      // axios.get('https://api.buzo.xyz/api/v1/resources/links?count=10')
      //   .then( response => this.links = response.data)
      //   .catch( err => console.log(err));
  },
  methods: {
  }
}

</script>

<style>

</style>
