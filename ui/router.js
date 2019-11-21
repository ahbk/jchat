import Vue from 'vue'
import VueRouter from 'vue-router'
import Chat from './components/Chat.vue'
import Home from './components/Home.vue'

Vue.use(VueRouter);

const routes = [
  { path: '/', component: Home },
  { path: '/chat/:group', component: Chat, props: true },
]

export default new VueRouter({
  mode: 'history',
  routes
})
