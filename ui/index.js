import { be$ } from './controller.js'
import { getCookie, setCookie } from 'tiny-cookie'
import { filter } from 'rxjs/operators'
import Vue from 'vue'
import router from './router.js'
import App from './App.vue'

new Vue({ router, render: h => h(App) }).$mount('#app');

// Create or resume session
be$.next({ fn: 'session' });

be$.pipe(
    filter(r => r.fn === 'session'),
).subscribe(r => setCookie('sessionid', r.result.sessionid))
