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

import { webSocket } from "rxjs/webSocket"

const url = process.env.NODE_ENV === 'development' ?
	'ws://' + window.location.hostname + ':8000' :
	'wss://' + window.location.hostname + ':8443'

export default chat => Observable.create(observer => {

	let websocket = webSocket({
		url: url,
		openObserver: { next: e => observer.next(chat.message(e.type)) },
		closeObserver: { next: e => observer.next(chat.message(e.type)) },
	})

	let workers$ = chat.replay.pipe(
		chat.sys(/^backend /),
		tap(m => websocket.next(m)),
	)

	let backend$ = websocket.pipe(
		backoff(1000, 50),
		map(chat.patch),
		tap(m => observer.next(m)),
	)

	let subs = merge(workers$, backend$).subscribe()

	return () => {
		subs.unsusbscribe()
	}
})

function backoff(maxTries, ms) {
	return pipe(
		retryWhen(attempts => zip(range(1, maxTries), attempts).pipe(
			map(([i]) => i * i),
			mergeMap(i =>  timer(i * ms))
		))
	)
}
