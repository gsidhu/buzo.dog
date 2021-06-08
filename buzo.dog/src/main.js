import Vue from 'vue'
import App from './App.vue'
import router from './router'
import VueGtag from "vue-gtag";

Vue.config.productionTip = false

Vue.use(VueGtag, {
  config: { id: "G-JQCWSQ7304" },
}, router);

new Vue({
  router,
  render: h => h(App)
}).$mount('#app')
