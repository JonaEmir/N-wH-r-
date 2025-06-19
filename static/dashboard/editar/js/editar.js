/* editar.js */
document.getElementById('editarForm').addEventListener('submit', async (e) => {
  e.preventDefault();

  const form     = e.target;
  const mensaje  = document.getElementById('mensaje');
  mensaje.textContent = '';

  const formData   = new FormData(form);
  const productoId = formData.get('id');

  try {
    /* 1. Actualiza el producto principal ----------------------- */
    const resProd = await fetch(`/api/productos/update/${productoId}/`, {
      method: 'POST',
      credentials: 'same-origin',   // ← envía cookies (csrftoken, sessionid)
      body: formData
    });

    const dataProd = await resProd.json();
    if (!resProd.ok) throw new Error(dataProd.error || 'Error al actualizar producto');

    /* 2. Actualiza cada variante ------------------------------- */
    const variantes = form.querySelectorAll('input[name="variante_id"]');

    for (let input of variantes) {
      const vId    = input.value;
      const stock  = form.querySelector(`[name="variante_stock_${vId}"]`)?.value;
      const precio = form.querySelector(`[name="variante_precio_${vId}"]`)?.value;

      await fetch(`/api/variantes/update/${vId}/`, {
        method: 'POST',
        credentials: 'same-origin',               // ← necesario para CSRF
        headers: {
          'X-CSRFToken': getCSRFToken(),          // ← token real
          'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: new URLSearchParams({ stock, precio })
      });
    }

    /* 3. Mensaje de éxito */
    mensaje.style.color = 'green';
    mensaje.textContent = dataProd.mensaje || 'Actualizado ✔️';

  } catch (err) {
    mensaje.style.color = 'red';
    mensaje.textContent = '❌ ' + err.message;
    console.error(err);
  }
});

/* Obtiene el token CSRF del meta del <head> ------------------ */
function getCSRFToken() {
  return document.querySelector('meta[name="csrf-token"]')?.content || '';
}
