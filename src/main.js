import App from './App.svelte';
import { webSocket } from 'rxjs/webSocket'
import page from 'page'

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

const ws = webSocket({
	url: `ws://${ window.location.hostname}:8443`,
	openObserver: { next: e => console.log('ws: open') },
	closeObserver: { next: e => console.log('ws: closed') },
})
ws.pipe(tap(console.log), backoff(1000, 50)).subscribe(console.log)


const app = new App({
	target: document.body,
	props: {
		ws,
	}
});

function backoff(maxTries, ms) {
	return pipe(
		retryWhen(attempts => zip(range(1, maxTries), attempts).pipe(
			map(([i]) => i * i),
			tap(i => console.log(`ws: retrying again in ${i * ms} milliseconds`)),
			mergeMap(i => timer(i * ms)),
		))
	)
}
export default app;
