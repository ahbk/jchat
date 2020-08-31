<template>
	<div class="app">
		<guide></guide>
		<router-view></router-view>
	</div>
</template>
<script>
import Guide from './Guide.vue'

export default {
  components: {
    Guide,
  },
}
</script>
