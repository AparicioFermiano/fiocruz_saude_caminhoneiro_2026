/* ── Progress bar + back-to-top + TOC highlight ── */
(function () {
  var pf = document.getElementById('pf'),
      tt = document.getElementById('totop'),
      toc = document.querySelectorAll('.toc a'),
      secs = document.querySelectorAll('.content section');

  function upd() {
    var d = document.documentElement,
        t = d.scrollTop || document.body.scrollTop,
        h = d.scrollHeight - d.clientHeight;
    if (pf) pf.style.width = (h > 0 ? t / h * 100 : 0) + '%';
    if (tt) { t > 300 ? tt.classList.add('is-shown') : tt.classList.remove('is-shown'); }
    if (toc.length && secs.length) {
      var cur = '';
      secs.forEach(function (s) { if (s.getBoundingClientRect().top <= 120) cur = s.id; });
      toc.forEach(function (a) { a.classList.toggle('is-active', a.getAttribute('href') === '#' + cur); });
    }
  }

  window.addEventListener('scroll', upd, { passive: true });
  if (tt) tt.addEventListener('click', function () { window.scrollTo({ top: 0, behavior: 'smooth' }); });
  upd();
})();

/* ── Modal helpers ── */
function openModal(id) {
  var o = document.getElementById(id);
  if (o) { o.classList.add('is-open'); document.body.style.overflow = 'hidden'; }
}

function closeModal(id) {
  var o = document.getElementById(id);
  if (o) { o.classList.remove('is-open'); document.body.style.overflow = ''; }
}

/* ── Modal event delegation (data-open-modal / data-close-modal) ── */
document.addEventListener('click', function (e) {
  var op = e.target.closest('[data-open-modal]');
  if (op) { openModal(op.dataset.openModal); return; }
  var cl = e.target.closest('[data-close-modal]');
  if (cl) { closeModal(cl.dataset.closeModal); return; }
  var ov = e.target.closest('.overlay');
  if (ov && e.target === ov) closeModal(ov.id);
});

document.addEventListener('keydown', function (e) {
  if (e.key === 'Escape')
    document.querySelectorAll('.overlay.is-open').forEach(function (o) { closeModal(o.id); });
});

/* ── Hotspots ── */
(function () {
  var fig = document.querySelector('.hotspot-fig');
  if (!fig) return;

  fig.querySelectorAll('.hotspot').forEach(function (h) {
    h.addEventListener('click', function (e) {
      e.stopPropagation();
      var b = document.getElementById(h.dataset.balloon),
          open = b && b.classList.contains('is-open');
      fig.querySelectorAll('.balloon').forEach(function (x) { x.classList.remove('is-open'); });
      fig.querySelectorAll('.hotspot').forEach(function (x) { x.classList.remove('is-active'); });
      if (b && !open) { b.classList.add('is-open'); h.classList.add('is-active'); }
    });
  });

  fig.querySelectorAll('.balloon__close').forEach(function (c) {
    c.addEventListener('click', function () {
      c.closest('.balloon').classList.remove('is-open');
      fig.querySelectorAll('.hotspot').forEach(function (x) { x.classList.remove('is-active'); });
    });
  });

  fig.addEventListener('click', function () {
    fig.querySelectorAll('.balloon').forEach(function (x) { x.classList.remove('is-open'); });
    fig.querySelectorAll('.hotspot').forEach(function (x) { x.classList.remove('is-active'); });
  });
})();

/* ── Sidebar toggle ── */
(function () {
  var btn = document.getElementById('sidebar-toggle'),
      sb  = document.getElementById('sidebar'),
      cls = document.getElementById('sidebar-close'),
      ov  = document.getElementById('sidebar-overlay');
  if (!sb) return;

  function mobile() { return window.innerWidth <= 920; }

  if (btn) {
    btn.addEventListener('click', function () {
      if (mobile()) {
        var open = sb.classList.toggle('is-open');
        if (ov) ov.classList.toggle('is-open', open);
        btn.setAttribute('aria-expanded', String(open));
      } else {
        var closed = document.body.classList.toggle('sidebar-closed');
        btn.setAttribute('aria-expanded', String(!closed));
      }
    });
  }

  if (cls) {
    cls.addEventListener('click', function () {
      if (mobile()) {
        sb.classList.remove('is-open');
        if (ov) ov.classList.remove('is-open');
        if (btn) btn.setAttribute('aria-expanded', 'false');
      } else {
        document.body.classList.add('sidebar-closed');
        if (btn) btn.setAttribute('aria-expanded', 'false');
      }
    });
  }

  if (ov) {
    ov.addEventListener('click', function () {
      sb.classList.remove('is-open');
      ov.classList.remove('is-open');
      if (btn) btn.setAttribute('aria-expanded', 'false');
    });
  }

  window.addEventListener('resize', function () {
    if (!mobile()) {
      sb.classList.remove('is-open');
      if (ov) ov.classList.remove('is-open');
    }
  });
})();
