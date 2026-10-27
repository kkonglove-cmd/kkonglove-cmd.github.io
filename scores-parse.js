// 학원 문자(사진에서 읽은 글자 또는 붙여넣은 글)에서 점수와 피드백을 찾는다.
// 학원마다 형식이 달라서 여러 모양을 받는다.
//   국어학원)  (1) 국어 / - 과제수행도: 상 / - 어휘테스트: 8/10 / *어휘테스트 통과 기준: 8개
//   영어학원)  ★10/22 학생 시험 성적★ / 1) day 19-22: +118/120 (cut:-12) / => 구두테스트 통과 / ★10/27까지 숙제★ …
// "이름: 점수/만점" 줄은 점수로, "항목: 글" 줄·결과·재시험·숙제는 피드백으로 모은다.
// 학생 이름 같은 개인정보는 저장하지 않도록, 인사말·안내문·'학생'이 들어간 줄은 버리고 문장 앞 이름은 지운다.

// '710' 같은 숫자를 점수/만점으로 나눈다. 만점은 흔한 값(10, 20, 50, 100 …)이고 점수가 만점보다 크지 않아야 한다.
const TOTALS = [5, 10, 15, 20, 25, 30, 40, 50, 60, 100];
function splitScore(digits) {
  for (let i = 1; i < digits.length; i++) {
    const score = Number(digits.slice(0, i)), total = Number(digits.slice(i));
    if (digits[i] !== '0' && TOTALS.includes(total) && score <= total) return { score, total };
  }
  return null;
}

const SKIP = /Web발신|안녕하세요|안내|성취도|입니다\.?$|문의|연락|메시지|보내주|재시험|하원|미통과|통과자|드리겠|바랍니다|감사합니다|학생|^\[|^\]|^#/;
const ENGLISH = /그래머|grammar|독해|듣기|작문|voca|단어|day\s*\d|lesson|reading|listening/i;
const NAME_FIRST = /^[가-힣]{2,4}(?:이가|이는|가|는)\s+/;   // "이현이가 …" → 이름 빼기

// 날짜: ★10/22 학생 시험 성적★ 처럼 시험 날짜가 적혀 있으면 그 날을 쓴다
function testDate(flat, today) {
  const m = flat.match(/(\d{1,2})\s*\/\s*(\d{1,2})\s*(?:일)?\s*(?:학생\s*)?(?:시험|테스트)?\s*(?:성적|결과)/);
  if (!m) return '';
  const [y, tm] = today.split('-').map(Number);
  const mo = Number(m[1]), d = Number(m[2]);
  const year = mo > tm + 1 ? y - 1 : y;   // 12월에 1월 날짜 같은 경우는 거의 없으니, 앞으로 먼 달이면 작년
  return `${year}-${String(mo).padStart(2, '0')}-${String(d).padStart(2, '0')}`;
}

// 괄호 속 통과 기준: (cut:-12) → 만점-12, (cut:108) · (통과 108) → 108
function cutoff(note, total) {
  const m = (note || '').match(/(?:cut|컷|통과|기준)\s*[:：]?\s*([+-]?\d+)/i);
  if (!m) return null;
  const v = Number(m[1]);
  return m[1].startsWith('-') ? total + v : v;
}

export function parseScoreText(raw, today = new Date().toISOString().slice(0, 10)) {
  // 사진 글자 인식은 숫자 사이의 0을 O로, /를 |로 읽기도 해서 먼저 고친다
  const text = raw
    .replace(/(\d)\s*[|lI]\s*(\d)/g, '$1/$2')
    .replace(/(?<=\d)[Oo]|[Oo](?=\d)/g, '0')
    .replace(/[－–—]/g, '-');
  const flat = text.replace(/\s+/g, ' ');
  const academy = (flat.match(/\[([^\]]*학원)\]/) || [])[1]?.trim() || '';
  const session = (flat.match(/(\d+\s*분기\s*\d+\s*강(?:\s*정규\s*수업)?|\d+\s*월\s*\d+\s*주\s*차?)/) || [])[1]?.replace(/\s+/g, ' ') || '';
  const date = testDate(flat, today);

  const lines = text.split(/\r?\n/).map(s => s.trim()).filter(Boolean);
  let subject = '', homework = null;
  const scores = [], feedback = [], pass = {};
  const endHomework = () => {
    if (homework && homework.lines.length) feedback.push({ subject, item: homework.title, text: homework.lines.join(' · ') });
    homework = null;
  };

  for (const l of lines) {
    let m;
    // ★ … ★ 같은 구역 머리줄. 숙제 구역이면 아래 줄들을 숙제 목록으로 모은다
    if (/^[★☆■□◆◇]|[★☆]$/.test(l)) {
      endHomework();
      if (/숙제|과제/.test(l)) {
        const due = l.match(/(\d{1,2}\s*\/\s*\d{1,2})\s*까지/);
        homework = { title: due ? `숙제 (${due[1].replace(/\s/g, '')}까지)` : '숙제', lines: [] };
      }
      continue;
    }
    if (homework) { homework.lines.push(l.replace(/^[-•·*\s]+/, '')); continue; }

    // 과목 머리줄: (1) 국어 / 1. 영어 / [영어]
    if ((m = l.match(/^(?:\(?\s*\d+\s*[).]\s*([가-힣A-Za-z]{1,8})|\[\s*([가-힣A-Za-z]{1,4})\s*\])$/)) && !/학원|발신/.test(l)) { subject = m[1] || m[2]; continue; }
    // 통과 기준: *어휘테스트 통과 기준: 8개
    if ((m = l.match(/([가-힣A-Za-z ]{1,14}?)\s*통과\s*기준\s*[:：]?\s*(\d+)/))) { pass[m[1].replace(/^[-•·*\s]+/, '').trim()] = Number(m[2]); continue; }
    // 점수: 어휘테스트: 8/10 · Reading 18/20 · 1) day 19-22: +118/120 (cut:-12)
    if ((m = l.match(/^[-•·*\s]*(?:\d+\s*[).]\s*)?([가-힣A-Za-z][가-힣A-Za-z0-9 \-~.]{0,20}?)\s*[:：]?\s*\+?(\d+)\s*\/\s*(\d+)\s*(?:점|개)?\s*(?:\((.*)\))?\s*$/))) {
      const total = Number(m[3]);
      scores.push({ subject, test: m[1].trim(), score: Number(m[2]), total, cut: cutoff(m[4], total) });
      continue;
    }
    // 사진 인식이 '/'를 놓친 경우: 어휘테스트: 710 → 7/10 으로 추정하고 확인 표시
    if ((m = l.match(/^[-•·*\s]*([가-힣A-Za-z][가-힣A-Za-z0-9 ]{0,14}?(?:테스트|시험|평가|퀴즈|[Tt]est|[Qq]uiz))\s*[:：]?\s*(\d{2,6})\s*(?:점|개)?$/))) {
      const split = splitScore(m[2]);
      if (split) { scores.push({ subject, test: m[1].trim(), ...split, check: true }); continue; }
    }
    // 결과 줄: => 구두테스트 통과
    if ((m = l.match(/^(?:=>|->|→|⇒)\s*(.+)$/))) { feedback.push({ subject, item: '결과', text: m[1].trim() }); continue; }
    // 재시험 일정 안내 (요일·시간이 있는 문장만, 앞의 이름은 지움)
    if (/재시험/.test(l) && /[월화수목금토일]요일|\d+\s*시/.test(l)) { feedback.push({ subject, item: '재시험', text: l.replace(NAME_FIRST, '') }); continue; }
    if (SKIP.test(l)) continue;
    // 피드백: 과제수행도: 상 / 코멘트: 단어 암기가 부족해요
    if ((m = l.match(/^[-•·*\s]*([가-힣A-Za-z ]{1,12})\s*[:：]\s*(.+)$/))) { feedback.push({ subject, item: m[1].trim(), text: m[2].trim() }); continue; }
    // 과목 안의 나머지 문장은 선생님 말씀으로 모은다 (화면 테두리 등 글자 인식 찌꺼기는 버림)
    const hangul = (l.match(/[가-힣]/g) || []).length;
    if (subject && hangul >= 4 && hangul / l.replace(/\s/g, '').length >= 0.6) feedback.push({ subject, item: '메모', text: l.replace(/^[-•·*\s]+/, '') });
  }
  endHomework();

  // 과목 머리줄이 없는 영어학원 문자는 '영어'로 본다 (확인 화면에서 고칠 수 있음)
  const guess = !scores.some(s => s.subject) && (ENGLISH.test(flat) || /영어/.test(academy)) ? '영어' : '';
  for (const s of scores) {
    s.pass = pass[s.test] ?? s.cut ?? null;
    delete s.cut;
    // 직접 쓴 "영어 단어시험: 18/20" → 과목 영어, 시험 단어시험
    const m = s.test.match(/^(국어|영어|수학|과학|논술|역사|한문|사회)\s+(.+)$/);
    if (m && (!s.subject || s.subject === m[1])) { s.subject = m[1]; s.test = m[2]; }
    if (!s.subject) s.subject = guess;
  }
  for (const f of feedback) if (!f.subject) f.subject = guess;
  return { academy, session, date, scores, feedback };
}
