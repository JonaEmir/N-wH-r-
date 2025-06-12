/* caballero/js/main.js
   Tarjetas llegan ya renderizadas desde el template de Django
   (bucle {% for producto in productos %}). El script:
   1) Maneja el dropdown de categorías
   2) Filtra las tarjetas existentes
   3) Aplica efecto fade-in a la sección
   4) Aplica zoom al hacer scroll
   5) Guarda en localStorage datos mínimos del producto clicado
*/

window.addEventListener('load', () => {

  /* ====== referencias DOM ====== */
  const dropdown     = document.getElementById('dropdown');
  const selectedDiv  = dropdown.querySelector('.selected');
  const optionsList  = dropdown.querySelector('.options');
  const grid         = document.querySelector('.productos-grid');
  /* todas las tarjetas que YA existen en el HTML */
  const allCards     = Array.from(grid.querySelectorAll('.producto-card'));

  /* ---------------------------------------------------
     1. Apertura / cierre del menú desplegable
  --------------------------------------------------- */
  selectedDiv.addEventListener('click', () =>
    dropdown.classList.toggle('open')
  );

  document.addEventListener('click', e => {
    if (!dropdown.contains(e.target)) dropdown.classList.remove('open');
  });

  /* ---------------------------------------------------
     2. Filtrado de tarjetas por categoría
        (usa el data-atribute que puso el template)
  --------------------------------------------------- */
  const renderProductos = categoria => {
    allCards.forEach(card => {
      const cat  = card.getAttribute('data-categoria');   // ej. "tenis"
      const show = categoria === 'all' || cat === categoria;
      card.style.display = show ? 'block' : 'none';
    });
  };

  /* estado inicial = mostrar todo */
  renderProductos('all');

  /* cambio de categoría en la lista */
  optionsList.addEventListener('click', e => {
    const option = e.target.closest('.option');
    if (!option) return;

    /* marcar visualmente la opción activa */
    optionsList.querySelectorAll('.option')
               .forEach(o => o.classList.remove('selected'));
    option.classList.add('selected');

    /* texto visible en el dropdown */
    selectedDiv.childNodes[0].nodeValue = option.textContent.trim();

    /* aplicar filtro */
    renderProductos(option.dataset.value);

    dropdown.classList.remove('open');
  });

  /* ---------------------------------------------------
     3. Fade-in de la sección Caballero
        (la clase .fade-in quita opacity:0 del CSS)
  --------------------------------------------------- */
  document.querySelectorAll('.caballero-section')
          .forEach(sec => sec.classList.add('fade-in'));

  /* ---------------------------------------------------
     4. Guardar en localStorage el producto clicado
        -> El template debe pasar data-id, data-nombre, etc.
           (al menos id para recuperar detalles vía backend)
  --------------------------------------------------- */
  allCards.forEach(card => {
    const link = card.querySelector('a');
    if (!link) return;

    link.addEventListener('click', () => {
      /* recogemos datos mínimos desde los data-attributes
         añadidos en caballero.html (id, nombre y precio) */
      const productoSeleccionado = {
        id      : card.dataset.id,
        nombre  : card.dataset.nombre,
        precio  : card.dataset.precio
      };
      localStorage.setItem('productoSeleccionado',
                           JSON.stringify(productoSeleccionado));
      localStorage.setItem('origenSeccion', 'caballero');
    });
  });
});

/* -----------------------------------------------------
   5. Efecto zoom al hacer scroll (igual que antes)
----------------------------------------------------- */
(() => {
  const onScrollProductos = () => {
    const productoCards = document.querySelectorAll('.producto-card');
    const windowHeight  = window.innerHeight;

    productoCards.forEach(card => {
      const img = card.querySelector('.zoomable');
      if (!img) return;

      const rect          = card.getBoundingClientRect();
      const visibleRatio  = Math.min(
                              Math.max((windowHeight - rect.top) / windowHeight, 0),
                              1
                            );

      img.style.transform  = `scale(${1 + visibleRatio * 0.2})`;
      img.style.transition = 'transform 0.2s ease-out';
    });
  };

  window.addEventListener('scroll', onScrollProductos, { passive: true });
  onScrollProductos(); // llamada inicial
})();
