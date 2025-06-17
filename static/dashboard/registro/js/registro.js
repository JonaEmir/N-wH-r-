// static/dashboard/registro/js/registro.js

const form            = document.getElementById('productoForm');
const mensaje         = document.getElementById('mensaje');
const tallasContainer = document.getElementById('tallasContainer');
const addTallaBtn     = document.getElementById('addTalla');
const categoriaSelect = document.querySelector('select[name="categoria_id"]');

// 1️⃣ Función que crea una fila (talla + stock + botón de quitar)
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

// 2️⃣ Añadir una nueva fila cuando se pulsa el botón
addTallaBtn.addEventListener('click', () => {
  tallasContainer.appendChild(crearFilaTalla());
});

// 3️⃣ Delegación para quitar filas al pulsar “✖”
tallasContainer.addEventListener('click', e => {
  if (e.target.classList.contains('removeTalla')) {
    e.target.closest('.talla-row').remove();
  }
});

// 4️⃣ Cargar categorías desde la API al inicio
document.addEventListener('DOMContentLoaded', async () => {
  try {
    const res = await fetch(form.getAttribute('action').replace('/crear/', '/categorias/'));
    if (!res.ok) throw new Error('No se pudo obtener la lista de categorías');
    const cats = await res.json();
    categoriaSelect.innerHTML = '<option value="">— selecciona —</option>';
    cats.forEach(c => {
      const opt = document.createElement('option');
      opt.value = c.id;
      opt.textContent = c.nombre;
      categoriaSelect.appendChild(opt);
    });
  } catch (err) {
    alert(err.message);
  }
});

// 5️⃣ Envío del formulario por AJAX
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

    // Dejar una única fila vacía de tallas
    tallasContainer.innerHTML = '';
    tallasContainer.appendChild(crearFilaTalla());
  } catch (err) {
    mensaje.style.color = 'red';
    mensaje.textContent = `❌ ${err.message}`;
  }
});
