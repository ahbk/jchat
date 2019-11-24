import { webSocket } from "rxjs/webSocket"
import { Subject, interval } from 'rxjs'
import { filter, map, retryWhen } from 'rxjs/operators'

const beurl = process.env.NODE_ENV === 'development' ?
	'ws://' + window.location.hostname + ':8000' :
	'wss://' + window.location.hostname + ':8443'

var bews$ = webSocket(beurl)
var be$ = bews$.pipe(retryWhen(res => interval(200)))

function queue(task, options) {
	bews$.next({
		fn: task,
		args: options,
	})
}

export { be$, queue }
