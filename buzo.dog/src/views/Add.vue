<template>
  <div class="text-center space-out bg-color"> 
    <h4 class="mt-5 font-weight-normal">{{msg}}</h4>
    <form v-if="!fetched" class="form-signin">
      <div class="my-2">
        <label for="inputLink" class="sr-only">Link</label>
        <input type="text" id="inputLink" class="form-control" placeholder="URL" required="true" autofocus="" autocomplete="off">
      </div>
      <button v-if="isLoggedIn" class="btn btn-lg btn-primary btn-block mb-5" @click="fetch()">Fetch!</button>
    </form>

    <section id="result" class='col-10 col-lg-8 col-xl-6 mx-auto d-none'>
        <div>
            <h5><strong>Submitted URL: </strong><a id='submitted-link' href="/" rel="nofollow" target="_blank"></a></h5>
        </div>
        <div class="row row-cols-1">
            <div class="col my-2">
              <label for="link-title"><strong>Title</strong></label>
              <input type="text" class="form-control" id="link-title" placeholder="" value="">
            </div>
            <div class="col my-2">
              <label for="link-publication"><strong>Publication</strong></label>
              <input type="text" class="form-control" id="link-publication" placeholder="" value="">
            </div>
            <div class='col my-2'>
              <label for="link-description"><strong>Description</strong></label>
              <textarea type="text" class="form-control" id="link-description" placeholder="" value=""></textarea>
            </div>
            <div class='col my-2'>
              <label for="link-tags"><strong>Tags</strong></label>
              <input type="text" class="form-control" id="link-tags" placeholder="" value="">
            </div>
            <div class='col my-2'>
              <label for="link-language"><strong>Language</strong></label>
              <input type="text" class="form-control" id="link-language" placeholder="" value="EN">
            </div>
            <div class='col my-2'>
              <label for="link-author"><strong>Author</strong></label>
              <input type="text" class="form-control" id="link-author" placeholder="" value="">
            </div>
            <div class='col my-2'>
              <label for="link-html"><strong>Raw HTML</strong></label>
              <textarea type="text" class="form-control" id="link-html" placeholder="" value=""></textarea>
            </div>
            <div class='col my-2'>
              <label for="link-text"><strong>Text</strong></label>
              <textarea type="text" class="form-control" id="link-text" placeholder="" value=""></textarea>
            </div>
            <div class='col my-2'>
              <label class=''>
                <input id="link-fix" type="checkbox" aria-label="Mark item as 'to fix'"> <strong>Needs fixing</strong>
              </label>
            </div>
        </div>
        <div class="" style="display: inline">
            <button class="btn btn-lg btn-primary mr-3 mb-5" @click="push()">Submit</button>
            <button class="btn btn-lg btn-warning mb-5" @click="reset()">Cancel</button>
        </div>
    </section>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'Add',
  data: function() {
    return {
      link: '',
      bone: [],
      fetched: false,
      msg: 'Add a new article',
      isLoggedIn: sessionStorage.getItem('isLoggedIn')
    };
  },
  created() {
  },
  methods: {
    fetch() {
      this.link = document.getElementById('inputLink').value
      axios.get(("https://api.buzo.dog/api/v1/storage/fetch?link=" + encodeURI(this.link)))
        .then ( response => { 
          this.bone = response.data
          this.fetched = true
          document.getElementById('result').classList.remove('d-none')
          this.populateFields()
        })
        .catch ( err => {
          console.log(err)
          this.reset(0);
        })
    },
    populateFields() {
      var host = new URL(this.link)
      host = host.host
      // document.getElementById('submitted-link').textContent = this.bone[0].link
      document.getElementById('submitted-link').textContent = this.link
      document.getElementById('submitted-link').href = this.link
      document.getElementById('link-title').value = this.bone.title
      document.getElementById('link-publication').value = host
      document.getElementById('link-description').value = this.bone.description
      // document.getElementById('link-tags').value = this.bone[0].tags
      document.getElementById('link-author').value = this.bone.author
      document.getElementById('link-html').value = this.bone.html
      document.getElementById('link-text').value = this.bone.text
    },
    push() {
      var payload = {
        link: this.link,
        title: document.getElementById('link-title').value,
        source: document.getElementById('link-publication').value,
        description: document.getElementById('link-description').value,
        tags: document.getElementById('link-tags').value,
        language: document.getElementById('link-language').value,
        author: document.getElementById('link-author').value,
        // text: document.getElementById('link-text').value,
        // html: document.getElementById('link-html').value,
        pubdate: this.bone.pubdate
      }
      console.log(payload)
      payload = this.toQueryString(payload)

      // const config = {
      //   headers: {
      //     "Referer": "https://buzo.dog",
      //     "Referrer-Policy": "same-origin"
      //   },
      // };
      axios.put(("https://api.buzo.dog/api/v1/storage/add" + payload))
        .then(response => {
          if(response.data === 'Success') {
            this.reset(1)
          } else {
            this.reset(0)
          }
        })
        .catch(error => {
          console.log(error);
        });
    },
    toQueryString(payload) {
      var keys = Object.keys(payload)
      var query = '?' + keys[0] + '=' + payload[keys[0]]
      for (var i = 1; i < keys.length; i++) {
        query = query + '&' + keys[i] + '=' + payload[keys[i]]
      }
      query = encodeURI(query)
      return query
    },
    reset(success=null) {
      if (success === null) {
        this.msg = "Add a new article"
      } else if (success === 1) {
        this.msg = "Link added successfully. Add another?"
      } else if (success === 0) {
        this.msg = "Link could not be added. Try another?"
      }
      this.link = ''
      this.bone = []
      this.query = null
      this.fetched = false
      document.getElementById('result').classList.add('d-none')
    }
  }
};
</script>

<style scoped>
.form-signin {
	width: 50%;
	max-width: 250px;
	margin: auto;
}
.space-out {
  margin-top: 5rem !important;
  margin-bottom: 5rem !important;
}
.bg-color {
  /* background: #FFEACB; */
  background-color: #fef7f2;
	overflow: hidden;
	width: 100%;
	border-radius: 16px;
	box-sizing: border-box;
}
#link-description {
    height: 100px;
}
#link-html,
#link-text {
    height: 200px;
    overflow: auto;
}
</style>