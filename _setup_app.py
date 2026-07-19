"""
Generator script — writes all source files for the OCR Flask web application.
Run once with:  python _setup_app.py
"""
import pathlib

ROOT = pathlib.Path(__file__).parent

# ── ensure directories exist ──────────────────────────────────────────────────
for d in ["templates", "static/css", "static/js", "uploads",
          "service", "controller"]:
    (ROOT / d).mkdir(parents=True, exist_ok=True)

for pkg in ["service", "controller"]:
    init = ROOT / pkg / "__init__.py"
    if not init.exists():
        init.write_text("# package\n", encoding="utf-8")

# ── index.html ────────────────────────────────────────────────────────────────
HTML = """\
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>OCR Vision – AI Text Extractor</title>
  <meta name="description" content="Extract text from images with AI-powered OCR technology. Upload any image and get accurate text instantly.">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
</head>
<body>

  <div class="bg-canvas">
    <div class="orb orb-1"></div>
    <div class="orb orb-2"></div>
    <div class="orb orb-3"></div>
  </div>

  <header>
    <div class="header-inner">
      <div class="logo">
        <svg width="38" height="38" viewBox="0 0 38 38" fill="none">
          <rect width="38" height="38" rx="11" fill="url(#lg)"/>
          <path d="M10 13h18M10 19h13M10 25h16" stroke="white" stroke-width="2.6" stroke-linecap="round"/>
          <defs>
            <linearGradient id="lg" x1="0" y1="0" x2="38" y2="38" gradientUnits="userSpaceOnUse">
              <stop stop-color="#6366f1"/><stop offset="1" stop-color="#8b5cf6"/>
            </linearGradient>
          </defs>
        </svg>
        <span>OCR Vision</span>
      </div>
      <p class="tagline">AI-powered text extraction from images</p>
    </div>
  </header>

  <main>
    <div class="top-grid">

      <!-- ── Upload Card ── -->
      <div class="glass-card upload-card">
        <div class="card-head">
          <div>
            <h1>Upload Image</h1>
            <p class="sub">Drag & drop or browse to extract text using EasyOCR</p>
          </div>
        </div>

        <div class="drop-zone" id="dropZone">
          <!-- empty state -->
          <div class="dz-empty" id="emptyState">
            <div class="dz-icon">
              <svg width="54" height="54" viewBox="0 0 24 24" fill="none"
                stroke="currentColor" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round">
                <rect x="3" y="3" width="18" height="18" rx="3"/>
                <circle cx="8.5" cy="8.5" r="1.5"/>
                <path d="m21 15-5-5L5 21"/>
              </svg>
            </div>
            <p class="dz-title">Drag & drop your image here</p>
            <span class="dz-or">or</span>
            <label class="browse-btn" for="fileInput">
              <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor"
                stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
                <polyline points="17 8 12 3 7 8"/>
                <line x1="12" y1="3" x2="12" y2="15"/>
              </svg>
              Browse Image
            </label>
            <input type="file" id="fileInput" accept="image/*" hidden>
            <p class="dz-fmt">Supports: JPG &middot; PNG &middot; BMP &middot; TIFF &middot; WebP</p>
          </div>

          <!-- preview state -->
          <div class="dz-preview" id="previewState" style="display:none">
            <img id="previewImg" src="" alt="Preview">
            <div class="preview-footer">
              <span id="previewName" class="prev-name"></span>
              <button id="changeBtn" class="change-btn">Change</button>
            </div>
          </div>
        </div>

        <button class="extract-btn" id="extractBtn" disabled>
          <span id="btnLabel">
            <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor"
              stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
              <circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/>
            </svg>
            Extract Text
          </span>
          <span id="btnLoading" style="display:none">
            <svg class="spin-icon" width="17" height="17" viewBox="0 0 24 24" fill="none"
              stroke="currentColor" stroke-width="2.5">
              <circle cx="12" cy="12" r="10" stroke-opacity="0.25"/>
              <path d="M12 2a10 10 0 0 1 10 10" stroke-linecap="round"/>
            </svg>
            Extracting...
          </span>
        </button>
      </div>

      <!-- ── Result Card ── -->
      <div class="glass-card result-card" id="resultCard" style="display:none">
        <div class="card-head">
          <div>
            <h2>Extracted Text</h2>
            <p class="sub" id="resultMeta">—</p>
          </div>
          <button class="icon-btn" id="copyBtn" title="Copy to clipboard">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor"
              stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <rect x="9" y="9" width="13" height="13" rx="2"/>
              <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/>
            </svg>
            Copy
          </button>
        </div>
        <div class="result-body">
          <div class="result-text" id="resultText"></div>
        </div>
        <div class="result-chips">
          <span class="chip" id="charChip"></span>
          <span class="chip" id="wordChip"></span>
        </div>
      </div>

    </div><!-- /top-grid -->

    <!-- ── History Card ── -->
    <div class="glass-card history-card">
      <div class="card-head">
        <div>
          <h2>Processing History</h2>
          <p class="sub">All images processed and their extracted text</p>
        </div>
        <span class="badge" id="histBadge">0 records</span>
      </div>
      <div class="table-wrap">
        <table class="htable" id="histTable">
          <thead>
            <tr>
              <th style="width:46px">#</th>
              <th style="width:72px">Thumb</th>
              <th style="width:180px">File Name</th>
              <th>Extracted Text</th>
              <th style="width:94px">Action</th>
            </tr>
          </thead>
          <tbody id="histBody">
            <tr id="emptyRow">
              <td colspan="5">
                <div class="empty-hist">
                  <svg width="46" height="46" viewBox="0 0 24 24" fill="none" stroke="currentColor"
                    stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                    <polyline points="14 2 14 8 20 8"/>
                    <line x1="16" y1="13" x2="8" y2="13"/>
                    <line x1="16" y1="17" x2="8" y2="17"/>
                  </svg>
                  <p>No images processed yet. Upload one to get started!</p>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

  </main>

  <div class="toast" id="toast"></div>

  <!-- Full-text modal -->
  <div class="modal-overlay" id="modalOverlay">
    <div class="modal">
      <div class="modal-head">
        <h3 id="modalTitle">Full Extracted Text</h3>
        <button class="close-btn" id="closeModal">&times;</button>
      </div>
      <img id="modalImg" class="modal-img" src="" alt="">
      <pre class="modal-text" id="modalText"></pre>
    </div>
  </div>

  <script src="{{ url_for('static', filename='js/app.js') }}"></script>
</body>
</html>
"""

# ── style.css ─────────────────────────────────────────────────────────────────
CSS = """\
:root {
  --bg:        #06060f;
  --surface:   rgba(255,255,255,0.04);
  --surface-h: rgba(255,255,255,0.07);
  --border:    rgba(255,255,255,0.07);
  --border-a:  rgba(99,102,241,0.45);
  --text:      #f1f5f9;
  --text2:     #94a3b8;
  --text3:     #64748b;
  --accent:    #6366f1;
  --accent2:   #8b5cf6;
  --success:   #10b981;
  --error:     #ef4444;
  --grad:      linear-gradient(135deg,#6366f1,#8b5cf6);
  --shadow:    0 24px 64px -12px rgba(0,0,0,.7);
  --r:         18px;
  --r-sm:      10px;
  --trans:     all .3s cubic-bezier(.4,0,.2,1);
}
*, *::before, *::after { box-sizing:border-box; margin:0; padding:0; }
html { scroll-behavior:smooth; }
body { font-family:'Inter',system-ui,sans-serif; background:var(--bg); color:var(--text); min-height:100vh; overflow-x:hidden; }

/* ── Orbs ── */
.bg-canvas { position:fixed; inset:0; pointer-events:none; z-index:0; overflow:hidden; }
.orb { position:absolute; border-radius:50%; filter:blur(110px); opacity:.11; animation:drift 22s ease-in-out infinite alternate; }
.orb-1 { width:620px;height:620px;background:#6366f1;top:-180px;left:-140px;animation-delay:0s; }
.orb-2 { width:520px;height:520px;background:#8b5cf6;bottom:-160px;right:-100px;animation-delay:-8s; }
.orb-3 { width:360px;height:360px;background:#06b6d4;top:42%;left:50%;animation-delay:-15s; }
@keyframes drift { from{transform:translate(0,0) scale(1)} to{transform:translate(28px,18px) scale(1.06)} }

/* ── Header ── */
header {
  position:relative;z-index:10;
  padding:24px 40px;
  border-bottom:1px solid var(--border);
  backdrop-filter:blur(20px);
  background:rgba(6,6,15,.65);
}
.header-inner { max-width:1200px;margin:0 auto;display:flex;align-items:center;justify-content:space-between; }
.logo { display:flex;align-items:center;gap:12px;font-size:21px;font-weight:800;letter-spacing:-.5px; }
.tagline { font-size:13px;color:var(--text2); }

/* ── Main ── */
main { position:relative;z-index:10;max-width:1200px;margin:0 auto;padding:36px 40px;display:flex;flex-direction:column;gap:28px; }
.top-grid { display:grid;grid-template-columns:1fr 1fr;gap:22px; }

/* ── Glass Card ── */
.glass-card {
  background:var(--surface);
  border:1px solid var(--border);
  border-radius:var(--r);
  backdrop-filter:blur(24px);
  padding:30px;
  box-shadow:var(--shadow);
  transition:border-color .3s;
}
.glass-card:hover { border-color:rgba(99,102,241,.13); }

.card-head { display:flex;align-items:flex-start;justify-content:space-between;margin-bottom:22px; }
.card-head h1 { font-size:20px;font-weight:700;letter-spacing:-.3px; }
.card-head h2 { font-size:18px;font-weight:700;letter-spacing:-.3px; }
.sub { font-size:13px;color:var(--text2);margin-top:4px; }

/* ── Drop Zone ── */
.drop-zone {
  border:2px dashed var(--border);
  border-radius:14px;
  min-height:210px;
  display:flex;align-items:center;justify-content:center;
  transition:var(--trans);cursor:pointer;overflow:hidden;margin-bottom:18px;
}
.drop-zone.drag-over { border-color:var(--accent);background:rgba(99,102,241,.07);transform:scale(1.01); }

.dz-empty { display:flex;flex-direction:column;align-items:center;gap:10px;padding:30px;text-align:center;width:100%; }
.dz-icon { color:var(--text3);margin-bottom:4px; }
.dz-title { font-size:15px;font-weight:500;color:var(--text2); }
.dz-or { font-size:13px;color:var(--text3); }
.dz-fmt { font-size:12px;color:var(--text3);margin-top:4px; }

/* ── Browse Button ── */
.browse-btn {
  display:inline-flex;align-items:center;gap:8px;
  padding:10px 22px;border-radius:var(--r-sm);cursor:pointer;
  font-size:14px;font-weight:600;letter-spacing:.2px;
  background:var(--grad);color:#fff;
  transition:var(--trans);box-shadow:0 4px 20px rgba(99,102,241,.35);
}
.browse-btn:hover { opacity:.9;transform:translateY(-2px);box-shadow:0 8px 28px rgba(99,102,241,.45); }

/* ── Preview ── */
.dz-preview { display:flex;flex-direction:column;align-items:center;gap:12px;padding:16px;width:100%; }
.dz-preview img { max-height:165px;max-width:100%;border-radius:10px;object-fit:contain;box-shadow:0 8px 28px rgba(0,0,0,.45); }
.preview-footer { display:flex;align-items:center;gap:12px; }
.prev-name { font-size:13px;color:var(--text2);max-width:180px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap; }
.change-btn { font-size:12px;color:var(--accent);background:none;border:1px solid var(--accent);border-radius:6px;padding:4px 10px;cursor:pointer;transition:var(--trans); }
.change-btn:hover { background:rgba(99,102,241,.15); }

/* ── Extract Button ── */
.extract-btn {
  width:100%;padding:14px;border-radius:12px;border:none;cursor:pointer;
  background:var(--grad);color:#fff;font-size:15px;font-weight:600;letter-spacing:.2px;
  display:flex;align-items:center;justify-content:center;gap:8px;
  transition:var(--trans);box-shadow:0 4px 24px rgba(99,102,241,.28);
}
.extract-btn:disabled { opacity:.35;cursor:not-allowed;box-shadow:none; }
.extract-btn:not(:disabled):hover { transform:translateY(-2px);box-shadow:0 8px 32px rgba(99,102,241,.45); }
.extract-btn:not(:disabled):active { transform:translateY(0); }
#btnLabel,#btnLoading { display:flex;align-items:center;gap:8px; }
.spin-icon { animation:spin .75s linear infinite; }
@keyframes spin { to{transform:rotate(360deg)} }

/* ── Result Card ── */
.result-card { display:flex;flex-direction:column; }
.result-body { background:rgba(0,0,0,.22);border-radius:10px;padding:18px;flex:1;margin-bottom:14px; }
.result-text { font-size:14px;line-height:1.8;color:var(--text2);white-space:pre-wrap;word-break:break-word;max-height:230px;overflow-y:auto; }
.result-text::-webkit-scrollbar { width:4px; }
.result-text::-webkit-scrollbar-thumb { background:var(--border-a);border-radius:4px; }
.result-chips { display:flex;gap:8px;flex-wrap:wrap; }
.chip { display:inline-block;padding:4px 12px;border-radius:20px;font-size:12px;font-weight:500;background:rgba(99,102,241,.12);color:var(--accent);border:1px solid rgba(99,102,241,.2); }

/* ── Icon Button ── */
.icon-btn { display:inline-flex;align-items:center;gap:6px;padding:8px 14px;border-radius:8px;border:1px solid var(--border);background:var(--surface-h);color:var(--text2);font-size:13px;cursor:pointer;transition:var(--trans); }
.icon-btn:hover { border-color:var(--accent);color:var(--accent); }

/* ── History ── */
.badge { padding:4px 12px;border-radius:20px;font-size:13px;font-weight:500;background:rgba(99,102,241,.1);color:var(--accent);border:1px solid rgba(99,102,241,.2);white-space:nowrap; }
.table-wrap { overflow-x:auto; }
.htable { width:100%;border-collapse:collapse;font-size:14px; }
.htable th { padding:11px 14px;text-align:left;font-size:11px;font-weight:600;text-transform:uppercase;letter-spacing:.8px;color:var(--text3);border-bottom:1px solid var(--border); }
.htable td { padding:13px 14px;vertical-align:middle;border-bottom:1px solid rgba(255,255,255,.03); }
.htable tr:last-child td { border-bottom:none; }
.htable tbody tr { transition:background .2s; }
.htable tbody tr:hover { background:var(--surface-h); }
.thumb { width:52px;height:52px;border-radius:8px;object-fit:cover;border:1px solid var(--border);display:block; }
.text-preview { color:var(--text2);overflow:hidden;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;line-height:1.55;max-width:340px; }
.view-btn { padding:6px 14px;border-radius:8px;font-size:12px;font-weight:500;cursor:pointer;background:rgba(99,102,241,.1);color:var(--accent);border:1px solid rgba(99,102,241,.2);transition:var(--trans);white-space:nowrap; }
.view-btn:hover { background:rgba(99,102,241,.22); }
.empty-hist { display:flex;flex-direction:column;align-items:center;gap:12px;padding:52px;color:var(--text3);font-size:14px; }

/* ── Toast ── */
.toast { position:fixed;bottom:28px;left:50%;transform:translateX(-50%) translateY(16px);padding:12px 24px;border-radius:12px;font-size:14px;font-weight:500;opacity:0;pointer-events:none;z-index:2000;transition:all .35s;backdrop-filter:blur(20px);box-shadow:0 8px 32px rgba(0,0,0,.4); }
.toast.show { opacity:1;transform:translateX(-50%) translateY(0); }
.toast.success { background:rgba(16,185,129,.15);border:1px solid rgba(16,185,129,.3);color:#10b981; }
.toast.error   { background:rgba(239,68,68,.15); border:1px solid rgba(239,68,68,.3); color:#ef4444; }
.toast.info    { background:rgba(99,102,241,.15);border:1px solid rgba(99,102,241,.3);color:#818cf8; }

/* ── Modal ── */
.modal-overlay { position:fixed;inset:0;background:rgba(0,0,0,.72);z-index:1000;display:flex;align-items:center;justify-content:center;backdrop-filter:blur(8px);opacity:0;pointer-events:none;transition:opacity .3s; }
.modal-overlay.open { opacity:1;pointer-events:all; }
.modal { background:#0d0d1c;border:1px solid var(--border);border-radius:var(--r);max-width:640px;width:92%;max-height:82vh;overflow-y:auto;padding:28px;box-shadow:var(--shadow);transform:scale(.94);transition:transform .3s; }
.modal-overlay.open .modal { transform:scale(1); }
.modal-head { display:flex;align-items:center;justify-content:space-between;margin-bottom:18px; }
.modal-head h3 { font-size:17px;font-weight:700;word-break:break-all; }
.close-btn { background:none;border:none;color:var(--text2);cursor:pointer;font-size:24px;line-height:1;padding:0 4px;transition:color .2s; }
.close-btn:hover { color:var(--text); }
.modal-img { width:100%;max-height:300px;object-fit:contain;border-radius:10px;margin-bottom:16px;border:1px solid var(--border); }
.modal-text { font-size:14px;line-height:1.8;color:var(--text2);white-space:pre-wrap;word-break:break-word;font-family:'Inter',system-ui,sans-serif; }

/* ── Responsive ── */
@media (max-width:800px) {
  header { padding:18px 20px; }
  .header-inner { flex-direction:column;gap:6px;text-align:center; }
  main { padding:20px; gap:20px; }
  .top-grid { grid-template-columns:1fr; }
}
"""

# ── app.js ────────────────────────────────────────────────────────────────────
JS = """\
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
  const words = clean.replace(/\\s+/g,' ').trim().split(' ').filter(Boolean).length;
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
"""

# ── service/ocr_service.py ────────────────────────────────────────────────────
OCR_SERVICE = """\
\"\"\"EasyOCR wrapper — lazily initialises the reader on first call.\"\"\"
import easyocr

_reader = None


def _get_reader() -> easyocr.Reader:
    global _reader
    if _reader is None:
        # gpu=False keeps things portable; set True if CUDA is available
        _reader = easyocr.Reader(['en'], gpu=False)
    return _reader


def extract_text_from_image(image_path: str) -> str:
    \"\"\"
    Run EasyOCR on *image_path* and return the extracted text as a single string.
    Individual detected paragraphs are joined by newlines.
    \"\"\"
    reader  = _get_reader()
    results = reader.readtext(image_path, detail=0, paragraph=True)
    return '\\n'.join(results)
"""

# ── controller/image_controller.py ───────────────────────────────────────────
CONTROLLER = """\
\"\"\"Image upload controller: saves file, persists to DB, runs OCR.\"\"\"
import os
from flask import current_app
from werkzeug.utils import secure_filename

from extensions import db
from model.image_model import Image
from model.text_to_image_model import TextToImage
from service.ocr_service import extract_text_from_image

ALLOWED_EXT = {'png', 'jpg', 'jpeg', 'bmp', 'tiff', 'tif', 'webp', 'gif'}
UPLOAD_FOLDER = 'uploads'


def allowed_file(filename: str) -> bool:
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXT


def process_image(file) -> dict:
    \"\"\"
    1. Save uploaded file to disk.
    2. Insert an Image record (stores the URL/path).
    3. Run EasyOCR and insert a TextToImage record.
    Returns a dict with image metadata and extracted text.
    \"\"\"
    filename   = secure_filename(file.filename)
    upload_dir = os.path.join(current_app.root_path, UPLOAD_FOLDER)
    os.makedirs(upload_dir, exist_ok=True)

    filepath = os.path.join(upload_dir, filename)
    file.save(filepath)

    # ── persist image record ──
    image_url    = f'/uploads/{filename}'
    image_record = Image(image_url=image_url)
    db.session.add(image_record)
    db.session.flush()          # get auto-generated id before FK insert

    # ── extract text ──
    extracted_text = extract_text_from_image(filepath)

    # ── persist text record ──
    text_record = TextToImage(image_id=image_record.id, text=extracted_text)
    db.session.add(text_record)
    db.session.commit()

    return {
        'image_id':  image_record.id,
        'image_url': image_url,
        'filename':  filename,
        'text':      extracted_text,
    }


def get_all_records() -> list:
    \"\"\"Return all text-to-image records joined with their image data, newest first.\"\"\"
    rows = (
        db.session.query(TextToImage, Image)
        .join(Image, TextToImage.image_id == Image.id)
        .order_by(TextToImage.id.desc())
        .all()
    )
    return [
        {
            'id':        tti.id,
            'image_id':  img.id,
            'image_url': img.image_url,
            'filename':  img.image_url.rsplit('/', 1)[-1],
            'text':      tti.text,
        }
        for tti, img in rows
    ]
"""

# ── route/main_routes.py ──────────────────────────────────────────────────────
ROUTES = """\
from flask import Blueprint, render_template, request, jsonify, send_from_directory, current_app
import os

from controller.image_controller import process_image, allowed_file, get_all_records

bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    return render_template('index.html')


@bp.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in request'}), 400
    file = request.files['file']
    if not file or file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    if not allowed_file(file.filename):
        return jsonify({'error': 'Unsupported file type. Use JPG, PNG, BMP, TIFF, or WebP.'}), 415
    try:
        result = process_image(file)
        return jsonify(result), 200
    except Exception as exc:
        current_app.logger.exception('Image processing failed')
        return jsonify({'error': str(exc)}), 500


@bp.route('/history')
def history():
    return jsonify(get_all_records())


@bp.route('/uploads/<path:filename>')
def serve_upload(filename):
    upload_dir = os.path.join(current_app.root_path, 'uploads')
    return send_from_directory(upload_dir, filename)
"""

# ── app.py ────────────────────────────────────────────────────────────────────
APP = """\
import os
from flask import Flask
from dotenv import load_dotenv

from extensions import db, migrate
from config import config

load_dotenv()


def create_app(config_name: str = None) -> Flask:
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')

    app = Flask(__name__)
    app.config.from_object(config.get(config_name, config['default']))

    db.init_app(app)
    migrate.init_app(app, db)

    # Import models so Flask-Migrate / Alembic detects them
    from model import image_model, text_to_image_model  # noqa: F401

    from route.main_routes import bp
    app.register_blueprint(bp)

    return app


if __name__ == '__main__':
    application = create_app()
    application.run(debug=True)
"""

# ── config.py (uses quote_plus to handle special chars in password) ───────────
CONFIG = """\
import os
from urllib.parse import quote_plus
from dotenv import load_dotenv

load_dotenv()


def _db_url() -> str:
    user     = os.getenv('DB_USER',     'root')
    password = quote_plus(os.getenv('DB_PASSWORD', ''))
    host     = os.getenv('DB_HOST',     'localhost')
    port     = os.getenv('DB_PORT',     '3306')
    name     = os.getenv('DB_NAME',     'object_detection_db')
    return f'mysql+pymysql://{user}:{password}@{host}:{port}/{name}'


class Config:
    SECRET_KEY                  = os.getenv('SECRET_KEY', 'change-me')
    SQLALCHEMY_DATABASE_URI     = _db_url()
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAX_CONTENT_LENGTH          = 16 * 1024 * 1024   # 16 MB upload limit


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False


config = {
    'development': DevelopmentConfig,
    'production':  ProductionConfig,
    'default':     DevelopmentConfig,
}
"""

# ── write all files ───────────────────────────────────────────────────────────
files = {
    'templates/index.html':              HTML,
    'static/css/style.css':              CSS,
    'static/js/app.js':                  JS,
    'service/ocr_service.py':            OCR_SERVICE,
    'controller/image_controller.py':    CONTROLLER,
    'route/main_routes.py':              ROUTES,
    'app.py':                            APP,
    'config.py':                         CONFIG,
}

for rel, content in files.items():
    path = ROOT / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding='utf-8')
    print(f'  OK {rel}')

print('\nAll application files written successfully!')

