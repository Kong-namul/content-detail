# 상세 페이지 5종 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 리서치 아키타입 5종(A 갤러리형, B 챕터형, C 성과 도시에형, D 롱리드형, E 국내 케이스형)을 가상 프로젝트로 채운 정적 상세 페이지 5개를 만든다.

**Architecture:** 스타일마다 폴더 하나. 폴더 안에 스타일 공통 토큰(`colors_and_type.css`), 스타일 공통 블록(`components.css`), 상세 페이지 HTML이 있다. 스타일과 무관한 리셋·자리표시 박스는 `shared/base.css`. 빌드 없음, 더블클릭으로 열림. 검사는 `tools/check.py`.

**Tech Stack:** HTML, CSS (커스텀 프로퍼티, grid, aspect-ratio), 바닐라 JS (B만), Google Fonts / jsDelivr(Pretendard), Python 3 표준 라이브러리 (검사 스크립트).

## Global Constraints

- 설계 문서: `docs/specs/2026-11-26-detail-pages-design.md` — 페이지 내용과 블록 순서의 기준
- 리서치: `docs/research/agency-project-detail.md` — 5장 아키타입 골격, 3장 카피 규칙
- 폰트 크기 값은 72 / 48 / 32 / 24 / 22 / 18 / 14 px뿐. CSS의 `font-size`는 반드시 `var(--fs-*)`
- `components.css`에 색 값(hex, rgb, 이름 있는 색) 직접 입력 금지. 토큰만
- 토큰이 더 필요하면 만들지 말고 멈춰서 보고한다 (사용자에게 물어야 함). `colors_and_type.css`는 수정 금지
- 헤딩은 흑/백 단색. 액센트 색 금지. 예외: C의 `--brand`는 상단 밴드 배경과 Outcomes 숫자에만
- 자리표시: `<div class="ph r-16x9" role="img" aria-label="…">용도 · 비율</div>` (비율 클래스 r-21x9 / r-16x9 / r-3x2 / r-4x3 / r-1x1 / r-3x4 / r-9x16, 높이 채우기는 `ph--fill`)
- 로컬 CSS/JS 링크에 `?v=1`. 스타일시트 순서: `../shared/base.css` → `colors_and_type.css` → `components.css`
- `<html lang>`: A~D `en`, E `ko`
- 가상 링크(사이트, 이메일, 앱스토어)는 `href="#"`. `<a>`로 실제 도메인 금지
- inline `style` 속성에 font / color / background 금지
- 1440px, 375px 둘 다 가로 스크롤 없음
- JS는 B의 `chapter-nav.js`뿐
- 카피: 영문 문단 25~90단어, 국문 문단 100~300자, E는 합니다체. 참고 사이트 문장 옮기기 금지, 새로 쓴다. 가상 에이전시: Ondo Studio / 온도 스튜디오
- 순환 링크: A→B→C→D→E→A, E는 PREV(D)·NEXT(A)·목록(`../index.html`), B의 View all은 `../index.html`

---

### Task 1: 기반 파일 — 완료

**Files (생성됨):**
- `tools/check.py` — 정적 검사. `python3 tools/check.py [style…]`
- `shared/base.css` — 리셋, body 기본값(토큰 사용), `.ph`, `r-*`, `.sr-only`, `.catalog`
- `a-gallery/colors_and_type.css`, `b-chapter/colors_and_type.css`, `c-dossier/colors_and_type.css`, `d-longread/colors_and_type.css`, `e-kr-case/colors_and_type.css`
- `b-chapter/chapter-nav.js` — 챕터 바 (파일 상단 주석에 마크업 계약)
- `index.html`

검증: `python3 tools/check.py` → 남은 오류는 "missing components.css / page" 뿐.

---

### Task 2~6 공통 절차 (스타일 하나 = 태스크 하나)

**Files:**
- Create: `<style>/components.css`
- Create: `<style>/<page>.html`
- 읽기만: `shared/base.css`, `<style>/colors_and_type.css` (B는 `chapter-nav.js`도)

**Interfaces:**
- Consumes: `shared/base.css`의 `.ph`, `.r-*`, `.ph--fill`, `.sr-only`, body 기본값. `<style>/colors_and_type.css`의 토큰 전부 (파일 열어서 이름 확인)
- Produces: 다른 태스크가 쓰는 것 없음. 순환 링크 경로만 지킨다

- [ ] **Step 1: 실패 확인** — `python3 tools/check.py <style>` → `FAIL … missing <style>/components.css`, `missing <style>/<page>.html`
- [ ] **Step 2: components.css 작성** — 설계 문서 해당 절의 블록마다 클래스 하나씩. 값은 토큰만. 768px 이하 미디어쿼리로 모바일 레이아웃(그리드 → 1열)
- [ ] **Step 3: HTML 작성** — 아래 head 템플릿 + 설계 문서 해당 절 블록 순서 그대로. 헤드라인·숫자·라벨은 설계 문서 값 그대로, 문단은 카피 규칙대로 새로 쓴다
- [ ] **Step 4: 통과 확인** — `python3 tools/check.py <style>` → `OK — 4 files checked`
- [ ] **Step 5: 화면 확인** — 브라우저에서 `file://` 로 열어 1440px, 375px 스크린샷. 가로 스크롤(`document.documentElement.scrollWidth > innerWidth`), 겹침, 넘침 확인 후 고침. 고친 뒤 Step 4 다시

**head 템플릿** (스타일별 폰트 줄만 다름)

```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Project Name — Ondo Studio</title>
  <meta name="description" content="한 줄 프레이밍 문장">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="stylesheet" href="FONT_URL">
  <link rel="stylesheet" href="../shared/base.css?v=1">
  <link rel="stylesheet" href="colors_and_type.css?v=1">
  <link rel="stylesheet" href="components.css?v=1">
</head>
```

| 태스크 | 스타일 폴더 | 페이지 | 설계 문서 절 | FONT_URL |
|---|---|---|---|---|
| 2 | `a-gallery` | `northmere-library.html` | 4장 A | `https://fonts.googleapis.com/css2?family=Inter+Tight:wght@400;500&display=swap` |
| 3 | `b-chapter` | `tamo-bank.html` | 4장 B | `https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500&display=swap` |
| 4 | `c-dossier` | `fieldnote.html` | 4장 C | `https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Instrument+Serif&display=swap` |
| 5 | `d-longread` | `meridian-rail.html` | 4장 D | `https://fonts.googleapis.com/css2?family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,500;1,6..72,400&family=Inter:wght@400;500&display=swap` |
| 6 | `e-kr-case` | `onuljang.html` | 4장 E | `https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable-dynamic-subset.min.css` (Google preconnect 두 줄은 빼고, `lang="ko"`) |

**태스크별 추가 사항**

- Task 3 (B): `chapter-nav.js` 상단 주석의 마크업 계약을 그대로 따른다. `<script src="chapter-nav.js?v=1" defer></script>`. 챕터 바가 숨김 상태일 때(`.chapter-bar:not(.is-visible)`) 화면 밖으로 내리고 `visibility: hidden`. 열린 메뉴는 바 위로 펼친다. 하단 고정 바가 푸터 마지막 내용을 가리지 않게 `body` 아래 여백을 `--bar-h`만큼 준다
- Task 4 (C): `--brand`는 `.band` 배경과 Outcomes 숫자 색에만. 밴드 위 H1·부제는 `--on-brand`
- Task 5 (D): 데스크톱에서 본문은 `--measure` 폭으로 오른쪽 치우침, 인용은 왼쪽 `--hang` 칼럼에 걸림. 모바일은 1열
- Task 6 (E): `word-break: keep-all`. 메타는 `<dl>`로 라벨을 단다. PREV / 목록 / NEXT는 한 줄 3칸

---

### Task 7: 통합 검증

- [ ] `python3 tools/check.py` → `OK — 17 files checked`
- [ ] index.html에서 시작해 A→B→C→D→E→A 링크를 따라가며 모두 열리는지 확인
- [ ] 5페이지 × (1440, 375) 스크린샷, 가로 스크롤 0
- [ ] B: 스크롤 시 챕터 이름 변경, 메뉴 열기 → 항목 클릭 → 이동 → 닫힘, Esc 닫힘
- [ ] 콘솔 에러 0
