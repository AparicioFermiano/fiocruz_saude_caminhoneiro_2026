
/* -- Sidebar: destaque da secao ativa ----- */
const sidebarLinks = document.querySelectorAll(".sidebar-nav__link");
if (sidebarLinks.length) {
  const sections = document.querySelectorAll("section[id]");
  const obs = new IntersectionObserver(
    (entries) => {
      entries.forEach(e => {
        if (e.isIntersecting) {
          sidebarLinks.forEach(l => l.classList.remove("is-active"));
          const sel = ".sidebar-nav__link[href=\"#" + e.target.id + "\"]";
          const a = document.querySelector(sel);
          if (a) a.classList.add("is-active");
        }
      });
    },
    { rootMargin: "-15% 0px -75% 0px" }
  );
  sections.forEach(s => obs.observe(s));
}
