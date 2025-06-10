window.addEventListener('DOMContentLoaded', () => {
  const producto = JSON.parse(localStorage.getItem('productoSeleccionado'));
  if (!producto) return;

  // Ejemplo: insertamos en elementos del DOM
  document.getElementById('detalle-img').src = producto.img;
  document.getElementById('detalle-nombre').textContent = producto.nombre;
  document.getElementById('detalle-precio').textContent = producto.precio;
});

window.addEventListener('load', () => {
  document.querySelectorAll('.detalle-section').forEach(el => {
    el.classList.add('fade-in');
  });
});

window.addEventListener('DOMContentLoaded', () => {
  /* --- Cargar info producto (lo que ya tienes) --- */
  const producto = JSON.parse(localStorage.getItem('productoSeleccionado'));
  if (producto) {
    /* …pintar imagen, nombre, precio… */
  }

  /* --- Ajustar enlace de regreso --- */
  const origen = localStorage.getItem('origenSeccion') || 'caballero';
  const backLink = document.getElementById('volver-atras');
  backLink.setAttribute('href', `/${origen}`);
});

// al hacer click en la flecha, limpia para no acumular valores viejos
document.getElementById('volver-atras').addEventListener('click', () => {
  localStorage.removeItem('origenSeccion');
});
