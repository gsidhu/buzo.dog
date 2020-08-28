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
      <button class='btn btn-light mr-2' v-on:click="toggleView()">Toggle Text View</button>
      <button class='btn btn-light' v-on:click="getCachedLinks()">Show Internal Links</button>
      
      <!-- <div v-html="link[0].html" class='raw d-none' id='raw-html'>
      </div> -->

      <!-- <div v-html="link[0].rawhtml" class='raw' id='raw-html'>
      </div> -->

      <!-- <div class='raw d-none' id='raw-text'>
        {{link[0].text}}
      </div> -->

      <div class='raw' id='raw-buzotext'>
        {{link[0].buzotext}}
      </div>

      <button class='btn btn-light' v-on:click="scrollUp()">Go Up</button>
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
      link: {},
      cachedLinks: [],
      cachedIndices: [],
      promises: []
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
    },
    toggleView() {
      $('#raw-text').toggleClass('d-none');
      $('#raw-buzotext').toggleClass('d-none');
    },
    getCachedLinks() {
      var all_href = $('a');
      var currentHost = (new URL(this.link[0].link)).hostname;

      for (var i=0; i < all_href.length; i++) {
        let tempLink = all_href[i].href
        if (tempLink.indexOf('?') > 0) {
          tempLink = tempLink.slice(0,tempLink.indexOf('?'))
        }
        var newHost = (new URL(tempLink)).hostname;
        if (currentHost === newHost) {
          tempLink = 'https://api.buzo.dog/api/v1/resources/links?link=' + encodeURI(tempLink);
          this.cachedLinks.push(tempLink)
          this.cachedIndices.push(i)
        }
      }
      
      this.cachedLinks.forEach(myURL => {
        this.promises.push(axios.get(myURL));
      });

      let self = this

      Promise.all(this.promises).then(function (results) {
        results.forEach(function (response, i) {
          if (response.data.length > 0) {
            const tempID = response.data[0]._id;
            if(tempID.length > 0) {
              all_href[self.cachedIndices[i]].outerHTML = all_href[self.cachedIndices[i]].outerHTML + " (<a href=/#/cache?id=" + tempID + ">cached</a>)";
            }
          }
        });
      });
    }
  }
}

</script>

<style>
.raw {
  text-align: left;
}
.raw img {
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
  /* border-bottom: 1px black solid; */
  color: black;
}
.raw blockquote {
  padding-left: 10px;
  border-left: 5px #ddd solid;
}
.raw blockquote > p {
  margin: 0 2rem 1rem 0;
}

#raw-text, #raw-buzotext {
  white-space: pre-line;
}
</style>
