/* dama/js/main.js
   - filtra las tarjetas ya impresas por Django
   - gestiona dropdown y zoom igual que caballero
*/

window.addEventListener('load', () => {
  const dropdown     = document.getElementById('dropdown');
  const selectedDiv  = dropdown.querySelector('.selected');
  const optionsList  = dropdown.querySelector('.options');
  const grid         = document.querySelector('.productos-grid');
  const allCards     = Array.from(grid.querySelectorAll('.producto-card'));

  /* ▸ abrir / cerrar dropdown */
  selectedDiv.addEventListener('click', () => dropdown.classList.toggle('open'));
  document.addEventListener('click', e => {
    if (!dropdown.contains(e.target)) dropdown.classList.remove('open');
  });

  /* ▸ filtrado por data-categoria */
  const renderProductos = cat => {
    allCards.forEach(card => {
      const c = card.dataset.categoria;
      card.style.display = (cat === 'all' || c === cat) ? 'block' : 'none';
    });
  };
  renderProductos('all');

  optionsList.addEventListener('click', e => {
    const option = e.target.closest('.option');
    if (!option) return;

    optionsList.querySelectorAll('.option')
               .forEach(o => o.classList.remove('selected'));
    option.classList.add('selected');
    selectedDiv.childNodes[0].nodeValue = option.textContent.trim();
    renderProductos(option.dataset.value);
    dropdown.classList.remove('open');
  });

  /* ▸ fade-in de la sección */
  document.querySelectorAll('.dama-section')
          .forEach(sec => sec.classList.add('fade-in'));

  /* ▸ zoom on scroll */
  const onScroll = () => {
    const wH = window.innerHeight;
    allCards.forEach(card => {
      const img  = card.querySelector('.zoomable');
      const rect = card.getBoundingClientRect();
      const r    = Math.min(Math.max((wH - rect.top) / wH, 0), 1);
      img.style.transform  = `scale(${1 + r * 0.2})`;
      img.style.transition = 'transform 0.2s ease-out';
    });
  };
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  /* ▸ guardar producto clicado */
  allCards.forEach(card => {
    const link = card.querySelector('a');
    link && link.addEventListener('click', () => {
      localStorage.setItem('productoSeleccionado', JSON.stringify({
        id     : card.dataset.id,
        nombre : card.dataset.nombre,
        precio : card.dataset.precio
      }));
      localStorage.setItem('origenSeccion', 'dama');
    });
  });
});
