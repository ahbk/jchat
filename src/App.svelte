<script>
	import page from 'page'
	import Home from './Home.svelte'
	import Chat from './Chat.svelte'

	export let ws
	let component

	page('/', () => component = Home)
	page('/chat', () => component = Chat)

	page.start()
</script>

<svelte:component this={component} ws={ws} />
