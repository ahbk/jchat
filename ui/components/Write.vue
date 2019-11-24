<template>
  <div class="write">
    <form v-on:submit.prevent="send" class="write-form">
      <label for="text" class="write-text-label">Meddelande</label>
      <textarea name="text" class="write-text-input" required></textarea>
      <input type="submit" class="write-text-send" value="Skicka">
    </form>
  </div>
</template>

<script>
import { be$, queue } from '../controller.js'

export default {
  props: ['group'],
  methods: {
    send: function() {
      let textarea = document.getElementsByName('text')[0]
      queue('post', {
				text: textarea.value,
				group: this.group,
				parents: [],
			})
			textarea.value = ''
		},
  },
}
</script>
