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
      {"title": 'Recent'},
      {"title": 'Favourite'}],
      pubs: [{"title": 'Brain Pickings'},
      {"title": 'Aeon'},
      // {"title": 'Pinboard'},
      // {"id": 5, "title": 'xkcd'},
      // {"id": 6, "title": "Three Word Phrase"},
      {"title": "Margins"},
      {"title": "Stratechery"},
      {"title": "Mark Manson"},
      {"title": "fs blog"},
      {"title": "Alex Danco's Newsletter"},
      {"title": "Drew Devault's Blog"},
      {"title": "Seminar"}]
    }
  },
  created() {
    document.getElementsByTagName('title')[0].textContent = "Browse | buzo.dog" 
    // code for pulling publications from API
      // axios.get('https://api.buzo.dog/api/v1/resources/links?count=10')
      //   .then( response => this.links = response.data)
      //   .catch( err => console.log(err));
  },
  methods: {
  }
}

</script>

<style>

</style>
