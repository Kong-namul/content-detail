# content-detail

에이전시 웹사이트의 **프로젝트 상세 페이지**가 정보를 어떻게 적는지 리서치하고, 그 결과로 만든 상세 페이지 템플릿 5종입니다. 국문·영문 두 언어로 되어 있습니다.

모든 프로젝트·인물·수상 내역은 가상입니다 (가상 에이전시 Ondo Studio / 온도 스튜디오).

## 보기

배포: **https://kong-namul.github.io/content-detail/** (GitHub Pages, `main` 브랜치 루트)

로컬에서는 `index.html`을 브라우저로 열면 됩니다. 빌드 과정은 없습니다. 로컬 서버로 보려면:

```bash
python3 -m http.server 8000
```

상세 페이지 안에서는 상단 `KOR | ENG`로 언어를 바꿀 수 있습니다.

## 템플릿 5종

| 스타일 | 가상 프로젝트 | 참고한 구조 |
|---|---|---|
| A 갤러리형 | Northmere Library | 이미지가 이야기하는 갤러리 중심 |
| B 챕터형 | Tamo Bank | 결과물 단위 챕터 + 하단 고정 챕터 바 |
| C 성과 도시에형 | Fieldnote | 숫자·인용·수상이 먼저 나오는 팩트시트 |
| D 에디토리얼 롱리드형 | Meridian Rail | 읽는 이야기, 여러 사람의 목소리 |
| E 국내 케이스형 | 오늘장 앱 리뉴얼 | 영문 라벨 + 국문 본문, GOAL·CONCEPT |

## 구조

```
shared/base.css            스타일과 무관한 리셋, 자리표시 박스
<style>/colors_and_type.css 스타일 공통 토큰 (색·폰트·타입 스케일·간격)
<style>/components.css      스타일 공통 블록 (토큰만 사용)
<style>/*.html              상세 페이지 (영문 / .ko.html 국문, E는 .en.html 영문)
tools/check.py              규칙 검사
docs/                       리서치, 설계, 구현 계획
```

같은 스타일로 프로젝트를 늘릴 때는 그 폴더의 HTML을 복사해서 내용만 바꿉니다.

## 규칙 검사

```bash
python3 tools/check.py
```

폰트 크기는 72/48/32/24/22/18/14 스케일만, 색·간격·행간은 토큰만, 링크·언어 전환·국영문 마크업 일치 등을 검사합니다.

## 문서

- [리서치: 에이전시 프로젝트 상세 페이지 정보 작성 방식](docs/research/agency-project-detail.md)
- [설계](docs/specs/2026-11-26-detail-pages-design.md)
- [구현 계획](docs/plans/2026-11-26-detail-pages-plan.md)
