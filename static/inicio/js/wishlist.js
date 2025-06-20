/* static/js/wishlist.js
   Módulo ES para manejar la wishlist (solo frontend por ahora) */

export function initWishlist({
  selector   = '.wishlist-btn',   // botón que dispara la acción
  storageKey = 'wishlist_ids',    // localStorage key
  backendURL = null,              // pon la URL cuando exista la API
  csrfToken  = null               // opcional si usarás fetch
} = {}) {

  /* ─── Helpers de almacenamiento ─────────────────────────────── */
  const getList = () => {
    try { return JSON.parse(localStorage.getItem(storageKey)) || []; }
    catch { return []; }
  };

  const setList = arr => localStorage.setItem(storageKey, JSON.stringify(arr));

  /* ─── UI helpers ────────────────────────────────────────────── */
  const toggleBtn = (btn, active) => {
    btn.classList.toggle('active', active);
    const icon = btn.querySelector('i');
    icon.classList.toggle('fa-regular', !active);
    icon.classList.toggle('fa-solid',   active);
  };

  const hydrate = () => {
    const list = getList();
    list.forEach(id => {
      const btn = document.querySelector(`${selector}[data-product-id="${id}"]`);
      if (btn) toggleBtn(btn, true);
    });
  };

  /* ─── Evento click ──────────────────────────────────────────── */
  const clickHandler = async e => {
    const btn = e.target.closest(selector);
    if (!btn) return;

    const id     = btn.dataset.productId;
    let   list   = getList();
    const active = !btn.classList.contains('active'); // estado deseado

    // 1) UI inmediata
    toggleBtn(btn, active);

    // --- POP animation -----------------------------------------
    btn.classList.add('pop');                               // dispara la animación
    btn.addEventListener('animationend', () =>              // elimina la clase al terminar
      btn.classList.remove('pop'), { once: true });

    // 2) Actualiza localStorage
    if (active) {
      if (!list.includes(id)) list.push(id);
    } else {
      list = list.filter(x => x !== id);
    }
    setList(list);

    // 3) (Opcional) Sincroniza con tu backend cuando esté listo
    if (backendURL) {
      try {
        const res = await fetch(backendURL, {
          method : active ? 'POST' : 'DELETE',
          headers: {
            'Content-Type': 'application/json',
            ...(csrfToken && { 'X-CSRFToken': csrfToken })
          },
          body: JSON.stringify({ product_id: id })
        });
        if (!res.ok) throw new Error('Bad response');
      } catch (err) {
        // Revertir UI/local en caso de error
        toggleBtn(btn, !active);
        active
          ? setList(list.filter(x => x !== id))
          : setList([...list, id]);
        console.error('Wishlist sync error:', err);
        alert('No se pudo actualizar tu wishlist. Intenta de nuevo.');
      }
    }
  };

  /* ─── Activación ───────────────────────────────────────────── */
  hydrate();
  document.body.addEventListener('click', clickHandler);

  /* ─── API opcional que devuelve la instancia ───────────────── */
  return {
    destroy() {
      document.body.removeEventListener('click', clickHandler);
    },
    getWishlist: getList,
    setWishlist: setList
  };
}
