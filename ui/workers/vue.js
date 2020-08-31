import {
	Observable,
	from,
	merge,
} from 'rxjs'

import {
	tap,
	filter,
	switchMap,
} from 'rxjs/operators'

import Vue from 'vue'
import VueRouter from 'vue-router'
import Vuex from 'vuex'

import Chat from '../components/Chat.vue'
import Home from '../components/Home.vue'
import App from '../components/App.vue'

Vue.use(VueRouter)
Vue.use(Vuex)

function sortedIndex(messages, message) {
	//let key = message.pk ? 'pk' : 'id'
	let key = 'created'
	var low = 0,
		high = messages.length;

	while (low < high) {
		var mid = (low + high) >>> 1;
		if (messages[mid][key] < message[key]) low = mid + 1;
		else high = mid;
	}
	return low;
}

const store = new Vuex.Store({
	state: {
		feed: {},
	},
	mutations: {
		feedMessage(state, message) {
			if(!Array.isArray(state.feed[message.group])) {
				Vue.set(state.feed, message.group, [])
			}
			let index = sortedIndex(state.feed[message.group], message)
			state.feed[message.group].splice(index, 0, message)
		},
	}
})

const routes = [
	{ name: 'home', path: '/', component: Home },
	{ name: 'chat', path: '/chat/:group', component: Chat, props: true },
]

export default chat => Observable.create(observer => {
	let router = new VueRouter({ mode: 'history', routes })

	let plain$ = chat.replay.pipe(tap(m => store.commit('feedMessage', m)))

	let payload$ = chat.stream.pipe(
		chat.sys(/^vue feed/),
		switchMap(m => from(m.payload)),
		tap(m => store.commit('feedMessage', m)),
	)

	let subs = merge(plain$, payload$).subscribe()

	router.beforeResolve((to, from, next) => {
		observer.next(chat.message('resolved ' + to.name, [], { group: to.params.group }))
		next()
	})

	let vue = new Vue({
		router,
		render: h => h(App),
		mounted: () => observer.next(chat.message('vue is up')),
		store: store,
	})

	vue.$mount('#app')

	return () => {
		subs.unsubscribe()
	}
})
