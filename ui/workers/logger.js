import {
	Observable,
	from,
} from 'rxjs'

import {
	filter,
	switchMap,
	tap,
} from 'rxjs/operators'

const logger = console.log

export default chat => Observable.create(observer => {

	let subs = chat.replay.subscribe(logger)
	observer.next(chat.message('hello'))

	return () => {
		subs.unsubscribe()
	}
})
