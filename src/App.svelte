<script>
	import Home from './Home.svelte'
	import Chat from './Chat.svelte'

	export let page, ws

	let component
	let user

	page('/', () => component = 'home')
	page('/chat/:user', ctx => user = ctx.params.user)
	page('/chat*', () => component = 'chat')

	page.start()

	function login(e) {
		ws.next({
			req: 'login',
			name: e.detail.name,
			password: e.detail.password,
		})
	}
</script>

{#if component === 'home'}
	<Home on:login={login}/>
{:else}
	<Chat bind:user={user}/>
{/if}
