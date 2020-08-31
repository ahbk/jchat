import { concat, from } from 'rxjs'
import { filter, tap } from 'rxjs/operators'

export default (record, stream) => group => sign => {
	const replay = concat(from(record), stream)
	const sys = regex => filter(m => m.group === group && regex.test(m.text))
	const res = message => filter(m => isResponse(m, message))

	function message(text, parents, payload) {
		return { group, sign, text, parents, payload }
	}

	function parents(message, filter) {
		var parents = message.parents || []
		if(message.pk) {
			parents = parents.map(pk => record.filter(m => m.pk === pk)[0])
		} else {
			parents = parents.map(id => record[id])
		}
		return filter ? parents.filter(filter) : parents
	}

	function patch(message) {
		message.group = message.group || group
		message.sign = message.sign || sign
		return message
	}

	function isEqual(messageA, messageB) {
		return ['group', 'sign', 'text'].every(p => messageA[p] === messageB[p])
	}

	function isResponse(message, to) {
		let result = parents(parent => isEqual(parent, to)).length > 0
		return result
	}

	return { group, sign, stream, replay, patch, message, sys, res }
}
