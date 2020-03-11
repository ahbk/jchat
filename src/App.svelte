<script>
	import Home from './Home.svelte'
	import Chat from './Chat.svelte'

	export let page, ws

	let component
	let receiver

	page('/', () => component = 'home')
	page('/chat/:receiver', selectReceiver)
	page('/chat*', () => component = 'chat')

	page.start()

	function selectReceiver(context, next) {
		receiver = context.params.receiver
		ws.next({
			req: 'messages',
			receiver
		})
		next()
	}

	function login(e) {
		ws.next({
			req: 'login',
			name: e.detail.name,
			password: e.detail.password,
		})
	}

	function post(e) {
		ws.next({
			req: 'post',
			text: e.detail.text,
			receiver: e.detail.receiver,
		})
	}
</script>

{#if component === 'home'}
	<Home on:login={login} />
{:else}
	<Chat bind:receiver={receiver} on:post={post} />
{/if}
