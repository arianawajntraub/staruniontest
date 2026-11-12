// EXTRACTOR SEGURO DE WHATSAPP WEB BUSINESS (SOLO LECTURA DE INDEXEDDB 'model-storage' + SCROLL DE HISTORIAL)
// Cuenta: 4 - STAR UNION S.R.L. (+54 9 11 2275-9369)
(async () => {
  console.log("🟢 Iniciando extracción segura de WhatsApp Web Business (Star Union)...");
  const pane = document.querySelector('#pane-side');
  if (pane) {
    for (let i = 0; i < 15; i++) {
      pane.scrollTop = pane.scrollHeight;
      await new Promise(r => setTimeout(r, 350));
    }
  }
  const openDB = (name) => new Promise((res, rej) => {
    const req = indexedDB.open(name);
    req.onsuccess = () => res(req.result);
    req.onerror = () => rej(req.error);
  });
  const readStore = (db, storeName) => new Promise((res) => {
    if (!db.objectStoreNames.contains(storeName)) return res([]);
    const tx = db.transaction(storeName, 'readonly');
    const req = tx.objectStore(storeName).getAll();
    req.onsuccess = () => res(req.result || []);
    req.onerror = () => res([]);
  });
  const db = await openDB('model-storage');
  const chats = await readStore(db, 'chat');
  const msgs = await readStore(db, 'message');
  const contacts = await readStore(db, 'contact');
  const labels = await readStore(db, 'label');
  const labelAssocs = await readStore(db, 'label-association');

  const contactMap = {};
  for (const c of contacts) {
    contactMap[c.id] = { name: c.name || c.pushname || c.verifiedName || '', shortName: c.shortName || '', isBusiness: !!c.isBusiness };
  }
  const cleanMsgs = msgs
    .filter(m => m && (m.body || m.caption || m.type))
    .map(m => ({
      id: m.id,
      chatId: m.id ? String(m.id).split('_')[1] : (m.from || m.to || ''),
      t: m.t ? new Date(m.t * 1000).toISOString() : null,
      fromMe: !!(m.id && String(m.id).startsWith('true_')),
      type: m.type || 'chat',
      body: m.body || m.caption || ''
    }));
  const payload = {
    extractedAt: new Date().toISOString(),
    account: "4 - STAR UNION S.R.L.",
    totals: { chats: chats.length, messages: cleanMsgs.length, contacts: contacts.length, labels: labels.length },
    labels,
    labelAssocs,
    chats: chats.map(c => ({
      id: c.id,
      name: c.name || (contactMap[c.id] && contactMap[c.id].name) || '',
      unreadCount: c.unreadCount || 0,
      t: c.t ? new Date(c.t * 1000).toISOString() : null
    })),
    messages: cleanMsgs
  };
  const blob = new Blob([JSON.stringify(payload, null, 2)], { type: 'application/json' });
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = 'STAR_UNION_WHATSAPP_COMPLETO.json';
  document.body.appendChild(a);
  a.click();
  a.remove();
  console.log("✅ Listo: se descargó STAR_UNION_WHATSAPP_COMPLETO.json con", chats.length, "chats y", cleanMsgs.length, "mensajes.");
})();
