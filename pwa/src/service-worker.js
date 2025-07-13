import { build, files, version } from '$service-worker';
import { precacheAndRoute } from 'workbox-precaching';
import { registerRoute } from 'workbox-routing';
import { StaleWhileRevalidate } from 'workbox-strategies';
import PouchDB from 'pouchdb-browser';

// Precache all static assets
precacheAndRoute(build);

// Use a StaleWhileRevalidate strategy for all other requests.
registerRoute(
  ({ request }) => true,
  new StaleWhileRevalidate({
    // Put all cached files in a cache named 'pages'
    cacheName: 'pages',
  })
);

const localDB = new PouchDB('pos-db');
const remoteDB = new PouchDB('http://localhost:5984/pos-db');

localDB.sync(remoteDB, {
  live: true,
  retry: true
}).on('change', function (info) {
  console.log('Sync change:', info);
}).on('paused', function (err) {
  console.log('Sync paused:', err);
}).on('active', function () {
  console.log('Sync active');
}).on('denied', function (err) {
  console.log('Sync denied:', err);
}).on('complete', function (info) {
  console.log('Sync complete:', info);
}).on('error', function (err) {
  console.log('Sync error:', err);
});
