<template>
  <div class="feed">
    <ol class="messages">
      <li v-for="m in messages" class="message" :id="'message-' + m.id">
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
            <li v-for="mid in m.parents" class="message-parent" :id="'message-parent-' + m.id">
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
import { be$ } from '../controller.js'
import { from, merge } from 'rxjs'
import { filter, map, exhaustMap, tap, delayWhen } from 'rxjs/operators'
const moment = require('moment')

function dateformat(timestamp) {
  return moment(new Date(timestamp)).format('HH:mm')
}

function escapeHtml(unsafe) {
  return unsafe
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}

function urlify(text) {
  var urlRegex = /(https?:\/\/[^\s]+)/g
  return text.replace(urlRegex, function(url) {
    return '<a href="' + url + '" target="_blank">' + url + '</a>'
  })
}

export default {
  props: ['group'],
  data() {
    return {
      messages: [],
    }
  },
  created: function() {
    be$.next({
      fn: 'enter',
      args: {
        group: this.group,
      }
    })
    be$.next({
      fn: 'messages',
      args: {
        group: this.group,
      }
    })

  },
  mounted: function() {
    let db = be$.pipe(
      filter(r => r.fn === 'messages'),
      exhaustMap(r => from(r.result))
    )

    let rt = be$.pipe(
      filter(r => r.type === 'group_receive'),
      map(r => r.message),
    )

    merge(db, rt).pipe(
      tap(m => {
        m.text = urlify(escapeHtml(m.text))
        m.created = dateformat(m.created)
        this.messages.push(m)
        this.messages.sort(function(m1, m2) { return m1.id - m2.id })
      }),
      delayWhen(m => from(this.$nextTick())),
    ).subscribe(message => {
      this.$el.scrollTop = this.$el.scrollHeight
    })
  },
}
</script>
