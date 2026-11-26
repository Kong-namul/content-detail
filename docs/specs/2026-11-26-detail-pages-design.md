# 상세 페이지 5종 — 설계 문서

- 작성일: 2026-11-26
- 근거: [에이전시 프로젝트 상세 페이지 리서치](../research/agency-project-detail.md)
- 범위: 프로젝트 **상세 페이지만** 만든다. 목록 페이지는 만들지 않는다. 확인용으로 링크만 있는 `index.html` 하나를 둔다.

## 1. 결정 사항

| 항목 | 결정 |
|---|---|
| 템플릿 | 리서치 아키타입 5종 전부: A 갤러리형, B 챕터형, C 성과 도시에형, D 에디토리얼 롱리드형, E 국내 케이스형 |
| 구현 | 페이지마다 정적 HTML. 빌드 도구·프레임워크 없음. 더블클릭으로 열린다 |
| 공통 파일 | **스타일마다** `colors_and_type.css`(색·폰트·타입 스케일)와 `components.css`(레이아웃·블록)를 둔다. 스타일과 무관한 리셋과 자리표시 박스만 `shared/base.css`에 둔다 |
| 이미지 | 회색 자리표시 박스. 박스 안에 용도와 비율을 적는다 (`HERO VIDEO · 16:9`) |
| 언어 | A~D 영문, E 국문 (헤딩은 영문 라벨 + 국문 제목 혼용, 국내 관습) |
| 콘텐츠 | 가상 에이전시 **Ondo Studio / 온도 스튜디오**의 가상 프로젝트 5개. 참고 사이트 문장은 옮기지 않고 새로 쓴다 |
| 연결 | Next 링크로 A → B → C → D → E → A 순환. E에는 PREV / NEXT와 목록(index.html) 버튼 |

## 2. 폴더 구조

```
content/
├─ index.html                     링크 5개만 있는 확인용 페이지
├─ shared/
│  └─ base.css                    리셋 + .ph 자리표시 박스 (색은 스타일 토큰을 씀)
├─ a-gallery/
│  ├─ colors_and_type.css         A 스타일 공통 토큰
│  ├─ components.css              A 스타일 공통 블록
│  └─ northmere-library.html
├─ b-chapter/
│  ├─ colors_and_type.css
│  ├─ components.css
│  ├─ chapter-nav.js              하단 고정 챕터 바
│  └─ tamo-bank.html
├─ c-dossier/
│  ├─ colors_and_type.css
│  ├─ components.css
│  └─ fieldnote.html
├─ d-longread/
│  ├─ colors_and_type.css
│  ├─ components.css
│  └─ meridian-rail.html
├─ e-kr-case/
│  ├─ colors_and_type.css
│  ├─ components.css
│  └─ onuljang.html
└─ docs/ (research, specs)
```

같은 스타일로 프로젝트를 늘릴 때는 그 폴더의 HTML을 복사해서 내용만 바꾼다. CSS는 건드리지 않는다.

## 3. 공통 규칙

### 3-1. 타입 스케일

모든 스타일은 같은 일곱 값만 쓴다: **72 / 48 / 32 / 24 / 22 / 18 / 14 (px)**. 스타일마다 `colors_and_type.css`에서 아래 변수로 선언하고, `components.css`는 변수만 참조한다.

```css
--fs-72: 72px; --fs-48: 48px; --fs-32: 32px; --fs-24: 24px;
--fs-22: 22px; --fs-18: 18px; --fs-14: 14px;
```

- 역할 변수(`--fs-display`, `--fs-h2`, `--fs-body`, `--fs-label` 등)는 스타일이 자유롭게 매핑한다. 값은 반드시 위 일곱 개 중 하나다.
- 모바일(가로 768px 이하)에서는 역할 변수만 한 단계씩 내린다: 72→48, 48→32, 32→24. 그 외는 그대로.
- 스케일 밖 값(13px, 16px, 120px 등)이 필요하면 만들지 말고 먼저 사용자에게 묻는다.

### 3-2. 색

- 헤딩은 흑 또는 백 단색. 보라 등 액센트 색을 임의로 넣지 않는다.
- 스타일마다 최소 토큰: `--bg`, `--fg`, `--fg-muted`, `--line`, `--ph-bg`, `--ph-fg`.
- 예외: C의 `--brand`(Fieldnote 숲 초록)와 `--on-brand`. 상단 컬러 밴드 배경과 Outcomes 큰 숫자에만 쓴다 (사용자 승인).
- `components.css`에는 색 값(hex, rgb)을 직접 쓰지 않는다. 토큰만 쓴다.

### 3-3. 폰트

| 스타일 | 폰트 | 출처 |
|---|---|---|
| A | Inter Tight | Google Fonts |
| B | Space Grotesk | Google Fonts |
| C | Inter + Instrument Serif (부제·인용) | Google Fonts |
| D | Newsreader (본문·헤딩) + Inter (라벨) | Google Fonts |
| E | Pretendard v1.3.9 | jsDelivr |

폰트 링크는 각 HTML `<head>`에, 패밀리 이름은 `colors_and_type.css`의 `--font-*` 변수에 둔다.

### 3-4. 자리표시 박스 `.ph`

```html
<div class="ph r-16x9" role="img" aria-label="Hero video">HERO VIDEO · 16:9</div>
```

- `shared/base.css`에 정의: 배경 `var(--ph-bg)`, 글자 `var(--ph-fg)`, 가운데 정렬, `var(--fs-14)`, 대문자, 자간 약간.
- 비율 클래스: `r-21x9`, `r-16x9`, `r-3x2`, `r-4x3`, `r-1x1`, `r-3x4`, `r-9x16`.
- 박스 텍스트는 `용도 · 비율` 형식. 용도 예: HERO VIDEO, IDENTITY, POSTER, SIGNAGE, APP SCREENS, DEVICE MOCKUP, LOOP VIDEO, INTERACTIVE, PHOTO, LOGO.

### 3-4-1. 간격 · 행간 · 폭 토큰 (2026-11-26 추가, 사용자 승인)

- 모든 스타일 공통 이름: `--space-4 / 8 / 12 / 16 / 20`, `--lh-none (1) / --lh-tight (1.25) / --lh-snug (1.4)`.
  기존 `--space-s/m/l/xl`, `--gap`, `--lh-display/heading/body`와 함께 쓴다.
- 스타일 전용: A `--radius-pill` · B `--surface --hero-min-h --stat-min-h` · C `--measure-* --logo-max-w --index-col` ·
  D `--fs-next --fs-dropcap` · E `--header-h --measure-wide --measure --measure-quote --store-min-w --label-col-compact --icon-size`.
- `components.css`의 padding / margin / gap / 폭 / 높이 / 행간 / 자간은 토큰만 쓴다. 예외: 1~2px 선, 0, %, vw/vh.
  `tools/check.py`가 검사한다.
- B 챕터 바 현재 항목은 `aria-current="location"`, 토글 안에 `<span class="sr-only">Current chapter:</span>`.

### 3-5. 기타

- CSS 링크에는 `?v=1`을 붙인다. 공통 CSS를 고치면 버전을 올린다.
- 시맨틱 마크업: `header`, `main`, `section`, `footer`, 헤딩 순서 지키기, `lang` 속성(A~D `en`, E `ko`).
- 실제로 동작하지 않는 링크(가상 사이트, 이메일, 앱스토어)는 `href="#"`. 진짜 도메인으로 보내지 않는다.
- 가로 스크롤 없음 (1440px, 375px 둘 다).
- JS는 B의 챕터 바 하나뿐이다. 나머지는 HTML + CSS만. (E 모바일 햄버거 메뉴도 `<details>`로 JS 없이)
- 국문 문단 길이 100~300자는 공백 포함으로 센다.

## 4. 페이지별 설계

각 페이지 본문 문단은 리서치 3장의 카피 규칙을 따른다: 영문 문단 25~90단어, 국문 문단 100~300자. 이름·헤드라인·숫자는 아래에 정한 대로 쓴다.

### A. 갤러리형 — Northmere Library (`a-gallery/northmere-library.html`)

참고: Locomotive (상단 메타, Awards, Credits, Next 카드), Pentagram (미디어 사이 큰 스테이트먼트)
톤: 흰 배경, 검정 글자, 12컬럼 그리드, 여백 넉넉히. 텍스트 총량 150단어 안팎.

1. 헤더: 왼쪽 `Ondo` 워드마크, 오른쪽 Work / Studio / Contact
2. 상단 그리드
   - 작은 라벨 `Case Study` + 태그 `Branding` `Wayfinding` `Print`
   - H1 `Northmere Library` (display 72)
   - 옆에 메타: `©2026` · `Culture & Public` · `Leeds, UK`
3. 히어로 `.ph r-16x9` + 아래 짧은 태그라인 `Every shelf, a doorway`
4. 피치 줄: 라벨 `Website` → `northmere-library.org ↗` + 한 줄 설명
5. About: 라벨 왼쪽, 2문단 오른쪽 (합계 약 100단어. 공공도서관 재개관, 세대를 아우르는 아이덴티티와 사인 시스템)
6. `Awards (3)` 2단 목록 (가상 시상): Northern Design Awards — Gold, Identity / Type & Place Prize — Shortlist / Civic Design Review — Best Wayfinding
7. 미디어 런: 자리표시 20개 안팎, 캡션 없음. 풀폭 16:9, 2-up 1:1, 풀폭 21:9, 2-up 3:4, 3-up 4:3, LOOP VIDEO 섞기. 중간에 **스테이트먼트 2개** (32~48 크기, 20~40단어)
8. Credits: 역할 : 이름 2단 목록 — Client, Creative Director, Design Director, Designers, Wayfinding, Motion, Photography, Type Partner
9. `Visit northmere-library.org ↗`
10. Next Project 카드: 라벨 `Next Project`, `Tamo Bank`, `2026 · Banking`, 큰 자리표시, `Read more` → `../b-chapter/tamo-bank.html`
11. 푸터: `Let's talk` + 이메일 텍스트, ©

### B. 챕터형 — Tamo Bank (`b-chapter/tamo-bank.html`)

참고: Koto (챕터 구조, 하단 고정 챕터 바, Outcome 콜라주·숫자), 플러스엑스 (결과물 순서)
톤: 다크 배경(흰 글자), 풀블리드 히어로. 챕터마다 문단 하나라 텍스트는 짧다.

1. 헤더: 히어로 위에 투명하게 겹침
2. 풀블리드 히어로 `.ph` (화면 높이 가득, 최소 16:9)
3. 타이틀: H1 `Tamo Bank`, 태그라인 `Money, made lighter` (클라이언트 브랜드 라인), 메타 `BANKING · 2026` (작은 대문자)
4. 인트로 2문단 (청년층 앱 은행이 전 세대 은행으로 커지는 상황)
5. **하단 고정 챕터 바**: `TAMO BANK | <현재 챕터> ▾`. 누르면 챕터 7개 목록이 열리고 누르면 그 챕터로 이동
6. 챕터 7개. 각 챕터 = 작은 라벨 + 헤드라인(48) + 1문단(약 50단어) + 자리표시 2~5개

   | 라벨 | 헤드라인 | 미디어 |
   |---|---|---|
   | Challenge | One bank, two generations | 풀폭 1 |
   | Graphic System | A circle that holds everything | 풀폭 1 + 2-up |
   | Typography | Numbers you can trust | 풀폭 1 + 3-up |
   | Illustration | Room for small joys | 2-up + 풀폭 |
   | Digital Design | From sign-up to first savings | APP SCREENS 3-up 9:16 + INTERACTIVE 태그 박스 1 |
   | Launch | Lighting up the city | 풀폭 21:9 + 2-up |
   | Outcome | Lighter, for everyone | 숫자 타일 3개 + 모자이크 콜라주 8~10칸 |

   Outcome 숫자: `2.1M` new accounts in six months / `4.8` average app rating / `38%` of new customers over 40
7. Next up: `NEXT UP` + `[ View all projects ]`(→ `../index.html`), `Fieldnote`, 태그라인, 풀폭 자리표시 → `../c-dossier/fieldnote.html`
8. 푸터

**chapter-nav.js 동작**

- `section[data-chapter]`를 IntersectionObserver로 보고, 화면 중앙에 걸린 챕터 이름을 바에 표시한다.
- 바 버튼은 `aria-expanded`로 목록을 열고 닫는다. 항목을 누르거나 Esc를 누르면 닫힌다.
- 첫 챕터에 닿기 전(히어로 구간)에는 바를 숨긴다.
- JS가 꺼져 있어도 챕터 내용은 다 보인다 (바만 없음).

### C. 성과 도시에형 — Fieldnote (`c-dossier/fieldnote.html`)

참고: Work & Co (컬러 밴드, 라벨 왼쪽·내용 오른쪽, Outcomes, 3 Big Takeaways), Collins (지표 카드), Basic/Dept (Accolades 목록)
톤: 흰 배경 + 상단 브랜드 컬러 밴드, 가는 구분선으로 나눈 팩트시트, 큰 숫자는 브랜드 컬러.

1. 헤더
2. **컬러 밴드** (`--brand` 배경): H1 `Fieldnote` (흰 글자), 세리프 부제 `Gear for the long way round` (32)
3. 히어로 `.ph r-16x9`
4. 팩트시트 (라벨 왼쪽 / 내용 오른쪽, 행마다 위 구분선)
   - `Visit` → `fieldnote.co ↗`
   - `What We Did` → Digital Strategy, E-commerce Platform, Design System, Headless Build, Product Content Direction, Localization
5. `Outcomes` — 숫자 4개 (숫자 72, `--brand`, 단위 기호 %·s·x는 작게 같은 `--brand`. "markets" 같은 단어 단위는 숫자 옆이 아니라 아래 설명 문구로)
   - `32%` higher conversion on mobile
   - `1.4s` median page load, down from 4.2s
   - `18` markets launched in one release
   - `3x` revenue from bundles
6. `Overview` 3문단
7. 인용 (세리프 32, 가운데): Fieldnote 최고디지털책임자(가상 인물 이름 + 직함)
8. `Awards & Recognition`: 로고 자리표시 3개 + 캡션 (가상 시상), 프레스 2개 (가상 매체 로고 자리표시 + 짧은 인용 + `Read more`)
9. `3 Big Takeaways` — 번호 목차 01~03
10. 테이크어웨이 챕터 (번호 + 선언형 제목(48) + 하위 기능 [제목 22 + 1문단 + 자리표시 1개])
    - 01 `Shop the way you pack` — Kit Builder / Trail-tested Filters / Field Notes Journal
    - 02 `Fast on a mountain signal` — Edge-rendered Pages / A Lighter Image Pipeline
    - 03 `One system, eighteen markets` — Design Tokens / Localization at Launch / After Launch
11. `More Case Studies`: 맨 위에 `Next — Meridian Rail →`(→ `../d-longread/meridian-rail.html`), 그 아래 다른 프로젝트 이름 텍스트 목록 (A·B·E는 링크, 나머지 가상 이름은 텍스트)
12. 푸터

### D. 에디토리얼 롱리드형 — Meridian Rail (`d-longread/meridian-rail.html`)

참고: ustwo (이야기형 H2, 여러 목소리의 인용, Opportunity → Impact), Wolff Olins Bergdorf (왼쪽에 걸린 인용, 본문 속 숫자)
톤: 따뜻한 미색 배경, 세리프 본문, 좁은 본문 칼럼(약 680px)을 오른쪽으로 치우치게, 인용은 데스크톱에서 왼쪽 여백에 걸기. 텍스트 총량 900~1,100단어.

1. 헤더 + 브레드크럼 `Work / Meridian Rail`
2. H1 `Meridian Rail` (72 세리프) + 부제 `Redesigning how forty million passengers find their way through the station` (24)
3. 히어로 `.ph r-16x9`
4. 맥락 3문단 (클라이언트 소개 → 문제 → 브리프)
5. 클라이언트 인용 (Director of Customer Experience, 가상 인물)
6. H2 `The opportunity` — 2문단 + 풀폭 PHOTO
7. H2 `Listening on the platform` — 3문단, 이용자 인용 (`Commuter, Leeds`), 2-up PHOTO
8. H2 `A station that explains itself` — 2문단, 직원 인용 (직함만 대문자 `STATION MANAGER`), 풀폭 SIGNAGE
9. H2 `Making it real` — 시범 운영 2문단, 2-up PROTOTYPE
10. H2 `What we delivered` — 결과물 6개 불릿
11. H2 `The impact` — 숫자를 문장 안에 (예: 6개월 시범 기간 안내 데스크 길찾기 문의 41% 감소, 환승 시간 평균 2분 단축) + 마무리 클라이언트 인용
12. `Project details` 정의목록: Client / Sector / Services / Year
13. Next Project → `../e-kr-case/onuljang.html`
14. 푸터

### E. 국내 케이스형 — 오늘장 (`e-kr-case/onuljang.html`)

참고: 이모션글로벌 (2단 타이틀, PROJECT GOAL 포인트 3개, DESIGN CONCEPT, PROJECT INTERVIEW, 목록 버튼), 바이널씨 (정의목록 메타, 문단↔미디어 교차, Credits, App download), 펜타브리드 (PREV / NEXT)
톤: 흰 배경, Pretendard, 영문 대문자 섹션 라벨 + 국문 제목·본문, 합니다체.

1. 헤더: `온도 스튜디오` 워드마크, 프로젝트 / 스튜디오 / 문의, `KOR | ENG` 표시. 모바일(768px 이하)은 햄버거 버튼 → 누르면 링크 3개가 헤더 아래로 펼쳐짐 (`<details>`, JS 없음)
2. 2단 타이틀: `새로운 장보기의 시작,` (48) / `오늘장 앱 리뉴얼` (72)
3. 메타 정의목록 (라벨을 단다 — 리서치 6장 함정 참고)
   - 클라이언트 (주)오늘장 · 런칭 2026.03 · 범위 Mobile App, Renewal, UX/UI · 플랫폼 iOS, Android
4. 키비주얼 `.ph r-16x9`
5. 대형 리드 문단 (32, 굵게, 3줄 안팎)
6. `PROJECT GOAL`: 와이드 배너 자리표시 + 설명 문단 → 포인트 3개 (왼쪽 작은 국문 라벨, 오른쪽 설명 + 풀폭 자리표시)
   - 발견하는 장보기 / 30분 배송의 신뢰 / 다시 찾는 단골
7. `DESIGN CONCEPT` 3행: `KEYWORD` 신선함이 보이는 화면 / `COLOR SYSTEM` 채소 색에서 가져온 6색 / `ICON STYLE` 손에 잡히는 둥근 선 — 각각 설명 + 자리표시
8. 문단 ↔ 풀폭 자리표시 교차 3회 (문단 첫 줄에 굵은 소제목)
9. `PROJECT INTERVIEW`: 내부 PM 소감 1문단 + 이름·역할
10. `CREDITS` 정의목록: Creative Director, Project Manager, UX Planner, UI Designer, Interaction Designer, Front-end Developer (가상 국문 이름)
11. 앱 다운로드 버튼 2개: App Store, Google Play (`href="#"`)
12. 하단 내비: 큰 `PREV` (→ D) / `NEXT` (→ A) + 가운데 `목록` (→ `../index.html`)
13. 푸터: `함께 만들 프로젝트가 있나요?` + 이메일 텍스트

## 5. index.html

디자인 없이 제목 한 줄과 링크 5개 목록만. 각 링크 옆에 스타일 이름(A 갤러리형 등)을 적는다. `shared/base.css`(맨 아래 `.catalog` 블록)와 흑백 토큰을 빌려 쓰기 위해 `a-gallery/colors_and_type.css`를 쓴다.

## 5-1. 검사 스크립트

`tools/check.py` — 6장 완료 기준 중 코드로 확인할 수 있는 것(파일 존재, 토큰 규칙, 폰트 크기, 색 직접 입력, 링크, `.ph` 접근성, B 챕터 7개, C 브랜드 토큰)을 검사한다. `python3 tools/check.py` 전체, `python3 tools/check.py b-chapter` 한 스타일만.

## 5-2. 한/영 버전 (2026-11-26 추가, 사용자 결정)

- 방식: 언어별 파일. 기존 파일 이름은 그대로 두고 다른 언어 파일을 옆에 둔다. JS 없음.

  | 스타일 | 영문 | 국문 |
  |---|---|---|
  | A | `northmere-library.html` | `northmere-library.ko.html` |
  | B | `tamo-bank.html` | `tamo-bank.ko.html` |
  | C | `fieldnote.html` | `fieldnote.ko.html` |
  | D | `meridian-rail.html` | `meridian-rail.ko.html` |
  | E | `onuljang.en.html` | `onuljang.html` |

- 언어 전환: 모든 상세 페이지 헤더 오른쪽에 `KOR | ENG`. 현재 언어는 굵게(`aria-current="true"`), 다른 언어는 같은 폴더의 짝 파일로 가는 링크(`hreflang`). `<head>`에 `<link rel="alternate" hreflang="…" href="짝 파일">`.
- 순환 링크는 언어별로 따로 돈다: 국문 A→B→C→D→E→A, 영문 A→B→C→D→E→A. E의 PREV/NEXT도 같은 언어로. 목록·View all은 `../index.html`.
- 시작 페이지(index.html): 한국어 / English 두 묶음으로 언어를 고르고 들어간다.
- 국문판 카피: 섹션 라벨(Case Study, About, Credits, Outcomes…)은 영문 그대로, 제목·본문·캡션은 국문 합니다체. 프로젝트 이름(Northmere Library 등)과 숫자는 그대로.
- 영문판 E: 라벨은 그대로, 국문 제목·본문을 영문으로. 워드마크는 `Ondo Studio`.
- 폰트: A~D 폰트 목록에 영문 폰트 다음으로 `"Pretendard Variable", "Pretendard"`를 넣어 한글만 Pretendard로 대체한다 (D 세리프 본문도 한글은 Pretendard, 사용자 결정). 국문 페이지는 Pretendard를 jsDelivr에서 불러온다.
- 국문 조판: A~D `components.css`에 `:lang(ko)` 규칙으로 `word-break: keep-all`.

## 6. 완료 기준

- 5개 페이지와 index.html이 더블클릭으로 열리고 콘솔 에러가 없다.
- 1440px과 375px 너비에서 가로 스크롤이 없고, 레이아웃이 깨지지 않는다.
- `font-size`는 전부 `--fs-*` 변수를 거친다. CSS에 스케일 밖 px 값이 없다.
- `components.css`에 색 값 직접 입력이 없다.
- Next / PREV / 목록 링크가 순환 구조대로 이어진다.
- B: 스크롤하면 챕터 바 이름이 바뀌고, 목록에서 누르면 그 챕터로 이동한다.
- 각 페이지가 리서치 5장의 해당 아키타입 골격 순서를 따른다.
