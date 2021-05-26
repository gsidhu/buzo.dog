<template>
  <div class="modal" tabindex="-1">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">Edit article</h5>
          <button type="button" class="close" data-dismiss="modal" aria-label="Close">
            <span aria-hidden="true">&times;</span>
          </button>
        </div>
        <div class="modal-body">
          <div v-if="!this.submitted" class="row row-cols-1">
            <p>id: <span id="link-id"></span></p>
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
              <label for="link-author"><strong>Author(s)</strong></label>
              <input type="text" class="form-control" id="link-author" placeholder="" value="">
            </div>
            <div class='col my-2'>
              <label class='text-danger'>
                <input id="link-delete" type="checkbox" aria-label="Delete item from database."> <strong>Delete</strong>
              </label>
            </div>
          </div>
          <!-- Response after submission -->
          <h2 class='d-none' id="submission-response"></h2>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
          <button type="button" class="btn btn-primary" @click="submit()">Save</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: "Edit",
  props: [],
  data() {
    return {
      submitted: false
    }
  },
  methods: {
    submit() {
      if (document.getElementById('link-delete').checked) {
        const iD = document.getElementById('link-id').textContent
        axios.delete("https://api.buzo.dog/api/v1/storage/purge?iD=" + iD)
          .then( response => {
            console.log(response.data)
          })
          .catch(error => console.log(error))
      }
      var payload = {
        iD: document.getElementById('link-id').textContent,
        title: document.getElementById('link-title').value,
        source: document.getElementById('link-publication').value,
        description: document.getElementById('link-description').value,
        tags: document.getElementById('link-tags').value,
        author: document.getElementById('link-author').value
      }
      console.log(payload)
      payload = this.toQueryString(payload)
      console.log(payload)

      axios.post(("https://api.buzo.dog/api/v1/storage/update" + payload))
        .then(response => {
          if(response.data.success) {
            console.log("success")
            document.getElementById('submission-response').textContent = 'Changes made successfully!'
            document.getElementById('submission-response').classList.remove('d-none')
          } else {
            console.log("failed")
            document.getElementById('submission-response').textContent = 'Could not make those changes. Try again later.'
            document.getElementById('submission-response').classList.remove('d-none')
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
        if (payload[keys[i]].length > 0) {
          query = query + '&' + keys[i] + '=' + payload[keys[i]]
        }
      }
      query = encodeURI(query)
      return query
    }
  }
}
</script>

<style scoped>
textarea {
  height: 100px;
}
</style>