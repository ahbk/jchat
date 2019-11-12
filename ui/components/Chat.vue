<template>
  <div>
    <ul>
      <li v-for="m in messages">
        <dl>
          <dt>Message:</dt>
          <dd>{{ m.text }}</dd>
          <dt>Posted:</dt>
          <dd>{{ new Date(m.created).toLocaleDateString() }}</dd>
          <dt>Sign:</dt>
          <dd>{{ m.sign }}</dd>
          <dt>Parents:</dt>
          <dd>
            <ul>
              <li v-for="message in m.parents">
                <router-link :to="`/${group}/${message.id}`">{{ message.id }}</router-link>
              </li>
            </ul>
          </dd>
        </dl>
      </li>
    </ul>

    <form v-on:submit.prevent="send">
      <label for="text">Meddelande</label>
      <textarea name="text" required></textarea>
      <input type="submit" value="Skicka">
    </form>
  </div>
</template>
<script>
import Vue from "vue";
import { be$, grouplist$ } from '../controller.js'
import { filter } from 'rxjs/operators'

export default Vue.extend({
  data() {
    return {
      group: this.$route.params.group,
      messages: [],
    };
  },
  methods: {
    send: function() {
      be$.next({
        fn: 'post',
        args: {
          text: document.getElementsByName('text')[0].value,
          group: this.$data.group,
          parents: [],
        }
      });
    },
  },
  mounted: function() {
    be$.pipe(filter(r => r.fn === 'messages')).subscribe(r => {
      r.result.forEach(m => {
        console.log(m)
        this.$data.messages.push(m)
      })
    })

    be$.next({ fn: 'messages', 'args': {group: this.$data.group}})
  },
});
</script>

