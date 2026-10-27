"""전체 키워드 14장 (에디토리얼 스타일): 아이보리 종이 위에 세리프 번호, 핵심 인사이트,
사례 사진 두 장 + CASE 설명, FOR BEAUTY 박스. 사진은 ../img 에서 가져온다."""
import math

N = 15
SRC = '『트렌드 코리아 2027』 전미영 연구위원 강연 정리'


def burst(cx, cy, r, color, n, op):
    lines = ''.join(
        f'<line x1="{cx + r * .14 * math.cos(a):.1f}" y1="{cy + r * .14 * math.sin(a):.1f}" '
        f'x2="{cx + r * math.cos(a):.1f}" y2="{cy + r * math.sin(a):.1f}"/>'
        for a in (2 * math.pi * k / n for k in range(n)))
    return f'<g stroke="{color}" stroke-width="1.2" stroke-opacity="{op}">{lines}</g>'


DECO = ('<svg class="deco" viewBox="0 0 1080 1350" aria-hidden="true">'
        + burst(1040, 250, 200, '#8EC3F0', 140, .42) + burst(905, 330, 85, '#1117A9', 90, .16) + '</svg>')


def card(i, meta, body):
    return f'''<section class="card" id="c{i}">{DECO}
  <div class="top"><span>{meta}</span><b>{i:02d} / {N}</b></div>
  {body}
  <div class="foot"><span>오파의 작업실</span><span>{SRC}</span></div>
</section>'''


def photo(name, cls=''):
    if name.startswith('quote:'):  # 사진이 없는 사례는 인용 타일로
        return f'<div class="ph qt {cls}"><p>{name[6:]}</p></div>'
    return f'<div class="ph {cls}"><img src="../img/{name}.png" alt=""></div>'


def kw(i, num, ko, en, define, insight, cases, beauty):
    cs = ''.join(f'''<div class="case">{photo(img)}<div class="cl">CASE {j:02d}</div>
      <div class="ch">{head}</div><div class="cd">{desc}</div></div>''' for j, (img, head, desc) in enumerate(cases, 1))
    return card(i, f'KEYWORD {num} / 10', f'''
  <div class="title"><em>{num}</em>{ko}</div>
  <div class="en">{en}</div>
  <p class="def">{define}</p>
  <hr>
  <div class="lab">핵심 인사이트</div>
  <h3>{insight}</h3>
  <div class="cases">{cs}</div>
  <div class="beauty"><span>시사점</span>{beauty}</div>''')


KW = [
    ('01', '권태사회', 'Age of Ennui Society', '자극은 넘치는데, 마음은 더 쉽게 심심해지는 사회.',
     '더 채우는 것보다, 의미 있는 경험을 골라야 해요.',
     [('runtae', '런태기 · 골태기 · 얼태기', '권태가 오면 근본을 고민하기보다 새 운동화, 새 골프채를 사요.'),
      ('bookstore', '단 한 권만 파는 서점', '도쿄 모리오카 서점. 덜어낸 큐레이션이 오히려 만족을 높여요.')],
     '제품을 더 보여주기보다,<br><b>기다려지는 자극과 고를 이유</b>를 선명하게.'),
    ('02', '라이프 ROI', 'Life ROI', '시간·노력·관계까지, 삶의 모든 선택을 수익률로 계산하는 태도.',
     '가성비를 넘어서, 내 시간과 에너지가 중요해졌어요.',
     [('volar', 'AI 아바타 데이팅 앱', '내 성향을 닮은 AI끼리 먼저 연애해 보고, 잘 맞으면 만나요.'),
      ('petpred', '반려견 미래 진료비 예측', '입양 전에 평생 병원비를 미리 계산해 주는 서비스.')],
     '"써보면 압니다"는 안 통해요.<br><b>첫 경험에서 가치</b>가 느껴지게.'),
    ('03', '폼팩터 시프트', 'Plasticity in the Form Factor Shift', '기능은 그대로 두고, 형태·물성·사용 방식을 바꿔 새 시장을 여는 변화.',
     '새로운 기능보다, 손에 쥐는 경험이 중요해졌어요.',
     [('tint', '물성 시프트', '젤리처럼 탱글한 틴트, 휘핑크림처럼 짜서 바르는 선크림.'),
      ('casio_ring', '카시오 반지시계', '디지털시계를 그대로 반지로. 강연자가 직접 끼고 와서 보여준 사례예요.')],
     '모양만 바꾸면 실패해요.<br><b>"왜 이 형태인가"</b>가 장점을 말해야 해요.'),
    ('04', '해봄경제', "'Have-a-Go' Economy", '완벽하게 준비하기보다, 일단 해보고 고쳐 나가는 경제.',
     '실행해 본 사람이 다음 기회를 더 빨리 찾아요.',
     [('shade', '그늘로만 걷는 길', '폭염에 지친 대학생이 직접 만든 길 안내 앱.'),
      ('solo', '1인 기업의 성장', 'AI·노코드로 실행 비용이 낮아지며 혼자 만드는 사람이 늘어요.')],
     '완벽한 기획서보다 <b>작은 출시와 빠른 개선</b>.<br>Done is better than perfect.'),
    ('05', '저장인류', 'All is Saved : Homo Archivarius', '고른 뒤 저장하지 않고, 일단 저장한 뒤 고르는 사람들.',
     '모아 둔 데이터보다, 다시 쓰는 데이터가 자산이에요.',
     [('drink', '매일 마신 음료 기록', '사진첩 속 음료만 모아 요일별로 정리해 주는 앱.'),
      ('repov', '취향 기록 앱', '본 영화와 읽은 책이 쌓이면 나만의 자서전이 돼요.')],
     '고객 데이터는 <b>목표를 먼저 정하고</b> 쌓아야<br>기회가 보여요.'),
    ('06', '바이브 워킹', 'Seamless AI Integration : Vibe Working', '사람과 AI가 한 팀처럼 맥락을 공유하며 일하는 방식.',
     '생산성의 병목은 AI가 아니라 조직에 있어요.',
     [('jcurve', '보고서 2일 → 반나절', '그런데 팀 프로젝트는 여전히 3개월. 일하는 방식이 그대로라서.'),
      ('cba', '맥락 없는 도입의 실패', 'AI 음성봇을 서둘러 도입했다가 되돌린 해외 은행 사례.')],
     '우수 사례 경진대회 대신 <b>실패 사례</b>를 모으세요.<br>그게 팀의 학습이 돼요.'),
    ('07', '리:텐션 전략', 'Hold on to Your Customers! Retention Strategy', '경쟁의 중심이 신규 고객에서, 다시 오게 하는 힘으로.',
     '신규 고객보다, 지금 고객이 계속 머물 이유를 만들어야 해요.',
     [('dawn', '역체감 리텐션', '떠나 봐야 아는 가치. 새벽배송을 한번 쓰면 돌아가기 어려워요.'),
      ('quote:새 맛을 낼수록<br>오리지널이<br>더 잘 팔린다', '프링글스의 변주', '새 맛을 계속 내는 이유는, 그럴 때마다 오리지널이 더 팔리기 때문이래요.')],
     '쿠폰으로 붙잡기보다 <b>돌아올 이유</b>를.<br>만족한 고객이 다음 고객을 데려와요.'),
    ('08', '휴먼엣지', 'Every AI Needs the Human Edge', 'AI가 결과를 쉽게 만드는 시대, 사람의 경험·손길·시간이 차별화가 된다.',
     'AI가 답을 늘릴수록, 사람이 고르는 기준이 남아요.',
     [('monet', 'AI 모네 실험', 'AI 그림이라 하면 혹평, 원본이라 밝히자 찬사로 반전.'),
      ('patina', '시간의 엣지', '오래 쓸수록 멋이 드는 가죽의 파티나.')],
     '결과만이 아니라 <b>어떻게 만들었는지</b>,<br>고생한 흔적을 보여주세요.'),
    ('09', '하프시그널', "Embracing Menopause : The 'Half Signal'", '갱년기를 끝이 아닌, 인생 후반전을 알리는 신호로 다시 읽는 흐름.',
     "'이제 겨우 절반'이라는 관점이 인상적이었어요.",
     [('kit', '갱년기 진단 키트', '감추고 견디던 증상을 정확히 진단하고 관리해요.'),
      ('sleep', '갱년기 수면 제품', 'X세대는 참지 않아요. 말하고, 소비하고, 준비해요.')],
     '갱년기는 상품기획의 <b>중요한 생애 구간</b>.<br>4050이 가장 큰손이에요.'),
    ('10', '안목자본', 'Power of Taste Capital', '좋은 것을 발견하고, 판별하고, 고르는 감각이 경쟁력이 되는 시대.',
     '같은 AI를 써도 결과가 다른 건, 결국 보는 눈이에요.',
     [('aesop', '공간의 미감', '이솝처럼 매장 디테일을 일관되게 지키는 브랜드.'),
      ('clinic', '꽃병으로 고르는 피부과', '20대는 대기실 인테리어와 꽃병의 꽃으로 의사의 미감을 판단해요.')],
     '고객의 안목을 인정해 주세요.<br><b>"안목 있다"</b>가 가장 큰 칭찬이에요.'),
]

def chips(ks):
    return '<div class="chips">' + ''.join(f'<span>{k}</span>' for k in ks) + '</div>'


cards = [card(1, 'TREND KOREA 2027 &nbsp;/&nbsp; THE OVERVIEW', '''
  <div class="lab big">AN EDITORIAL NOTE · 2027</div>
  <h1>트렌드 코리아 2027<br><span>한눈에</span></h1>
  <p class="def">10개 키워드를 다 듣고 나니,<br>결국 <b class="u">두 문장</b>이 남았어요.</p>
  <div class="ph hero">''' + '<img src="../img/flock.png" alt="">' + '''</div>
  <div class="banner">넘겨서 두 문장부터 확인해 보세요 <b>→</b></div>'''),
         card(2, 'MESSAGE 01 / 02', '''
  <div class="msg">
    <div class="lab big">첫 번째 문장</div>
    <h2 class="big">풍요의 시대에는<br><span>결핍보다 과잉이</span><br>문제가 돼요.</h2>
    <p class="lead">더 많은 선택지보다<br>의미 있는 경험과 <b>선별</b>이 중요해져요.</p>
    <div class="lab">이 문장을 풀어주는 키워드</div>''' + chips(['권태사회', '라이프 ROI', '저장인류', '안목자본']) + '''
  </div>'''),
         card(3, 'MESSAGE 02 / 02', '''
  <div class="msg">
    <div class="lab big">두 번째 문장</div>
    <h2 class="big">AI는 기본값,<br><span>성과는 일하는 방식을</span><br>바꿀 때 생겨요.</h2>
    <p class="lead">도구를 들이는 것과<br>일과 조직을 다시 설계하는 건 <b>별개의 과제</b>예요.</p>
    <div class="lab">이 문장을 풀어주는 키워드</div>''' + chips(['바이브 워킹', '해봄경제', '폼팩터 시프트', '리:텐션 전략', '휴먼엣지', '하프시그널']) + '''
  </div>
  <div class="banner">이제 10개 키워드를 하나씩 풀어볼게요 <b>→</b></div>''')]
cards += [kw(i, *k) for i, k in enumerate(KW, 4)]
cards.append(card(14, 'WHAT STAYS AFTER THE TALK', '''
  <div class="msg">
    <div class="lab big">강연의 마지막 문장</div>
    <h2 class="big quote">"어제의 해결책이<br><span>오늘의 문제점</span>이다."</h2>
    <p class="lead">어제 문제를 풀 때 유용했던 지식이<br>오늘은 발목을 잡을 수도 있어요.</p>
    <p class="lead close">그래서 필요한 건,<br><b>과거의 성공 공식을 흘려보내는 용기.</b></p>
  </div>'''))
cards.append(card(15, 'SAVE THIS PAGE', '''
  <div class="lab big">저장용 한 장 요약</div>
  <h2>2027 키워드 10</h2>
  <p class="def">무리에서 가장 먼저 변화를 시도하는 양, ALPHA SHEEP.</p>
  <div class="grid10">''' + ''.join(
    f'<div><em>{a}</em><b>{k}</b><p>{d}</p></div>' for a, k, d in [
        ('A', '권태사회', '넘치는 자극 속 무료함'), ('S', '바이브 워킹', '사람과 AI가 한 팀처럼'),
        ('L', '라이프 ROI', '삶의 모든 선택을 수익률로'), ('H', '리:텐션 전략', '붙잡기보다 돌아올 이유를'),
        ('P', '폼팩터 시프트', '기능은 그대로, 형태를 바꾸다'), ('E', '휴먼엣지', '결과보다 사람의 흔적'),
        ('H', '해봄경제', '완벽보다 완료, 일단 해본다'), ('E', '하프시그널', '갱년기는 후반전의 신호'),
        ('A', '저장인류', '일단 저장하고 나중에 고른다'), ('P', '안목자본', '좋은 것을 알아보는 눈')]) + '''</div>
  <div class="banner">내년 기획 전에 다시 꺼내 보세요 <b>📌</b></div>'''))

open('full.html', 'w').write('''<!doctype html><html lang="ko"><head><meta charset="utf-8"><title>full</title>
<link rel="stylesheet" href="../fonts/noto.css"><link rel="stylesheet" href="../fonts/extra.css">
<link rel="stylesheet" href="full.css"></head><body>
''' + '\n'.join(cards) + '\n</body></html>')
print(len(cards))
