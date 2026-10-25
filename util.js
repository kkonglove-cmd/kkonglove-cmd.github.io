// 날짜는 모두 한국 시간(Asia/Seoul) 기준 'YYYY-MM-DD' 문자열로 다룬다.
export const WD = '일월화수목금토';

export function todayKST() {
  return new Intl.DateTimeFormat('en-CA', { timeZone: 'Asia/Seoul', year: 'numeric', month: '2-digit', day: '2-digit' }).format(new Date());
}
const ms = ymd => { const [y, m, d] = ymd.split('-').map(Number); return Date.UTC(y, m - 1, d); };
const toYmd = t => new Date(t).toISOString().slice(0, 10);

export const mk = (y, m, d) => `${y}-${String(m).padStart(2, '0')}-${String(d).padStart(2, '0')}`;
export const addDays = (ymd, n) => toYmd(ms(ymd) + n * 864e5);
export const wd = ymd => new Date(ms(ymd)).getUTCDay();
export const diffDays = (a, b) => Math.round((ms(b) - ms(a)) / 864e5);
export const weekStart = ymd => addDays(ymd, -((wd(ymd) + 6) % 7)); // 월요일 시작
export const compact = ymd => ymd.replaceAll('-', '');
export const fromCompact = s => `${s.slice(0, 4)}-${s.slice(4, 6)}-${s.slice(6, 8)}`;

export function isValid(y, m, d) {
  const t = new Date(Date.UTC(y, m - 1, d));
  return t.getUTCMonth() === m - 1 && t.getUTCDate() === d;
}

export function label(ymd, withYear = false) {
  if (!ymd) return '날짜 미정';
  const [y, m, d] = ymd.split('-').map(Number);
  return `${withYear ? y + '년 ' : ''}${m}월 ${d}일 (${WD[wd(ymd)]})`;
}

export function dday(ymd, today = todayKST()) {
  const n = diffDays(today, ymd);
  if (n === 0) return '오늘';
  if (n === 1) return '내일';
  return n > 0 ? `D-${n}` : `${-n}일 지남`;
}

export function esc(s) {
  return String(s ?? '').replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
}

// 같은 안내문을 다시 넣었는지 알아보기 위한 지문(공백을 지운 뒤 계산)
export function fingerprint(text) {
  const s = text.replace(/\s+/g, '');
  let h = 5381;
  for (let i = 0; i < s.length; i++) h = ((h << 5) + h + s.charCodeAt(i)) | 0;
  return (h >>> 0).toString(36) + s.length.toString(36);
}

export const uid = () => Date.now().toString(36) + Math.random().toString(36).slice(2, 7);
