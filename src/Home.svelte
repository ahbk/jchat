<script>
	import { createEventDispatcher } from 'svelte'
	const dispatch = createEventDispatcher()

	let name
	let password
</script>

<main>
	<div class="login">

		<h1>Login</h1>

		<form on:submit|preventDefault={() => dispatch('login', {name, password})}>
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
