/**
 * initWishlist – versión multi-usuario robusta
 *   • Una clave de localStorage por usuario (o "guest").
 *   • Migración automática de wishlist_ids_guest → wishlist_ids_<clienteId>.
 *   • Retorna { clearWishlist } para que puedas vaciar la lista al hacer logout.
 * --------------------------------------------------------------------------
 */
export function initWishlist({
  selector          = '.wishlist-btn',
  storageKey        = 'wishlist_ids',   // clave base (se versiona internamente)
  backendURL        = null,
  csrfToken         = null,
  isAuthenticated   = false,
  onRequireLogin    = null,
  fetchProductoURL  = null,
  clienteId         = null
} = {}) {

/* ─────────────── 0. Clave de almacenamiento y migración ─────────────── */
const storageKeyBase = storageKey;
const storageKeyUser = (isAuthenticated && clienteId != null)
      ? `${storageKeyBase}_${clienteId}`   // p.ej. wishlist_ids_42
      : `${storageKeyBase}_guest`;         // navegación sin login

if (isAuthenticated && clienteId != null) {
  // Pasa los likes del invitado al usuario que acaba de iniciar sesión
  try {
    const guestKey   = `${storageKeyBase}_guest`;
    const guestRaw   = localStorage.getItem(guestKey);
    if (guestRaw) {
      const guestList = JSON.parse(guestRaw) || [];
      const userRaw   = localStorage.getItem(storageKeyUser);
      const userList  = userRaw ? JSON.parse(userRaw) : [];
      const merged    = [...new Set([...userList, ...guestList])];
      localStorage.setItem(storageKeyUser, JSON.stringify(merged));
      localStorage.removeItem(guestKey);
    }
  } catch { /* Si hay error de parseo, simplemente lo ignoramos */ }
}

/* ───────────────────── 1. Referencias DOM ───────────────────────────── */
const wishlistIcon    = document.querySelector('#btn-wishlist-panel i');
const wishlistCount   = document.querySelector('#btn-wishlist-panel .wishlist-count');
const wishlistBtn     = document.getElementById('btn-wishlist-panel');
const wishlistPanel   = document.getElementById('wishlist-panel');
const closeBtn        = document.getElementById('close-wishlist-panel');
const wishlistContent = wishlistPanel?.querySelector('.wishlist-content');
const overlay         = document.querySelector('.page-overlay');

/* ───────────────────── 2. LocalStorage helpers ──────────────────────── */
const getList = () => {
  try { return JSON.parse(localStorage.getItem(storageKeyUser)) || []; }
  catch { return []; }
};
const setList = list => {
  localStorage.setItem(storageKeyUser, JSON.stringify(list));
  updateHeaderUI(list);
};

/* ───────────────────── 3. Header UI helpers ─────────────────────────── */
const toggleBtn = (btn, on) => {
  btn.classList.toggle('active', on);
  const ic = btn.querySelector('i');
  if (ic) { ic.classList.toggle('fa-solid', on);
            ic.classList.toggle('fa-regular', !on); }
};
const updateHeaderUI = list => {
  wishlistIcon?.classList.toggle('fa-solid', !!list.length);
  wishlistIcon?.classList.toggle('fa-regular', !list.length);
  if (wishlistIcon) wishlistIcon.style.color = list.length ? '#ff4d6d' : '';
  if (wishlistCount) {
    wishlistCount.textContent = list.length;
    wishlistCount.hidden = list.length === 0;
  }
};
const hydrate = () => {
  const list = getList();
  list.forEach(id => {
    const btn = document.querySelector(
      `${selector}[data-product-id="${id}"]`);
    btn && toggleBtn(btn, true);
  });
  updateHeaderUI(list);
};

/* ───────────────────── 4. clearWishlist (API pública) ───────────────── */
function clearWishlist() {
  localStorage.removeItem(storageKeyUser);
  updateHeaderUI([]);
  document.querySelectorAll(`${selector}.active`)
          .forEach(btn => toggleBtn(btn, false));
}

/* ───────────────────── 5. Panel show/hide ───────────────────────────── */
const showWishlist = () => {
  wishlistPanel?.classList.add('open');
  overlay?.classList.add('active');
};
const hideWishlist = () => {
  const picker = wishlistPanel.querySelector('.size-picker');
  if (picker) closeSizePicker(picker, 'side');
  wishlistPanel.classList.remove('open');
  overlay.classList.remove('active');
};
overlay?.addEventListener('click', hideWishlist);

/* ───────────────────── 6. Corazones del catálogo ───────────────────── */
document.body.addEventListener('click', e => {
  const heart = e.target.closest(selector);
  if (!heart) return;

  if (!isAuthenticated) { onRequireLogin?.(); return; }

  const id   = heart.dataset.productId;
  let   list = getList();
  const add  = !heart.classList.contains('active');

  toggleBtn(heart, add);
  add ? list.push(id) : list = list.filter(x => x !== id);
  setList(list);

  if (backendURL && clienteId != null) {
    fetch(`${backendURL}${clienteId}/`, {
      method : add ? 'PATCH' : 'DELETE',
      headers: { 'Content-Type':'application/json',
                 ...(csrfToken && { 'X-CSRFToken': csrfToken })},
      body   : JSON.stringify({ producto_id: id })
    }).catch(err => console.error('Wishlist sync', err));
  }
});

/* ───────────────────── 7. Placeholder “add to cart” ─────────────────── */
const addToCart = (productoId, talla) => {
  console.log(`addToCart → id=${productoId} talla=${talla}`);
  /* TODO: fetch('/carrito/', { body:{productoId, talla} }) */
};

/* ───────────────────── 8. Render del panel ─────────────────────────── */
const renderWishlistPanel = async () => {
  wishlistContent.textContent = 'Cargando…';
  if (!fetchProductoURL || !clienteId) {
    wishlistContent.textContent = 'No tienes productos en tu wishlist.';
    return;
  }
  try {
    const res = await fetch(`${fetchProductoURL}${clienteId}/`);
    if (!res.ok) throw new Error('Error al obtener productos');
    const { productos = [] } = await res.json();
    if (!productos.length) {
      wishlistContent.textContent = 'No tienes productos en tu wishlist.';
      return;
    }
    const frag = document.createDocumentFragment();
    for (const p of productos) {
      const sizes = Array.isArray(p.tallas) && p.tallas.length
        ? p.tallas.join(',') : '';
      const item = document.createElement('div');
      item.className = 'wishlist-item';
      item.innerHTML = `
        <img src="${p.imagen || '/static/img/no-image.jpg'}" alt="${p.nombre}">
        <div class="wishlist-details">
          <h4>${p.nombre}</h4>
          <span class="precio">$${p.precio}</span>
        </div>
        <div class="wishlist-actions">
          <button class="btn-carrito-mini"
                  data-id="${p.id}"
                  data-sizes="${sizes}">
            Agregar
          </button>
        </div>`;
      frag.appendChild(item);
    }
    wishlistContent.innerHTML = '';
    wishlistContent.appendChild(frag);
  } catch (err) {
    console.error(err);
    wishlistContent.textContent = 'Hubo un error al cargar tu wishlist.';
  }
};

/* ============== 9. Selector de talla dinámico ======================== */
wishlistContent?.addEventListener('click', async e => {
  /* —— click en “Agregar” —— */
  if (e.target.matches('.btn-carrito-mini')) {
    const pid  = e.target.dataset.id;
    const open = wishlistPanel.querySelector('.size-picker');
    if (open) {
      if (open.dataset.productId === pid) { closeSizePicker(open); return; }
      closeSizePicker(open);
    }
    /* 1. solicitar tallas al back-end */
    let sizes = [];
    try {
      const res  = await fetch(`/api/productos/${pid}/`);
      if (!res.ok) throw new Error('Error fetch tallas');
      const data = await res.json();
      sizes = Array.isArray(data.tallas) && data.tallas.length
              ? data.tallas : ['Única'];
    } catch {
      sizes = ['Única'];
    }
    /* 2. construir el selector */
    const picker = document.createElement('div');
    picker.className = 'size-picker slide-up-full';
    picker.dataset.productId = pid;
    picker.innerHTML = `
      <div class="size-picker-inner">
        <h3>Selecciona tu talla</h3>
        <div class="size-options">
          ${sizes.map(s => `<button class="size-option" data-size="${s.trim()}">${s.trim()}</button>`).join('')}
        </div>
        <button class="close-size-picker">✕</button>
      </div>`;
    picker.addEventListener('click', ev => {
      if (ev.target.matches('.close-size-picker')) {
        closeSizePicker(picker);
      }
    });
    wishlistPanel.appendChild(picker);
    /* 3. posicionar y bloquear scroll interno */
    const rect = wishlistPanel.getBoundingClientRect();
    picker.style.position = 'fixed';
    picker.style.left     = `${rect.left}px`;
    picker.style.width    = `${rect.width}px`;
    picker.style.bottom   = '0';
    wishlistPanel.dataset.prevOverflow = wishlistPanel.style.overflowY || '';
    wishlistPanel.style.overflowY = 'hidden';
    wishlistContent.classList.add('blurred');
    return;
  }
  /* —— click en talla —— */
  if (e.target.matches('.size-option')) {
    const talla = e.target.dataset.size;
    const pid   = e.target.closest('.size-picker').dataset.productId;
    addToCart(pid, talla);
    e.target.classList.add('chosen');
    setTimeout(() => closeSizePicker(
                 e.target.closest('.size-picker')), 150);
    return;
  }
});

/* —— cerrar picker haciendo click fuera —— */
wishlistPanel.addEventListener('click', e => {
  const picker = wishlistPanel.querySelector('.size-picker');
  if (!picker) return;
  const inside = picker.contains(e.target);
  const addBtn = e.target.matches('.btn-carrito-mini');
  if (!inside && !addBtn) closeSizePicker(picker);
});

/* ─── animación de cierre ─── */
function closeSizePicker(node, mode = 'down') {
  if (!node) return;
  node.classList.add(mode === 'side' ? 'fade-out-side' : 'fade-out-down');
  wishlistPanel.style.overflowY =
    wishlistPanel.dataset.prevOverflow || 'auto';
  delete wishlistPanel.dataset.prevOverflow;
  wishlistContent.classList.remove('blurred');
  node.addEventListener('animationend', () => node.remove(), { once: true });
}

/* ───────────────────── 10. Bootstrap ─────────────────────────────── */
hydrate();
wishlistBtn?.addEventListener('click', () => { renderWishlistPanel(); showWishlist(); });
closeBtn  ?.addEventListener('click', hideWishlist);
document.getElementById('link-wishlist')
  .addEventListener('click', e => {
      e.preventDefault();
      renderWishlistPanel();
      showWishlist();
  });

/* ─── Devuelve API pública ─── */
return { clearWishlist };
}
