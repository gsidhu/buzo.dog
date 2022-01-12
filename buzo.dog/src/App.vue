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
  metaInfo: {
    title: 'buzo.xyz',
    titleTemplate: '%s | buzo.xyz',
    htmlAttrs: {
      lang: 'en-UK'
    },
    meta: [
      { charset: 'utf-8' },
      { name: 'description', content: 'A personal archive.' },
      { name: 'viewport', content: 'width=device-width, initial-scale=1' },
      { name: 'og:url', content: 'https://buzo.xyz' },
      { name: 'og:type', content: 'website' },
      { name: 'og:title', content: 'buzo.xyz' },
      { name: 'og:description', content: 'A personal archive.' },
      { name: 'twitter:description', content: 'A personal archive.' }
    ]
  },
  created() {
    // let googleanalytics = document.createElement('script')
    // googleanalytics.async = true
    // googleanalytics.setAttribute('src', 'https://www.googletagmanager.com/gtag/js?id=G-JQCWSQ7304')
    // document.head.appendChild(googleanalytics)
    // let analytics = document.createElement('script')
    // analytics.text = "window.dataLayer = window.dataLayer || [];function gtag(){dataLayer.push(arguments);}gtag('js', new Date());gtag('config', 'G-JQCWSQ7304');"
    // document.head.appendChild(analytics)

    let goatcounter = document.createElement('script')
    goatcounter.async = true
    goatcounter.setAttribute('src', '//gc.zgo.at/count.js')
    goatcounter.setAttribute('data-goatcounter', 'https://buzo.goatcounter.com/count')
    document.head.appendChild(goatcounter)

       
    // <meta property="og:description" content="I work with data in the social sector quite often. In this article, I am going to share a framework that I use myself to plan data-related projects.">
    // <meta name="twitter:description" content="I work with data in the social sector quite often. In this article, I am going to share a framework that I use myself to plan data-related projects.">
    // <meta property="og:url" content="https://thatgurjot.com">
    // <meta property="og:type" content="website">
    // <meta property="og:title" content="Framework for a Robust Data Pipeline | That Gurjot">
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
