import {
	Observable,
} from 'rxjs'
import { 
	filter,
	map,
	tap,
} from 'rxjs/operators'

import { setCookie } from 'tiny-cookie'

export default function(chat$) {
	function setSession(sessionid) {
		setCookie('sessionid', sessionid, { expires: '1Y' })
	}

	return Observable.create(observer => {
		chat$.pipe(
			filter(message => message.sign === 'backend' && message.group === 'chat' && message.text === 'open'),
		).subscribe(message => observer.next({
			group: 'chat',
			sign: 'session',
			text: 'establish session',
			parents: [ message ],
		}))

		let session_regex = /^session is (\S+)$/
		chat$.pipe(
		  filter(message => message.group === 'chat' && message.sign === 'backend' && session_regex.test(message.text)),
			tap(message => setSession(session_regex.exec(message.text)[1])),
		).subscribe(message => observer.next({
			group: 'chat',
			sign: 'session',
			text: 'ok',
			parents: [ message ],
		}))
	})
}
