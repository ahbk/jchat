import { webSocket } from "rxjs/webSocket"
import { Subject } from 'rxjs'
import { filter, map } from 'rxjs/operators'

const beurl = process.env.NODE_ENV === 'development' ?
  'ws://' + window.location.hostname + ':8000' :
  'wss://' + window.location.hostname + ':8443'

const be$ = webSocket(beurl)

export { be$ }
