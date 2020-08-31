import {
	Observable,
} from 'rxjs'
import { 
	filter,
	map,
	tap,
} from 'rxjs/operators'

import { setCookie } from 'tiny-cookie'

export default chat => Observable.create(observer => {
	let req = chat.message('backend session')

	let res = chat.stream.pipe(
		chat.res(req),
		tap(setSession),
	).subscribe()

	observer.next(req)

	function setSession(message) {
		setCookie('sessionid', message.payload.id, { expires: '1Y' })
		observer.next(chat.message('session is now ' + message.payload.id))
		res.unsubscribe()
	}

	return () => {
		res.unsusbscribe()
	}
})
