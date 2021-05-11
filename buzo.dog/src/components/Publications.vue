<template>
    <div class='mx-auto my-4'>
      <toolbar :reader=0 @toggle="card = !card"></toolbar>
        <h3 id='links'>Publications</h3>
        <div class="row mx-auto justify-content-center">
            <div v-bind:key="index" v-for="(pub, index) in pubs" class="links-div mb-2 mx-1 shadow-sm">
                <a role='button' class="no-underline btn btn-light link" v-on:click="fetchMore(pub.title, 0)">
                    {{ pub.title }}
                </a>
            </div>
        </div>

        <Links v-bind:links="links" :title="title" :card="card"/>
    </div>
</template>

<script>
import Links from '../components/Links';
import Toolbar from '@/components/Toolbar'

import axios from 'axios';
import $ from 'jquery';

// eslint-disable-line no-unused-vars
export default {
  name: 'Publications',
  props: ["pubs"],
  components: {
    Links,
    Toolbar
  },
  data() {
    return {
      links: [],
      title: "All",
      card: true
    }
  },
  beforeMount() {
      this.fetchMore('All', 0)

      // code for pulling publications from API
  },
  mounted() {
    this.infiniteMore();
  },
  methods: {
    fetchMore(source, push) {
        if (source === 'Stratechery') {
          source = 'Statechery';
        } 
        this.title = source;

        // fetch new links
        var api_link = '';
        if (source === 'All') {
            api_link = 'https://api.buzo.dog/api/v1/resources/links?count=15';
        } else {
            api_link = 'https://api.buzo.dog/api/v1/resources/links?count=15' + '&source=' + encodeURI(source);
        }
        
        // push them to the variable
        if (push) {
          axios.get(api_link)
            .then( response => {
              this.links.push.apply(this.links, response.data);
            })
            .catch( err => console.log(err));
        } else {
          axios.get(api_link)
            .then( response => this.links = response.data)
            .catch( err => console.log(err));
        }
    },
    infiniteMore() {
      window.onscroll = () => {
        let bottomOfWindow = document.documentElement.scrollTop + window.innerHeight === document.documentElement.offsetHeight;
        if (bottomOfWindow) {
          this.fetchMore(this.title, 1)
        }
      }
    },
    scrollUp() {
      $([document.documentElement, document.body]).animate({
              scrollTop: $("#scroll-area").offset().top
        }, 1000);
    }
  }
}
</script>

<style scoped>
</style>