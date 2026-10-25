// 구글 시트를 브라우저에서 바로 읽는다. 서버가 없어도 작동해서 그대로 인터넷에 올릴 수 있다.
// 시트가 '링크가 있는 모든 사용자: 보기'로 공유돼 있어야 읽을 수 있다.
// 마지막으로 읽은 계획은 이 기기에 남겨서, 인터넷이 잠깐 끊겨도 화면이 비지 않게 한다.
export const SHEET_ID = '1HmJ0AtrpRoocs8KZxAcqX3D1NIBUAOePid6u8hQ6_q8';
const CACHE_KEY = 'sosik.planner.cache';

function parseCsv(text) {
  const rows = []; let row = [], cell = '', q = false;
  for (let i = 0; i < text.length; i++) {
    const c = text[i];
    if (q) { if (c === '"' && text[i + 1] === '"') { cell += '"'; i++; } else if (c === '"') q = false; else cell += c; }
    else if (c === '"') q = true;
    else if (c === ',') { row.push(cell); cell = ''; }
    else if (c === '\n') { row.push(cell); rows.push(row); row = []; cell = ''; }
    else if (c !== '\r') cell += c;
  }
  if (cell || row.length) { row.push(cell); rows.push(row); }
  return rows;
}

async function sheetTab(name) {
  const url = `https://docs.google.com/spreadsheets/d/${SHEET_ID}/gviz/tq?tqx=out:csv&headers=0&sheet=${encodeURIComponent(name)}`;
  const res = await fetch(url);
  if (!res.ok || !/csv/.test(res.headers.get('content-type') || '')) throw new Error('not_shared');
  return parseCsv(await res.text());
}

async function readSheet() {
  // 세 탭을 동시에 읽는다. 반영비율·공부 방법 탭은 없어도 플래너는 작동
  const [rows, w, m] = await Promise.all([
    sheetTab('50일 플래너'),
    sheetTab('2학기 평가 반영비율').catch(() => []),
    sheetTab('공부 방법').catch(() => []),
  ]);
  // 구글 CSV 내보내기는 날짜 열의 머리글('날짜')을 빈칸으로 바꾸기도 한다.
  // 그래서 머리글을 찾지 않고, 첫 칸이 날짜(YYYY-MM-DD)인 줄만 할 일로 읽는다.
  const tasks = rows
    .map(r => ({ date: (r[0].match(/\d{4}-\d{2}-\d{2}/) || [''])[0], phase: r[1], subject: r[2], task: r[3], range: r[4], minutes: Number(r[5]) || 0, link: /^https?:\/\//.test(r[6] || '') ? r[6] : '', memo: r[7] || '' }))
    .filter(t => t.date && t.task);
  if (!tasks.length) throw new Error('50일 플래너 탭에서 날짜가 있는 줄을 찾지 못했어요');
  // 2학기 평가 반영비율: 2차(기말) 반영(%)은 G열. 숫자가 있는 과목 줄만 쓴다.
  const weights = {};
  for (const r of w) if (/^[가-힣·]{2,6}$/.test(r[0]?.trim() || '') && Number(r[6])) weights[r[0].trim()] = Number(r[6]);
  // 공부 방법: 과목 | 할 일에 들어간 말 | 방법(줄바꿈으로 단계)
  const methods = m
    .filter(r => r[0] && r[0].trim() !== '과목' && r[2]?.trim())
    .map(r => ({ subject: r[0].trim(), keyword: (r[1] || '').trim(), steps: r[2].split('\n').map(s => s.trim()).filter(Boolean) }));
  return { tasks, weights, methods, fetchedAt: new Date().toISOString(), live: true };
}

export async function loadPlanner() {
  try {
    const data = await readSheet();
    try { localStorage.setItem(CACHE_KEY, JSON.stringify(data)); } catch {}
    return data;
  } catch (e) {
    let cached = null;
    try { cached = JSON.parse(localStorage.getItem(CACHE_KEY)); } catch {}
    if (cached) return { ...cached, live: false, reason: e.message };
    throw e;
  }
}
