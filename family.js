// 가족 연결 — 비공개 구글 시트(엄마 계정의 Apps Script)에 플래너 완료 체크와 학원 성적을 저장해서,
// 엄마 폰과 아이 폰이 같은 기록을 본다. 가족 코드를 아는 폰만 읽고 쓸 수 있다.
// 가족 코드는 이 파일(공개 저장소)에 넣지 않는다. 처음 한 번 '주소#family=코드' 링크로 열면 그 폰이 기억한다.

// Apps Script 웹 앱 주소 (엄마가 배포한 뒤 채움). 비어 있으면 모든 기록은 이 폰에만 저장된다.
export const FAMILY_API = 'https://script.google.com/macros/s/AKfycbzNZeWg5wJbn4oaej5CE60bcn9UJkac55Glz3oz_Dh1hM1hAR3u8iyCNba3kkUFgT2Eyw/exec';
const CODE_KEY = 'family.code';

(function rememberCode() {
  const m = location.hash.match(/family=([\w-]+)/);
  if (!m) return;
  try { localStorage.setItem(CODE_KEY, m[1]); } catch {}
  history.replaceState(null, '', location.pathname + location.search);
})();

export function familyCode() { try { return localStorage.getItem(CODE_KEY) || ''; } catch { return ''; } }
export const familyOn = () => !!(FAMILY_API && familyCode());

export async function familyGet() {
  const res = await fetch(`${FAMILY_API}?action=data&code=${encodeURIComponent(familyCode())}`);
  const d = await res.json();
  if (d.error) throw new Error(d.error);
  return d;
}

// text/plain 으로 보내야 브라우저가 사전 확인 요청 없이 Apps Script로 바로 보낸다
export async function familyPost(body) {
  const res = await fetch(FAMILY_API, { method: 'POST', headers: { 'content-type': 'text/plain;charset=utf-8' }, body: JSON.stringify({ ...body, code: familyCode() }) });
  const d = await res.json();
  if (d.error) throw new Error(d.error);
  return d;
}

// 모든 화면 맨 아래 만든 사람 표시 (플래너·학원 성적·엄마들 공유용 공통)
// 오파의 작업실 푸터처럼: 왼쪽 고양이 마크 + 이름, 오른쪽 인스타·작업실 사이트 알약 버튼 (좁은 폰에서는 아래 줄로)
export function siteFooter() {
  // 가족 사이트는 아이가 매일 보는 화면이라 맨 아래에 아주 작고 흐리게 한 줄만
  if (document.body.dataset.site === 'family') return `<footer class="sfoot-quiet">created by opa ·
    <a href="https://www.instagram.com/open.pouch_/" target="_blank" rel="noopener me">@open.pouch_</a> ·
    <a href="https://openpouch.kr/" target="_blank" rel="noopener me">openpouch.kr</a></footer>`;
  return `<footer class="sfoot"><div class="sfoot-in">
    <span class="sfoot-by"><img src="opa-mark.svg" alt="" width="9" height="22">created by opa</span>
    <span class="sfoot-links"><a class="sfoot-ig" href="https://www.instagram.com/open.pouch_/" target="_blank" rel="noopener me" aria-label="Instagram @open.pouch_ (새 탭에서 열림)">
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r=".6" fill="currentColor"/></svg>
      <span aria-hidden="true">@open.pouch_</span></a>
    <a class="sfoot-ig" href="https://openpouch.kr/" target="_blank" rel="noopener me" aria-label="오파의 작업실 openpouch.kr (새 탭에서 열림)">
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3a14 14 0 0 1 0 18M12 3a14 14 0 0 0 0 18"/></svg>
      <span aria-hidden="true">openpouch.kr</span></a></span>
  </div></footer>`;
}

// 가족 사이트(플래너+성적)에서만 보이는 아래 메뉴. 엄마들 공유용 성적 페이지에는 나오지 않는다.
export function familyNav(active) {
  if (document.body.dataset.site !== 'family') return '';
  const tab = (href, key, text) => `<a href="${href}" class="${active === key ? 'on' : ''}">${text}</a>`;
  return `<nav class="tabs fnav">${tab('planner.html', 'plan', '오늘 공부')}${tab('scores.html', 'scores', '학원 성적')}</nav>`;
}
