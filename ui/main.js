import { Subject, merge } from 'rxjs'

import backend from './workers/backend.js'
import logger from './workers/logger.js'
import session from './workers/session.js'
import user from './workers/user.js'
import vue from './workers/vue.js'
import ctx from './workers/_ctx.js'

const messages$ = new Subject()
const messages = []
const workergroup = 'workerslounge'

const wl = ctx(messages, messages$.asObservable())(workergroup)

const main = merge(
	logger(wl('logger')),
	backend(wl('backend')),
	session(wl('session')),
	user(wl('user')),
	vue(wl('vue')),
).subscribe(relay)

function relay(message) {
	message.id = messages.length
	message.created = message.created || Date.now()

	messages.push(message)
	messages$.next(message)

	return message
}
