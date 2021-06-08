<template>
  <div id="app">
    <Header />
    <Navigation />
    <router-view :key="$route.fullPath"></router-view>
    <Footer />
  </div>
</template>

<script>
import Header from './layout/Header';
import Navigation from './layout/Navigation';
import Footer from './layout/Footer';

import 'bootstrap/dist/css/bootstrap.min.css'
import 'jquery/src/jquery.js'
import 'bootstrap/dist/js/bootstrap.min.js'

export default {
  name: 'App',
  components: {
    Header,
    Navigation,
    Footer
  },
  created() {
    // let googleanalytics = document.createElement('script')
    // googleanalytics.async = true
    // googleanalytics.setAttribute('src', 'https://www.googletagmanager.com/gtag/js?id=G-JQCWSQ7304')
    // document.head.appendChild(googleanalytics)
    // let analytics = document.createElement('script')
    // analytics.text = "window.dataLayer = window.dataLayer || [];function gtag(){dataLayer.push(arguments);}gtag('js', new Date());gtag('config', 'G-JQCWSQ7304');"
    // document.head.appendChild(analytics)
  }
}
</script>
<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 20px;
}
</style>
