document.addEventListener('DOMContentLoaded', async () => {
  try {
    const res = await fetch('/api/productos/');
    if (!res.ok) throw new Error('Error al obtener productos');
    const productos = await res.json();

    const container = document.getElementById('productos-container');
    container.innerHTML = '';

    if (productos.length === 0) {
      container.innerHTML = '<p>No hay productos registrados.</p>';
      return;
    }

    productos.forEach(p => {
      const card = document.createElement('div');
      card.classList.add('producto-card');

      card.innerHTML = `
        <img src="${p.imagen}" alt="Imagen de ${p.nombre}" height="120">
        <h3>${p.nombre}</h3>
        <p><strong>Descripción:</strong> ${p.descripcion}</p>
        <p><strong>Precio:</strong> $${p.precio}</p>
        <p><strong>Categoría:</strong> ${p.categoria}</p>
        <p><strong>Género:</strong> ${p.genero}</p>
        <p><strong>Stock:</strong> ${p.stock}</p>
        <p><strong>Oferta:</strong> ${p.en_oferta ? 'Sí' : 'No'}</p>
        <button onclick="editarProducto(${p.id})">✏️ Editar</button>
        <button onclick="eliminarProducto(${p.id})">🗑️ Eliminar</button>
        <hr>
      `;

      container.appendChild(card);
    });
  } catch (err) {
    document.getElementById('productos-container').innerHTML = `<p>Error: ${err.message}</p>`;
  }
});

function editarProducto(id) {
  window.location.href = `/dashboard/productos/editar/${id}/`;
}

async function eliminarProducto(id) {
  if (!confirm('¿Seguro que deseas eliminar este producto?')) return;

  try {
    const res = await fetch(`/api/productos/delete/${id}/`, {
      method: 'DELETE',
      headers: {
        'X-CSRFToken': getCookie('csrftoken'),
      },
    });

    const data = await res.json();
    alert(data.mensaje || data.error);
    location.reload();
  } catch (err) {
    alert('Error al eliminar producto: ' + err.message);
  }
}

function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
}