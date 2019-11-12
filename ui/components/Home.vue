<template>
  <div>
    <router-link to="/start-group">Starta grupp</router-link>
    <ul>
      <li v-for="m in ms">
        <router-link :to="`/${m.group.id}`">Chat</router-link>
        <dl>
          <dt>Sign</dt>
          <dd>
          {{ m.member.sign }}
          </dd>
          <dt>Created</dt>
          <dd>{{ new Date(m.member.created).toLocaleDateString() }}</dd>
          <dt>Group</dt>
          <dd>
          <router-link :to="`/group/${m.group.id}`">{{ m.group.id }}</router-link>
          </dd>
          <dt>Created</dt>
          <dd>{{ new Date(m.group.created).toLocaleDateString() }}</dd>
        </dl>
      </li>
    </ul>
  </div>
</template>
<script>
import Vue from "vue";
import { be$, grouplist$ } from '../controller.js'
import { filter } from 'rxjs/operators'

const data = {
  ms: [],
}

be$.next({ fn: 'memberships' })

be$.pipe(filter(r => r.fn === 'memberships')).subscribe(r => {
  r.result.forEach(m => data.ms.push(m))
})


export default Vue.extend({
  data() {
    return data;
  },
  methods: { },
});
</script>
