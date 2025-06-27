export function setupHeaderScroll() {
  window.addEventListener('scroll', () => {
    document.querySelector('header')
            .classList.toggle('scrolled', window.scrollY > 10);
  });
}
