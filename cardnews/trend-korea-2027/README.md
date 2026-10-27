# 트렌드 코리아 2027 카드뉴스

오파의 작업실 팔레트(`../../opa-theme.css`)에 맞춘 1080×1350 카드뉴스 두 벌.

- `A_full/` — 전체 요약 14장 (10대 키워드 전부)
- `B_pick/` — 인상 파트 10장 (바이브 워킹 · 하프시그널 · 안목자본)

## 다시 만들기

```sh
python3 build.py                       # full.html, pick.html 생성
node render.js "$PWD" full.html A_full  # PNG 내보내기
node render.js "$PWD" pick.html B_pick
```

문구는 `build.py`, 색·크기는 `opa-cards.css`에서 고친다. `img/`는 강연 자료 PDF에서 잘라낸 사례 이미지, `fonts/`는 Noto Sans KR·Jost 로컬 사본.
