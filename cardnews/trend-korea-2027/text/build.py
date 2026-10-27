"""텍스트 카드뉴스: 진한 울트라마린(#0B0F7A)과 연하늘(#E3F0FC) 바탕을 번갈아 쓰고,
작은 라벨 + 굵은 제목 + 본문으로 위계를 준다. 본문의 [[ ]] 는 밑줄 강조."""
import re

SLIDES = [
    dict(k='강연에서 남은 질문', t='AI가 다 만들어주는 시대,\n사람에게 남는 건 뭘까요?',
         b=["트렌드 코리아 2027 키워드에는 'AI'가 없어요.\n이미 공기처럼 당연해졌으니까요.",
            '강연이 내놓은 답은 세 가지였어요.\n[[해봄경제 · 휴먼엣지 · 안목자본]]']),
    dict(k='01 · 해봄경제', t='완벽하게 준비하느라\n아직 시작 못 한 일, 있나요?',
         b=["폭염에 지친 한 대학생은\n'그늘로만 걷는 길 안내 앱'을 직접 만들었어요.",
            'AI로 실행 비용이 거의 0이 된 지금,\n경쟁력은 [[무엇을 실제로 해봤는가]]예요.']),
    dict(k='01 · 해봄경제', t='북한산에서 가장\n오르기 어려운 코스는?',
         b=["정답은 '우리 집 대문'이래요.",
            '계획 → 실행이 아니라\n실행 → 실행 → 개선.',
            '[[해보는 사람과 안 해보는 사람]]의\n격차가 벌어지는 시대예요.']),
    dict(k='02 · 휴먼엣지', t='AI가 그렸다고 하면 혹평,\n원본이라 하면 찬사',
         b=["AI로 그린 모네의 '수련'이라며 올리자\n\"색이 별로\"라는 댓글이 달렸어요.",
            '사실 원본이었다고 밝히자\n\"역시 색이 오묘하다\"로 바뀌었죠.',
            '결과가 같아도 사람들은\n[[사람의 흔적]]에 값을 매겨요.']),
    dict(k='02 · 휴먼엣지', t='고생한 흔적이\n프리미엄이 돼요',
         steps=[('결정', '"예쁘게"보다 "제 매력 포인트로"'), ('과정', '메이킹 필름을 보면 결과가 달라 보여요'),
                ('손길', '만지고 바르는 손끝의 즐거움'), ('시간', '오래 쓸수록 멋이 드는 가죽처럼')],
         b=['결과만이 아니라 [[어떻게 만들었는지]]를 보여주세요.']),
    dict(k='03 · 안목자본', t='"너 감각 있다"\n한국인이 가장 좋아하는 칭찬',
         b=['"예쁘다"보다 "안목 있다"는 말에\n더 기뻐한대요.',
            'AI가 매끈한 결과물을 무한히 만드는 시대,\n[[한 끗 차이를 알아보고 고르는 눈]]이\n자본이 돼요.']),
    dict(k='03 · 안목자본', t='AI를 써도\n글을 못 쓰는 이유',
         b=['좋은 글이 뭔지 모르기 때문이에요.',
            "20대가 피부과를 고르는 3순위 기준은 '미감'.\n대기실 인테리어와 [[꽃병의 꽃]]을 보고 판단해요."]),
    dict(k='03 · 안목자본', t='그럼 안목은\n어떻게 키울까요?',
         steps=[('01', '좋은 것을 많이 보고'), ('02', '사진만 찍지 말고 내 언어로 표현하고'),
                ('03', '전문가의 평가와 비교해 보고'), ('04', '오래 반복하기')],
         b=['촌스러워도, 틀려도 괜찮아요.\n일단 [[말로 꺼내는 게]] 시작이에요.']),
    dict(k='세 키워드의 연결', t='안목은 결국\n해봄에서 자라요',
         b=['보고, 써보고, 골라보고, 틀려보는 시간.\n돈과 시간과 노력이 드는 일이라\n직접 해본 사람에게만 쌓여요.',
            '[[해봄 → 안목 → 휴먼엣지]]\n해봐야 보이고, 보여야 나만의 엣지가 생겨요.']),
    dict(k='브랜드에게', t='고객의 안목을\n인정해 주세요',
         b=['"이 차이를 알아보셨네요."',
            '안목을 인정받은 고객이\n자발적으로 [[브랜드를 알리는 프로모터]]가 돼요.']),
    dict(k='강연의 마지막 문장', t='어제의 해결책이\n오늘의 문제점이에요',
         b=['잘해온 방식을 지키는 것과\n익숙한 방식만 고집하는 건\n다른 일이니까요.']),
    dict(k='저장용 한 장 요약', t='트렌드 코리아 2027\nALPHA SHEEP',
         table=[('A', '권태사회', '넘치는 자극 속 무료함'), ('L', '라이프 ROI', '모든 선택을 수익률로'),
                ('P', '폼팩터 시프트', '기능은 그대로, 형태를 바꾸다'), ('H', '해봄경제', '완벽보다 완료, 일단 해본다', 1),
                ('A', '저장인류', '일단 저장하고 나중에 고른다'), ('S', '바이브 워킹', '사람과 AI가 한 팀처럼'),
                ('H', '리:텐션 전략', '붙잡기보다 돌아올 이유를'), ('E', '휴먼엣지', '결과보다 사람의 흔적', 1),
                ('E', '하프시그널', '갱년기는 후반전의 신호'), ('P', '안목자본', '좋은 것을 알아보는 눈', 1)],
         b=[]),
]


def fmt(t):
    t = t.replace('\n', '<br>')
    return re.sub(r'\[\[(.+?)\]\]', r'<em>\1</em>', t, flags=re.S)


N = len(SLIDES)
cards = []
for i, s in enumerate(SLIDES, 1):
    tone = 'dark' if i % 2 else 'light'
    parts = [f'<div class="k">{s["k"]}</div>', f'<h2>{fmt(s["t"])}</h2>']
    if 'steps' in s:
        parts.append('<ol class="steps">' + ''.join(f'<li><span>{a}</span>{x}</li>' for a, x in s['steps']) + '</ol>')
    if 'table' in s:
        parts.append('<div class="tbl">' + ''.join(
            f'<div class="tr{" on" if len(r) > 3 else ""}"><b>{r[0]}</b><strong>{r[1]}</strong><span>{r[2]}</span></div>'
            for r in s['table']) + '</div>')
    if 'qs' in s:
        parts.append('<ol class="qs">' + ''.join(f'<li><span>{j:02d}</span>{x}</li>' for j, x in enumerate(s['qs'], 1)) + '</ol>')
    parts += [f'<p>{fmt(p)}</p>' for p in s['b']]
    cards.append(f'''<section class="card {tone}" id="c{i}">
  <div class="top"><span>TREND KOREA 2027</span><span>{i:02d} / {N:02d}</span></div>
  <div class="txt">{''.join(parts)}</div>
  <div class="foot"><span>오파의 작업실</span><span>『트렌드 코리아 2027』 전미영 연구위원 강연 정리</span></div>
</section>''')

open('text.html', 'w').write(f'''<!doctype html><html lang="ko"><head><meta charset="utf-8"><title>text cards</title>
<link rel="stylesheet" href="../fonts/noto.css">
<style>
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
body {{ background: #888; }}
.card {{ width: 1080px; height: 1350px; margin: 0 auto 30px; padding: 72px 76px; display: flex; flex-direction: column;
  font-family: 'Noto Sans KR', sans-serif; text-align: center; word-break: keep-all; letter-spacing: -0.02em; }}
.dark {{ background: #0B0F7A; color: #FAF3E6; --k: #8FD0FF; --sub: rgba(250,243,230,.85); --line: #8FD0FF; --meta: rgba(250,243,230,.6); }}
.light {{ background: #E3F0FC; color: #0B0F7A; --k: #3D6FC4; --sub: #2A2F66; --line: #7FB2EA; --meta: rgba(11,15,122,.6); }}
.top, .foot {{ display: flex; justify-content: space-between; font-size: 21px; font-weight: 500; color: var(--meta); letter-spacing: .02em; }}
.txt {{ flex: 1; display: flex; flex-direction: column; justify-content: center; align-items: center; }}
.k {{ font-size: 25px; font-weight: 500; color: var(--k); margin-bottom: 26px; }}
h2 {{ font-size: 62px; font-weight: 700; line-height: 1.32; letter-spacing: -0.04em; margin-bottom: 56px; }}
p {{ font-size: 36px; font-weight: 400; line-height: 1.6; color: var(--sub); }}
p + p {{ margin-top: 38px; }}
em {{ font-style: normal; font-weight: 700; color: inherit; text-decoration: underline; text-decoration-color: var(--line);
  text-decoration-thickness: 5px; text-underline-offset: 10px; }}
.dark em {{ color: #FFFFFF; }}
.steps, .qs {{ list-style: none; text-align: left; margin-bottom: 44px; }}
.steps li, .qs li {{ font-size: 35px; line-height: 1.5; padding: 12px 0; color: var(--sub); font-weight: 500; }}
.steps span, .qs span {{ display: inline-block; width: 64px; font-size: 24px; font-weight: 700; color: var(--k); vertical-align: 4px; }}
.qs li {{ font-size: 32px; padding: 10px 0; }}
.steps span {{ width: 86px; }}
.tbl {{ width: 100%; text-align: left; margin-top: -16px; }}
.tr {{ display: grid; grid-template-columns: 64px 250px 1fr; align-items: center; padding: 14px 22px; border-bottom: 1px solid rgba(11,15,122,.12); }}
.tr b {{ font-size: 34px; font-weight: 700; color: var(--k); }}
.tr strong {{ font-size: 31px; font-weight: 700; }}
.tr span {{ font-size: 25px; color: var(--sub); }}
.tr.on {{ background: #FFFFFF; border-radius: 14px; border-bottom-color: transparent; box-shadow: 0 6px 18px -10px rgba(11,15,122,.35); }}
.tr.on b, .tr.on strong {{ color: #0B0F7A; }}
</style></head><body>
{chr(10).join(cards)}
</body></html>''')
print(N)
