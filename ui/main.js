import { Subject, merge } from 'rxjs'

import backend from './workers/backend.js'
import user from './workers/user.js'
import logger from './workers/logger.js'
import session from './workers/session.js'
import routing from './workers/routing.js'

const chat$ = new Subject()

const main = merge(
	backend(chat$),
	user(chat$),
	logger(chat$),
	session(chat$),
	routing(chat$),
).subscribe(message => chat$.next(message))
