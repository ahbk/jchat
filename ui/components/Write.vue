<template>
  <div class="write">
    <form v-on:submit.prevent="send" class="write-form" method="post">
      <label for="text" class="write-text-label">Meddelande</label>
      <textarea ref="write" name="text" v-model="text" class="write-text-input" required></textarea>
			<input type="hidden" name="group" :value="group">
      <input type="submit" class="write-text-send" value="Skicka">
    </form>
  </div>
</template>

<script>

export default {
  props: ['group'],
	data: function() {
		return {
			text: '',
			parents: [],
		}
	},
  methods: {
    send: function() {
			let message = {
				text: this.text,
				group: this.group,
				parents: this.parents,
			} 
			let event = new CustomEvent('post', { detail: message })
			this.$el.dispatchEvent(event)
		},
  },
	mounted: function() {
		let event = new CustomEvent( 'writeCreated', { detail: this.$el })
		document.dispatchEvent(event)
	},
}
</script>
