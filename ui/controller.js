import { webSocket } from "rxjs/webSocket"
import { Subject } from 'rxjs'
import { filter, map } from 'rxjs/operators'

const be$ = webSocket('wss://' + window.location.hostname + ':443/wss/')

export { be$ }
