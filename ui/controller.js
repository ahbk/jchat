import { webSocket } from "rxjs/webSocket"
import { Subject } from 'rxjs'
import { filter, map } from 'rxjs/operators'

const be$ = webSocket("ws://chat.lxc:8000/chat/")

export { be$ }
