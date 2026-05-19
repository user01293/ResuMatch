/* ── ResuMatch v2 Frontend ──────────────────────────────────────── */

let allResults   = [];
let selectedFile = null;
let embeddingTier = '';

const CATEGORY_ICONS = {
  'Engineering':       { icon: '⚙️',  bg: 'rgba(108,99,255,.12)' },
  'AI/ML':             { icon: '🤖',  bg: 'rgba(168,85,247,.12)' },
  'Data & Analytics':  { icon: '📊',  bg: 'rgba(6,182,212,.12)'  },
  'Product':           { icon: '🎯',  bg: 'rgba(245,158,11,.12)' },
  'Design':            { icon: '🎨',  bg: 'rgba(236,72,153,.12)' },
  'Security':          { icon: '🔒',  bg: 'rgba(239,68,68,.12)'  },
  'Finance':           { icon: '💹',  bg: 'rgba(34,197,94,.12)'  },
  'Marketing':         { icon: '📣',  bg: 'rgba(251,146,60,.12)' },
  'Human Resources':   { icon: '👥',  bg: 'rgba(99,102,241,.12)' },
  'Sales':             { icon: '📈',  bg: 'rgba(20,184,166,.12)' },
  'Business':          { icon: '💼',  bg: 'rgba(234,179,8,.12)'  },
};

function getCategoryStyle(cat) {
  return CATEGORY_ICONS[cat] || { icon: '💡', bg: 'rgba(108,99,255,.12)' };
}

function getScoreColor(score) {
  if (score >= 70) return '#22c55e';
  if (score >= 45) return '#f59e0b';
  return '#6b7280';
}

function tierBadgeHTML(tierName) {
  if (!tierName) return '';
  const isBert = tierName.includes('BERT') || tierName.includes('sentence');
  const isLSA  = tierName.includes('LSA');
  const color  = isBert ? '#22c55e' : isLSA ? '#f59e0b' : '#6b7280';
  const label  = isBert ? '🤖 BERT Active' : isLSA ? '🧠 LSA Active' : 'TF-IDF Only';
  return `<span style="font-size:.72rem;padding:.2rem .7rem;border-radius:100px;
          border:1px solid ${color}33;color:${color};background:${color}11;
          display:inline-block">${label}</span>`;
}

/* ── File drag/drop ─────────────────────────────────────────────── */
const dropZone = document.getElementById('dropZone');
const fileInput = document.getElementById('fileInput');

dropZone.addEventListener('dragover', e => { e.preventDefault(); dropZone.classList.add('drag-over'); });
dropZone.addEventListener('dragleave', () => dropZone.classList.remove('drag-over'));
dropZone.addEventListener('drop', e => {
  e.preventDefault(); dropZone.classList.remove('drag-over');
  if (e.dataTransfer.files[0]) setFile(e.dataTransfer.files[0]);
});
fileInput.addEventListener('change', e => { if (e.target.files[0]) setFile(e.target.files[0]); });

function setFile(file) {
  const ext = '.' + file.name.split('.').pop().toLowerCase();
  if (!['.pdf','.docx','.doc','.txt'].includes(ext)) {
    alert('Please upload a PDF, DOCX, DOC, or TXT file.'); return;
  }
  selectedFile = file;
  let info = dropZone.querySelector('.file-selected-info');
  if (!info) { info = document.createElement('div'); info.className = 'file-selected-info'; dropZone.appendChild(info); }
  info.innerHTML = `✅ <strong>${file.name}</strong> &nbsp;·&nbsp; ${formatBytes(file.size)}`;
  document.getElementById('resumeText').value = '';
}

function formatBytes(b) {
  if (b < 1024) return b + ' B';
  if (b < 1048576) return (b/1024).toFixed(1) + ' KB';
  return (b/1048576).toFixed(1) + ' MB';
}

/* ── Loading ────────────────────────────────────────────────────── */
function showLoading() {
  document.getElementById('loadingOverlay').removeAttribute('hidden');
  const labels = ['📄 Extracting & preprocessing text', '🧠 NLTK tokenise → lemmatise → stem',
                  '🔍 TF-IDF + Embedding similarity', '✅ Ranking results'];
  const ids = ['step1','step2','step3','step4'];
  let i = 0;
  const iv = setInterval(() => {
    if (i > 0) { const prev = document.getElementById(ids[i-1]); prev.className = 'loading-step done'; prev.textContent = '✅ ' + labels[i-1].replace(/^.{2}/,''); }
    if (i < ids.length) { document.getElementById(ids[i]).classList.add('active'); i++; }
    else clearInterval(iv);
  }, 700);
  return iv;
}

function hideLoading() {
  document.getElementById('loadingOverlay').setAttribute('hidden','');
  const labels = ['📄 Extracting & preprocessing text','🧠 NLTK tokenise → lemmatise → stem',
                  '🔍 TF-IDF + Embedding similarity','✅ Ranking results'];
  ['step1','step2','step3','step4'].forEach((id, i) => {
    const el = document.getElementById(id); el.className = 'loading-step'; el.textContent = labels[i];
  });
}

/* ── Analyze ────────────────────────────────────────────────────── */
async function analyzeResume() {
  const resumeText = document.getElementById('resumeText').value.trim();
  if (!selectedFile && !resumeText) { alert('Please upload a resume or paste text.'); return; }

  const iv = showLoading();
  try {
    let resp;
    if (selectedFile) {
      const fd = new FormData(); fd.append('resume', selectedFile);
      resp = await fetch('/api/match', { method: 'POST', body: fd });
    } else {
      resp = await fetch('/api/match', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ resume_text: resumeText }),
      });
    }
    const data = await resp.json();
    clearInterval(iv);
    await new Promise(r => setTimeout(r, 350));
    hideLoading();

    if (!resp.ok || !data.success) { showError(data.error || 'Unexpected error'); return; }
    displayResults(data);
  } catch(err) {
    clearInterval(iv); hideLoading();
    showError('Network error: ' + err.message);
  }
}

/* ── Display results ────────────────────────────────────────────── */
function displayResults(data) {
  allResults   = data.matches;
  const info   = data.resume_info;
  embeddingTier = info.embedding_tier || '';

  document.getElementById('resultsSection').removeAttribute('hidden');
  document.getElementById('resultsSection').scrollIntoView({ behavior: 'smooth' });

  /* Resume summary */
  const skills   = info.detected_skills || [];
  const visible  = skills.slice(0, 12);
  const extra    = skills.length - visible.length;
  const weights  = info.weights || {};
  const phrases  = (info.noun_phrases || []).slice(0, 5);

  document.getElementById('resumeSummary').innerHTML = `
    <div class="summary-block">
      <span class="summary-label">File</span>
      <span class="summary-value">📄 ${info.filename}</span>
    </div>
    <div class="summary-block">
      <span class="summary-label">Education</span>
      <span class="summary-value">${info.education}</span>
    </div>
    <div class="summary-block">
      <span class="summary-label">Experience</span>
      <span class="summary-value">${info.experience_years ? info.experience_years + ' yrs' : '—'}</span>
    </div>
    <div class="summary-block">
      <span class="summary-label">NLP Engine</span>
      <span class="summary-value">${tierBadgeHTML(embeddingTier)}</span>
    </div>
    <div class="summary-block" style="flex:1">
      <span class="summary-label">Detected Skills (${skills.length}) — Score weights: TF-IDF ${Math.round(weights.tfidf*100)}% | Embed ${Math.round(weights.embed*100)}% | Skill ${Math.round(weights.skill*100)}%</span>
      <div class="skills-chips">
        ${visible.map(s => `<span class="skill-chip">${s}</span>`).join('')}
        ${extra > 0 ? `<span class="skill-chip skill-chip-more">+${extra} more</span>` : ''}
      </div>
      ${phrases.length ? `<div style="margin-top:.4rem;font-size:.72rem;color:var(--muted)">Key phrases: ${phrases.join(', ')}</div>` : ''}
    </div>
  `;

  document.getElementById('resultsSubtitle').textContent =
    `Analyzed ${data.total_jobs_analyzed} roles · showing top ${allResults.length} matches`;

  /* Category filter */
  const cats = [...new Set(allResults.map(m => m.category))].sort();
  const sel  = document.getElementById('categoryFilter');
  sel.innerHTML = '<option value="">All Categories</option>';
  cats.forEach(c => { const o = document.createElement('option'); o.value = o.textContent = c; sel.appendChild(o); });

  renderCards(allResults);
}

function filterResults() {
  const cat = document.getElementById('categoryFilter').value;
  renderCards(cat ? allResults.filter(m => m.category === cat) : allResults);
}

function renderCards(matches) {
  const grid = document.getElementById('jobsGrid');
  if (!matches.length) { grid.innerHTML = '<div class="empty-state">No matches in this category.</div>'; return; }

  grid.innerHTML = matches.map((m, idx) => {
    const rank = idx + 1;
    const { icon, bg } = getCategoryStyle(m.category);
    const color = getScoreColor(m.match_score);
    const visSkills = m.matched_skills.slice(0, 4);
    const extraSk  = m.matched_skills.length - visSkills.length;

    let rankClass = '', rankLabel = `#${rank}`;
    if (rank === 1) { rankClass = 'rank-1'; rankLabel = '🥇 #1 Match'; }
    else if (rank === 2) { rankClass = 'rank-2'; rankLabel = '🥈 #2'; }
    else if (rank === 3) { rankClass = 'rank-3'; rankLabel = '🥉 #3'; }

    /* mini score bars */
    const embedLabel = embeddingTier.includes('BERT') ? 'BERT' :
                       embeddingTier.includes('LSA')  ? 'LSA'  : 'Embed';

    return `
      <div class="job-card" onclick="openModal(${m.id})" style="animation-delay:${idx*.05}s">
        <div class="card-rank ${rankClass}">${rankLabel}</div>
        <div class="card-header">
          <div class="card-icon" style="background:${bg}">${icon}</div>
          <div class="card-meta">
            <div class="card-title">${m.title}</div>
            <div class="card-company">${m.company}</div>
            <div class="card-location">📍 ${m.location}</div>
          </div>
        </div>

        <!-- Main score -->
        <div class="card-score-row">
          <div class="score-bar-wrap">
            <div class="score-bar-bg">
              <div class="score-bar-fill" style="width:${m.match_score}%;background:${color}"></div>
            </div>
          </div>
          <div class="score-val" style="color:${color}">${m.match_score}%</div>
        </div>

        <!-- Sub-scores -->
        <div class="sub-scores">
          <div class="sub-score">
            <span class="sub-label">TF-IDF</span>
            <div class="sub-bar-bg"><div class="sub-bar-fill" style="width:${Math.min(100,m.tfidf_score*2.5)}%;background:#6c63ff"></div></div>
            <span class="sub-val">${m.tfidf_score}%</span>
          </div>
          <div class="sub-score">
            <span class="sub-label">${embedLabel}</span>
            <div class="sub-bar-bg"><div class="sub-bar-fill" style="width:${Math.min(100,m.embed_score*2.5)}%;background:#a855f7"></div></div>
            <span class="sub-val">${m.embed_score}%</span>
          </div>
          <div class="sub-score">
            <span class="sub-label">Skills</span>
            <div class="sub-bar-bg"><div class="sub-bar-fill" style="width:${m.skill_overlap_pct}%;background:#22c55e"></div></div>
            <span class="sub-val">${m.skill_overlap_pct}%</span>
          </div>
        </div>

        <div class="card-tags">
          <span class="tag tag-salary">${m.salary}</span>
          <span class="tag tag-type">${m.type}</span>
          <span class="tag tag-exp">${m.experience}</span>
        </div>

        ${visSkills.length ? `
        <div class="card-skills">
          <div class="skills-header">Matched Skills (${m.skill_match_count}/${m.total_skills})</div>
          <div class="matched-skills">
            ${visSkills.map(s => `<span class="mskill">${s}</span>`).join('')}
            ${extraSk > 0 ? `<span class="mskill mskill-extra">+${extraSk}</span>` : ''}
          </div>
        </div>` : ''}
      </div>
    `;
  }).join('');
}

/* ── Modal ──────────────────────────────────────────────────────── */
function openModal(jobId) {
  const m = allResults.find(x => x.id === jobId);
  if (!m) return;
  const { icon, bg } = getCategoryStyle(m.category);
  const color = getScoreColor(m.match_score);
  const embedLabel = embeddingTier.includes('BERT') ? 'BERT Semantic' :
                     embeddingTier.includes('LSA')  ? 'LSA Embedding' : 'Embedding';

  document.getElementById('modalContent').innerHTML = `
    <div style="display:flex;align-items:center;gap:.8rem;margin-bottom:.3rem">
      <div class="card-icon" style="background:${bg};width:52px;height:52px;font-size:1.6rem;border-radius:14px;display:flex;align-items:center;justify-content:center">${icon}</div>
      <div>
        <div class="modal-title">${m.title}</div>
        <div class="modal-company">${m.company} &nbsp;·&nbsp; ${m.location}</div>
      </div>
    </div>

    <!-- Score breakdown -->
    <div class="modal-score-row">
      <div>
        <div class="modal-score-big" style="color:${color}">${m.match_score}%</div>
        <div class="modal-score-label">Overall Match</div>
      </div>
      <div style="flex:1;display:flex;flex-direction:column;gap:.5rem">
        ${scoreBar('TF-IDF Similarity', m.tfidf_score, Math.min(100,m.tfidf_score*2.5), '#6c63ff')}
        ${scoreBar(embedLabel, m.embed_score, Math.min(100,m.embed_score*2.5), '#a855f7')}
        ${scoreBar('Skill Overlap', m.skill_overlap_pct, m.skill_overlap_pct, '#22c55e')}
        ${scoreBar(`Skills Matched (${m.skill_match_count}/${m.total_skills})`, 0,
                   Math.round(m.skill_match_count/Math.max(1,m.total_skills)*100), '#06b6d4', true)}
      </div>
    </div>

    <div class="modal-details">
      <div class="modal-detail-item"><span class="modal-detail-label">Salary</span><span class="modal-detail-value" style="color:#22c55e">${m.salary}</span></div>
      <div class="modal-detail-item"><span class="modal-detail-label">Type</span><span class="modal-detail-value">${m.type}</span></div>
      <div class="modal-detail-item"><span class="modal-detail-label">Experience</span><span class="modal-detail-value">${m.experience}</span></div>
      <div class="modal-detail-item"><span class="modal-detail-label">Education</span><span class="modal-detail-value">${m.education}</span></div>
      <div class="modal-detail-item"><span class="modal-detail-label">Category</span><span class="modal-detail-value">${m.category}</span></div>
      <div class="modal-detail-item"><span class="modal-detail-label">NLP Engine</span><span class="modal-detail-value">${tierBadgeHTML(embeddingTier)}</span></div>
      <div class="modal-detail-item"><span class="modal-detail-label">Data Source</span><span class="modal-detail-value" style="font-size:.8rem;color:var(--muted)">${m.source || 'Built-in curated'}</span></div>
    </div>

    <div class="modal-section-title">Job Description</div>
    <p class="modal-description">${m.description}</p>

    <div class="modal-section-title">Skills Analysis</div>
    <div class="all-skills">
      ${m.matched_skills.map(s => `<span class="askill askill-match">✓ ${s}</span>`).join('')}
      ${m.missing_skills.map(s => `<span class="askill askill-miss">✗ ${s}</span>`).join('')}
    </div>
    <p style="font-size:.78rem;color:var(--muted);margin-top:.5rem">
      <span style="color:#22c55e">■</span> You have &nbsp;
      <span style="color:#f87171">■</span> To develop
    </p>
  `;

  document.getElementById('modalOverlay').classList.add('open');
}

function scoreBar(label, rawVal, pct, color, noVal = false) {
  return `
    <div class="modal-progress-row">
      <span class="progress-label">${label}</span>
      <div class="progress-bar-bg"><div class="progress-bar-fill" style="width:${pct}%;background:${color}"></div></div>
      ${noVal ? `<span class="progress-val" style="color:${color}">${pct}%</span>` :
                `<span class="progress-val" style="color:${color}">${rawVal}%</span>`}
    </div>`;
}

function closeModal(e) {
  if (e && e.target !== document.getElementById('modalOverlay') &&
      !e.target.classList.contains('modal-close')) return;
  document.getElementById('modalOverlay').classList.remove('open');
}
document.addEventListener('keydown', e => { if (e.key === 'Escape') closeModal(); });

/* ── Reset ──────────────────────────────────────────────────────── */
function resetApp() {
  allResults = []; selectedFile = null;
  fileInput.value = '';
  document.getElementById('resumeText').value = '';
  const inf = dropZone.querySelector('.file-selected-info');
  if (inf) inf.remove();
  document.getElementById('resultsSection').setAttribute('hidden','');
  window.scrollTo({ top: 0, behavior: 'smooth' });
}

function showError(msg) {
  const s = document.getElementById('resultsSection');
  s.removeAttribute('hidden'); s.scrollIntoView({ behavior: 'smooth' });
  document.getElementById('jobsGrid').innerHTML = `<div class="error-banner">⚠️ ${msg}</div>`;
}

/* ── Init ───────────────────────────────────────────────────────── */
fetch('/api/health').then(r => r.json()).then(d => {
  if (d.jobs_loaded) document.getElementById('statJobs').textContent = d.jobs_loaded.toLocaleString();
  if (d.embedding_tier) {
    const badge = document.getElementById('embeddingBadge');
    if (badge) badge.innerHTML = tierBadgeHTML(d.embedding_tier);
  }
  if (d.dataset_source) {
    document.getElementById('datasetSource').textContent = '📦 ' + d.dataset_source;
    const isLinkedIn = d.dataset_source.includes('LinkedIn');
    document.getElementById('datasetSub').textContent = isLinkedIn
      ? 'Real LinkedIn job postings 2023-2024 (Kaggle dataset)'
      : 'Place data/linkedin/postings.csv for 5,000+ real LinkedIn jobs';
  }
}).catch(() => {});
