window.addEventListener('DOMContentLoaded', () => {
  const producto = JSON.parse(localStorage.getItem('productoSeleccionado'));
  if (!producto) return;

  const img    = document.getElementById('detalle-img');
  const nombre = document.getElementById('detalle-nombre');
  const precio = document.getElementById('detalle-precio');

  if (img)    img.src = producto.img;
  if (nombre) nombre.textContent = producto.nombre;
  if (precio) precio.textContent = producto.precio;

  const backLink = document.getElementById('volver-atras');
  const origen = localStorage.getItem('origenSeccion') || 'caballero';
  if (backLink) backLink.setAttribute('href', `/${origen}`);
});

window.addEventListener('load', () => {
  document.querySelectorAll('.detalle-section').forEach(el => {
    el.classList.add('fade-in');
  });
});

document.addEventListener('DOMContentLoaded', () => {
  const volver = document.getElementById('volver-atras');
  if (volver) {
    volver.addEventListener('click', (e) => {
      e.preventDefault(); // Evita comportamiento por defecto del enlace
      history.back();     // Vuelve a la página anterior
    });
  }
});


