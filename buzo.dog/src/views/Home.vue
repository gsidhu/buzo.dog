<template>
    <article>
        <section>
            <div class='container'>
                <div class='card-deck my-5'>
                    <div class='card' id='fetch'>
                        <a id='fetch-link' rel="nofollow" target="_blank" v-on:click="fetchAgain()">
                            <div class='card-body'>
                                <svg aria-hidden="true" focusable="false" data-prefix="fas" data-icon="random" class="svg-inline--fa fa-random fa-w-16" role="img" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">
                                    <path fill="currentColor" d="M504.971 359.029c9.373 9.373 9.373 24.569 0 33.941l-80 79.984c-15.01 15.01-40.971 4.49-40.971-16.971V416h-58.785a12.004 12.004 0 0 1-8.773-3.812l-70.556-75.596 53.333-57.143L352 336h32v-39.981c0-21.438 25.943-31.998 40.971-16.971l80 79.981zM12 176h84l52.781 56.551 53.333-57.143-70.556-75.596A11.999 11.999 0 0 0 122.785 96H12c-6.627 0-12 5.373-12 12v56c0 6.627 5.373 12 12 12zm372 0v39.984c0 21.46 25.961 31.98 40.971 16.971l80-79.984c9.373-9.373 9.373-24.569 0-33.941l-80-79.981C409.943 24.021 384 34.582 384 56.019V96h-58.785a12.004 12.004 0 0 0-8.773 3.812L96 336H12c-6.627 0-12 5.373-12 12v56c0 6.627 5.373 12 12 12h110.785c3.326 0 6.503-1.381 8.773-3.812L352 176h32z"></path>
                                </svg>
                                <h3>Fetch</h3>
                            </div>
                        </a>
                    </div>
                    <div class='card' id='walk'>
                        <router-link to="/scroll">
                        <div class='card-body' @click="walk = !walk">
                            <svg aria-hidden="true" focusable="false" data-prefix="fas" data-icon="stream" class="svg-inline--fa fa-stream fa-w-16" role="img" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">
                                <path fill="currentColor" d="M16 128h416c8.84 0 16-7.16 16-16V48c0-8.84-7.16-16-16-16H16C7.16 32 0 39.16 0 48v64c0 8.84 7.16 16 16 16zm480 80H80c-8.84 0-16 7.16-16 16v64c0 8.84 7.16 16 16 16h416c8.84 0 16-7.16 16-16v-64c0-8.84-7.16-16-16-16zm-64 176H16c-8.84 0-16 7.16-16 16v64c0 8.84 7.16 16 16 16h416c8.84 0 16-7.16 16-16v-64c0-8.84-7.16-16-16-16z"></path>
                            </svg>
                            <h3>Walk</h3>
                        </div>
                        </router-link>
                    </div>
                </div>
            </div>
        </section>
        <!-- <section id="scroll-area">
            <Scroll v-if="walk" />
        </section> -->
    </article>
</template>

<script>
import axios from 'axios';
// axios.defaults.headers.common['header1'] = 'buzo.dog'

export default {
    name: "Home",
    data() {
        return {
            bone: [],
            walk: false
        }
    },
    components: {
    },
//    beforeCreate() {
//       axios.get('https://api.buzo.dog/api/v1/resources/links?count=1')
//         .then( response => this.bone = response.data)
//         .catch( err => console.log(err));
//   },
  created() {
      axios.get('https://api.buzo.dog/api/v1/resources/links?count=1')
        .then( response => {
            this.bone = response.data
            const el = document.getElementById('fetch-link')
            el.href = this.bone[0].link
            el.title = this.bone[0].title
        })
        .catch( err => console.log(err));
  },
  methods: {
    fetchAgain() {
      axios.get('https://api.buzo.dog/api/v1/resources/links?count=1')
        .then( response => this.bone = response.data)
        .catch( err => console.log(err));
    }
  }
}
</script>
<style scoped>
.card {
    margin-bottom: 2rem;
    cursor: pointer;
}
.card:hover {
    background-color: #f7f5f5;
}
svg {
    width: 10%;
}
a, a:hover,
a:visited {
    color: inherit;
    text-decoration: none;
}
h3 {
    margin-bottom: 0;
}
</style>