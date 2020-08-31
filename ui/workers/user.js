import {
	Observable,
	fromEvent,
	merge,
	from,
} from 'rxjs'

import { 
	map,
	tap,
	switchMap,
	filter,
	last,
} from 'rxjs/operators'


function posts(observer, chat) {
	return fromEvent(document, 'writeCreated').pipe(
		switchMap(event => fromEvent(event.detail, 'post')),
		map(event => event.detail),
		tap(message => {
			if(message.group === chat.group) {
				message = chat.patch(message)
			} else {
				message = chat.message('backend post', [], message)
			}
			observer.next(message)
		}),
	)
}

function more(observer, chat) {
	return fromEvent(document, 'feedCreated').pipe(
		switchMap(event => fromEvent(event.detail, 'more')),
		map(event => event.detail),
		tap(m => observer.next(chat.message('more', [], m))),
	)
}

function messages(observer, chat) {
	return chat.stream.pipe(
		chat.res(chat.message('backend messages')),
		switchMap(m => from(m.payload)),
		tap(m => observer.next(m)),
	)
}

export default chat => Observable.create(observer => {
	let work = [posts, more, messages].map(fn => fn(observer, chat).subscribe())

	chat.replay.pipe(
		chat.sys(/^resolved chat$/),
		tap(m => observer.next(chat.message('backend messages', [m], m.payload))),
	).subscribe()

	return () => {
		work.map(sub => sub.unsubscribe())
	}
})
