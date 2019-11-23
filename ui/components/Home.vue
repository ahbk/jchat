<template>
  <div class="home">
    <h1>Chat</h1>
    <table class="memberships">
      <tr class="memberships-heading">
        <td class="memberships-heading-group">Grupp</td>
        <td class="memberships-heading-name">Namn</td>
        <td class="memberships-heading-notifications">Notis</td>
      </tr>
      <tr v-for="m in memberships" class="membership" :id="'membership-' + m.member.id">
          <td class="membership-cell-group">/{{ m.group.sign }}</td>
          <td class="membership-cell-sign">{{ m.member.sign }}</td>
          <td class="membership-cell-notifications">
            <input type="checkbox" :value="m.member.id" v-model="m.member.notifications" v-on:click="toggle_notifications">
          </td>
        </dl>
      </li>
    </ol>
  </div>
</template>

<script>
import { be$ } from '../controller.js'
import { from, merge } from 'rxjs'
import { filter, map, exhaustMap, tap } from 'rxjs/operators'

export default {
  data() {
    return {
      memberships: [],
    }
  },
  methods: {
    toggle_notifications: function(event) {
      Notification.requestPermission().then(function(result) {
          console.log(result);
      });
      var notification = new Notification("Hi there!");
      console.log(event.target.value)
      console.log(event.target.checked)
    },
  },
  created: function() {
    be$.next({ fn: 'memberships' })
  },
  mounted: function() {
    be$.pipe(
      filter(r => r.fn === 'memberships'),
      exhaustMap(r => from(r.result)),
    ).subscribe(membership => this.memberships.push(membership))
  },
}
</script>
