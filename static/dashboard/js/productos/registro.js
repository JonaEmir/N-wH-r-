document.addEventListener('DOMContentLoaded', () => {
  const form            = document.getElementById('productoForm');
  const mensaje         = document.getElementById('mensaje');
  const tallasContainer = document.getElementById('tallasContainer');
  const addTallaBtn     = document.getElementById('addTalla');
  const categoriaSelect = document.querySelector('select[name="categoria_id"]');

  // 🔁 Función que crea una fila nueva de talla + stock
  function crearFilaTalla() {
    const row = document.createElement('div');
    row.classList.add('talla-row');
    row.innerHTML = `
      <label>
        Talla
        <input type="text" name="tallas" required placeholder="Ej. 39" />
      </label>
      <label>
        Stock
        <input type="number" name="stocks" min="0" required placeholder="Ej. 5" />
      </label>
      <button type="button" class="removeTalla">✖</button>
    `;
    return row;
  }

  // ➕ Añadir fila de talla
  addTallaBtn.addEventListener('click', () => {
    tallasContainer.appendChild(crearFilaTalla());
  });

  // ❌ Eliminar fila
  tallasContainer.addEventListener('click', e => {
    if (e.target.classList.contains('removeTalla')) {
      e.target.closest('.talla-row').remove();
    }
  });

  // 🔃 Cargar categorías desde API
  // 🔃 Cargar categorías desde API
(async () => {
  try {
    const urlCategorias = form.dataset.catsUrl;
    const res = await fetch(urlCategorias);
    if (!res.ok) throw new Error('No se pudo obtener la lista de categorías');
    const cats = await res.json();
    categoriaSelect.innerHTML = '<option value="">— selecciona —</option>';
    cats.forEach(c => {
      const opt = document.createElement('option');
      opt.value = c.id;
      opt.textContent = c.nombre;
      categoriaSelect.appendChild(opt);
    });

    // Agrega una fila de talla por defecto
    tallasContainer.innerHTML = '';
    tallasContainer.appendChild(crearFilaTalla());
  } catch (err) {
    alert(err.message);
  }
})();


  // 🚀 Enviar formulario
  form.addEventListener('submit', async e => {
    e.preventDefault();
    mensaje.textContent = '';

    const formData = new FormData(form);

    try {
      const resp = await fetch(form.getAttribute('action'), {
        method: 'POST',
        body: formData
      });

      if (!resp.ok) {
        const err = await resp.json();
        throw new Error(err.error || 'Error desconocido');
      }

      const data = await resp.json();
      mensaje.style.color = 'green';
      mensaje.textContent = `✅ Producto #${data.id} creado con éxito`;

      form.reset();

      // Dejar una fila vacía
      tallasContainer.innerHTML = '';
      tallasContainer.appendChild(crearFilaTalla());

    } catch (err) {
      mensaje.style.color = 'red';
      mensaje.textContent = `❌ ${err.message}`;
    }
  });
});
