<template>
  <div class="feed">
    <ol class="messages">
      <li v-for="m in feed" class="message" :id="'message-' + m.id">
        <dl>
          <dt class="message-text-label">Text:</dt>
          <dd class="message-text-value" v-html="m.text"></dd>
          <dt class="message-created-label">Created:</dt>
          <dd class="message-created-value">{{ m.created }}</dd>
          <dt class="message-sign-label">Sign:</dt>
          <dd class="message-sign-value">{{ m.sign }}</dd>
          <dt class="message-parents-label">Parents:</dt>
          <dd class="message-parents-value">
          <ul>
            <li v-for="mid in m.parents" class="message-parent" :id="'message-parent-' + mid">
              <router-link :to="`/${group}/${mid}`">{{ mid }}</router-link>
            </li>
          </ul>
          </dd>
        </dl>
      </li>
    </ol>
  </div>
</template>

<script>

export default {
  props: ['group'],
	computed: {
		feed() {
			return this.$store.state.feed[this.group]
		},
	},
	methods: {
		more() {
			let event = new CustomEvent('more', { detail: this.group })
			this.$el.dispatchEvent(event)
		},
	},
	mounted: function() {
		let event = new CustomEvent('feedCreated', { detail: this.$el })
		document.dispatchEvent(event)
	},
	activated: function() {
		let event = new CustomEvent('active', { detail: this.group })
		this.$el.dispatchEvent(event)
	},
	deactivated: function() {
		let event = new CustomEvent('idle', { group: this.group })
		this.$el.dispatchEvent(event)
	},
}
</script>
