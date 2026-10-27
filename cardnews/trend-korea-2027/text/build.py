"""텍스트 카드뉴스: 진한 울트라마린(#0B0F7A)과 연하늘(#E3F0FC) 바탕을 번갈아 쓰고,
작은 라벨 + 굵은 제목 + 본문으로 위계를 준다. 본문의 [[ ]] 는 밑줄 강조."""
import re

SLIDES = [
    dict(k='강연에서 남은 질문', t="2027 키워드에는\n'AI'가 없어요",
         b=["1년 만에 AI가 전기처럼\n당연한 것이 됐기 때문이에요.",
            "이제 질문은 'AI를 쓰느냐'가 아니라\n[['AI 때문에 달라진 걸 어떻게 다루느냐']]예요."]),
    dict(k='01 · 바이브 워킹', t='AI를 쓴다고\n일을 잘하게 되는 건 아니에요',
         b=['보고서는 2일 → 반나절,\n팀 프로젝트는 3개월 그대로.',
            '병목은 AI가 아니라\n[[일하는 방식]]에 있어요.']),
    dict(k='01 · 바이브 워킹', t='AI는 아직\n신입사원이에요',
         b=['10년 손발 맞춘 동료는\n"3년 전 그 PPT처럼" 한마디면 알아들어요.',
            'AI도 그렇게 되려면\n[[우리 팀의 맥락]]부터 가르쳐야 해요.']),
    dict(k='01 · 바이브 워킹', t='우수 사례보다\n실패 사례를 모으세요',
         b=['경진대회는 부담이라 아무도 안 내요.',
            '"이렇게 썼더니 망했어"는\n누구나 신나게 공유해요.',
            '그게 쌓이면 [[팀의 실력]]이 돼요.']),
    dict(k='02 · 하프시그널', t='갱년기는 끝이 아니라\n하프타임이에요',
         b=['100세 시대, 50대는\n인생의 딱 절반이에요.',
            'X세대는 참지 않아요.\n말하고, 소비하고, [[후반전을 준비]]해요.']),
    dict(k='02 · 하프시그널', t='이제 갱년기는\n일터의 이야기이기도 해요',
         b=['자녀 사춘기, 부부 갱년기, 부모 부양이\n한꺼번에 오는 시기.',
            '이케아는 배려 매뉴얼을,\n노무라는 유급휴가를 만들었어요.',
            '[[혼자 견디는 일에서 함께 챙기는 일로]].']),
    dict(k='03 · 안목자본', t='AI를 써도\n글을 못 쓰는 이유',
         b=['좋은 글이 뭔지 모르기 때문이에요.',
            '무엇이든 무한히 만들어지는 시대에는\n[[고르는 눈]]이 실력이에요.']),
    dict(k='03 · 안목자본', t='보고 저장만 하면\n안목은 생기지 않아요',
         steps=['좋은 것을 많이 보고', '내 언어로 표현하고', '전문가의 평가와 비교하고', '오래 반복하기'],
         b=['촌스러워도, 틀려도 괜찮아요.']),
    dict(k='강연의 마지막 문장', t='어제의 해결책이\n오늘의 문제점이에요',
         b=['잘해온 방식을 지키는 것과\n익숙한 방식만 고집하는 건\n다른 일이니까요.']),
    dict(k='나를 위한 체크리스트', t='2027년을 앞두고\n나에게 던져볼 5가지 질문',
         qs=['AI를 쓰면서도 그대로인 일하는 방식은?', '우리 팀이 AI에게 가르쳐야 할 맥락은?',
             '이번 달 모아둔 실패 사례는?', '내 인생의 후반전, 무엇을 준비하고 있나?',
             "최근 '좋다'고 느낀 걸 내 언어로 설명할 수 있나?"],
         b=['저장해두고 내년 기획 전에 다시 꺼내 보세요.']),
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
        parts.append('<ol class="steps">' + ''.join(f'<li><span>{j:02d}</span>{x}</li>' for j, x in enumerate(s['steps'], 1)) + '</ol>')
    if 'qs' in s:
        parts.append('<ol class="qs">' + ''.join(f'<li><span>{j:02d}</span>{x}</li>' for j, x in enumerate(s['qs'], 1)) + '</ol>')
    parts += [f'<p>{fmt(p)}</p>' for p in s['b']]
    cards.append(f'''<section class="card {tone}" id="c{i}">
  <div class="top"><span>TREND KOREA 2027</span><span>{i:02d} / {N:02d}</span></div>
  <div class="txt">{''.join(parts)}</div>
  <div class="foot"><span>오파의 작업실</span><span>『트렌드 코리아 2027』 강연 정리</span></div>
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
</style></head><body>
{chr(10).join(cards)}
</body></html>''')
print(N)
