<template>
  <div id="app" class='container'>
    <div id='meta-box' class='col-md-6 mx-auto my-4'>
      <h5><a :href='link[0].link' rel="nofollow" target="_blank">{{link[0].title}}</a></h5>
      <p v-if='link[0].description != null'>{{link[0].description}}</p>
      <p style='text-align: right'><b>&mdash; {{link[0].source}}</b></p>
      <p>Tags: {{link[0].tags}}</p>
      <p v-if='link[0].pubdate != null'>Published on: {{link[0].pubdate}}</p>
    </div>
    <div class='col-sm-10 mx-auto my-4'>

      <button class='btn btn-light' v-on:click="removeImages()">Text Only</button>
      <!-- <button class='btn btn-light' v-on:click="fetchMore(title)">More</button> -->
      
      
      <div v-html="link[0].html" id='raw-text'>
      </div>

      <button class='btn btn-light mr-2' v-on:click="scrollUp()">Go Up</button>
    </div>
  </div>
</template>

<script>
// import Publications from '../components/Publications';

import axios from 'axios';
import $ from 'jquery';

export default {
  name: 'Cache',
  props: ["links"],
  components: {
    // Publications
  },
  data() {
    return {
      id: this.$route.query.id,
      link: {}
    }
  },
  created() {
      var api_link = 'https://api.buzo.dog/api/v1/resources/links?_id=' + this.id;
      axios.get(api_link)
        .then( response => this.link = response.data)
        .catch( err => console.log(err));
  },
  methods: {
    scrollUp() {
      $([document.documentElement, document.body]).animate({
              scrollTop: $("#app").offset().top
        }, 1000);
    },
    removeImages() {
      var imageNodes = $('img');
      for (var i=0; i < imageNodes.length; i++) {
        imageNodes[i+1].remove()
      }
    }
  }
}

</script>

<style>
#raw-text {
  text-align: left;
}
#raw-text img {
  width: auto;
  height: 30vw;
  object-fit: cover;
}

#meta-box {
  text-align: left;
  padding: 20px;
  background: bisque;
}
#meta-box p {
  margin-bottom: 5px;
}
#meta-box a {
  text-decoration: none;
  border-bottom: 1px black solid;
  color: black;
}
#raw-text blockquote {
  padding-left: 10px;
  border-left: 5px #ddd solid;
}
#raw-text blockquote > p {
  margin: 0 2rem 1rem 0;
}
</style>
