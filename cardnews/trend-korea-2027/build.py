"""두 버전 카드뉴스 HTML 생성: full.html(전체 14장), pick.html(인상 파트 10장)."""
MARK = ('<svg viewBox="100 24 100 252" aria-hidden="true"><g fill="currentColor">'
        '<circle cx="150" cy="86.7" r="45.6"/><path d="M110.8 66C110.6 52 112 38 114.6 31.2Q117 27 120.4 30.4L136 47Z"/>'
        '<path d="M189.2 66C189.4 52 188 38 185.4 31.2Q183 27 179.6 30.4L164 47Z"/><circle cx="150" cy="186.3" r="45.6"/>'
        '<path d="M195.6 196C196 214 191.6 229 182 241C171.6 254 158 263.6 145 269.4C139 272 133.6 273 131.6 269.4C130 266.4 132.6 263.6 137.6 259.4C146 252.4 154 244 158.6 234.6L166 226Z"/></g></svg>')
SRC = '『트렌드 코리아 2027』 저자 강연 정리'


def card(i, total, label, body, blue=False):
    cls = 'card blue' if blue else 'card'
    return f'''<section class="{cls}" id="c{i}">
  <div class="head"><span class="lbl">{label}</span><span class="pg">{i:02d} / {total:02d}</span></div>
  {body}
  <div class="foot"><span class="sig" style="font-family:var(--body);letter-spacing:.02em;font-size:22px">{MARK}오파의 작업실</span><span class="src">{SRC}</span></div>
</section>'''


def pic(name, cap='', h=300):
    c = f'<span>{cap}</span>' if cap else ''
    return f'<div class="pic" style="height:{h}px"><img src="img/{name}.png" alt="">{c}</div>'


def pics(items, h=300):
    return f'<div class="pics c{len(items)} mt-m">' + ''.join(pic(n, c, h) for n, c in items) + '</div>'


def kw(num, axis, title, en, define, rows, insight, images, h=210):
    rs = ''.join(f'<div class="row"><span class="n">{j}</span><div><div class="h">{a}</div>'
                 + (f'<div class="d">{b}</div>' if b else '') + '</div></div>'
                 for j, (a, b) in enumerate(rows, 1))
    return f'''<div class="ktop"><span class="knum" style="font-size:116px">{num}</span><span class="axis">{axis}</span></div>
  <h2 class="mt-m" style="font-size:76px">{title}</h2>
  <div class="en">{en}</div>
  <p class="lead mt-s" style="font-size:29px;line-height:1.5">{define}</p>
  {pics(images, h)}
  <div class="rows mt-m kr">{rs}</div>
  <div class="box pink mt-s" style="padding:24px 34px"><div class="t">For Beauty</div><p style="font-size:28px">{insight}</p></div>'''


def page(title, cards):
    return f'''<!doctype html><html lang="ko"><head><meta charset="utf-8"><title>{title}</title>
<link rel="stylesheet" href="fonts/noto.css"><link rel="stylesheet" href="fonts/jost.css">
<link rel="stylesheet" href="opa-cards.css"></head><body>
{chr(10).join(cards)}
</body></html>'''


# ───────────── 버전 A: 전체 ─────────────
A = []
T = 14
A.append(('Trend Korea 2027', f'''
  <div class="kicker">2027 Consumer Trend</div>
  <h1>트렌드 코리아<br><span class="u">2027</span> 한눈에</h1>
  <p class="lead mt-m">무리에서 먼저 뛰어나오는 양,<br><b>ALPHA SHEEP</b>의 10가지 키워드</p>
  <div class="pic mt-l" style="height:520px;border-radius:40px"><img src="img/flock.png" alt="" style="object-position:center 40%"></div>
''', False))

A.append(('Intro', f'''
  <div class="kicker">The Big Shift</div>
  <h2>2027 키워드엔<br><span class="u">'AI'가 없다</span></h2>
  <p class="lead mt-m">2026년 1번 키워드는 AI였지만, 1년 만에 AI는 전기·스마트폰처럼 <span class="hl">당연한 범용재</span>가 됐어요. 그래서 이제는 AI 때문에 달라진 우리의 모습을 봅니다.</p>
  <div class="box mt-m">
    <div class="t">범용재가 된 AI → 4가지 변화</div>
    <div class="rows" style="border-top:none">
      <div class="row"><span class="n">01</span><div><div class="h">사회의 변화</div><div class="d">권태사회</div></div></div>
      <div class="row"><span class="n">02</span><div><div class="h">개인의 변화</div><div class="d">라이프 ROI · 저장인류 · 하프시그널</div></div></div>
      <div class="row"><span class="n">03</span><div><div class="h">조직의 변화</div><div class="d">바이브 워킹 · 폼팩터 시프트 · 리:텐션 전략</div></div></div>
      <div class="row" style="border-bottom:none"><span class="n">04</span><div><div class="h">우리의 대응</div><div class="d">휴먼엣지 · 해봄경제 · 안목자본</div></div></div>
    </div>
  </div>
''', False))

A.append(('Alpha Sheep', '''
  <div class="kicker">10 Keywords</div>
  <h2 style="font-size:54px">중간이 없는 격변의 시대,<br><span class="u">이끌 것인가, 뒤처질 것인가</span></h2>
  <div class="acro mt-s">
    <div><span class="a">A</span><span class="k">권태사회</span><span class="d">넘치는 자극 속 무료함</span></div>
    <div><span class="a">L</span><span class="k">라이프 ROI</span><span class="d">삶의 모든 선택을 수익률로</span></div>
    <div><span class="a">P</span><span class="k">폼팩터 시프트</span><span class="d">기능은 그대로, 형태를 바꾸다</span></div>
    <div><span class="a">H</span><span class="k">해봄경제</span><span class="d">완벽보다 완료, 일단 해본다</span></div>
    <div><span class="a">A</span><span class="k">저장인류</span><span class="d">일단 저장하고 나중에 고른다</span></div>
    <div><span class="a">S</span><span class="k">바이브 워킹</span><span class="d">사람과 AI가 한 팀처럼</span></div>
    <div><span class="a">H</span><span class="k">리:텐션 전략</span><span class="d">붙잡기보다 돌아올 이유를</span></div>
    <div><span class="a">E</span><span class="k">휴먼엣지</span><span class="d">결과보다 사람의 흔적</span></div>
    <div><span class="a">E</span><span class="k">하프시그널</span><span class="d">갱년기는 후반전의 신호</span></div>
    <div><span class="a">P</span><span class="k">안목자본</span><span class="d">좋은 것을 알아보는 눈</span></div>
  </div>
''', False))

KW = [
 ('01', '사회적 변화', '권태사회', 'Age of Ennui Society',
  '할 일이 없어서가 아니라, <b>과도한 자극에 지쳐</b> 무료함을 느끼는 사회.',
  [('"더 나은 게 있을 텐데 왜 이걸 하고 있지?"', '얼태기·골태기·런태기 — 근본 해결 대신 새 물건으로 권태를 달랜다'),
   ('한국 직장인 몰입도 13.8%', '140개국 중 105위. 3M 15% 룰, 코니카미놀타 사내 부업 제도')],
  '고객은 뷰티 제품 자체에 권태롭다. <b>기다려지는 자극</b>을 설계할 것.',
  [('ennui', '인사이드 아웃 2 · 따분이')]),
 ('02', '개인적 변화', '라이프 ROI', 'Life ROI',
  '인생·일·관계의 모든 국면에서 <b>투자 대비 수익</b>을 따지고, 아니면 손절.',
  [('하루 10명 로테이션 소개팅', '꾸미고 나간 김에 산출을 최대로'),
   ('AI 아바타끼리 먼저 연애해보는 앱', '맞는다는 결과가 나와야 실제로 만난다')],
  '"써보면 압니다"는 안 통한다. <b>첫 경험에서 ROI</b>를 느끼게 하는 두괄식 상품기획.',
  [('volar', 'AI 데이팅 앱 볼라')]),
 ('03', '조직 차원 변화', '폼팩터 시프트', 'Plasticity in the Form Factor Shift',
  '핵심 기능은 그대로, <b>형태·물성·사용 행동</b>을 바꿔 새 시장을 만든다.',
  [('기능 혁신이 한계에 오면 형태가 바뀐다', '카시오 반지시계, 붙이는 영양제'),
   ('뷰티·식품이 가장 활발한 영역', '젤리 틴트, 휘핑크림 같은 선크림')],
  '모양만 바꾸면 실패. <b>"왜 이 형태인가"</b>가 제품의 장점을 말해야 한다.',
  [('tint', '젤리 틴트'), ('whip', '휘핑 선크림'), ('patch', '붙이는 영양제')], 200),
 ('04', '우리의 대응', '해봄경제', "'Have-a-Go' Economy",
  '완벽하게 준비하기보다 <b>일단 해보고</b>, 배우고, 고쳐 나가는 경제.',
  [('폭염에 지친 대학생의 "그늘로" 앱', '그늘로만 걷는 길 안내 — 직접 만들어 해결'),
   ('BYD, 한국에서 일본 브랜드 합계 추월', '"일단 출시 후 개선"이 이 시대에 맞는 속도')],
  '계획 → 실행이 아니라 <b>실행 → 실행 → 최적화</b>. Done is better than perfect.',
  [('shade', '대학생이 만든 그늘 찾는 앱')]),
 ('05', '개인적 변화', '저장인류', 'All is Saved : Homo Archivarius',
  '고른 뒤 저장하지 않고, <b>일단 저장한 뒤 고르는</b> 사람들.',
  [('1TB면 고화질 사진 20년 치', '저장은 싸고, 검색은 쉬워졌다'),
   ('피부 진단서를 모아 AI에게 묻는 소비자', '실장님 추천은 "상술", AI 추천은 "나를 위한 것"')],
  '"데이터 다 꺼내봐"로는 아무것도 안 나온다. <b>목표를 먼저</b> 정하고 쌓을 것.',
  [('drink', '음료 기록 앱 Brewwww')]),
 ('06', '조직 차원 변화', '바이브 워킹', 'Seamless AI Integration : Vibe Working',
  '사람과 AI가 <b>한 팀처럼 맥락을 공유</b>하며 일하도록 업무를 재설계.',
  [('보고서는 2일 → 반나절, 프로젝트는 3개월 그대로', '병목은 조직이 만든다'),
   ('상담 연결 47초 → 5초', '사람이 받고, AI가 요약·해결안 3개 제시')],
  '경진대회 대신 <b>실패 사례</b>를 모아라. 개인의 요령이 조직의 자산이 된다.',
  [('bcg', 'BCG · AI 도입 3단계')]),
 ('07', '조직 차원 변화', '리:텐션 전략', 'Hold on to Your Customers!',
  '경쟁의 중심이 고객 획득에서 <b>고객 유지</b>로. Lock-in에서 Stay-in으로.',
  [('신규 가입 쿠폰, 5천 원엔 안 오고 2만 원엔 온다', '그리고 2만 원만 쓰고 탈퇴'),
   ('역체감 · 환대 · 메모리 · 혜택', '리츠칼튼은 잃어버린 인형의 "호텔 휴가" 사진을 보냈다')],
  '떠나봐야 아는 가치, <b>역체감</b>을 키워라. 다시 돌아올 이유를 만드는 것.',
  [('ritz', '리츠칼튼 · 조시 인형')]),
 ('08', '우리의 대응', '휴먼엣지', 'Every AI Needs the Human Edge',
  'AI가 결과를 쉽게 만드는 시대, <b>사람의 경험·손길·시간</b>이 차별화가 된다.',
  [('AI 모네 실험', 'AI 그림이라 하면 혹평, 원본이라 밝히자 찬사로 반전'),
   ('"예쁘게" 대신 "제 매력 포인트로"', '평균을 넘는 결정은 사람만 할 수 있다')],
  '고생한 과정을 보여줘라. <b>결점·과정·손길·시간</b>이 프리미엄이 된다.',
  [('monet', 'AI 모네 실험'), ('patina', '가죽의 파티나')], 210),
 ('09', '개인적 변화', '하프시그널', "Embracing Menopause : The 'Half Signal'",
  '갱년기를 끝이 아닌 <b>인생 후반전을 알리는 신호</b>로 다시 읽는 흐름.',
  [('X세대는 참지 않는다', '말하고, 소비하고, 필요한 상품을 요구한다'),
   ('호르몬+미용 패키지 약 1,000만 원', '갱년기 보험, 진단 키트까지 — 하나의 시장으로')],
  '갱년기는 상품기획의 <b>중요한 생애 구간</b>. 4050 고객이 가장 큰손이다.',
  [('pubertybook', '『사춘기 대 갱년기』'), ('kit', '갱년기 진단 키트')], 210),
 ('10', '우리의 대응', '안목자본', 'Power of Taste Capital',
  '발굴안·심미안·감식안, <b>좋은 것을 알아보는 눈</b>이 AI 시대 핵심 경쟁력.',
  [('AI를 써도 글을 못 쓰는 이유', '좋은 글이 뭔지 모르기 때문'),
   ('20대가 피부과를 고르는 3순위 "미감"', '대기실 인테리어와 꽃병의 꽃을 본다')],
  '한국인이 가장 좋아하는 칭찬은 <b>"안목 있다"</b>. 고객의 안목을 인정하라.',
  [('aesop', '이솝 매장'), ('clinic', '클리닉 인테리어')], 210),
]
for k in KW:
    A.append((f'Keyword {k[0]}', kw(*k), False))

A.append(('Closing', '''
  <div class="kicker">Last Message</div>
  <h2 style="font-size:76px">"어제의 해결책이<br>오늘의 문제점이다."</h2>
  <p class="lead mt-m">과거의 성공 공식을 흘려보내는 용기.</p>
  <div class="rows mt-l">
    <div class="row"><span class="n">Q1</span><div><div class="h">10년 넘은 브랜드가 올드해지지 않으려면?</div><div class="d">프링글스는 새 맛을 낼 때마다 오리지널이 더 팔린다. 변주를 두려워하지 말 것.</div></div></div>
    <div class="row"><span class="n">Q2</span><div><div class="h">K-뷰티가 다시 뜬 이유는?</div><div class="d">한류가 아니라 제품 그 자체, 특히 속도. 인디 브랜드는 3개월마다 신제품.</div></div></div>
  </div>
  <div class="pills mt-l"><span class="pill">여러분은 어떤 키워드가 와닿았나요?</span></div>
''', True))

# ───────────── 버전 B: 인상 파트 ─────────────
B = []
B.append(('Trend Korea 2027', '''
  <div class="kicker">My Pick · 3 of 10</div>
  <h1>트렌드 코리아<br>2027에서<br><span class="u">내가 꽂힌 3가지</span></h1>
  <div class="pills mt-m"><span class="pill on">바이브 워킹</span><span class="pill sky">하프시그널</span><span class="pill pink">안목자본</span></div>
  <div style="display:flex;justify-content:flex-end;margin-top:auto;margin-bottom:24px"><img class="blend" src="img/sheep.png" alt="" style="height:420px"></div>
''', False))

B.append(('Intro', '''
  <div class="kicker">The Big Shift</div>
  <h2>2027 키워드엔<br><span class="u">'AI'가 없다</span></h2>
  <p class="lead mt-m">2026년 1번 키워드였던 AI가 1년 만에 전기처럼 <span class="hl">당연한 범용재</span>가 됐기 때문이래요.</p>
  <div class="pic mt-l" style="height:400px;border-radius:40px"><img src="img/flock.png" alt="" style="object-position:center 35%"></div>
  <div class="box sky mt-m"><div class="t">Alpha Sheep</div><p>무리(조직)에 기대기만 해선 안 되는 시대. <b>무리에서 먼저 뛰어나와 변화를 시도하는 양</b>이 되자는 뜻.</p></div>
''', False))

B.append(('Pick 01 · Vibe Working', '''
  <div class="ktop"><span class="knum" style="font-size:150px">01</span><span class="axis">조직 차원 변화</span></div>
  <h2 class="mt-m" style="font-size:84px">바이브 워킹</h2>
  <div class="en">Seamless AI Integration</div>
  <p class="lead mt-m">이런 생각, 해본 적 있지 않나요?</p>
  <div class="vs mt-s">
    <div class="side"><div class="s1">AI로 쓰는 내 보고서</div><div class="s2">2일 → 반나절</div></div>
    <div class="mid">VS</div>
    <div class="side on"><div class="s1">우리 팀 프로젝트</div><div class="s2">3개월 그대로</div></div>
  </div>
  <div class="box mt-m"><div class="t">Why</div><p>개인 생산성은 올랐는데 <b>일하는 방식은 그대로</b>. AI로 쓰고 → 흔적 지우고 → 보고하고 → 피드백 받고 → 또 고치고…</p></div>
  <p class="lead mt-m" style="font-size:40px;font-weight:900;color:var(--accent)">"병목은 조직이 만든다."</p>
''', False))

B.append(('Pick 01 · Vibe Working', '''
  <div class="kicker">AI는 아직 신입사원</div>
  <h2>10년 손발 맞춘 동료처럼<br><span class="u">바이브가 통하려면</span></h2>
  <div class="rows mt-m">
    <div class="row"><span class="n">01</span><div><div class="h">우리 회사의 맥락을 학습시키기</div><div class="d">많은 데이터보다 신뢰할 수 있는 맥락. 과거 부품을 학습한 "부품 찾기" 에이전트로 신입도 옛 부품을 찾아 쓴다</div></div></div>
    <div class="row"><span class="n">02</span><div><div class="h">사람과 AI의 역할 나누기</div><div class="d">전화는 무조건 사람이 받고, AI는 실시간 요약 + 해결안 3개. 최종 선택은 사람</div></div></div>
  </div>
  <div class="box ink mt-m" style="display:flex;align-items:center;justify-content:space-between">
    <div><div class="t">상담 연결 시간</div><p style="font-size:26px;color:rgba(250,243,230,.85)">같은 인원으로 더 많은 일</p></div>
    <div style="font-family:var(--display);font-weight:600;font-size:96px;line-height:1">47s<span style="color:var(--sky);font-size:60px"> → </span><span style="color:var(--apricot)">5s</span></div>
  </div>
''', False))

B.append(('Pick 01 · Vibe Working', '''
  <div class="kicker">내일 팀에서 해볼 것</div>
  <h2>바이브 워커가 되는<br><span class="u">3가지 습관</span></h2>
  <div class="box mt-m"><div class="t">Don't</div><p>우수 사례 <b>경진대회</b> — 스트레스만 받고 아무도 안 낸다</p></div>
  <div class="box sky"><div class="t">Do</div><p><b>실패 사례</b>를 모은다. "이렇게 썼더니 망했어"는 다들 신나게 공유하고, 그게 조직의 학습이 된다</p></div>
  <div class="box"><div class="t">Measure</div><p>"AI를 얼마나 썼나"가 아니라 <b>"업무 성과가 얼마나 났나"</b></p></div>
  <div class="pills mt-m"><span class="pill">목적·우선순위 선택</span><span class="pill">예외의 판단</span><span class="pill">결과를 의심하기</span><span class="pill">고객·동료와 소통</span></div>
''', False))

B.append(('Pick 02 · Half Signal', '''
  <div class="ktop"><span class="knum" style="font-size:150px">02</span><span class="axis">개인적 변화</span></div>
  <h2 class="mt-m" style="font-size:84px">하프시그널</h2>
  <div class="en">Embracing Menopause</div>
  <p class="lead mt-m">갱년기는 끝이 아니라<br><span class="hl">인생 후반전을 알리는 하프타임</span></p>
  <div class="vs mt-m">
    <div class="side"><div class="s1">예전 갱년기</div><div class="s2" style="font-size:38px">"남은 10년<br>정리할 때"</div></div>
    <div class="mid">→</div>
    <div class="side on"><div class="s1">100세 시대 갱년기</div><div class="s2" style="font-size:38px">"이제 겨우<br>절반 왔다"</div></div>
  </div>
  <div class="pics c2 mt-m">''' + pic('pubertybook', '『사춘기 대 갱년기』', 280) + pic('sleep', '갱년기 수면 제품', 280) + '''</div>
''', False))

B.append(('Pick 02 · Half Signal', '''
  <div class="kicker">갱년기, 집에서 직장으로</div>
  <h2>이제 갱년기는<br><span class="u">일터의 이슈</span>이기도 하다</h2>
  <p class="lead mt-m" style="font-size:31px">은퇴 뒤에 오던 갱년기가 <b>한창 일할 때</b> 찾아온다. 늦은 출산으로 자녀 사춘기 + 부부 갱년기 + 부모 부양의 <b>3중 파도</b>까지.</p>
  <div class="box mt-m"><div class="t">회사가 함께 챙기기 시작</div><p>이케아 — 갱년기 동료 배려 매뉴얼<br>노무라(일본 금융사) — 갱년기 유급휴가</p></div>
  <div class="box pink"><div class="t">시장도 커지는 중</div><p>호르몬+미용 시술 패키지 <b>약 1,000만 원</b> · 갱년기 보험 · 진단 키트 · 수면 제품</p></div>
  <p class="lead mt-m" style="font-size:36px;font-weight:900;color:var(--accent)">"하프타임은 후반전을 준비하는<br>절호의 시간이다."</p>
''', False))

B.append(('Pick 03 · Taste Capital', '''
  <div class="ktop"><span class="knum" style="font-size:150px">03</span><span class="axis">우리의 대응</span></div>
  <h2 class="mt-m" style="font-size:84px">안목자본</h2>
  <div class="en">Power of Taste Capital</div>
  <p class="lead mt-m" style="font-size:31px">AI를 써도 글을 못 쓰는 사람이 있다.<br>이유는 하나, <span class="hl">좋은 글이 뭔지 모르기 때문.</span></p>
  <div class="pills mt-m"><span class="pill sky">발굴안 · 뜰 것을 보는 눈</span><span class="pill sky">심미안 · 아름다움</span><span class="pill sky">감식안 · 작은 차이</span></div>
  <div class="pics c2 mt-m">''' + pic('aesop', '이솝 매장', 250) + pic('clinic', '클리닉 인테리어', 250) + '''</div>
  <div class="box pink mt-m" style="padding:28px 36px"><div class="t">For Beauty</div><p style="font-size:28px">20대가 피부과를 고르는 3순위 기준은 <b>미감</b>. 판단 근거는 대기실 인테리어와 <b>꽃병의 꽃</b>.</p></div>
''', False))

B.append(('Pick 03 · Taste Capital', '''
  <div class="kicker">안목, 키울 수 있을까?</div>
  <h2>보고 저장만 하면<br><span class="u">안목은 안 생긴다</span></h2>
  <div class="rows mt-m">
    <div class="row"><span class="n">01</span><div><div class="h">좋은 것을 많이 본다</div><div class="d">사진 찍어 저장하는 데서 멈추지 않기</div></div></div>
    <div class="row"><span class="n">02</span><div><div class="h">내 언어로 표현한다</div><div class="d">촌스러워도, 틀려도 OK. "이건 이래서 좋다"</div></div></div>
    <div class="row"><span class="n">03</span><div><div class="h">전문가 평가와 비교한다</div><div class="d">같은 대상을 전문가는 어떻게 봤는지 확인</div></div></div>
    <div class="row"><span class="n">04</span><div><div class="h">오래 반복한다</div><div class="d">쌓이면 그 분야의 안목이 된다</div></div></div>
  </div>
  <div class="box ink mt-m"><p>한국인이 가장 좋아하는 칭찬은 "예쁘다"가 아니라 <b>"안목 있다"</b>. 고객의 안목을 인정하는 브랜드가 팬을 만든다.</p></div>
''', False))

B.append(('Outro', '''
  <div class="kicker">Three in One Line</div>
  <h2 style="font-size:64px">일은 AI와 다시 설계하고,<br>인생은 후반전까지 보고,<br><span class="u">결국 남는 건 사람의 눈.</span></h2>
  <div class="rows mt-l">
    <div class="row"><span class="n">01</span><div><div class="h">바이브 워킹</div><div class="d">AI 도입이 아니라 데이터·조직·사람의 바이브</div></div></div>
    <div class="row"><span class="n">02</span><div><div class="h">하프시그널</div><div class="d">하프타임은 후반전을 준비하는 시간</div></div></div>
    <div class="row"><span class="n">03</span><div><div class="h">안목자본</div><div class="d">AI가 공기가 된 시대, 인간의 무기는 안목</div></div></div>
  </div>
  <p class="lead mt-l" style="font-size:40px;font-weight:900">"어제의 해결책이 오늘의 문제점이다."</p>
  <div class="pills mt-m"><span class="pill">여러분은 어떤 키워드가 와닿았나요?</span></div>
''', True))

for fname, lst in (('full.html', A), ('pick.html', B)):
    n = len(lst)
    html = page(fname, [card(i, n, lab, body, blue) for i, (lab, body, blue) in enumerate(lst, 1)])
    open(fname, 'w').write(html)
    print(fname, n)
