/* eslint-disable no-undef */

import { precacheAndRoute } from 'workbox-precaching';
import { registerRoute } from 'workbox-routing';
import { StaleWhileRevalidate, NetworkFirst } from 'workbox-strategies';
import PouchDB from 'pouchdb-browser';

// Precache all assets defined in the Workbox manifest
precacheAndRoute(self.__WB_MANIFEST);

// Cache pages with a Stale-While-Revalidate strategy
registerRoute(
  ({ request }) => request.mode === 'navigate',
  new StaleWhileRevalidate({
    cacheName: 'pages',
  })
);

// Cache API calls with a Network-First strategy to ensure fresh data
registerRoute(
  ({ url }) => url.pathname.startsWith('/api/'),
  new NetworkFirst({
    cacheName: 'api-cache',
    plugins: [
      new workbox.expiration.ExpirationPlugin({
        maxEntries: 50,
        maxAgeSeconds: 5 * 60, // 5 minutes
      }),
    ],
  })
);


// --- PouchDB Sync ---

const localDB = new PouchDB('pos-db');
const remoteDB = new PouchDB('http://localhost:5984/pos-db');

self.addEventListener('online', () => {
  console.log('Online, starting sync...');
  localDB.sync(remoteDB, {
    live: true,
    retry: true
  }).on('change', function (info) {
    console.log('Sync change:', info);
    self.registration.showNotification('Data Synced', {
      body: 'Your local data has been synced with the server.'
    });
  }).on('error', function (err) {
    console.error('Sync error:', err);
  });
});

console.log('Custom Service Worker loaded.');
