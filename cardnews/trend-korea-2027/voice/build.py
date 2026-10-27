"""텍스트 카드뉴스: 진한 울트라마린(#0B0F7A)과 연하늘(#E3F0FC) 바탕을 번갈아 쓰고,
작은 라벨 + 굵은 제목 + 본문으로 위계를 준다. 본문의 [[ ]] 는 밑줄 강조."""
import re

SLIDES = [
    dict(k='트렌드 코리아 2027을 듣고', t="10개 키워드를 듣는 내내\n'맞아, 맞아' 했어요",
         b=['그런데 듣다 보니\n전부 [[내 얘기]]였어요.']),
    dict(k='권태사회', t='풍요로우니까\n빨리 지겨워져요',
         b=['새로운 게 매일 쏟아지니\n금방 또 다음 걸 찾게 되죠.',
            '그래서 요즘은 이렇게 생각해요.\n[[괜찮으면, 그냥 즐기자.]]']),
    dict(k='라이프 ROI', t='사랑까지\nROI를 따지는 시대',
         b=['성향을 넣은 AI 아바타끼리 먼저 데이트해 보고\n잘 맞으면 만난대요.',
            '처음엔 충격이었는데,\n상처받지 않고 [[미리 해볼 수 있다면]]\n나쁘지 않겠다 싶었어요.',
            '생각해 보면 나도 이미\n매일 ROI를 따지고 있더라고요.']),
    dict(k='저장인류', t='다 저장하는데,\n그게 누구에게 좋은 일일까?',
         b=['사진, 캡처, 나에게 보내기.\n내 데이터는 매일 쌓이는데',
            '그게 결국 누구에게 좋은 일인지\n[[가끔 멈칫]]하게 돼요.\n물론 나도 오늘 또 저장했지만요.']),
    dict(k='폼팩터 시프트', t='완전히 새로 만들기보다\n살짝 비틀어 보기',
         b=['기능은 그대로, 형태만 바꿔도\n사람들은 새롭다고 느껴요.',
            '회사에서 [[당장 해볼 수 있는]]\n가장 현실적인 혁신 같았어요.']),
    dict(k='해봄경제 × 권태사회', t='요즘 나는\n엄청 해보는 중이에요',
         b=['작업실도 만들고, 카드뉴스도 만들고.\n생각한 게 뚝딱 만들어지니 재밌어요.',
            '그런데 가끔 허무해져요.\n이 마음은 뭘까요.\n[[풍요 속에 오는 권태]]일까요.']),
    dict(k='바이브 워킹', t='회사는 AI 에이전트를\n만들라고 하는데',
         b=['솔직히 내가 쌓은 노하우를\n회사에 다 꺼내 놓고 싶지는 않아요.',
            '개인과 조직 사이의 이 간극은\n[[일하는 방식]]이 바뀌어야 메워질 것 같아요.']),
    dict(k='바이브 워킹', t='성공 사례 말고\n실패 사례를 나누는 판',
         b=['"이렇게 했더니 망했어요"는\n누구나 신나게 말할 수 있잖아요.',
            '그런 판이 깔리면\n[[나도 꺼내 놓을 수 있을 것]] 같아요.']),
    dict(k='리:텐션 전략', t='새 사람을 데려오는 건\n너무 어려워요',
         b=['2만 원 쿠폰을 줘도\n쓰고 나면 탈퇴하는 시대.',
            '그래서 지금 곁에 있는 사람이\n[[더 오래 머물게]] 하는 쪽으로.\n나한테도 필요한 이야기였어요.']),
    dict(k='휴먼엣지', t='너무 번듯하면\n넘기게 돼요',
         b=["AI로 매끈하게 만든 건\n'아, AI 돌렸구나' 하고 스킵하게 되더라고요.",
            '사람이 [[수고한 흔적]]이 느껴져야\n마음이 가요.']),
    dict(k='하프시그널', t='나도 X세대,\n하프시그널 세대예요',
         b=['갱년기라고 구질구질하게 버티지 않아요.',
            '[[나한테 쓰면서]]\n후반전을 준비하는 중이에요.']),
    dict(k='안목자본', t='그래서 결국은\n안목이에요',
         b=['넘치는 것들 사이에서\n무엇을 즐기고, 무엇을 남길지.',
            '[[고르는 눈]]을 키우는 한 해를\n보내 보려고요.']),
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
  <div class="foot"><span>오파의 작업실</span><span>『트렌드 코리아 2027』 강연 후기</span></div>
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
