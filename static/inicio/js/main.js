// ─────────────────────────────────────────────────────────────────────────────
// 1. Forzar que la página abra arriba
// ─────────────────────────────────────────────────────────────────────────────
if ('scrollRestoration' in history) history.scrollRestoration = 'manual';

window.addEventListener('load', () => {
  document.documentElement.style.scrollBehavior = 'auto';
  window.scrollTo(0, 0);
  document.documentElement.style.scrollBehavior = '';

  document.querySelectorAll('.fade-in')
          .forEach(el => el.classList.add('fade-active'));

  document.querySelector('.hero-banner')?.classList.add('fade-in');
  setTimeout(() => {
    document.querySelector('.banner-text')?.classList.add('fade-in');
  }, 1000);

  document.querySelectorAll('.categoria-card')
          .forEach(c => c.classList.add('visible'));
});

// ─────────────────────────────────────────────────────────────────────────────
// 3. Header compacto
// ─────────────────────────────────────────────────────────────────────────────
window.addEventListener('scroll', () => {
  document.querySelector('header')
          .classList.toggle('scrolled', window.scrollY > 10);
});

// ─────────────────────────────────────────────────────────────────────────────
// 4. Overlay del menú burger
// ─────────────────────────────────────────────────────────────────────────────
const burger  = document.getElementById('burger');
const overlay = document.querySelector('.page-overlay');
const navMenu = document.querySelector('.nav-menu');

burger.addEventListener('change', () => {
  const open = burger.checked;
  overlay.style.opacity       = open ? '1' : '0';
  overlay.style.pointerEvents = open ? 'auto' : 'none';
  navMenu.style.transform     = open ? 'translateX(0)' : 'translateX(-100%)';
});

// ─────────────────────────────────────────────────────────────────────────────
// 5. Sticky-zoom progresivo sin saltos
// ─────────────────────────────────────────────────────────────────────────────
(() => {
  const header   = document.querySelector('header');
  const banners  = Array.from(document.querySelectorAll('.banner-zoom'));
  const cards    = document.querySelectorAll('.categoria-card');

  /* 5-A ▸ Altura real del header a variable CSS */
  const setHeaderH = () =>
    document.documentElement.style.setProperty(
      '--header-h', `${header.getBoundingClientRect().height}px`);
  setHeaderH();
  addEventListener('resize', setHeaderH);

  /* 5-B ▸ Scroll handler */
  const onScroll = () => {
    const sy      = window.scrollY;
    const hHeader = header.offsetHeight;

    banners.forEach((banner, i) => {
      const topDoc   = banner.offsetTop;          // parte superior absoluta
      const hBanner  = banner.offsetHeight;
      const start    = topDoc - hHeader;          // banner inicia sticky
      const end      = start + hBanner;           // banner deja de ser sticky
      const nextTop  = banners[i+1]
                       ? banners[i+1].offsetTop - hHeader
                       : end + hBanner;           // inicio del sig. o infinito

      const zoomable = banner.querySelector('.zoomable');

      /* ① Progreso global 0-1 desde que el header toca el banner
           hasta que el header toca el pie del banner                */
      const progress = Math.min(Math.max((sy - start) / hBanner, 0), 1);

      /* ② Zoom y opacidad con el MISMO progress
           - escala: 1 → 1.2
           - opacidad: 1 → 0                                   */
      zoomable.style.transform = `scale(${1 + progress * 0.20})`;
      banner.style.opacity     = `${1 - progress}`;

      /* ③ Asegurarse de que el banner no siga visible tras su tramo */
      if (sy >= nextTop) banner.style.opacity = '0';
      if (sy < start)   banner.style.opacity = '1'; // al subir reaparece
    });

    /* ④ Fade-in de tarjetas de producto */
    cards.forEach(card => {
      if (card.getBoundingClientRect().top < innerHeight - 50){
        card.classList.add('visible');
      }
    });
  };

  addEventListener('scroll', onScroll, { passive:true });
  onScroll(); // primera llamada
})();


function setupAccordion() {
  const toggles = document.querySelectorAll('.accordion-toggle');

  toggles.forEach(toggle => {
    toggle.addEventListener('click', () => {
      const content = toggle.nextElementSibling;

      const isOpen = content.classList.contains('open');
      content.classList.toggle('open', !isOpen);
      toggle.classList.toggle('active', !isOpen);
    });
  });
}

window.addEventListener('DOMContentLoaded', setupAccordion);

// Selecciona todos los botones con la clase común
document.querySelectorAll('.btn-seleccion').forEach(btn => {
  btn.addEventListener('click', () => {
    const seccion = btn.dataset.seccion;               // "caballero" o "dama"
    localStorage.setItem('origenSeccion', seccion);    // para la flecha de regreso
    window.location.href = `/templates/${seccion}.html`;
  });
});
