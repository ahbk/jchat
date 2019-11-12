<template>
  <div>
    Starta grupp
    {{ message }}
    <form v-on:submit.prevent="startgroup">
      <label for="name">Vad vill du heta i gruppen?</label>
      <input type="text" name="name" minlength="2" maxlength="16" size="22" />
      <input type="submit" value="Starta grupp">
    </form>
  </div>
</template>

<script>
import Vue from "vue";
import { be$, newgroup$ } from '../controller.js'

const data = { message: 'asdf' }

export default Vue.extend({
  data() { return data },
  methods: {
    startgroup: function() {
      be$.next({
        fn: 'startgroup',
        args: {
          sign: document.getElementsByName('name')[0].value
        }
      });
    },
  },
});
</script>

<style scoped>
</style>
