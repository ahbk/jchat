import App from './App.svelte';
import page from 'page';

import { user, userlist, messagelist } from './stores.js';
import { get } from 'svelte/store';

import { filter } from 'rxjs/operators';

import ws from './ws.js';

// Unauthenticated requests on websocket should trigger a redirect to /
ws.pipe(filter(m => !m.auth)).subscribe(m => page('/'));

// A request on /chat implies a request for userlist
page('/chat', function(context, next) {
  ws.next({ req: 'users' });
  next();
});

// Handle responses to login requests
ws.pipe(filter(m => m.req === 'login')).subscribe(function(message) {
  if (message.res) {
    page('/chat');
    user.set(message.name);
  } else {
    page('/');
  }
});

// Handle responses to userlist requests
ws.pipe(filter(m => m.req === 'users')).subscribe(m => userlist.set(m.res));

// Handle responses to messagelist requests
ws.pipe(filter(m => m.req === 'messages')).subscribe(m =>
  messagelist.set(m.res)
);

// Handle responses to message posts
ws.pipe(filter(m => m.req === 'post')).subscribe(m =>
  messagelist.set([...get(messagelist), m.res])
);

const app = new App({ target: document.body, props: { page, ws } });
export default app;
