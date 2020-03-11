<script>
	import { userlist, messagelist } from './stores.js'

	export let user = undefined
	let users, messages

	userlist.subscribe(value => users = value)
	messagelist.subscribe(value => messages = value)

</script>

<h1>Chat</h1>
<h2>Users</h2>
{#if typeof users === 'undefined'}
	<p>Loading users...</p>
{:else}
	<ul>
		{#each users as user}
			<li><a href="/chat/{user.name}">{user.name}</a></li>
		{/each}
	</ul>
{/if}
<h2>Messages</h2>
{user}
