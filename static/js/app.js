'use strict';

// ── DOM refs ──
const dropZone    = document.getElementById('dropZone');
const fileInput   = document.getElementById('fileInput');
const emptyState  = document.getElementById('emptyState');
const previewState= document.getElementById('previewState');
const previewImg  = document.getElementById('previewImg');
const previewName = document.getElementById('previewName');
const changeBtn   = document.getElementById('changeBtn');
const extractBtn  = document.getElementById('extractBtn');
const btnLabel    = document.getElementById('btnLabel');
const btnLoading  = document.getElementById('btnLoading');
const resultCard  = document.getElementById('resultCard');
const resultText  = document.getElementById('resultText');
const resultMeta  = document.getElementById('resultMeta');
const charChip    = document.getElementById('charChip');
const wordChip    = document.getElementById('wordChip');
const copyBtn     = document.getElementById('copyBtn');
const histBody    = document.getElementById('histBody');
const histBadge   = document.getElementById('histBadge');
const emptyRow    = document.getElementById('emptyRow');
const toast       = document.getElementById('toast');
const modalOverlay= document.getElementById('modalOverlay');
const modalImg    = document.getElementById('modalImg');
const modalTitle  = document.getElementById('modalTitle');
const modalText   = document.getElementById('modalText');
const closeModal  = document.getElementById('closeModal');

let selectedFile  = null;
let historyCache  = [];

// ── Drag & drop ──
['dragenter','dragover'].forEach(evt =>
  dropZone.addEventListener(evt, e => { e.preventDefault(); dropZone.classList.add('drag-over'); }));
['dragleave','drop'].forEach(evt =>
  dropZone.addEventListener(evt, e => { e.preventDefault(); dropZone.classList.remove('drag-over'); }));
dropZone.addEventListener('drop', e => {
  const f = e.dataTransfer.files[0];
  if (f) handleFile(f);
});

// click anywhere on empty zone → open picker
emptyState.addEventListener('click', e => {
  if (!e.target.matches('label, label *')) fileInput.click();
});

fileInput.addEventListener('change', () => {
  if (fileInput.files.length) handleFile(fileInput.files[0]);
});

changeBtn.addEventListener('click', resetDrop);

function handleFile(file) {
  if (!file.type.startsWith('image/')) { showToast('Please select a valid image file', 'error'); return; }
  selectedFile = file;
  const reader = new FileReader();
  reader.onload = e => { previewImg.src = e.target.result; };
  reader.readAsDataURL(file);
  previewName.textContent = file.name;
  emptyState.style.display  = 'none';
  previewState.style.display = 'flex';
  extractBtn.disabled = false;
  resultCard.style.display = 'none';
}

function resetDrop() {
  selectedFile = null;
  fileInput.value = '';
  previewImg.src = '';
  emptyState.style.display   = 'flex';
  previewState.style.display = 'none';
  extractBtn.disabled = true;
}

// ── Extract ──
extractBtn.addEventListener('click', async () => {
  if (!selectedFile) return;
  setLoading(true);

  const fd = new FormData();
  fd.append('file', selectedFile);

  try {
    const res  = await fetch('/upload', { method:'POST', body: fd });
    const data = await res.json();
    if (!res.ok) throw new Error(data.error || 'Upload failed');
    showResult(data.text, data.filename);
    await loadHistory();
    showToast('Text extracted and saved!', 'success');
  } catch(err) {
    showToast(err.message || 'Something went wrong', 'error');
  } finally {
    setLoading(false);
  }
});

function setLoading(on) {
  extractBtn.disabled = on;
  btnLabel.style.display   = on ? 'none' : 'flex';
  btnLoading.style.display = on ? 'flex' : 'none';
}

function showResult(text, filename) {
  const clean = (text || '').trim() || '(No text detected in this image)';
  resultText.textContent = clean;
  const chars = clean.length;
  const words = clean.replace(/\s+/g,' ').trim().split(' ').filter(Boolean).length;
  charChip.textContent = chars + ' characters';
  wordChip.textContent = words + ' words';
  resultMeta.textContent = filename || '';
  resultCard.style.display = 'flex';
  resultCard.scrollIntoView({ behavior:'smooth', block:'nearest' });
}

// ── Copy ──
copyBtn.addEventListener('click', () => {
  const txt = resultText.textContent;
  if (!txt) return;
  navigator.clipboard.writeText(txt).then(() => showToast('Copied to clipboard!', 'info'));
});

// ── History ──
async function loadHistory() {
  try {
    const res = await fetch('/history');
    if (!res.ok) return;
    historyCache = await res.json();
    renderHistory(historyCache);
  } catch(e) { console.error('History error:', e); }
}

function renderHistory(records) {
  histBadge.textContent = records.length + ' record' + (records.length !== 1 ? 's' : '');

  // remove old data rows (keep emptyRow sentinel)
  [...histBody.querySelectorAll('tr.data-row')].forEach(r => r.remove());

  if (!records.length) {
    emptyRow.style.display = '';
    return;
  }
  emptyRow.style.display = 'none';

  records.forEach((rec, i) => {
    const tr = document.createElement('tr');
    tr.className = 'data-row';

    const thumb = document.createElement('td');
    const img   = document.createElement('img');
    img.className = 'thumb';
    img.src   = rec.image_url;
    img.alt   = rec.filename;
    img.onerror = () => { img.style.display='none'; };
    thumb.appendChild(img);

    const nameCell = document.createElement('td');
    nameCell.style.fontSize   = '13px';
    nameCell.style.color      = 'var(--text2)';
    nameCell.textContent      = rec.filename;

    const textCell = document.createElement('td');
    const preview  = document.createElement('div');
    preview.className  = 'text-preview';
    preview.textContent = rec.text || '';
    if (!rec.text) { preview.innerHTML = '<em style="color:var(--text3)">No text detected</em>'; }
    textCell.appendChild(preview);

    const numCell = document.createElement('td');
    numCell.style.color    = 'var(--text3)';
    numCell.style.fontSize = '13px';
    numCell.textContent    = records.length - i;

    const actionCell = document.createElement('td');
    const viewBtn    = document.createElement('button');
    viewBtn.className   = 'view-btn';
    viewBtn.textContent = 'View Full';
    viewBtn.addEventListener('click', () => openModal(rec));
    actionCell.appendChild(viewBtn);

    tr.append(numCell, thumb, nameCell, textCell, actionCell);
    histBody.insertBefore(tr, emptyRow);
  });
}

// ── Modal ──
function openModal(rec) {
  modalTitle.textContent = rec.filename;
  modalImg.src           = rec.image_url;
  modalText.textContent  = rec.text || '(No text detected)';
  modalOverlay.classList.add('open');
}
closeModal.addEventListener('click', () => modalOverlay.classList.remove('open'));
modalOverlay.addEventListener('click', e => { if (e.target === modalOverlay) modalOverlay.classList.remove('open'); });

// ── Toast ──
let toastTimer;
function showToast(msg, type = 'info') {
  toast.textContent = msg;
  toast.className   = 'toast ' + type;
  clearTimeout(toastTimer);
  requestAnimationFrame(() => toast.classList.add('show'));
  toastTimer = setTimeout(() => toast.classList.remove('show'), 3400);
}

// ── Init ──
loadHistory();
