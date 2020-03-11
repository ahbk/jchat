import { webSocket } from 'rxjs/webSocket'
import page from 'page'
import App from './App.svelte'
import { setCookie } from 'tiny-cookie'
import { user, userlist, messagelist } from './stores.js'
import { get } from 'svelte/store';


import {
	pipe,
	merge,
	range,
	zip,
	timer,
	Observable,
} from 'rxjs'

import { 
	map,
	tap,
	retryWhen,
	mergeMap,
	filter,
} from 'rxjs/operators'


const ws = webSocket({
	url: `ws://${ window.location.hostname}:8443`,
	openObserver: { next: e => console.log('ws: open') },
	closeObserver: { next: e => console.log('ws: closed') },
})

ws.pipe(
	filter(m => m.req === 'login' && m.res),
).subscribe(receiveLogin)

function receiveLogin(message) {
	if(message.res) {
		page('/chat')
		user.set(message.name)
	} else {
		page('/')
	}
}

function requestLogin(e) {
	ws.next({req: 'login', name, password})
}

ws.pipe(
	// tap(m => setCookie('sessionid', m.res.sid, { expires: '1Y' })),
	backoff(1000, 50)
).subscribe(console.log)

ws.pipe(
	filter(m => !m.auth),
).subscribe(m => page('/'))

ws.pipe(
	filter(m => m.req === 'users'),
).subscribe(m => userlist.set(m.res))

ws.pipe(
	filter(m => m.req === 'messages'),
).subscribe(m => messagelist.set(m.res))

ws.pipe(
	filter(m => m.req === 'post'),
).subscribe(m => messagelist.set([...get(messagelist), m.res]))

function backoff(maxTries, ms) {
	return pipe(
		retryWhen(attempts => zip(range(1, maxTries), attempts).pipe(
			map(([i]) => i * i),
			tap(i => console.log(`ws: retrying again in ${i * ms} milliseconds`)),
			mergeMap(i => timer(i * ms)),
		))
	)
}

page('/chat', users)

function users(context, next) {
	ws.next({ req: 'users' })
	next()
}

const app = new App({
	target: document.body,
	props: { page, ws }
});

export default app;
