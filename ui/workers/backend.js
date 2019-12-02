import {
	pipe,
	fromEvent,
	from,
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
	ignoreElements,
} from 'rxjs/operators'

import { webSocket } from "rxjs/webSocket"

export default function(chat$) {
	return Observable.create(observer => {

		// Absorb errors and resubscribe with expontentially increasing interval
		function backoff(maxTries, ms) {
			return pipe(
				retryWhen(attempts => zip(range(1, maxTries), attempts).pipe(
					map(([i]) => i * i),
					mergeMap(i =>  timer(i * ms))
				))
			)
		}

		// Next the status of the connection based on event type
		function status(event) {
			observer.next({
				group: 'chat',
				sign: 'backend',
				text: event.type, // Can be "open" or "close"
			})
		}
	
		let url = process.env.NODE_ENV === 'development' ?
			'ws://' + window.location.hostname + ':8000' :
			'wss://' + window.location.hostname + ':8443'

		// The websocket instance
		let websocket = webSocket({
			url: url,
			openObserver: { next: status },
			closeObserver: { next: status },
		})

		// Emits responses from backend (backoff absorbs errors)
		let receive$ = websocket.pipe(backoff(1000, 50))

		// Next all group messages as is
		let subs = receive$.pipe(
			filter(response => response.type === 'group_receive'),
			map(response => response.message),
		).subscribe(message => observer.next(message))

		// Next sessions should they appear
		subs.add(
			receive$.pipe(
				filter(response => response.fn === 'session'),
			).subscribe(response => observer.next({
				group: 'chat',
				sign: 'backend',
				text: 'session is ' + response.result.id,
			}))
		)

		// Post parents of posts
		subs.add(
			chat$.pipe(
				filter(message => message.group === 'chat' && message.text === 'post'),
				mergeMap(message => from(message.parents)),
			).subscribe(message => websocket.next({ fn: 'post', args: message }))
		)

		// Request session
		subs.add(
			chat$.pipe(
				filter(message => message.group === 'chat' && message.sign === 'session' && message.text === 'establish session'),
			).subscribe(message => websocket.next({ fn: 'session' }))
		)

		return () => {
			subs.unsusbscribe()
		}
	})
}
