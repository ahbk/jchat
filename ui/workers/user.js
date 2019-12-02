import {
	Observable,
	fromEvent
} from 'rxjs'

import { 
	map,
	tap,
	switchMap,
	filter,
} from 'rxjs/operators'

export default function(chat$) {
	return Observable.create(observer => {

		// When an instance of Write is created, start nexting its posts.
		let subs = chat$.pipe(
			switchMap(_ => fromEvent(document, 'writeCreated')),
			switchMap(event => fromEvent(event.detail, 'post')),
			map(event => event.detail),
			tap(message => observer.next(message)),
		).subscribe()

		// Emit messages that should be posted (but isn't)
		let posts$ = chat$.pipe(
			filter(message => message.group !== 'chat' && !message.id),
		)

		// Reply to unposted posts with "post"
		subs.add(posts$.subscribe(message => observer.next({
			group: 'chat',
			sign: 'user',
			text: 'post',
			parents: [ message ],
		})))

		return () => {
			subs.unsubscribe()
		}
	})
}
