/* ── Inicialização ──────────────────────────────────────────── */
lucide.createIcons();

/* ── Barra de progresso de leitura ─────────────────────────── */
const progressFill = document.getElementById("progressFill");

window.addEventListener("scroll", () => {
	const scrollTop = window.scrollY;
	const docHeight =
		document.documentElement.scrollHeight - window.innerHeight;
	if (docHeight > 0) {
		progressFill.style.width = `${(scrollTop / docHeight) * 100}%`;
	}
});

/* ── Modais ─────────────────────────────────────────────────── */
window.openModal = (modalId) => {
	const modal = document.getElementById(modalId);
	if (modal) {
		modal.classList.add("is-open");
		document.body.style.overflow = "hidden";
	}
};

window.closeModal = (modalId) => {
	const modal = document.getElementById(modalId);
	if (modal) {
		modal.classList.remove("is-open");
		document.body.style.overflow = "";
		const video = modal.querySelector("video");
		if (video) video.pause();
	}
};

// Fecha modal ao clicar fora (no overlay)
document.querySelectorAll(".overlay").forEach((overlay) => {
	overlay.addEventListener("click", (e) => {
		if (e.target === overlay) closeModal(overlay.id);
	});
});

/* ── Hotspot ────────────────────────────────────────────────── */
window.toggleHs = (btn, id) => {
	const pop = document.getElementById(id);
	const wasOpen = pop.classList.contains("is-open");
	const scene = btn.closest(".hs-scene");

	scene
		.querySelectorAll(".hs-popover")
		.forEach((p) => p.classList.remove("is-open"));
	scene
		.querySelectorAll(".btn, .hs-btn")
		.forEach((b) => b.classList.remove("is-active"));

	if (!wasOpen) {
		pop.classList.add("is-open");
		btn.classList.add("is-active");
	}
};

window.closeHs = (id) => {
	const pop = document.getElementById(id);
	if (pop) {
		pop.classList.remove("is-open");
		const scene = pop.closest(".hs-scene");
		if (scene) {
			scene
				.querySelectorAll(".btn, .hs-btn")
				.forEach((b) => b.classList.remove("is-active"));
		}
	}
};

/* ── Abas (Tabs) ────────────────────────────────────────────── */
window.switchTab = (tab, panelId) => {
	const tabs = tab.closest(".tabs");

	tabs.querySelectorAll(".tabs__tab").forEach((t) => {
		if (t.closest(".tabs") === tabs) {
			t.classList.remove("is-active");
			t.setAttribute("aria-selected", "false");
		}
	});

	tabs.querySelectorAll(".tabs__panel").forEach((p) => {
		if (p.closest(".tabs") === tabs) p.classList.remove("is-active");
	});

	tab.classList.add("is-active");
	tab.setAttribute("aria-selected", "true");

	const panel = document.getElementById(panelId);
	if (panel) panel.classList.add("is-active");
};

/* ── Carrossel ──────────────────────────────────────────────── */
window.crNav = (btn, dir) => {
	const car = btn.closest(".carousel");
	const slides = Array.from(car.querySelectorAll(".carousel__slide"));
	const dots = Array.from(car.querySelectorAll(".carousel__dot"));
	let cur = slides.findIndex((s) => s.classList.contains("is-active"));
	if (cur < 0) cur = 0;
	const next = (cur + dir + slides.length) % slides.length;

	slides[cur].classList.remove("is-active");
	slides[next].classList.add("is-active");
	if (dots[cur]) dots[cur].classList.remove("is-active");
	if (dots[next]) dots[next].classList.add("is-active");

	const counter = car.querySelector(".carousel__counter");
	if (counter) counter.textContent = `${next + 1} / ${slides.length}`;

	car.querySelectorAll(".hs-popover.is-open").forEach((p) =>
		p.classList.remove("is-open"),
	);
};

window.crGoTo = (dot, idx) => {
	const car = dot.closest(".carousel");
	const slides = Array.from(car.querySelectorAll(".carousel__slide"));
	const dots = Array.from(car.querySelectorAll(".carousel__dot"));
	const cur = slides.findIndex((s) => s.classList.contains("is-active"));
	if (cur === idx) return;

	slides[cur].classList.remove("is-active");
	slides[idx].classList.add("is-active");
	if (dots[cur]) dots[cur].classList.remove("is-active");
	if (dots[idx]) dots[idx].classList.add("is-active");

	const counter = car.querySelector(".carousel__counter");
	if (counter) counter.textContent = `${idx + 1} / ${slides.length}`;

	car.querySelectorAll(".hs-popover.is-open").forEach((p) =>
		p.classList.remove("is-open"),
	);
};

window.toggleCrPop = (btn, id) => {
	const pop = document.getElementById(id);
	const wasOpen = pop.classList.contains("is-open");
	btn.closest(".carousel")
		.querySelectorAll(".hs-popover")
		.forEach((p) => p.classList.remove("is-open"));
	if (!wasOpen) pop.classList.add("is-open");
};

window.closeCrPop = (id) => {
	document.getElementById(id).classList.remove("is-open");
};

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
