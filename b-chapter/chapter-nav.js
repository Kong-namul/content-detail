/* ==========================================================================
   B 챕터형 — 하단 고정 챕터 바
   마크업 계약:
     <nav class="chapter-bar" data-chapter-bar hidden aria-label="Chapters">
       <button type="button" class="chapter-bar__toggle" data-chapter-toggle
               aria-expanded="false" aria-controls="chapter-menu">
         <span class="chapter-bar__project">Tamo Bank</span>
         <span class="chapter-bar__sep" aria-hidden="true">|</span>
         <span class="sr-only">Current chapter:</span>
         <span class="chapter-bar__current" data-chapter-current>Challenge</span>
         <span class="chapter-bar__caret" aria-hidden="true">▾</span>
       </button>
       <ol class="chapter-bar__menu" id="chapter-menu" data-chapter-menu hidden></ol>
     </nav>
     <section class="chapter" id="challenge" data-chapter="Challenge">…</section>
   - 바는 HTML에서 hidden. JS가 켜질 때만 보인다 (JS가 없으면 챕터 내용만 보임).
   - 메뉴 항목은 section[data-chapter]에서 자동으로 만든다.
   - 첫 챕터가 화면 중앙에 닿기 전에는 .is-visible 이 빠진다 (CSS가 숨김 처리).
   ========================================================================== */
(() => {
  const bar = document.querySelector("[data-chapter-bar]");
  if (!bar) return;
  const toggle = bar.querySelector("[data-chapter-toggle]");
  const current = bar.querySelector("[data-chapter-current]");
  const menu = bar.querySelector("[data-chapter-menu]");
  const sections = Array.from(document.querySelectorAll("section[data-chapter][id]"));
  if (!toggle || !current || !menu || sections.length === 0) return;

  sections.forEach((section) => {
    const item = document.createElement("li");
    const link = document.createElement("a");
    link.href = `#${section.id}`;
    link.textContent = section.dataset.chapter;
    item.appendChild(link);
    menu.appendChild(item);
  });
  const links = Array.from(menu.querySelectorAll("a"));

  const setOpen = (open) => {
    toggle.setAttribute("aria-expanded", String(open));
    menu.hidden = !open;
    bar.classList.toggle("is-open", open);
  };

  const setCurrent = (section) => {
    current.textContent = section.dataset.chapter;
    links.forEach((link) => {
      if (link.hash === `#${section.id}`) link.setAttribute("aria-current", "location");
      else link.removeAttribute("aria-current");
    });
  };

  toggle.addEventListener("click", () => {
    setOpen(toggle.getAttribute("aria-expanded") !== "true");
  });
  links.forEach((link) => link.addEventListener("click", () => setOpen(false)));
  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && toggle.getAttribute("aria-expanded") === "true") {
      setOpen(false);
      toggle.focus();
    }
  });
  document.addEventListener("click", (event) => {
    if (!bar.contains(event.target)) setOpen(false);
  });

  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) setCurrent(entry.target);
      });
    },
    { rootMargin: "-50% 0px -50% 0px" }
  );
  sections.forEach((section) => observer.observe(section));

  const first = sections[0];
  const updateVisibility = () => {
    const visible = first.getBoundingClientRect().top < window.innerHeight * 0.5;
    bar.classList.toggle("is-visible", visible);
    if (!visible) setOpen(false);
  };

  setCurrent(first);
  setOpen(false);
  bar.hidden = false;
  updateVisibility();
  window.addEventListener("scroll", updateVisibility, { passive: true });
  window.addEventListener("resize", updateVisibility);
})();
