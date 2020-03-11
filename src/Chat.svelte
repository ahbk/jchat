<script>
	import { user, userlist, messagelist } from './stores.js'
	import { createEventDispatcher } from 'svelte'
	import moment from 'moment'

	export let receiver = undefined

	const dispatch = createEventDispatcher()
	let text
</script>

<h1>Chat - {$user}</h1>
<h2>Users</h2>
{#if typeof $userlist === 'undefined'}
	<p>Loading users...</p>
{:else}
	<ul>
		{#each $userlist as user}
			<li><a href="/chat/{user.name}">{user.name}</a></li>
		{/each}
	</ul>
{/if}
<h2>Messages</h2>
{#if typeof receiver === 'undefined'}
	<p>Select a user</p>
{:else if !Array.isArray($messagelist)}
	<p>Loading messages...</p>
{:else}
	<ul class="messages">
		{#each $messagelist as message}
      <li class="message">
        <dl>
          <dt class="message-text-label">Text:</dt>
					<dd class="message-text-value">{message.text}</dd>
          <dt class="message-created-label">Created:</dt>
          <dd class="message-created-value">{moment(message.timestamp).format("ddd, hA")}</dd>
          <dt class="message-sign-label">Sign:</dt>
          <dd class="message-sign-value">{message.sender}</dd>
        </dl>
      </li>
		{/each}
	</ul>
  <div class="write">
    <form on:submit|preventDefault={() => dispatch('post', {text, receiver})}>
      <label>Message</label>
			<textarea bind:value={text} required></textarea>
			<br/>
      <input type="submit" value="Post">
    </form>
  </div>
{/if}

<style>
.feed {
  flex: 1 1 auto;
  overflow-y: scroll;
}
.messages {
  font-size: 16px;
  list-style-type: none;
  padding: 0;
  margin: 0;
}

.message {
  padding: .5em 1em;
}

.message>dl {
  display: inline-grid;
  grid-template-columns: 5em auto;
  grid-template-rows: 1.4em auto;
  margin: 0;
}

.message>dl>dt {
  border: 0;
  clip-path: rect(0,0,0,0);
  height: 1px;
  margin: -1px;
  overflow: hidden;
  padding: 0;
  position: absolute;
  width: 1px;
}

.message-text-value {
  background: #f2f7fe;
  grid-column: 2;
  grid-row: 1 / span 2;
  font-size: 1.2em;
  margin: 0;
  padding: .5em 1em;
  border: 3px solid white;
  border-radius: 0px 10px 10px 10px;
}

.message-created-value {
  grid-row: 2;
  grid-column: 1;
  font-size: .8em;
  color: #777777;
  overflow: hidden;
  font-style: italic;
  margin: 0;
}

.message-sign-value {
  grid-row: 1;
  grid-column: 1;
  font-size: .8em;
  color: #777777;
  font-weight: bold;
  overflow: hidden;
  margin: 0;
}
</style>
