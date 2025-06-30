document.addEventListener('DOMContentLoaded', () => {
  const alertaMayoreo = document.getElementById('alerta-mayoreo');

  async function updateTotals() {
    if (!window.CLIENTE_ID) return;

    try {
      const res = await fetch(`/api/carrito/${CLIENTE_ID}/`);
      const data = await res.json();

      if (!res.ok) {
        console.error("Error al obtener carrito:", data);
        return;
      }

      const tieneProductos = data.items && data.items.length > 0;
      window.alternarVistaCarrito(tieneProductos);

      let total = 0;
      const items = document.querySelectorAll('.carrito-item');

        const totalPiezas = data.items.reduce((sum, item) => sum + item.cantidad, 0);
        const umbralMayoreo = 6;  // o el número que definas
        const piezasRestantes = Math.max(umbralMayoreo - totalPiezas, 0);

        const alertaMayoreo = document.getElementById('alerta-mayoreo');
        const alertaMeta = document.getElementById('alerta-meta-mayoreo');
        
        document.querySelectorAll('.piezas-restantes').forEach(el => {
            el.textContent = piezasRestantes;
        });



        if (data.mayoreo) {
        alertaMayoreo.style.display = 'block';
        alertaMeta.style.display = 'none';
        } else {
        alertaMayoreo.style.display = 'none';

        if (piezasRestantes > 0) {
            alertaMeta.style.display = 'block';
            document.querySelectorAll('.piezas-restantes').forEach(el => {
            el.textContent = piezasRestantes;
            });
        } else {
            alertaMeta.style.display = 'none';
        }

        }


      data.items.forEach((item, idx) => {
        const el = items[idx];
        const precio = data.mayoreo
          ? parseFloat(item.precio_mayorista)
          : parseFloat(item.precio_menudeo);

        const cantidad = item.cantidad;
        const subtotal = precio * cantidad;

        el.dataset.precio = precio;
        el.querySelector('.precio-unitario').textContent = precio.toFixed(2);
        el.querySelector('.qty').value = cantidad;
        el.querySelector('.subtotal').textContent = subtotal.toFixed(2);

        const badge = el.querySelector('.badge');
        if (badge) {
          badge.textContent = data.mayoreo ? '(mayoreo)' : '(menudeo)';
          badge.className = data.mayoreo ? 'badge badge-mayoreo' : 'badge badge-menudeo';
        }

        total += subtotal;
      });

      const subtotalEl = document.getElementById('carrito-subtotal');
      if (subtotalEl) {
        subtotalEl.textContent = `$${total.toFixed(2)}`;
      }

      if (alertaMayoreo) {
        alertaMayoreo.style.display = data.mayoreo ? 'block' : 'none';
      }

    } catch (err) {
      console.error("Error al actualizar totales:", err);
    }
  }

  async function patchCantidad(inputEl, cantidad) {
    const itemEl = inputEl.closest('.carrito-item');
    const varianteId = itemEl.dataset.varianteId;

    if (!CLIENTE_ID || !varianteId) return false;

    const res = await fetch(`/api/carrito/${CLIENTE_ID}/item/${varianteId}/actualizar/`, {
      method: 'PATCH',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie('csrftoken'),
      },
      body: JSON.stringify({ cantidad }),
    });

    return res.ok;
  }

  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let cookie of cookies) {
        cookie = cookie.trim();
        if (cookie.startsWith(name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }

  // Eventos cantidad
  document.querySelectorAll('.btn-minus').forEach(btn => {
    btn.addEventListener('click', async e => {
      const input = e.target.closest('.qty-wrap').querySelector('.qty');
      const newVal = Math.max(1, parseInt(input.value) - 1);
      input.value = newVal;
      if (await patchCantidad(input, newVal)) updateTotals();
    });
  });

  document.querySelectorAll('.btn-plus').forEach(btn => {
    btn.addEventListener('click', async e => {
      const input = e.target.closest('.qty-wrap').querySelector('.qty');
      const newVal = parseInt(input.value) + 1;
      input.value = newVal;
      if (await patchCantidad(input, newVal)) updateTotals();
    });
  });

  document.querySelectorAll('.qty').forEach(input => {
    input.addEventListener('change', async () => {
      let val = parseInt(input.value);
      if (isNaN(val) || val < 1) val = 1;
      input.value = val;
      if (await patchCantidad(input, val)) updateTotals();
    });
  });

  document.querySelectorAll('.item-remove').forEach(btn => {
    btn.addEventListener('click', async e => {
      const item = e.target.closest('.carrito-item');
      const varianteId = btn.dataset.varianteId;

      if (!CLIENTE_ID || !varianteId) return alert("Faltan datos.");

      try {
        const response = await fetch(`/api/carrito/${CLIENTE_ID}/item/${varianteId}/eliminar/`, {
          method: 'DELETE',
          headers: { 'X-CSRFToken': getCookie('csrftoken') }
        });

        if (response.ok) {
          item.remove();
          await updateTotals();
        } else {
          const data = await response.json();
          alert("Error al eliminar: " + (data.error || "desconocido"));
        }
      } catch {
        alert("Error de red al eliminar.");
      }
    });
  });

  document.querySelector('.btn-vaciar')?.addEventListener('click', async () => {
    if (!CLIENTE_ID) return alert("Cliente no identificado.");
    if (!confirm("¿Vaciar todo el carrito?")) return;

    try {
      const response = await fetch(`/api/carrito/${CLIENTE_ID}/empty/`, {
        method: 'DELETE',
        headers: { 'X-CSRFToken': getCookie('csrftoken') }
      });

      if (response.ok) {
        document.querySelectorAll('.carrito-item').forEach(item => item.remove());
        await updateTotals();
        alert("Carrito vaciado.");
      } else {
        const data = await response.json();
        alert("Error al vaciar: " + (data.error || 'Desconocido'));
      }
    } catch {
      alert("Error de red al vaciar.");
    }
  });

  document.querySelector('.btn-actualizar')?.addEventListener('click', () => {
    alert("Cantidades actualizadas.");
  });

  // ✅ Única definición limpia de la función global
  window.alternarVistaCarrito = function(hayProductos) {
    const activo = document.getElementById('carrito-activo');
    const vacio = document.getElementById('carrito-vacio');
    if (!activo || !vacio) return;

    if (hayProductos) {
      vacio.classList.remove('fade-in-down');
      vacio.classList.add('fade-out-up');
      setTimeout(() => {
        vacio.style.display = 'none';
        activo.style.display = 'block';
        activo.classList.remove('fade-out-down');
        activo.classList.add('fade-in-up');
      }, 300);
    } else {
      activo.classList.remove('fade-in-up');
      activo.classList.add('fade-out-down');
      setTimeout(() => {
        activo.style.display = 'none';
        vacio.style.display = 'block';
        vacio.classList.remove('fade-out-up');
        vacio.classList.add('fade-in-down');
      }, 300);
    }
  };

  updateTotals();

  const carritoContainer = document.getElementById('carrito-container');
setTimeout(() => {
  carritoContainer.classList.add('fade-in-carrito');
}, 100); // Pequeño delay para que el navegador detecte el cambio


});
