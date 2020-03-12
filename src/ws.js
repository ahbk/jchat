import { webSocket } from 'rxjs/webSocket';
import { pipe, range, zip, timer } from 'rxjs';
import { map, tap, retryWhen, mergeMap, filter } from 'rxjs/operators';

// Set up websocket
const protocol = window.location.hostname === 'seval.io' ? 'wss' : 'ws';

const ws = webSocket({
  url: `${protocol}://${window.location.hostname}:8443`,
  openObserver: { next: e => console.log('ws: open') },
  closeObserver: { next: e => console.log('ws: closed') },
});

ws.pipe(backoff(1000, 50)).subscribe(console.log);

function backoff(maxTries, ms) {
  return pipe(
    retryWhen(attempts =>
      zip(range(1, maxTries), attempts).pipe(
        map(([i]) => i * i),
        tap(i => console.log(`ws: retrying again in ${i * ms} milliseconds`)),
        mergeMap(i => timer(i * ms))
      )
    )
  );
}

export default ws;
