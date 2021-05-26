<template>
  <div class="text-center space-out bg-color"> 
    <h4 class="mt-5 font-weight-normal">{{msg}}</h4>
    <form v-if="!fetched && isLoggedIn" id='fetch-form' class="form-signin">
      <div class="my-2">
        <label for="inputLink" class="sr-only">Link</label>
        <input type="text" id="inputLink" class="form-control" placeholder="URL" required="true" autofocus="" autocomplete="off">
      </div>
      <button class="btn btn-lg btn-primary btn-block mb-5" @click="fetch()">Fetch!</button>
    </form>

    <section id="result" class='col-10 col-lg-8 col-xl-6 mx-auto d-none'>
        <div>
            <h5><strong>Submitted URL: </strong><a id='submitted-link' href="/" rel="nofollow" target="_blank"></a></h5>
            <a id='cached-link' href="" target="_blank">Read cached copy here.</a>
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
              <label class=''>
                <input id="link-delete" type="checkbox" aria-label="Mark item as 'to fix'"> <strong>Delete</strong>
              </label>
            </div>
        </div>
        <div class="" style="display: inline">
            <button class="btn btn-lg btn-primary mr-3 mb-5" @click="push()">Submit</button>
            <button class="btn btn-lg btn-warning mb-5" @click="reset()">Cancel</button>
        </div>
    </section>
    <section class='col-md-6 col-lg-4 mx-auto mb-5'>
      <Item v-if="submitted" v-bind:link="bone" v-bind:index="0" type='card' />
    </section>
  </div>
</template>

<script>
import axios from 'axios';
import Item from '../components/Item'

export default {
  name: 'Add',
  components: {
    Item
  },
  data: function() {
    return {
      link: '',
      bone: [],
      fetched: false,
      submitted: false,
      msg: 'Add a new article',
      isLoggedIn: sessionStorage.getItem('isLoggedIn')
    };
  },
  created() {
  },
  methods: {
    fetch() {
      this.link = document.getElementById('inputLink').value
      this.link = this.link.split(/[?#]/)[0] // remove query string
      axios.get(("https://api.buzo.dog/api/v1/storage/add?link=" + encodeURI(this.link)))
        .then ( response => { 
          this.bone = response.data
          if (response.data.exists) {
            this.msg = 'Article already exists in library.'
            this.submitted = true
            document.getElementById('fetch-form').classList.add('d-none')
          } else {
            this.fetched = true
            this.submitted = false
            document.getElementById('result').classList.remove('d-none')
            this.populateFields()
          }
        })
        .catch ( err => {
          console.log(err)
          this.reset(0);
        })
    },
    populateFields() {
      var host = new URL(this.link)
      host = host.host
      document.getElementById('submitted-link').textContent = this.link
      document.getElementById('submitted-link').href = this.link
      document.getElementById('cached-link').href = '/#/cache?id=' + this.bone._id
      document.getElementById('link-title').value = this.bone.title
      document.getElementById('link-publication').value = host
      document.getElementById('link-description').value = this.bone.description
      document.getElementById('link-author').value = this.bone.author
    },
    push() {
      if (document.getElementById('link-delete').checked) {
        axios.delete("https://api.buzo.dog/api/v1/storage/purge?iD=" + this.bone._id)
          .then( response => {
            console.log(response.data)
            this.reset()
            this.submitted = false
          })
          .catch(error => console.log(error))
      }
      var payload = {
        iD: this.bone._id,
        title: document.getElementById('link-title').value,
        source: document.getElementById('link-publication').value,
        description: document.getElementById('link-description').value,
        tags: document.getElementById('link-tags').value,
        language: document.getElementById('link-language').value,
        author: document.getElementById('link-author').value
      }
      console.log(payload)
      payload = this.toQueryString(payload)

      axios.post(("https://api.buzo.dog/api/v1/storage/update" + payload))
        .then(response => {
          if(response.data.success) {
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
      this.query = null
      this.fetched = false
      if (success === null) {
        this.msg = "Add a new article"
        this.bone = []
      } else if (success === 1) {
        this.msg = "Link added! Add another?"
        this.submitted = true
        this.bone.link = this.link
      } else if (success === 0) {
        this.msg = "That didn't work. Try again?"
        this.bone = []
      }
      this.link = ''
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