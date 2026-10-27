"""텍스트만 있는 카드뉴스: 울트라마린 단색 바탕 + 크림 글자, 가운데 정렬.
슬라이드마다 문단 리스트, 문단 안 줄바꿈은 \\n. [[ ]] 안은 연하늘 강조."""
import re

SLIDES = [
    ["트렌드 코리아 2027 키워드에는\n'AI'가 없다", "1년 만에 AI가 전기처럼\n당연한 것이 됐기 때문이다"],
    ["그래서 올해의 질문이 바뀌었다", "AI를 쓰느냐가 아니라\nAI 때문에 달라진 일, 인생, 감각을\n어떻게 다루느냐"],
    ["[[바이브 워킹]]", "AI로 보고서는 이틀에서 반나절이 됐는데\n팀 프로젝트는 여전히 3개월이다", "병목은 AI가 아니라\n일하는 방식에 있다"],
    ["AI는 아직 신입사원이다", "우리 회사의 맥락을 가르치고\n사람과 AI의 역할을 나눴더니\n상담 연결 시간이 [[47초에서 5초]]로 줄었다"],
    ["우수 사례 경진대회보다\n실패 사례를 모으는 팀이 더 빨리 배운다", "\"이렇게 썼더니 망했다\"는\n누구나 신나게 공유하기 때문이다"],
    ["[[하프시그널]]", "갱년기는 끝이 아니라\n인생 후반전을 알리는 하프타임이다", "X세대는 참지 않고\n말하고, 소비하고, 준비한다"],
    ["이제 갱년기는 집이 아니라\n일터의 문제이기도 하다", "이케아는 갱년기 동료 배려 매뉴얼을 만들었고\n노무라는 갱년기 유급휴가를 준다"],
    ["[[안목자본]]", "AI를 써도 글을 못 쓰는 사람이 있다\n좋은 글이 뭔지 모르기 때문이다", "무한히 만들어지는 시대에는\n고르는 눈이 실력이다"],
    ["안목은 이렇게 자란다", "많이 보고, 내 언어로 표현하고\n전문가의 평가와 비교하고, 오래 반복한다", "보고 저장만 하면\n안목은 생기지 않는다"],
    ["어제의 해결책이\n오늘의 문제점이 된다", "— 트렌드 코리아 2027 강연 중", "[[내년 기획 전에 다시 꺼내 볼 수 있게\n저장해두세요]]"],
]


def fmt(t):
    t = t.replace('\n', '<br>')
    return re.sub(r'\[\[(.+?)\]\]', r'<em>\1</em>', t, flags=re.S)


cards = []
for i, paras in enumerate(SLIDES, 1):
    body = ''.join(f'<p>{fmt(p)}</p>' for p in paras)
    cards.append(f'<section class="card" id="c{i}"><div class="txt">{body}</div>'
                 f'<div class="foot">오파의 작업실</div></section>')

open('text.html', 'w').write(f'''<!doctype html><html lang="ko"><head><meta charset="utf-8"><title>text cards</title>
<link rel="stylesheet" href="../fonts/noto.css">
<style>
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
body {{ background: #888; }}
.card {{ width: 1080px; height: 1350px; margin: 0 auto 30px; background: #1117A9; color: #FAF3E6;
  display: flex; align-items: center; justify-content: center; position: relative;
  font-family: 'Noto Sans KR', sans-serif; text-align: center; word-break: keep-all; padding: 0 80px; }}
.txt p {{ font-size: 44px; font-weight: 500; line-height: 1.62; letter-spacing: -0.02em; }}
.txt p + p {{ margin-top: 44px; }}
em {{ font-style: normal; color: #B9DCF7; font-weight: 700; }}
.foot {{ position: absolute; bottom: 64px; left: 0; right: 0; font-size: 24px; font-weight: 500; color: rgba(250,243,230,.45); letter-spacing: .02em; }}
</style></head><body>
{chr(10).join(cards)}
</body></html>''')
print(len(cards))
