<script>
	import { filter } from 'rxjs/operators'
	import page from 'page'


	export let ws;
	let name, password;

	ws.pipe(
		filter(m => m.req === 'login' && m.res),
	).subscribe(receiveLogin)

	function receiveLogin(message) {
		if(message.res) {
			page('/chat')
		} else {
			page('/')
		}
	}

	function requestLogin(e) {
		ws.next({req: 'login', name, password})
	}
</script>

<main>
	<div class="login">

		<h1>Login</h1>

		<form on:submit|preventDefault={requestLogin}>
			<label>Username</label>
			<input name="name" bind:value={name} required/>

			<label>Password</label>
			<input type="password" bind:value={password} required/>

			<br/>

			<button type="submit">Login</button>
		</form>

	</div>

</main>

<style>
	main {
		text-align: center;
		padding: 1em;
		max-width: 240px;
		margin: 0 auto;
	}

	h1 {
		font-size: 2em;
		font-weight: 100;
	}

	@media (min-width: 640px) {
		main {
			max-width: none;
		}
	}
</style>
