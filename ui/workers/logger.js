import { EMPTY } from 'rxjs'
export default function(chat$) {
	chat$.subscribe(console.log)
	return EMPTY
}
