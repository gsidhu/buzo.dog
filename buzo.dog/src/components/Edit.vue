<template>
  <div class="modal" tabindex="-1">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">Be careful, sonny</h5>
          <button type="button" class="close" data-dismiss="modal" aria-label="Close">
            <span aria-hidden="true">&times;</span>
          </button>
        </div>
        <div class="modal-body">
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
              <label class='text-danger'>
                <input id="link-delete" type="checkbox" aria-label="Delete item from database."> <strong>Delete</strong>
              </label>
            </div>
          </div>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
          <button type="button" class="btn btn-primary">Save</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "Edit",
  props: ["links"],
  data() {
    return {
    }
  }
}
</script>

<style scoped>
textarea {
  height: 100px;
}
</style>