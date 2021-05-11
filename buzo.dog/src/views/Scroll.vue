<template>
  <main class='container'>
    <Publications v-bind:pubs="pubs" />
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
      pubs: [{"id": 1, "title": 'All'},
      // {"id": 2, "title": 'Pinboard'},
      {"id": 3, "title": 'Brain Pickings'},
      {"id": 4, "title": 'Aeon'},
      // {"id": 5, "title": 'xkcd'},
      // {"id": 6, "title": "Three Word Phrase"},
      {"id": 7, "title": "Margins"},
      {"id": 8, "title": "Stratechery"},
      {"id": 9, "title": "Mark Manson"},
      {"id": 10, "title": "fs blog"},
      {"id": 11, "title": "Alex Danco's Newsletter"},
      {"id": 12, "title": "Drew Devault's Blog"},
      {"id": 13, "title": "Seminar"}]
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
