import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from './components/Home.vue'
import Group from './components/Group.vue'
import Chat from './components/Chat.vue'
import StartGroup from './components/StartGroup.vue'


Vue.use(VueRouter);

const routes = [
  { path: '/', component: Home },
  { path: '/start-group', component: StartGroup },
  { path: '/group/:group', component: Group },
  { path: '/:group', component: Chat },
]

export default new VueRouter({
  mode: 'history',
  routes
})
