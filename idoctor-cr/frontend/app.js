const api = {
  listSchedules: async () => (await fetch('/api/schedules')).json(),
  createSchedule: async (payload) => (
    await fetch('/api/schedules', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload) })
  ).json(),
  uploadRecording: async (scheduleId, blob, filename = 'audio.webm') => {
    const form = new FormData();
    form.append('file', blob, filename);
    form.append('media_type', 'audio');
    const res = await fetch(`/api/schedules/${scheduleId}/upload`, { method: 'POST', body: form });
    if (!res.ok) throw new Error('Upload échoué');
    return res.json();
  },
  getTranscription: async (scheduleId) => {
    const res = await fetch(`/api/transcriptions/${scheduleId}`);
    if (!res.ok) throw new Error('Pas encore de transcription');
    return res.json();
  },
  generateReport: async (scheduleId) => {
    const res = await fetch(`/api/schedules/${scheduleId}/generate_report`, { method: 'POST' });
    if (!res.ok) throw new Error('Génération CR échouée');
    return res.json();
  },
  getReport: async (scheduleId) => {
    const res = await fetch(`/api/reports/${scheduleId}`);
    if (!res.ok) throw new Error('CR indisponible');
    return res.json();
  }
};

const $ = (sel, el = document) => el.querySelector(sel);
const $$ = (sel, el = document) => Array.from(el.querySelectorAll(sel));

async function refreshSchedules() {
  const container = $('#schedules');
  container.innerHTML = 'Chargement...';
  const data = await api.listSchedules();
  if (!data.length) {
    container.innerHTML = '<p>Aucun rendez-vous.</p>';
    return;
  }
  container.innerHTML = '';

  data.forEach((s) => {
    const card = document.createElement('div');
    card.className = 'item';
    card.innerHTML = `
      <div class="item-row">
        <div>
          <div class="title">${s.patient_name} <span class="muted">(${s.patient_identifier || 'N/A'})</span></div>
          <div class="subtitle">${new Date(s.scheduled_at).toLocaleString()} — ${s.doctor_name}</div>
          <div class="badge">Statut: ${s.status}</div>
        </div>
        <div class="actions">
          <button class="record" data-id="${s.id}">Enregistrer audio</button>
          <label class="upload">Téléverser<input type="file" class="file" data-id="${s.id}" accept="audio/*,video/*" hidden /></label>
          <button class="transcript" data-id="${s.id}">Transcription</button>
          <button class="gen-report" data-id="${s.id}">Générer CR</button>
          <button class="report" data-id="${s.id}">Voir CR</button>
        </div>
      </div>
      <div class="details" id="details-${s.id}"></div>
    `;
    container.appendChild(card);
  });

  // Bindings
  $$('.record').forEach((btn) => btn.addEventListener('click', () => handleRecord(btn.dataset.id)));
  $$('.file').forEach((input) => input.addEventListener('change', () => handleUploadFile(input)));
  $$('.transcript').forEach((btn) => btn.addEventListener('click', () => showTranscription(btn.dataset.id)));
  $$('.gen-report').forEach((btn) => btn.addEventListener('click', () => generateReport(btn.dataset.id)));
  $$('.report').forEach((btn) => btn.addEventListener('click', () => showReport(btn.dataset.id)));
}

async function handleUploadFile(input) {
  const file = input.files[0];
  if (!file) return;
  const id = input.dataset.id;
  const details = document.getElementById(`details-${id}`);
  details.textContent = 'Téléversement en cours...';
  try {
    await api.uploadRecording(id, file, file.name);
    details.textContent = 'Fichier téléversé. Transcription en cours...';
    setTimeout(() => refreshSchedules(), 800);
  } catch (e) {
    details.textContent = 'Erreur de téléversement';
  } finally {
    input.value = '';
  }
}

async function handleRecord(id) {
  const details = document.getElementById(`details-${id}`);
  if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
    details.textContent = 'Enregistrement non supporté par ce navigateur.';
    return;
  }
  const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
  const recorder = new MediaRecorder(stream);
  const chunks = [];
  recorder.ondataavailable = (e) => chunks.push(e.data);
  recorder.onstop = async () => {
    const blob = new Blob(chunks, { type: 'audio/webm' });
    details.textContent = 'Envoi de l\'audio...';
    try {
      await api.uploadRecording(id, blob);
      details.textContent = 'Audio envoyé. Transcription en cours...';
      setTimeout(() => refreshSchedules(), 800);
    } catch (e) {
      details.textContent = 'Erreur lors de l\'envoi.';
    }
  };

  details.innerHTML = `<div class="rec">Enregistrement en cours... <button id="stop-${id}">Arrêter</button></div>`;
  recorder.start();
  $(`#stop-${id}`).addEventListener('click', () => {
    recorder.stop();
    stream.getTracks().forEach((t) => t.stop());
  });
}

async function showTranscription(id) {
  const details = document.getElementById(`details-${id}`);
  details.textContent = 'Chargement transcription...';
  try {
    const t = await api.getTranscription(id);
    details.innerHTML = `<pre class="pre">${(t.text || '').replace(/[<>&]/g, c => ({'<':'&lt;','>':'&gt;','&':'&amp;'}[c]))}</pre>`;
  } catch (e) {
    details.textContent = 'Transcription indisponible pour le moment.';
  }
}

async function generateReport(id) {
  const details = document.getElementById(`details-${id}`);
  details.textContent = 'Génération du CR...';
  try {
    await api.generateReport(id);
    details.textContent = 'CR en cours de génération...';
    setTimeout(() => showReport(id), 600);
  } catch (e) {
    details.textContent = 'Echec de la génération';
  }
}

async function showReport(id) {
  const details = document.getElementById(`details-${id}`);
  details.textContent = 'Chargement CR...';
  try {
    const r = await api.getReport(id);
    details.innerHTML = `<pre class="pre">${(r.text || '').replace(/[<>&]/g, c => ({'<':'&lt;','>':'&gt;','&':'&amp;'}[c]))}</pre>`;
  } catch (e) {
    details.textContent = 'CR indisponible pour le moment.';
  }
}

function bindCreateForm() {
  const form = document.getElementById('create-form');
  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const fd = new FormData(form);
    const payload = {
      patient_name: fd.get('patient_name'),
      patient_identifier: fd.get('patient_identifier') || null,
      doctor_name: fd.get('doctor_name'),
      scheduled_at: new Date(fd.get('scheduled_at')).toISOString(),
      notes: fd.get('notes') || null,
    };
    await api.createSchedule(payload);
    form.reset();
    refreshSchedules();
  });
}

bindCreateForm();
refreshSchedules();