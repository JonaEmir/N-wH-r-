import { productos } from './productos.js';

window.addEventListener('load', () => {
  const dropdown     = document.getElementById('dropdown');
  const selectedDiv  = dropdown.querySelector('.selected');
  const optionsList  = dropdown.querySelector('.options');
  const grid         = document.querySelector('.productos-grid');
  const categorias   = Object.keys(productos);

  /* abrir / cerrar dropdown */
  selectedDiv.addEventListener('click', () => dropdown.classList.toggle('open'));
  document.addEventListener('click', e => {
    if (!dropdown.contains(e.target)) dropdown.classList.remove('open');
  });

  /* render de tarjetas */
  const renderProductos = cat => {
    grid.innerHTML = '';

    const lista = cat === 'all'
      ? categorias.flatMap(c => productos[c])
      : productos[cat] || [];

    if (!lista.length) {
      grid.innerHTML = '<p>No hay productos disponibles.</p>';
      return;
    }

    lista.forEach(p => {
      const card = document.createElement('div');
      card.className = 'producto-card';
      card.innerHTML = `
        <div class="imagen-zoom">
          <a href="/detalles/">
            <img src="${p.img}" alt="${p.nombre}" class="zoomable">
          </a>
        </div>
        <div class="info">
          <h4>${p.nombre}</h4>
          <h5>${p.precio}</h5>
        </div>`;

      card.querySelector('a').addEventListener('click', () => {
        localStorage.setItem('productoSeleccionado', JSON.stringify(p));
        localStorage.setItem('origenSeccion', 'dama'); 
      });

      grid.appendChild(card);
    });
  };

  renderProductos('all');

  optionsList.addEventListener('click', e => {
    const option = e.target.closest('.option');
    if (!option) return;

    optionsList.querySelectorAll('.option').forEach(o => o.classList.remove('selected'));
    option.classList.add('selected');

    selectedDiv.childNodes[0].nodeValue = option.textContent.trim();
    renderProductos(option.dataset.value);

    dropdown.classList.remove('open');
  });
});

/* activar fade-in */
document.querySelectorAll('.dama-section').forEach(sec => sec.classList.add('fade-in'));
