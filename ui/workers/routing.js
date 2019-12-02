import Vue from 'vue'
import Vuex from 'vuex'
import VueRouter from 'vue-router'
import { Observable } from 'rxjs'

import Chat from '../components/Chat.vue'
import Home from '../components/Home.vue'
import App from '../components/App.vue'

export default function(chat$) {
	Vue.use(Vuex)
	Vue.use(VueRouter)

	const store = new Vuex.Store({
		state: {
			feed: {}
		},
		mutations: {
			feedMessage (state, message) {
				if(!Array.isArray(state.feed[message.group])) {
					Vue.set(state.feed, message.group, [])
				}
				state.feed[message.group].push(message)
			}
		}
	})

	chat$.subscribe(message => {
		store.commit('feedMessage', message)
	})

	const routes = [
		{ name: 'home', path: '/', component: Home },
		{ name: 'chat', path: '/chat/:group', component: Chat, props: true },
	]

	const router = new VueRouter({
		mode: 'history',
		routes
	})

	return Observable.create(function(observer) {
		router.beforeResolve((to, from , next) => {
			let message = {
				group: 'chat',
				sign: 'routing',
				text: 'resolved ' + to.name,
			}
			observer.next(message)
			next()
		})

		let mounted = function() {
			let message = {
				group: 'chat',
				sign: 'routing',
				text: 'document ready',
			}
			observer.next(message)
		}

		const vm = new Vue({ router, render: h => h(App), mounted, store })
		vm.$mount('#app')

		return () => vm.$destroy()
	})
}
