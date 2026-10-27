// 기말고사 50일 플래너 — 구글 시트 '50일 플래너' 탭을 읽어서 오늘 할 공부를 보여준다.
// 체크한 것은 이 폰에 저장되고, 가족 연결이 되어 있으면 비공개 가족 시트에도 함께 기록된다.
import { todayKST, addDays, diffDays, weekStart, wd, label, esc, WD } from './util.js';
import { loadPlanner, SHEET_ID } from './sheet.js';
import { familyOn, familyGet, familyPost, familyNav, siteFooter } from './family.js';

const EXAM = '2026-12-14';
const SHEET_URL = `https://docs.google.com/spreadsheets/d/${SHEET_ID}/edit`;
const DONE_KEY = 'sosik.planner.done';
const PENDING_KEY = 'family.pending';   // 아직 가족 시트에 못 보낸 체크
const $root = document.getElementById('planner');

const state = { data: null, error: '', day: todayKST(), showLate: false, scores: [], sync: familyOn() ? 'loading' : 'off' };
const load = (k, d) => { try { return JSON.parse(localStorage.getItem(k)) ?? d; } catch { return d; } };
const store = (k, v) => { try { localStorage.setItem(k, JSON.stringify(v)); } catch {} };
let done = load(DONE_KEY, {});
let pending = load(PENDING_KEY, []);
const saveDone = () => store(DONE_KEY, done);

// 밀린 체크를 가족 시트로 보낸다. 실패하면 남겨 두었다가 다음에 다시 보낸다.
async function flush() {
  if (!familyOn() || !pending.length) return;
  const items = pending.slice();
  try {
    await familyPost({ action: 'check', items });
    pending = pending.slice(items.length); store(PENDING_KEY, pending);
    state.sync = 'ok';
  } catch { state.sync = 'error'; }
  render();
}

// 가족 시트에서 체크와 학원 성적을 불러온다 (연결 안 됐으면 이 폰에 저장된 성적만)
async function loadFamily() {
  if (!familyOn()) { state.scores = load('sosik.scores', []); return; }
  try {
    await flush();
    const d = await familyGet();
    done = Object.fromEntries(d.checks.map(k => [k, true]));
    for (const p of pending) { if (p.done) done[p.key] = true; else delete done[p.key]; }
    saveDone();
    state.scores = d.records;
    if (state.sync !== 'error') state.sync = 'ok';
  } catch { state.sync = 'error'; state.scores = []; }
}

// 할 일 하나를 알아보는 이름. 시트에서 순서가 바뀌어도 체크가 유지된다.
const keyOf = t => `${t.date}|${t.subject}|${t.task}|${t.range}`;
const isDone = t => !!done[keyOf(t)];

const ddayText = d => { const n = diffDays(d, EXAM); return n > 0 ? `D-${n}` : n === 0 ? 'D-DAY' : `시험 ${-n + 1}일째`; };
const mins = m => m >= 60 ? `${Math.floor(m / 60)}시간${m % 60 ? ' ' + (m % 60) + '분' : ''}` : `${m}분`;

// 시트 '공부 방법' 탭에서 위에서부터 처음 맞는 방법을 고른다 (과목이 같거나 '공통', 할 일에 그 말이 들어 있으면)
function methodFor(t) {
  return (state.data.methods || []).find(m => (m.subject === t.subject || m.subject === '공통') && t.task.includes(m.keyword));
}

function taskCard(t, { showDate = false } = {}) {
  const w = state.data.weights?.[t.subject];
  const how = methodFor(t);
  return `<div class="pcard s-${esc(t.subject)} ${isDone(t) ? 'is-done' : ''}">
    <button class="pcheck" data-key="${esc(keyOf(t))}" aria-label="${isDone(t) ? '완료 취소' : '완료'}">${isDone(t) ? '✓' : ''}</button>
    <div class="pbody">
      <div class="ptop"><span class="psubj">${esc(t.subject)}</span>${w ? `<span class="pweight">기말 반영 ${w}%</span>` : ''}${t.minutes ? `<span class="pmin">${mins(t.minutes)}</span>` : ''}</div>
      <div class="ptask">${esc(t.task)}</div>
      ${t.range ? `<div class="prange">${showDate ? label(t.date) + ' · ' : ''}${esc(t.range)}</div>` : showDate ? `<div class="prange">${label(t.date)}</div>` : ''}
      ${t.memo ? `<div class="pmemo">${esc(t.memo)}</div>` : ''}
      ${t.link ? `<a class="plink" href="${esc(t.link)}" target="_blank" rel="noopener">▶ 인강 보기</a>` : ''}
      ${how && !isDone(t) ? `<details class="phow"><summary>공부법 보기</summary><ol>${how.steps.map(s => `<li>${esc(s)}</li>`).join('')}</ol></details>` : ''}
    </div>
  </div>`;
}

function render() {
  if (!state.data) {
    $root.innerHTML = `<main class="pad"><p class="muted" style="margin-top:40px">${state.error ? esc(state.error) : '계획을 불러오는 중…'}</p></main>`;
    return;
  }
  const { tasks, classes } = state.data;
  const today = todayKST(), day = state.day;
  const list = tasks.filter(t => t.date === day);
  const todayClasses = classes.filter(c => c.date === day);
  const left = list.filter(t => !isDone(t));
  const leftMin = left.reduce((s, t) => s + t.minutes, 0);
  const late = tasks.filter(t => t.date < today && !isDone(t));
  const doneAll = tasks.filter(isDone).length;
  const first = tasks[0]?.date, last = tasks[tasks.length - 1]?.date;
  const ws = weekStart(day);
  const week = Array.from({ length: 7 }, (_, i) => addDays(ws, i)).map(d => {
    const l = tasks.filter(t => t.date === d);
    return { d, n: l.length, k: l.filter(isDone).length };
  });
  const phase = list[0]?.phase || '';

  $root.innerHTML = `
  <header class="phead">
    <span class="k">Final Exam</span>
    <div class="pdday">${ddayText(today)}</div>
    <div class="psub">기말고사 ${label(EXAM)} 시작</div>
    <div class="pbar" role="progressbar" aria-valuemin="0" aria-valuemax="${tasks.length}" aria-valuenow="${doneAll}"><span style="width:${tasks.length ? (doneAll / tasks.length * 100).toFixed(1) : 0}%"></span></div>
    <div class="psub small">50일 계획 ${tasks.length}개 중 ${doneAll}개 완료</div>
  </header>

  <main class="pad">
    <div class="pleft">
    ${!state.data.live ? `<div class="banner warn small">지금은 구글 시트에 연결되지 않아 <b>${new Date(state.data.fetchedAt).toLocaleDateString('ko-KR')}</b>에 불러온 계획을 보여줘요. 시트를 고친 내용은 연결된 뒤에 반영돼요.</div>` : ''}

    <div class="pnav">
      <button class="ghost" data-go="-1" ${day <= first ? 'disabled' : ''} aria-label="전날">‹</button>
      <div class="pday"><b>${day === today ? '오늘' : day === addDays(today, 1) ? '내일' : day === addDays(today, -1) ? '어제' : ''}</b> ${label(day)}${phase ? `<span class="pphase">${esc(phase)}</span>` : ''}</div>
      <button class="ghost" data-go="1" ${day >= last ? 'disabled' : ''} aria-label="다음 날">›</button>
    </div>
    ${day !== today ? `<button class="link center-block" data-today>오늘로 돌아가기</button>` : ''}

    <div class="pweek">${week.map(w => `<button class="pwd ${w.d === day ? 'sel' : ''} ${w.d === today ? 'today' : ''}" data-day="${w.d}">
      <span>${WD[wd(w.d)]}</span><b>${Number(w.d.slice(8))}</b><i class="${w.n && w.k === w.n ? 'full' : w.k ? 'part' : w.n ? 'none' : 'rest'}"></i></button>`).join('')}</div>

    ${todayClasses.length ? `<div class="pclass">${todayClasses.map(c => `<span class="s-${esc(c.subject)}"><b>${esc(c.subject)} 학원</b> ${esc(c.range)}</span>`).join('')}</div>` : ''}
    </div>

    <div class="pright">
    <section>
      ${list.length ? `
        <span class="k">Today's Study</span>
        <p class="psummary">${left.length ? `남은 공부 <b>${left.length}개</b> · 약 ${mins(leftMin)}` : '<b>오늘 공부 끝!</b> 수고했어요.'}</p>
        <div class="plist">${[...left, ...list.filter(isDone)].map(t => taskCard(t)).join('')}</div>`
        : `<div class="empty"><p>이 날은 계획된 공부가 없어요.</p></div>`}
    </section>

    ${late.length && day === today ? `<section>
      <button class="plate" data-late>밀린 공부 ${late.length}개 ${state.showLate ? '접기' : '보기'}</button>
      ${state.showLate ? `<div class="plist">${late.map(t => taskCard(t, { showDate: true })).join('')}</div>` : ''}
    </section>` : ''}
    </div>

    <div class="pscores">${scoreSummary()}</div>

    <p class="note">계획은 구글 시트 <a href="${SHEET_URL}" target="_blank" rel="noopener">'50일 플래너' 탭</a>에서 고칠 수 있어요.
      ${state.sync === 'ok' ? '완료 체크는 가족 기록 시트에도 함께 저장돼요.' : state.sync === 'error' ? '<span class="warn-text">가족 기록 시트에 연결하지 못했어요. 체크는 이 폰에 남겨 두었다가 다음에 다시 보내요.</span>' : state.sync === 'loading' ? '가족 기록 시트와 맞추는 중…' : '완료 체크는 이 폰에만 저장돼요.'}</p>
  </main>
  ${siteFooter()}
  ${familyNav('plan')}`;
}

// 학원 성적 요약: 테스트마다 가장 최근 점수와 통과 여부
function scoreSummary() {
  const latest = new Map();
  for (const r of [...state.scores].sort((a, b) => a.date.localeCompare(b.date))) {
    for (const s of r.scores) latest.set(`${r.academy}|${s.subject}|${s.test}`, { ...s, date: r.date });
  }
  if (!latest.size) return '';
  return `<section><span class="k">Scores</span><h2 class="ph2">학원 성적 <span class="muted small">최근</span></h2><div class="list">
    ${[...latest.values()].map(s => {
      const ok = s.pass == null ? null : s.score >= s.pass;
      return `<a class="row srow-link" href="scores.html"><span class="body"><span class="title">${esc(s.subject)} · ${esc(s.test)}</span>
        <span class="meta">${label(s.date)}</span></span><b>${s.score}/${s.total}</b>${ok == null ? '' : `<span class="flag ${ok ? '' : 'warn'}">${ok ? '✓ 통과' : '! 재시험'}</span>`}</a>`;
    }).join('')}</div></section>`;
}

$root.addEventListener('click', e => {
  const b = e.target.closest('button');
  if (!b) return;
  if (b.dataset.key) {
    const key = b.dataset.key, now = !done[key];
    if (now) done[key] = new Date().toISOString(); else delete done[key];
    saveDone();
    if (familyOn()) { pending.push({ key, done: now }); store(PENDING_KEY, pending); flush(); }
  } else if (b.dataset.go) state.day = addDays(state.day, Number(b.dataset.go));
  else if (b.dataset.day) state.day = b.dataset.day;
  else if (b.hasAttribute('data-today')) state.day = todayKST();
  else if (b.hasAttribute('data-late')) state.showLate = !state.showLate;
  render();
});

loadPlanner()
  .then(d => {
    // '학원 수업' 줄은 체크할 일이 아니라 그날의 학원 시간표로 보여준다
    const isClass = t => t.task.startsWith('학원 수업');
    d.classes = d.tasks.filter(isClass);
    d.tasks = d.tasks.filter(t => !isClass(t)).sort((a, b) => a.date.localeCompare(b.date));
    state.data = d;
  })
  .catch(e => { state.error = e.message === 'not_shared' ? '구글 시트를 읽지 못했어요. 시트 공유를 "링크가 있는 모든 사용자: 보기"로 바꿔 주세요.' : `계획을 불러오지 못했어요 (${e.message})`; })
  .finally(render);
loadFamily().then(render);
render();
