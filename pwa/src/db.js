import Dexie from 'dexie';
import PouchDB from 'pouchdb-browser';

// Create a new PouchDB database
const pouch = new PouchDB('pos-db');

// Create a Dexie wrapper for the PouchDB instance
const db = new Dexie('PouchDB-pos-db');

// Define the database schema
db.version(1).stores({
  products: '++_id, sku, name',
  sales: '++_id, createdAt',
  stockEntries: '++_id, productId, createdAt',
  users: '++_id, name',
});

// Sync Dexie with PouchDB
db.open().then(() => {
  db.products.clear();
  db.sales.clear();
  db.stockEntries.clear();
  db.users.clear();

  pouch.allDocs({ include_docs: true }).then(result => {
    const docs = result.rows.map(row => row.doc);
    docs.forEach(doc => {
      const table = doc._id.split(':')[0] + 's';
      if (db[table]) {
        db[table].put(doc);
      }
    });
  });
});


// PouchDB sync with remote server
const remoteDB = new PouchDB('http://localhost:5984/pos-db');
pouch.sync(remoteDB, {
  live: true,
  retry: true
}).on('change', (info) => {
  console.log('Sync change:', info);
  // Update Dexie with changes from PouchDB
  info.change.docs.forEach(doc => {
    const table = doc._id.split(':')[0] + 's';
    if (db[table]) {
      if (doc._deleted) {
        db[table].delete(doc._id);
      } else {
        db[table].put(doc);
      }
    }
  });
}).on('error', (err) => {
  console.error('Sync error:', err);
});

export default db;
