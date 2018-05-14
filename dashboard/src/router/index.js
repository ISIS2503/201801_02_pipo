import Vue from 'vue'
import Router from 'vue-router'
import Dashboard from '@/components/Dashboard/Dashboard'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/dashboard/:username',
      name: 'Dashboard',
      component: Dashboard
    }
  ]
})
