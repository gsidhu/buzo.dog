<template>
  <article onscroll="blurToolbar()">

    <section id='meta'>
      <div id='meta-box' class='col-md-6 mx-auto my-4'>
        <h5 id='meta-title'><a id='meta-title-link' rel="nofollow" target="_blank"></a></h5>
        <p id='meta-description'></p>
        <p id='meta-source' style='text-align: right; font-weight: bold'></p>
        <p id='meta-tags'></p>
        <p id='meta-pubdate'></p>
      </div>
    </section>

    <Toolbar :reader="1" :isFaved="isFaved" @modal="populateModal" @links="getCachedLinks" @toggle="html = !html" @fav="favit"/>

    <section id='text' class='py-4'>
      <div class='col-10 col-md-8 col-xl-6 mx-auto my-4 px-1'>
        <div v-if='html' class='raw' id='raw-html'></div>
        <div v-else class='raw' id='raw-text'>{{ link[0].text }} </div>
      </div>
    </section>

    <Edit id="edit-modal" />
  </article>
</template>

<script>
import Edit from '@/components/Edit'
import Toolbar from '@/components/Toolbar'

import axios from 'axios';
import $ from 'jquery';

export default {
  name: 'Cache',
  metaInfo: {
    title: 'buzobuzo'
  },
  // props: ["links"],
  components: {
    Edit,
    Toolbar
  },
  data() {
    return {
      id: this.$route.query.link,
      link: {},
      cachedLinks: [],
      cachedIndices: [],
      promises: [],
      html: true,
      isFaved: false
    }
  },
  created() {
      var api_link = 'https://api.buzo.xyz/api/v1/resources/links?link=' + this.id;
      axios.get(api_link)
        .then( response => {
          var payload = response.data
          this.link = payload
          this.isFaved = payload[0].likes

          // add meta and text
          document.getElementById('meta-title-link').href = payload[0].url
          document.getElementById('meta-title-link').textContent = payload[0].title
          // document.getElementById('meta-description').textContent = payload[0].excerpt
          document.getElementById('meta-source').textContent = '— '.concat(payload[0].source)
          if (payload[0].tags) {document.getElementById('meta-tags').textContent = 'Tags: '.concat(payload[0].tags)}
          if (payload[0].pubdate) {document.getElementById('meta-pubdate').textContent = 'Published on: '.concat(payload[0].pubdate)}

          document.getElementById('raw-html').innerHTML = payload[0].html

          document.getElementsByTagName('title')[0].textContent = payload[0].title + " – " + payload[0].source + " | buzo.xyz" 
        })
        .catch( err => console.log(err));
  },
  mounted() {
  },
  updated() {
    // center align and add cross button
    this.fixImages()
  },
  methods: {
    blurToolbar() {
        document.getElementById('toolbar').style.opacity = 0.6
    },
    removeImages() {
      var imageNodes = $('#text img');
      for (var i=0; i < imageNodes.length; i++) {
        imageNodes[i+1].remove()
      }
    },
    fixImages() {
      var img = $('#text img')
      for (var i=0; i < img.length; i++) {
        var el = img[i]

        // remove links from images
        if (el.parentElement.tagName === 'A') {
          const a = el.parentNode
          // add the img tag to A's parent
          a.parentNode.insertBefore(el, a.nextSibling)
          // remove A
          a.remove()
        }
        // center align images
        if (el.closest('p')) {
          el.closest('p').style.textAlign = 'center'
        } else {
          const newP = document.createElement('p')
          newP.style.textAlign = 'center'
          el.parentNode.insertBefore(newP, el.nextSibling)
          newP.appendChild(el)
        }

        // add close button
        const newEl = document.createElement('span');
        newEl.appendChild(document.createTextNode('x'));
        newEl.style.fontWeight = 'bold';
        newEl.style.color = 'red';
        newEl.style.position = 'absolute';
        newEl.style.zIndex = '1';
        newEl.style.cursor = 'pointer';

        el.parentNode.insertBefore(newEl, el.nextSibling);

        newEl.onclick = function() {
          const parent = this.closest('p')
          parent.parentNode.removeChild(parent);
        }
      }
    },
    getCachedLinks() {
      var all_href = $('#text a');
      var currentHost = (new URL(this.link[0].url)).hostname;

      for (var i=0; i < all_href.length; i++) {
        // attach link
        let tempLink = all_href[i].href
        // remove any query terms
        if (tempLink.indexOf('?') > 0) {
          tempLink = tempLink.slice(0,tempLink.indexOf('?'))
        }
        // check link's host
        var newHost = (new URL(tempLink)).hostname;
        // if same host, store the link and its index
        if (currentHost === newHost) {
          tempLink = 'https://api.buzo.xyz/api/v1/resources/links?link=' + encodeURI(tempLink);
          this.cachedLinks.push(tempLink)
          this.cachedIndices.push(i)
        }
      }
      
      // 
      this.cachedLinks.forEach(myURL => {
        console.log(myURL)
        this.promises.push(axios.get(myURL));
      });

      let self = this

      Promise.all(this.promises).then(function (results) {
        results.forEach(function (response, i) {
          if (response.data.length > 0) {
            const tempID = response.data[0].url;
            if(tempID.length > 0) {
              all_href[self.cachedIndices[i]].outerHTML = all_href[self.cachedIndices[i]].outerHTML + " (<a href=/#/cache?link=" + tempID + ">cached</a>)";
            }
          }
        });
      });
    },
    populateModal() {
      document.getElementById('link-id').textContent = this.link[0]._id
      document.getElementById('link-title').value = this.link[0].title
      document.getElementById('link-publication').value = this.link[0].source
      document.getElementById('link-description').value = this.link[0].description
      document.getElementById('link-tags').value = this.link[0].tags
      document.getElementById('link-author').value = this.link[0].author
    },
    favit() {
      const iD = this.link[0].url
      if (this.isFaved) {
        var likes = 0
      } else { likes = 1 }

      axios.post(("https://api.buzo.xyz/api/v1/storage/update?link=" + iD + "&likes=" + likes))
        .then(response => {
        if(response.data.response) {
            console.log("success")
            this.isFaved = !this.isFaved
        } else {
            console.log("failed")
        }
        })
        .catch(error => {
        console.log(error);
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

@media screen and (max-width:400px) {
  .raw img {
    height: 70vw;
  }
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
#text {
  background-color: #fef7f2;
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
