<template>
    <div class='col-sm mx-auto my-4'>
        <h3 id='title'>Source: {{title}}</h3>
        
        <!-- Card view -->
        <div v-if="card" id='card-view' class='row row-cols-1 row-cols-md-2 row-cols-lg-3'>
            <div v-bind:key="index" v-for="(link, index) in links" class="col links-div my-2">
                <Item v-bind:link="link" v-bind:index="index" type='card' @call="populateModal" />
            </div>
        </div>

        <!-- List view -->
        <div v-else id='link-view'>
            <ol>
                <li v-bind:key="index" v-for="(link, index) in links" class="card-header my-1">
                    <Item v-bind:link="link" v-bind:index="index" type='list' @call="populateModal" />
                </li>
            </ol>
        </div>

        <!-- Edit modal -->
        <Edit id="edit-modal" />
    </div>
</template>

<script>
import Item from './Item'; 
import Edit from '@/components/Edit'
// eslint-disable-line no-unused-vars
export default {
    name: "Links",
    components: {
        Item,
        Edit
    },
    data() {
      return {
      };
    },
    props: ["links", "title", "card"],
    methods: {
        populateModal(e) {
            document.getElementById('link-id').textContent = this.links[e]._id
            document.getElementById('link-title').value = this.links[e].title
            document.getElementById('link-publication').value = this.links[e].source
            document.getElementById('link-description').value = this.links[e].description
            document.getElementById('link-tags').value = this.links[e].tags
            document.getElementById('link-author').value = this.links[e].author
        }

    }
}
</script>

<style scoped>
#link-view {
    text-align:left;
}
ol {
  padding-left: 1em;
}
</style>