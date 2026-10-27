// 학원 성적 기록 — 학원 문자 사진을 올리면 점수와 피드백을 찾아 쌓고, 테스트별로 차트를 그린다.
// 사진의 글자는 이 기기 브라우저 안에서 읽는다(사진을 어디에도 보내지 않음).
// 기록은 이 기기에 저장되고, 가족 연결이 되어 있으면 비공개 가족 시트에 저장해서 가족 폰이 함께 본다.
import { todayKST, label, esc, uid } from './util.js';
import { parseScoreText } from './scores-parse.js';
import { familyOn, familyGet, familyPost, familyNav, siteFooter } from './family.js';

const KEY = 'sosik.scores';
const $root = document.getElementById('scores');
const localRecords = () => { try { return JSON.parse(localStorage.getItem(KEY)) || []; } catch { return []; } };
let records = familyOn() ? [] : localRecords();
const save = () => { try { localStorage.setItem(KEY, JSON.stringify(records)); } catch { alert('이 기기에 저장하지 못했어요.'); } };

// 가족 연결이면 기록을 가족 시트에서 다시 불러온다
async function loadRecords() {
  if (!familyOn()) return;
  try { records = (await familyGet()).records; state.sync = 'ok'; }
  catch (e) { state.sync = 'error'; state.error = `가족 기록 시트를 불러오지 못했어요 (${e.message})`; }
}
// 한 기록을 저장: 가족 연결이면 시트로, 아니면 이 폰에
async function putRecord(rec) {
  if (familyOn()) { await familyPost({ action: 'saveRecord', record: rec }); return; }
  records = records.filter(x => x.id !== rec.id && !(x.date === rec.date && x.academy === rec.academy));
  records.push(rec); save();
}

const state = { draft: null, busy: '', error: '', filter: '전체', mode: 'photo', sync: familyOn() ? 'loading' : 'off' };

const pct = s => s.total ? Math.round(s.score / s.total * 100) : 0;
const passed = s => s.pass == null ? null : s.score >= s.pass;
const resultText = s => passed(s) == null ? '' : passed(s) ? '통과' : '재시험';

function toast(msg) {
  const t = document.getElementById('toast');
  t.textContent = msg; t.hidden = false;
  clearTimeout(toast.t); toast.t = setTimeout(() => { t.hidden = true; }, 2500);
}

// ───────── 사진 글자 읽기 (Tesseract.js, 처음 쓸 때만 불러옴) ─────────
function loadTesseract() {
  if (window.Tesseract) return Promise.resolve();
  return new Promise((ok, fail) => {
    const s = document.createElement('script');
    s.src = 'https://cdn.jsdelivr.net/npm/tesseract.js@5.1.1/dist/tesseract.min.js';
    s.onload = ok;
    s.onerror = () => fail(new Error('글자 인식 도구를 불러오지 못했어요. 인터넷 연결을 확인해 주세요.'));
    document.head.append(s);
  });
}
async function readPhoto(file) {
  state.busy = '글자 인식 도구 준비 중… (처음 한 번은 조금 걸려요)'; render();
  await loadTesseract();
  // 영어학원 문자(Reading Test 등)도 읽을 수 있게 한국어+영어
  const worker = await window.Tesseract.createWorker('kor+eng', 1, {
    logger: m => { if (m.status === 'recognizing text') { state.busy = `사진 속 글자 읽는 중 ${Math.round(m.progress * 100)}%`; render(); } },
  });
  try { return (await worker.recognize(file)).data.text; } finally { await worker.terminate(); }
}

// 처음 온 사람이 사진 없이 흐름을 볼 수 있게 하는 가짜 문자 (실제 학원·학생 아님)
const SAMPLE = `[예시학원]
안녕하세요, 예시학원입니다.

(1) 국어
- 과제수행도: 중
- 어휘테스트: 7/10
*어휘테스트 통과 기준: 8개

(2) 영어
- 단어시험: 45/50
- 코멘트: 문법 서술형 연습이 조금 더 필요해요.`;

function startDraft(text) {
  const p = parseScoreText(text, todayKST());
  // 학원 이름이 문자에 없으면, 같은 과목을 기록했던 학원을 채워 둔다
  const subj = p.scores[0]?.subject;
  const known = subj && [...records].reverse().find(r => r.scores.some(s => s.subject === subj))?.academy;
  state.draft = { date: p.date || todayKST(), academy: p.academy || known || '', session: p.session, scores: p.scores, feedback: p.feedback, dateFromText: !!p.date };
  state.error = p.scores.length ? '' : '점수를 찾지 못했어요. 아래에서 직접 넣거나, 문자를 복사해서 붙여넣어 보세요.';
}

// ───────── 차트: 테스트 하나 = 작은 꺾은선 하나 (정답률 %, 통과 기준은 점선) ─────────
function chart(points) {
  const W = 320, H = 130, L = 34, R = 40, T = 12, B = 22;
  const x = i => points.length === 1 ? (L + W - R) / 2 : L + i * (W - L - R) / (points.length - 1);
  const y = v => T + (100 - v) * (H - T - B) / 100;
  const last = points[points.length - 1];
  const passPct = last.pass != null ? Math.round(last.pass / last.total * 100) : null;
  const path = points.map((p, i) => `${i ? 'L' : 'M'}${x(i).toFixed(1)},${y(p.pct).toFixed(1)}`).join(' ');
  const md = d => `${Number(d.slice(5, 7))}/${Number(d.slice(8))}`;
  return `<svg class="schart" viewBox="0 0 ${W} ${H}" role="img" aria-label="정답률 변화, 최근 ${last.pct}%">
    ${[0, 50, 100].map(v => `<line class="grid" x1="${L}" x2="${W - R}" y1="${y(v)}" y2="${y(v)}"/><text class="axis" x="${L - 6}" y="${y(v) + 4}" text-anchor="end">${v}</text>`).join('')}
    ${passPct != null ? `<line class="passline" x1="${L}" x2="${W - R}" y1="${y(passPct)}" y2="${y(passPct)}"/><text class="axis" x="${W - R + 4}" y="${y(passPct) + 4}">통과 ${passPct}</text>` : ''}
    ${points.length > 1 ? `<path class="line" d="${path}"/>` : ''}
    ${points.map((p, i) => `<g class="pt"><circle cx="${x(i)}" cy="${y(p.pct)}" r="10" class="hit"/><circle cx="${x(i)}" cy="${y(p.pct)}" r="4.5" class="dot ${passed(p) === false ? 'miss' : ''}"/><title>${md(p.date)} · ${esc(p.test)} ${p.score}/${p.total} (${p.pct}%)${resultText(p) ? ' · ' + resultText(p) : ''}</title></g>`).join('')}
    <text class="vlabel" x="${x(points.length - 1) - 8}" text-anchor="end" y="${y(last.pct) < 24 ? y(last.pct) + 16 : y(last.pct) - 8}">${last.pct}%</text>
    <text class="axis" x="${x(0)}" y="${H - 4}" text-anchor="${points.length === 1 ? 'middle' : 'start'}">${md(points[0].date)}</text>
    ${points.length > 1 ? `<text class="axis" x="${x(points.length - 1)}" y="${H - 4}" text-anchor="end">${md(last.date)}</text>` : ''}
  </svg>`;
}

// 범위만 바뀌는 시험(day 19-22, day 23-26 …)은 한 차트로 모은다
const seriesName = test => test.replace(/\s*\d+\s*[-~]\s*\d+/g, '').replace(/\s+\d+$/, '').trim() || test;

function series() {
  const map = new Map();
  for (const r of records) {
    if (state.filter !== '전체' && r.academy !== state.filter) continue;
    for (const s of r.scores) {
      const name = seriesName(s.test);
      const k = `${r.academy}|${s.subject}|${name.toLowerCase()}`;
      if (!map.has(k)) map.set(k, { academy: r.academy, subject: s.subject, test: name, points: [] });
      map.get(k).points.push({ ...s, date: r.date, pct: pct(s) });
    }
  }
  for (const v of map.values()) v.points.sort((a, b) => a.date.localeCompare(b.date));
  return [...map.values()];
}

// ───────── 그리기 ─────────
function viewDraft() {
  const d = state.draft;
  return `<section class="card">
    <h2>찾은 내용 확인</h2>
    <p class="muted small">사진 글자 인식은 틀릴 수 있어요. 숫자를 꼭 확인하고 저장해 주세요.</p>
    <div class="two">
      <label>${d.dateFromText ? '시험 날짜 <span class="muted small">문자에서 찾음</span>' : '받은 날짜'}<input type="date" data-d="date" value="${esc(d.date)}"></label>
      <label>학원<input data-d="academy" value="${esc(d.academy)}" placeholder="예: 한맥국어학원" list="academyList"></label>
      <datalist id="academyList">${[...new Set(records.map(r => r.academy).filter(Boolean))].map(a => `<option value="${esc(a)}">`).join('')}</datalist>
    </div>
    <label>회차 <span class="muted small">선택</span><input data-d="session" value="${esc(d.session)}" placeholder="예: 6분기 3강"></label>
    <h3>점수</h3>
    ${d.scores.map((s, i) => `<div class="srow">
      <input data-s="${i}" data-k="subject" value="${esc(s.subject)}" placeholder="과목" aria-label="과목">
      <input data-s="${i}" data-k="test" value="${esc(s.test)}" placeholder="테스트 이름" aria-label="테스트">
      <span class="nums"><input data-s="${i}" data-k="score" inputmode="numeric" value="${esc(s.score)}" aria-label="점수"> / <input data-s="${i}" data-k="total" inputmode="numeric" value="${esc(s.total)}" aria-label="만점"></span>
      <label class="small">통과 기준<input data-s="${i}" data-k="pass" inputmode="numeric" value="${esc(s.pass ?? '')}" placeholder="없음"></label>
      <button class="ghost small" data-act="del-score" data-i="${i}">빼기</button>
      ${s.check ? `<p class="reason scheck">사진에서 '/'가 안 보여 ${s.score}/${s.total}(으)로 추정했어요. 맞는지 확인해 주세요.</p>` : ''}
    </div>`).join('') || '<p class="muted">찾은 점수가 없어요.</p>'}
    <button class="ghost" data-act="add-score">+ 점수 추가</button>
    <h3>피드백</h3>
    <textarea data-d="feedbackText" rows="5" placeholder="예: 국어 · 과제수행도: 상">${esc(d.feedback.map(f => `${f.subject ? f.subject + ' · ' : ''}${f.item === '메모' ? '' : f.item + ': '}${f.text}`).join('\n'))}</textarea>
    <p class="muted small">한 줄에 하나씩. 필요 없는 줄은 지워 주세요.</p>
    <div class="actions"><button class="primary" data-act="save">저장하기</button><button class="ghost" data-act="cancel">취소</button></div>
  </section>`;
}

function viewDashboard() {
  const academies = [...new Set(records.map(r => r.academy).filter(Boolean))];
  const list = series();
  const fb = records.filter(r => (state.filter === '전체' || r.academy === state.filter) && r.feedback.length).sort((a, b) => b.date.localeCompare(a.date));
  return `
    ${academies.length > 1 ? `<div class="chips">${['전체', ...academies].map(a => `<button class="chip ${state.filter === a ? 'on' : ''}" data-act="filter" data-v="${esc(a)}">${esc(a)}</button>`).join('')}</div>` : ''}
    <section><span class="k">Tests</span><h2>테스트별 점수</h2>
      ${list.length ? `<div class="sgrid">${list.map(sv => {
        const last = sv.points[sv.points.length - 1];
        const withPass = sv.points.filter(p => passed(p) != null);
        return `<div class="card scard">
          <div class="shead"><b>${esc(sv.subject)} · ${esc(sv.test)}</b><span class="muted small">${esc(sv.academy)}</span></div>
          <div class="sstat"><span class="big">${last.score}/${last.total}</span> ${resultText(last) ? `<span class="flag ${passed(last) ? '' : 'warn'}">${passed(last) ? '✓ 통과' : '! 재시험'}</span>` : ''}
            ${withPass.length ? `<span class="muted small">통과 ${withPass.filter(passed).length}/${withPass.length}회</span>` : ''}</div>
          ${chart(sv.points)}
          <details><summary>기록 표</summary><table class="stable"><tr><th>날짜</th><th>시험</th><th>점수</th><th>결과</th></tr>
            ${sv.points.map(p => `<tr><td>${label(p.date)}</td><td>${esc(p.test)}</td><td>${p.score}/${p.total} (${p.pct}%)</td><td>${resultText(p) || '-'}</td></tr>`).join('')}</table></details>
        </div>`;
      }).join('')}</div>` : `<div class="empty"><p><b>이렇게 써요</b></p>
        <ol class="howto"><li>학원에서 온 성적 문자를 캡처하거나 글을 복사해요</li><li>아래 <b>학원 문자 넣기</b>에서 <b>사진으로</b>를 골라 캡처 이미지를 고르거나, <b>글로</b> 붙여넣고 <b>정리하기</b>를 눌러요</li><li>찾은 점수를 확인하고 저장하면, 테스트별 차트와 선생님 피드백이 쌓여요</li></ol>
        <button class="ghost" data-act="sample">예시 문자로 먼저 해보기</button></div>`}
    </section>
    ${fb.length ? `<section><span class="k">Feedback</span><h2>선생님 피드백</h2><div class="list">${fb.map(r => `<div class="row"><div class="body">
      <span class="meta">${label(r.date)} · ${esc(r.academy)}${r.session ? ' · ' + esc(r.session) : ''}</span>
      <ul class="fb">${r.feedback.map(f => `<li>${f.subject ? `<b>${esc(f.subject)}</b> ` : ''}${f.item && f.item !== '메모' ? esc(f.item) + ': ' : ''}${esc(f.text)}</li>`).join('')}</ul></div></div>`).join('')}</div></section>` : ''}`;
}

// 저장한 문자 목록 · 백업 · 지우기
function viewManage() {
  const sorted = [...records].sort((a, b) => b.date.localeCompare(a.date));
  return `
    <section><details><summary>${records.length ? `저장한 문자 ${records.length}개 · ` : ''}백업 · 옮기기 · 지우기</summary>
      ${records.length ? `<div class="list">${sorted.map(r => `<div class="row"><div class="body"><span class="title">${label(r.date)} · ${esc(r.academy || '학원 미상')}</span>
        <span class="meta">${r.scores.map(s => `${esc(s.test)} ${s.score}/${s.total}`).join(', ') || '점수 없음'}</span></div>
        <button class="ghost small danger" data-act="del-record" data-id="${r.id}">지우기</button></div>`).join('')}</div>` : ''}
      <p class="muted small">${familyOn() ? '기록은 가족 기록 시트에 있어요. 따로 백업 파일로도 저장할 수 있어요.' : '기록은 이 휴대폰 브라우저에만 있어요. 폰을 바꾸기 전이나 가끔씩 백업 파일로 저장해 두세요.'}</p>
      <div class="actions">
        ${records.length ? `<button class="ghost" data-act="backup">백업 파일 저장</button>` : ''}
        <label class="ghost upload-ghost">백업 불러오기<input type="file" accept="application/json,.json" data-act="restore" hidden></label>
        ${records.length ? `<button class="ghost" data-act="copy">구글 시트·엑셀용 복사</button>` : ''}
      </div>
      ${records.length ? `<p class="muted small">복사한 뒤 시트의 빈 칸에 붙여넣으면 날짜·학원·과목·테스트·점수·만점·통과 기준이 한 줄씩 들어가요.</p>` : ''}
    </details></section>`;
}

function render() {
  $root.innerHTML = `
  <header class="shero"><div><span class="k">Academy Scores</span><h1>학원 성적 기록</h1><p class="muted small">학원 문자를 사진이나 글로 넣으면 점수와 피드백이 쌓여요</p></div>
    ${state.draft ? '' : '<a class="ghost small addjump" href="#add">＋ 학원 문자 넣기</a>'}</header>
  <main class="pad">
    ${state.draft ? viewDraft() : ''}
    ${state.error ? `<div class="banner warn">${esc(state.error)}</div>` : ''}
    ${familyOn() && localRecords().length ? `<div class="banner info">이 폰에만 저장된 기록이 ${localRecords().length}개 있어요. <button class="link" data-act="migrate">가족 기록 시트로 옮기기</button></div>` : ''}
    ${state.sync === 'loading' ? '<p class="muted">가족 기록 시트에서 불러오는 중…</p>' : viewDashboard()}
    ${state.draft ? '' : `<section class="card add" id="add">
      <span class="k">Add</span><h2>학원 문자 넣기</h2>
      <div class="seg" role="tablist" aria-label="넣는 방법">
        <button role="tab" aria-selected="${state.mode === 'photo'}" class="${state.mode === 'photo' ? 'on' : ''}" data-act="mode" data-v="photo">사진으로</button>
        <button role="tab" aria-selected="${state.mode === 'text'}" class="${state.mode === 'text' ? 'on' : ''}" data-act="mode" data-v="text">글로</button>
      </div>
      ${state.mode === 'photo' ? `
        <p class="add-help">학원 문자 화면을 캡처한 이미지를 골라 주세요. 이 폰 안에서 글자를 읽어요.</p>
        <label class="primary wide upload">캡처 이미지 고르기<input type="file" accept="image/*" data-act="photo" hidden></label>`
      : `
        <p class="add-help">학원 문자를 길게 눌러 복사해서 붙여넣거나, 직접 써 주세요. 예) 어휘테스트: 8/10</p>
        <textarea id="pasteText" rows="6" placeholder="여기에 붙여넣거나 써 주세요"></textarea>
        <button class="primary wide" data-act="parse-paste">정리하기</button>`}
      ${state.busy ? `<p class="busy">${esc(state.busy)}</p>` : ''}
    </section>`}
    ${viewManage()}
    ${state.sync === 'ok' ? '<p class="muted small center">가족 기록 시트에 저장돼요. 아이 폰에서도 같은 기록이 보여요.</p>' : ''}
    <p class="note">사진은 이 휴대폰 안에서만 읽고 어디에도 보내지 않아요. ${familyOn() ? '기록은 가족만 보는 비공개 구글 시트에 저장돼요.' : '기록도 이 휴대폰 브라우저에만 저장되고, 다른 사람과 공유되지 않아요.'} 학생 이름이 들어간 줄은 저장하지 않아요.<br>학원이나 학교의 공식 서비스가 아니에요.</p>
  </main>
  ${siteFooter()}
  ${familyNav('scores')}`;
}

// ───────── 동작 ─────────
$root.addEventListener('change', async e => {
  const el = e.target;
  if (el.dataset.act === 'restore' && el.files[0]) {
    // 백업 파일을 불러와 지금 기록과 합친다 (같은 날·같은 학원은 백업 쪽으로 바뀜)
    try {
      const list = JSON.parse(await el.files[0].text());
      if (!Array.isArray(list)) throw new Error();
      for (const r of list) {
        if (!r.date || !Array.isArray(r.scores)) continue;
        await putRecord({ id: r.id || uid(), date: r.date, academy: r.academy || '', session: r.session || '', scores: r.scores, feedback: r.feedback || [] });
      }
      await loadRecords(); toast(`백업에서 ${list.length}개를 불러왔어요`);
    } catch { state.error = '백업 파일을 읽지 못했어요. 이 페이지에서 저장한 .json 파일인지 확인해 주세요.'; }
    render(); return;
  }
  if (el.dataset.act !== 'photo' || !el.files[0]) return;
  await fromPhoto(el.files[0]);
});

async function fromPhoto(file) {
  state.error = '';
  try { startDraft(await readPhoto(file)); }
  catch (err) { state.error = err.message || '사진을 읽지 못했어요.'; }
  state.busy = ''; render(); scrollTo(0, 0);
}

// 캡처 이미지를 글 칸에 붙여넣으면 사진으로 읽는다 (글을 붙여넣으면 평소처럼 글로 들어감)
$root.addEventListener('paste', e => {
  if (e.target.id !== 'pasteText') return;
  const img = [...(e.clipboardData?.items || [])].find(i => i.type.startsWith('image/'));
  if (!img) return;
  e.preventDefault();
  fromPhoto(img.getAsFile());
});

$root.addEventListener('input', e => {
  const el = e.target, d = state.draft;
  if (!d) return;
  if (el.dataset.d) d[el.dataset.d] = el.value;
  if (el.dataset.s !== undefined) {
    const s = d.scores[Number(el.dataset.s)], k = el.dataset.k;
    s[k] = ['score', 'total', 'pass'].includes(k) ? (el.value === '' ? (k === 'pass' ? null : 0) : Number(el.value)) : el.value;
  }
});

$root.addEventListener('click', async e => {
  const b = e.target.closest('[data-act]');
  if (!b || b.dataset.act === 'photo') return;
  const act = b.dataset.act, d = state.draft;
  if (act === 'mode') state.mode = b.dataset.v;
  else if (act === 'sample') { startDraft(SAMPLE); toast('예시 문자예요. 저장하면 지울 때까지 남아요'); scrollTo(0, 0); }
  else if (act === 'backup') {
    const a = document.createElement('a');
    a.href = URL.createObjectURL(new Blob([JSON.stringify(records, null, 1)], { type: 'application/json' }));
    a.download = `학원성적기록-${todayKST()}.json`;
    a.click(); URL.revokeObjectURL(a.href);
  }
  else if (act === 'parse-paste') {
    const t = document.getElementById('pasteText').value;
    if (t.trim()) { startDraft(t); setTimeout(() => scrollTo(0, 0)); } else { state.error = '붙여넣은 글이 없어요. "글로"에서 학원 문자를 붙여넣거나 써 주세요.'; setTimeout(() => scrollTo(0, 0)); }
  }
  else if (act === 'add-score') d.scores.push({ subject: '', test: '', score: 0, total: 0, pass: null });
  else if (act === 'del-score') d.scores.splice(Number(b.dataset.i), 1);
  else if (act === 'cancel') { state.draft = null; state.error = ''; }
  else if (act === 'save') {
    const feedback = (d.feedbackText ?? null) !== null
      ? d.feedbackText.split('\n').map(s => s.trim()).filter(Boolean).map(line => {
          const m = line.match(/^([가-힣A-Za-z]{1,8})\s*·\s*(.*)$/);
          const rest = m ? m[2] : line, kv = rest.match(/^([^:：]{1,12})[:：]\s*(.+)$/);
          return { subject: m ? m[1] : '', item: kv ? kv[1].trim() : '메모', text: kv ? kv[2].trim() : rest };
        })
      : d.feedback;
    const scores = d.scores.filter(s => s.test && s.total > 0).map(({ check, ...s }) => s);
    // 같은 날·같은 학원 문자를 다시 올리면 새로 쌓지 않고 바꾼다
    const same = records.find(r => r.date === d.date && r.academy === d.academy);
    const rec = { id: same?.id || uid(), date: d.date, academy: d.academy.trim(), session: d.session.trim(), scores, feedback };
    if (familyOn()) { state.busy = '가족 기록 시트에 저장하는 중…'; render(); }
    try { await putRecord(rec); await loadRecords(); }
    catch (err) { state.busy = ''; state.error = `가족 기록 시트에 저장하지 못했어요 (${err.message}). 잠시 후 다시 눌러 주세요.`; render(); return; }
    state.busy = ''; state.draft = null; state.error = '';
    toast(same ? '같은 날 기록을 새 내용으로 바꿨어요' : `저장했어요 · 점수 ${scores.length}개`);
  }
  else if (act === 'filter') state.filter = b.dataset.v;
  else if (act === 'del-record') {
    if (!confirm('이 기록을 지울까요?')) return;
    if (familyOn()) {
      try { await familyPost({ action: 'deleteRecord', id: b.dataset.id }); await loadRecords(); }
      catch (err) { state.error = `지우지 못했어요 (${err.message})`; }
    } else { records = records.filter(r => r.id !== b.dataset.id); save(); }
  }
  else if (act === 'migrate') {
    // 가족 연결 전에 이 폰에만 저장한 기록을 가족 시트로 올리고, 이 폰의 사본은 지운다
    state.busy = '이 폰의 기록을 가족 시트로 올리는 중…'; render();
    try {
      for (const r of localRecords()) await familyPost({ action: 'saveRecord', record: r });
      localStorage.removeItem(KEY); await loadRecords(); toast('가족 시트로 옮겼어요');
    } catch (err) { state.error = `옮기지 못했어요 (${err.message})`; }
    state.busy = '';
  }
  else if (act === 'copy') {
    const tsv = [...records].sort((a, c) => a.date.localeCompare(c.date)).flatMap(r => r.scores.map(s => [r.date, r.academy, s.subject, s.test, s.score, s.total, s.pass ?? ''].join('\t'))).join('\n');
    try { await navigator.clipboard.writeText(tsv); toast('복사했어요. 시트에 붙여넣어 주세요'); } catch { prompt('아래 내용을 복사해 주세요', tsv); }
  }
  render();
});

render();
loadRecords().then(() => { if (state.sync === 'loading') state.sync = 'off'; render(); });
