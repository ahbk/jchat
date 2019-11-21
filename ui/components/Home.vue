<template>
  <div class="home">
    <h1>Chat</h1>
    <ol class="memberships">
      <li v-for="g in groups" class="membership" :id="'membership-' + g.id">
        <dl>
          <dt class="membership-group-label">Group:</dt>
          <dd class="membership-group-value">{{ g.sign }}</dd>
          <dt class="membership-sign-label">Sign:</dt>
          <dd class="membership-sign-value">{{ g.you.sign }}</dd>
        </dl>
      </li>
    </ol>
  </div>
</template>

<script>
import { be$ } from '../controller.js'
import { from, merge } from 'rxjs'
import { filter, map, exhaustMap, tap, delayWhen } from 'rxjs/operators'

export default {
  data() {
    return {
      groups: [],
    }
  },
  created: function() {
    be$.next({ fn: 'session' })
  },
  mounted: function() {
    be$.pipe(
      filter(r => r.fn === 'session'),
      map(r => r.result.memberships),
      delayWhen(s => from(this.$nextTick())),
    ).subscribe(s => {
      for (var group of Object.keys(s)) {
        this.groups.push({
          id: s[group].id,
          sign: group,
          you: {
            sign: s[group].sign,
          }
        })
      }
    })
  },
}
</script>
