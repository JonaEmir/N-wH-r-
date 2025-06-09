import { productos } from './productos.js';

window.addEventListener('load', () => {
  
  const dropdown     = document.getElementById('dropdown');
  const selectedDiv  = dropdown.querySelector('.selected');
  const optionsList  = dropdown.querySelector('.options');
  const grid         = document.querySelector('.productos-grid');
  const categorias   = Object.keys(productos);  // ["tenis", "playeras", "pantalones"]

  /* -------- lógica de desplegar/cerrar -------- */
  selectedDiv.addEventListener('click', () => {
    dropdown.classList.toggle('open');
  });

  // Cierra si se hace clic fuera
  document.addEventListener('click', (e) => {
    if (!dropdown.contains(e.target)) dropdown.classList.remove('open');
  });

  /* -------- renderizado de productos ---------- */
  const renderProductos = (categoria) => {
    grid.innerHTML = '';

    const lista = categoria === 'all'
      ? categorias.flatMap(c => productos[c])
      : productos[categoria] || [];

    if (!lista.length) {
      grid.innerHTML = '<p>No hay productos disponibles.</p>';
      return;
    }

    lista.forEach(p => {
      const card = document.createElement('div');
      card.className = 'producto-card';
      card.innerHTML = `
        <div class="imagen-zoom">
          <a href="/web/detalles de producto/detalles.html">
            <img src="${p.img}" alt="${p.nombre}" class="zoomable">
          </a>
        </div>
        <div class="info">
          <h4>${p.nombre}</h4>
          <h5>${p.precio}</h5>
        </div>`;

      // Escucha clic en el enlace o en la tarjeta
      card.querySelector('a').addEventListener('click', () => {
        localStorage.setItem('productoSeleccionado', JSON.stringify(p));
          localStorage.setItem('origenSeccion', 'caballero'); 
      });

      grid.appendChild(card);
    });

  };

  // Inicial – “Todo”
  renderProductos('all');

  /* -------- cambio de categoría -------------- */
  optionsList.addEventListener('click', (e) => {
    const option = e.target.closest('.option');
    if (!option) return;

    // marcar selección visual
    optionsList.querySelectorAll('.option').forEach(o => o.classList.remove('selected'));
    option.classList.add('selected');

    // actualizar texto visible
    selectedDiv.childNodes[0].nodeValue = option.textContent.trim();

    // renderizar
    renderProductos(option.dataset.value);

    // cerrar menú
    dropdown.classList.remove('open');
  });
});

/*  justo después del  window.addEventListener('load', () => {   */
document.querySelectorAll('.caballero-section')
        .forEach(sec => sec.classList.add('fade-in'));

(() => {
  const productoCards = document.querySelectorAll('.producto-card');

  const onScrollProductos = () => {
    const windowHeight = window.innerHeight;

    productoCards.forEach(card => {
      const img = card.querySelector('.zoomable');
      if (!img) return;

      const rect = card.getBoundingClientRect();
      const visibleRatio = Math.min(Math.max((windowHeight - rect.top) / windowHeight, 0), 1);

      // Zoom de 1 a 1.2 basado en visibilidad
      img.style.transform = `scale(${1 + visibleRatio * 0.2})`;
      img.style.transition = 'transform 0.2s ease-out';
    });
  };

  window.addEventListener('scroll', onScrollProductos, { passive: true });
  onScrollProductos(); // llamada inicial
})();
