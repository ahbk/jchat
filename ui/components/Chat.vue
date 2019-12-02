<template>
  <div class="chat">
    <feed :group="group"></feed>
    <write :group="group"></write>
  </div>
</template>

<script>
import Feed from './Feed.vue'
import Write from './Write.vue'

export default {
  props: ['group'],
  components: {
    Feed, Write
  },
}
</script>
