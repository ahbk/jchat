import Vue from 'vue'
import VueRouter from 'vue-router'
import Chat from './components/Chat.vue'

Vue.use(VueRouter);

const routes = [
  { path: '/chat/:group', component: Chat, props: true },
]

export default new VueRouter({
  mode: 'history',
  routes
})
