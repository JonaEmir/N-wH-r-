export function setupScrollRestoration() {
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
  });
}
