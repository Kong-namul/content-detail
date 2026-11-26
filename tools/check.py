#!/usr/bin/env python3
"""상세 페이지 사이트 정적 검사.

실행: python3 tools/check.py
설계 문서(docs/specs/2026-11-26-detail-pages-design.md) 6장 완료 기준 중
코드로 확인할 수 있는 것을 검사한다. 통과하면 exit 0, 아니면 오류 목록과 exit 1.
"""
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCALE = {"72", "48", "32", "24", "22", "18", "14"}
REQUIRED_TOKENS = [
    "--fs-72", "--fs-48", "--fs-32", "--fs-24", "--fs-22", "--fs-18", "--fs-14",
    "--fs-body", "--fs-label", "--font-body", "--lh-body",
    "--bg", "--fg", "--fg-muted", "--line", "--ph-bg", "--ph-fg",
]
ALLOWED_EXTERNAL = ("https://fonts.googleapis.com", "https://fonts.gstatic.com", "https://cdn.jsdelivr.net")

# 스타일마다 언어별 페이지 두 개. links = 반드시 있어야 하는 링크 (같은 언어 순환 + 목록),
# switch = 상단 KOR | ENG 전환이 가리켜야 하는 같은 프로젝트의 다른 언어 파일.
STYLES = {
    "a-gallery": [
        {"page": "northmere-library.html", "lang": "en", "switch": "northmere-library.ko.html",
         "links": ["../b-chapter/tamo-bank.html"]},
        {"page": "northmere-library.ko.html", "lang": "ko", "switch": "northmere-library.html",
         "links": ["../b-chapter/tamo-bank.ko.html"]},
    ],
    "b-chapter": [
        {"page": "tamo-bank.html", "lang": "en", "switch": "tamo-bank.ko.html",
         "links": ["../c-dossier/fieldnote.html", "../index.html"]},
        {"page": "tamo-bank.ko.html", "lang": "ko", "switch": "tamo-bank.html",
         "links": ["../c-dossier/fieldnote.ko.html", "../index.html"]},
    ],
    "c-dossier": [
        {"page": "fieldnote.html", "lang": "en", "switch": "fieldnote.ko.html",
         "links": ["../d-longread/meridian-rail.html"]},
        {"page": "fieldnote.ko.html", "lang": "ko", "switch": "fieldnote.html",
         "links": ["../d-longread/meridian-rail.ko.html"]},
    ],
    "d-longread": [
        {"page": "meridian-rail.html", "lang": "en", "switch": "meridian-rail.ko.html",
         "links": ["../e-kr-case/onuljang.en.html"]},
        {"page": "meridian-rail.ko.html", "lang": "ko", "switch": "meridian-rail.html",
         "links": ["../e-kr-case/onuljang.html"]},
    ],
    "e-kr-case": [
        {"page": "onuljang.html", "lang": "ko", "switch": "onuljang.en.html",
         "links": ["../a-gallery/northmere-library.ko.html", "../d-longread/meridian-rail.ko.html",
                   "../index.html"]},
        {"page": "onuljang.en.html", "lang": "en", "switch": "onuljang.html",
         "links": ["../a-gallery/northmere-library.html", "../d-longread/meridian-rail.html",
                   "../index.html"]},
    ],
}

errors = []


def err(path, msg):
    errors.append(f"{path.relative_to(ROOT)}: {msg}")


class Collector(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tags = []

    def handle_starttag(self, tag, attrs):
        self.tags.append((tag, {k: (v or "") for k, v in attrs}))

    handle_startendtag = handle_starttag


def parse_html(path):
    c = Collector()
    c.feed(path.read_text(encoding="utf-8"))
    return c.tags


def strip_comments(css):
    return re.sub(r"/\*.*?\*/", "", css, flags=re.S)


COLOR_LITERAL = re.compile(r"#[0-9a-fA-F]{3,8}\b|\b(?:rgba?|hsla?|oklch|oklab|lab|lch|color-mix)\(")
NAMED_COLOR = re.compile(
    r"(?:^|[;{\s])(?:color|background(?:-color)?|border(?:-[a-z-]+)?|outline(?:-color)?|fill|stroke|"
    r"text-decoration-color|box-shadow)\s*:[^;}]*\b(white|black|gray|grey|red|green|blue|purple|silver)\b")


def check_font_sizes(path, css):
    for m in re.finditer(r"(?<![-\w])font-size\s*:\s*([^;}{]+)", css):
        val = m.group(1).strip().replace("!important", "").strip()
        if not (re.fullmatch(r"var\(--fs-[a-z0-9-]+\)", val) or val in ("inherit", "1em", "100%")):
            err(path, f"font-size must use var(--fs-*): '{val}'")
    for m in re.finditer(r"(?<![-\w])font\s*:\s*([^;}{]+)", css):
        val = m.group(1).strip()
        if val != "inherit" and re.search(r"\d", val) and "var(--fs-" not in val:
            err(path, f"font shorthand with a raw size: '{val}'")


def check_token_file(path):
    css = strip_comments(path.read_text(encoding="utf-8"))
    for m in re.finditer(r"(--fs-\d+)\s*:\s*([^;]+);", css):
        name, val = m.group(1), m.group(2).strip()
        num = name.split("-")[-1]
        if num not in SCALE:
            err(path, f"{name} is not on the type scale 72/48/32/24/22/18/14")
        if val != f"{num}px":
            err(path, f"{name} must equal {num}px, got '{val}'")
    for m in re.finditer(r"(--fs-[a-z][a-z0-9-]*)\s*:\s*([^;]+);", css):
        name, val = m.group(1), m.group(2).strip()
        if not re.fullmatch(r"var\(--fs-\d+\)", val):
            err(path, f"role token {name} must point at a scale value var(--fs-NN), got '{val}'")
    for token in REQUIRED_TOKENS:
        if not re.search(re.escape(token) + r"\s*:", css):
            err(path, f"missing required token {token}")
    check_font_sizes(path, css)


SIZE_PROPS = (r"padding(?:-[a-z-]+)?|margin(?:-[a-z-]+)?|gap|row-gap|column-gap|inset(?:-[a-z-]+)?|"
              r"top|right|bottom|left|width|height|min-width|max-width|min-height|max-height|"
              r"grid-template-columns|grid-template-rows|grid-auto-rows|flex-basis|border-radius")
RAW_SIZE = re.compile(r"(?<![-\w])(" + SIZE_PROPS + r")\s*:\s*([^;}{]+)")
RAW_UNIT = re.compile(r"(?<![\w.-])(\d*\.?\d+)(px|em|rem|ch)\b")


def check_raw_sizes(path, css):
    """간격·폭·높이·행간·자간은 토큰으로. 예외: 1px·2px 선, 0, %, vw/vh, calc 안의 토큰 연산.
    @media / @container 조건은 var()를 못 쓰므로 검사에서 뺀다."""
    css = re.sub(r"@(media|container|supports)[^{]*\{", "{", css)
    for m in RAW_SIZE.finditer(css):
        prop, val = m.group(1), m.group(2)
        for u in RAW_UNIT.finditer(val):
            num = float(u.group(1))
            if u.group(2) == "px" and num <= 2:
                continue
            err(path, f"raw {prop} value '{u.group(0)}' — use a token (--space-*, --measure-*, …)")
    for m in re.finditer(r"(?<![-\w])line-height\s*:\s*([^;}{]+)", css):
        val = m.group(1).strip()
        if not (val.startswith("var(--lh-") or val in ("inherit", "normal")):
            err(path, f"raw line-height '{val}' — use a --lh-* token")
    for m in re.finditer(r"(?<![-\w])letter-spacing\s*:\s*([^;}{]+)", css):
        val = m.group(1).strip()
        if not (val.startswith("var(--ls-") or val in ("0", "inherit", "normal")):
            err(path, f"raw letter-spacing '{val}' — use a --ls-* token")


def check_component_css(path, strict_sizes=True):
    css = strip_comments(path.read_text(encoding="utf-8"))
    for m in COLOR_LITERAL.finditer(css):
        err(path, f"raw color literal '{m.group(0)}' — use a token from colors_and_type.css")
    for m in NAMED_COLOR.finditer(css):
        err(path, f"named color '{m.group(1)}' — use a token")
    if re.search(r"--fs-\d+\s*:", css):
        err(path, "type scale tokens belong in colors_and_type.css")
    check_font_sizes(path, css)
    if strict_sizes:
        check_raw_sizes(path, css)


def check_links(path, tags):
    hrefs = set()
    for tag, attrs in tags:
        for attr in ("href", "src"):
            url = attrs.get(attr)
            if url is None or url == "" or url.startswith("#"):
                continue
            if url.startswith(("mailto:", "tel:")):
                if tag == "a":
                    err(path, f"<a> must not point at a real address: {url} (use href=\"#\")")
                continue
            if url.startswith(("http://", "https://", "//")):
                if tag == "a":
                    err(path, f"<a> must not point at a real domain: {url} (use href=\"#\")")
                elif not url.startswith(ALLOWED_EXTERNAL):
                    err(path, f"external resource not allowed: {url}")
                continue
            clean = url.split("#")[0]
            local = clean.split("?")[0]
            target = (path.parent / local).resolve()
            if not target.exists():
                err(path, f"broken link: {url}")
            if tag in ("link", "script") and local.endswith((".css", ".js")) and "?v=" not in clean:
                err(path, f"local {local} must carry a ?v= cache version")
            if tag == "a":
                hrefs.add(local)
    return hrefs


def check_page(style, cfg):
    path = ROOT / style / cfg["page"]
    tags = parse_html(path)
    html_attrs = next((a for t, a in tags if t == "html"), {})
    if html_attrs.get("lang") != cfg["lang"]:
        err(path, f"<html lang> must be '{cfg['lang']}'")

    sheets = [a.get("href", "").split("?")[0] for t, a in tags
              if t == "link" and "stylesheet" in a.get("rel", "") and not a.get("href", "").startswith("http")]
    expected = ["../shared/base.css", "colors_and_type.css", "components.css"]
    normalized = [s[2:] if s.startswith("./") else s for s in sheets]
    if normalized != expected:
        err(path, f"local stylesheets must be exactly {expected} in that order, got {normalized}")

    for tag, attrs in tags:
        style_attr = attrs.get("style", "")
        if re.search(r"font|color|background", style_attr):
            err(path, f"inline style hardcodes design values on <{tag}>: '{style_attr}'")
        classes = attrs.get("class", "").split()
        if "ph" in classes:
            if attrs.get("role") != "img" or not attrs.get("aria-label"):
                err(path, f"placeholder .ph needs role=\"img\" and aria-label (classes: {classes})")
            if not any(c.startswith("r-") for c in classes) and "ph--fill" not in classes:
                err(path, f"placeholder .ph needs a ratio class r-* (classes: {classes})")

    hrefs = check_links(path, tags)
    for link in cfg["links"]:
        if link not in hrefs:
            err(path, f"missing required link to {link}")

    # 언어 전환: 같은 폴더의 다른 언어 파일로 가는 <a hreflang="…">, <head>의 rel=alternate
    other = "ko" if cfg["lang"] == "en" else "en"
    switch = [a for t, a in tags if t == "a" and a.get("href", "").split("?")[0] == cfg["switch"]]
    if not switch:
        err(path, f"missing KOR | ENG switch link to {cfg['switch']}")
    elif not any(a.get("hreflang") == other for a in switch):
        err(path, f"switch link to {cfg['switch']} needs hreflang=\"{other}\"")
    if not any(t == "link" and a.get("rel") == "alternate" and a.get("hreflang") == other
               and a.get("href", "").split("?")[0] == cfg["switch"] for t, a in tags):
        err(path, f"<head> needs <link rel=\"alternate\" hreflang=\"{other}\" href=\"{cfg['switch']}\">")
    if cfg["lang"] == "ko":
        fonts = [a.get("href", "") for t, a in tags if t == "link" and "stylesheet" in a.get("rel", "")]
        if not any("pretendard" in f.lower() for f in fonts):
            err(path, "Korean page must load Pretendard (jsDelivr) for Hangul")

    if style == "b-chapter":
        chapters = [a for t, a in tags if t == "section" and "data-chapter" in a]
        if len(chapters) != 7:
            err(path, f"expected 7 section[data-chapter], found {len(chapters)}")
        for a in chapters:
            if not a.get("id"):
                err(path, f"chapter '{a.get('data-chapter')}' needs an id")
        scripts = [a.get("src", "").split("?")[0] for t, a in tags if t == "script"]
        if "chapter-nav.js" not in scripts:
            err(path, "chapter-nav.js is not loaded")
    if style == "c-dossier":
        css = (ROOT / style / "colors_and_type.css").read_text(encoding="utf-8")
        for token in ("--brand", "--on-brand"):
            if not re.search(re.escape(token) + r"\s*:", css):
                err(ROOT / style / "colors_and_type.css", f"missing {token}")
        body = next((a for t, a in tags if t == "body"), {})
        client = body.get("data-client")
        if not client:
            err(path, "<body> needs data-client=\"…\" to pick a client brand colour")
        elif f'[data-client="{client}"]' not in css:
            err(path, f"no [data-client=\"{client}\"] block in colors_and_type.css")


VOID_TAGS = {"meta", "link", "br", "img", "input", "hr", "source", "area", "base", "col", "embed",
             "param", "track", "wbr"}


class Skeleton(HTMLParser):
    """body 안 요소의 (태그.클래스) 순서. .lang-switch 안쪽은 언어마다 다르므로 뺀다."""

    def __init__(self):
        super().__init__()
        self.seq, self.in_body, self.skip, self.stack = [], False, 0, []

    def handle_starttag(self, tag, attrs):
        a = {k: (v or "") for k, v in attrs}
        if tag == "body":
            self.in_body = True
            return
        if not self.in_body:
            return
        classes = a.get("class", "").split()
        entering_skip = "lang-switch" in classes
        if not self.skip:
            self.seq.append(".".join([tag] + sorted(classes)))
        if tag not in VOID_TAGS:
            self.stack.append(entering_skip)
            if entering_skip:
                self.skip += 1
        if entering_skip and tag in VOID_TAGS:
            pass

    def handle_endtag(self, tag):
        if self.in_body and tag not in VOID_TAGS and self.stack:
            if self.stack.pop():
                self.skip -= 1


def check_parity(style, pages):
    """같은 프로젝트의 국문/영문 파일은 마크업 골격이 같아야 한다 (글자만 다름)."""
    paths = [ROOT / style / cfg["page"] for cfg in pages]
    if not all(p.exists() for p in paths):
        return
    seqs = []
    for p in paths:
        s = Skeleton()
        s.feed(p.read_text(encoding="utf-8"))
        seqs.append(s.seq)
    a, b = seqs
    if a != b:
        i = next((k for k in range(min(len(a), len(b))) if a[k] != b[k]), min(len(a), len(b)))
        err(paths[1], f"markup skeleton differs from {paths[0].name} at element #{i}: "
                      f"{a[i:i + 3]} vs {b[i:i + 3]} ({len(a)} vs {len(b)} elements)")


def main():
    # 인자로 스타일 폴더 이름을 주면 그 스타일만 검사한다: python3 tools/check.py a-gallery
    only = sys.argv[1:]
    unknown = [s for s in only if s not in STYLES]
    if unknown:
        print(f"unknown style(s): {unknown}. choose from {list(STYLES)}")
        sys.exit(2)

    checked = 0
    base = ROOT / "shared" / "base.css"
    if not base.exists():
        err(ROOT, "missing shared/base.css")
    else:
        # base.css 는 스타일과 무관해서 스타일 토큰(--space-* 등)을 쓸 수 없다. 크기 검사는 제외.
        check_component_css(base, strict_sizes=False)
        checked += 1

    for style, pages in STYLES.items():
        if only and style not in only:
            continue
        for name in ["colors_and_type.css", "components.css"] + [cfg["page"] for cfg in pages]:
            if not (ROOT / style / name).exists():
                err(ROOT, f"missing {style}/{name}")
        if (ROOT / style / "colors_and_type.css").exists():
            check_token_file(ROOT / style / "colors_and_type.css")
            checked += 1
        if (ROOT / style / "components.css").exists():
            check_component_css(ROOT / style / "components.css")
            checked += 1
        for cfg in pages:
            if (ROOT / style / cfg["page"]).exists():
                check_page(style, cfg)
                checked += 1
        check_parity(style, pages)

    index = ROOT / "index.html"
    if only:
        pass
    elif not index.exists():
        err(ROOT, "missing index.html")
    else:
        tags = parse_html(index)
        hrefs = check_links(index, tags)
        for style, pages in STYLES.items():
            for cfg in pages:
                if f"{style}/{cfg['page']}" not in hrefs:
                    err(index, f"missing link to {style}/{cfg['page']}")
        checked += 1

    if errors:
        print(f"FAIL — {len(errors)} problem(s):")
        for e in errors:
            print("  -", e)
        sys.exit(1)
    print(f"OK — {checked} files checked")


if __name__ == "__main__":
    main()
