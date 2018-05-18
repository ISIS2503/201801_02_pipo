// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import BootstrapVue from 'bootstrap-vue'
import VueMaterial from 'vue-material'
import VueScrollTo from 'vue-scrollto'

import '../node_modules/bootstrap/dist/css/bootstrap.css'
import '../node_modules/bootstrap-vue/dist/bootstrap-vue.css'
import 'vue-material/dist/vue-material.min.css'


import App from './App'
import router from './router'

Vue.config.productionTip = false
Vue.config.devtools = true
Vue.use(BootstrapVue)
Vue.use(VueMaterial)
Vue.use(VueScrollTo)


/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  render: h => h(App),
  template: '<App/>'
})
