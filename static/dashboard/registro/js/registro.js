const form = document.getElementById('productoForm');
const mensaje = document.getElementById('mensaje');

form.addEventListener('submit', async (e) => {
  e.preventDefault();               // anulamos envío normal
  mensaje.textContent = '';         // limpiamos mensaje anterior

  // Creamos un FormData que incluye los datos y archivos del formulario
  const formData = new FormData(form);

  try {
    const resp = await fetch('/api/productos/crear/', {
      method: 'POST',
      // NO usamos headers manuales; el navegador los pone correctamente con FormData
      body: formData
    });

    if (!resp.ok) {
      // la vista devuelve JSON con {'error': '...'} en caso de error
      const err = await resp.json();
      throw new Error(err.error || 'Error desconocido');
    }

    const resJson = await resp.json();
    mensaje.style.color = 'green';
    mensaje.textContent = `✅ Producto #${resJson.id} creado con éxito`;
    form.reset();
  } catch (err) {
    mensaje.style.color = 'red';
    mensaje.textContent = `❌ ${err.message}`;
  }
});

const categoriaSelect = document.querySelector('select[name="categoria_id"]');

// 1️⃣  Pedir las categorías a la API al cargar la página
document.addEventListener('DOMContentLoaded', async () => {
  try {
    const res = await fetch('/api/categorias/');
    if (!res.ok) throw new Error('No se pudo obtener la lista de categorías');
    const categorias = await res.json();

    // 2️⃣  Vaciar opciones actuales y añadir las que vienen de la BD
    categoriaSelect.innerHTML = '<option value="">— selecciona —</option>';
    categorias.forEach(cat => {
      const opt = document.createElement('option');
      opt.value = cat.id;
      opt.textContent = cat.nombre;
      categoriaSelect.appendChild(opt);
    });
  } catch (err) {
    alert(err.message);
  }
});

/*  ⬇️  …el resto de tu código (submit, etc.) permanece igual … */
