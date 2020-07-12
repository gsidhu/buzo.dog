<template>
    <div class='col-sm-9 mx-auto my-4'>
        <h3 id='links'>Publications</h3>
        <div class="row mx-auto justify-content-center">
            <div v-bind:key="pub.id" v-for="pub in pubs" class="links-div mb-2 mx-1 shadow-sm">
                <a role='button' class="no-underline btn btn-light link" v-on:click="fetchMore(pub.title)">
                    {{ pub.title }}
                </a>
                <!-- <Pub v-bind:pub="pub" /> -->
            </div>
        </div>
        <Links v-bind:links="links" :title="title" />
        <button class='btn btn-light mr-2' v-on:click="scrollUp()">Go Up</button>
        <button class='btn btn-light' v-on:click="fetchMore(title)">More</button>
    </div>
</template>

<script>
import Links from '../components/Links';

import axios from 'axios';
import $ from 'jquery';

// eslint-disable-line no-unused-vars
export default {
  name: 'Scroll',
  props: ["pubs"],
  components: {
    Links
  },
  data() {
    return {
      links: [],
      title: "All"
    }
  },
  created() {
      axios.get('https://api.buzo.dog/api/v1/resources/links?count=10')
        .then( response => this.links = response.data)
        .catch( err => console.log(err));
      // code for pulling publications from API
  },
  computed: { 
  },
  methods: {
    fetchMore(source) {
        this.title = source;
        var api_link = '';
        if (source === 'All') {
            api_link = 'https://api.buzo.dog/api/v1/resources/links?count=10';
        } else {
            api_link = 'https://api.buzo.dog/api/v1/resources/links?count=10' + '&source=' + encodeURI(source);
        }
        console.log(api_link)
        axios.get(api_link)
            .then( response => this.links = response.data)
            .catch( err => console.log(err));
    },
    scrollUp() {
      $([document.documentElement, document.body]).animate({
              scrollTop: $("#links").offset().top
        }, 1000);
    }
  }
}
</script>

<style scoped>
</style>