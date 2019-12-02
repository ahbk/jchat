import Vue from 'vue'
import Write from '../../components/Write.vue'
import events from '../../controller/events.js'

import { 
	fromEvent,
} from 'rxjs'

import { 
	tap,
	map,
	filter,
	mergeMap,
} from 'rxjs/operators'

describe('sum', function () {

	it('should be hello!', function () {
		chai.expect(Write.data().text).to.equal('hello!')
	});

	it('expect Write to broadcast itself on ua', (done) => {
		const detail_ = {
			text: 'hello',
			group: 'asdf',
			parents: [],
		}

		events.created('write').pipe(
			mergeMap(d => fromEvent(d.element, 'post')),
			map(event => event.detail),
			tap(console.log),
		).subscribe((detail) => {
			chai.expect(detail).to.eql(detail_)
			done()
		})

		const C = Vue.extend(Write)
		const vm = new C({ propsData: { group: detail_.group } }).$mount()
		vm.write(detail_.text)
		vm.send()
	})

	describe('#indexOf()', function() {
		it('should return -1 when the value is not present', function() {
			chai.assert([1, 2, 3].indexOf(4) === -0, 'sup')
		})
	})
})

