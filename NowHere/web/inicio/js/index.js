// --- Forzar scroll al inicio al cargar la página ---
if ('scrollRestoration' in history) {
  history.scrollRestoration = 'manual';
}

// --- Cuando todo esté listo ---
window.addEventListener('load', () => {
  // Forzar scroll arriba y prevenir animaciones
  document.documentElement.style.scrollBehavior = 'auto';
  window.scrollTo(0, 0);
  document.documentElement.style.scrollBehavior = '';

  // Activar todos los fade-in
  document.querySelectorAll('.fade-in')
          .forEach(el => el.classList.add('fade-active'));

  // Activar hero-banner (en caso no tenga fade-in de antes)
  document.querySelector('.hero-banner')?.classList.add('fade-in');

  // Activar banner-text con retraso (1 segundo)
  setTimeout(() => {
    document.querySelector('.banner-text')?.classList.add('fade-in');
  }, 1000);
});

// --- Efecto header con scroll ---
window.addEventListener('scroll', () => {
  const header = document.querySelector('header');
  header.classList.toggle('scrolled', window.scrollY > 10);
});


