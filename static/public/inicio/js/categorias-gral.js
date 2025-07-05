export function setupCategoriaCards() {
  const cards = document.querySelectorAll('.categoria-card');
  console.log('🟢 Encontradas:', cards.length, 'tarjetas');

  if (!cards.length) return;

  const observer = new IntersectionObserver(entries => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        const card = entry.target;
        const index = [...cards].indexOf(card);
        const delay = index * 150;

        // Animación escalonada para la tarjeta
        card.style.transitionDelay = `${delay}ms`;

        // Animación escalonada + 500ms para el texto
        const overlay = card.querySelector('.overlay-text');
        if (overlay) {
          overlay.style.transitionDelay = `${delay + 500}ms`;
        }

        card.classList.add('visible');
        observer.unobserve(card);

        console.log('🔵 Activando animación en:', card);
      }
    });
  }, { threshold: 0.1 });

  cards.forEach(card => observer.observe(card));
}
