document.getElementById('editarForm').addEventListener('submit', async function(e) {
  e.preventDefault();
  const form = e.target;
  const mensaje = document.getElementById('mensaje');
  mensaje.textContent = '';

  const formData = new FormData(form);
  const productoId = formData.get('id');

  try {
    const res = await fetch(`/api/productos/update/${productoId}/`, {
      method: 'POST',
      body: formData
    });

    const data = await res.json();

    if (!res.ok) throw new Error(data.error || 'Error al actualizar');

    mensaje.style.color = 'green';
    mensaje.textContent = data.mensaje;
  } catch (err) {
    mensaje.style.color = 'red';
    mensaje.textContent = '❌ ' + err.message;
  }
});