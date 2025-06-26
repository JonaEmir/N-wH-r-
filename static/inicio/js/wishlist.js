/**
 * initWishlist
 * ------------
 * 1) Corazón en tarjetas del catálogo.
 * 2) Panel lateral con los favoritos.
 *    – Cada fila muestra sólo el botón **Agregar**.
 *    – Al hacer clic aparece un “selector de talla” que se despliega
 *      desde abajo (slide-up) justo ENCIMA del botón.
 *    – Al elegir la talla se llama a addToCart(id, talla) y se cierra
 *      el selector.
 *
 *  Nota:
 *    • El endpoint /api/productos/<id>/ debe devolver un array
 *      `tallas` con las tallas disponibles, p.ej. ["24", "25", "26"].
 *    • Sustituye addToCart() por tu llamada fetch real.
 */
export function initWishlist({
  selector        = '.wishlist-btn',        // corazón en catálogo
  storageKey      = 'wishlist_ids',
  backendURL      = null,                   // /wishlist/
  csrfToken       = null,
  isAuthenticated = false,
  onRequireLogin  = null,
  fetchProductoURL = null,                  // /productos/
  clienteId       = null
} = {}) {

/* ─────────────────────────── 1. Referencias DOM ────────────────────────── */
const wishlistIcon    = document.querySelector('#btn-wishlist-panel i');
const wishlistCount   = document.querySelector('#btn-wishlist-panel .wishlist-count');
const wishlistBtn     = document.getElementById('btn-wishlist-panel');
const wishlistPanel   = document.getElementById('wishlist-panel');
const closeBtn        = document.getElementById('close-wishlist-panel');
const wishlistContent = wishlistPanel?.querySelector('.wishlist-content');
const overlay         = document.querySelector('.page-overlay');

/* ─────────────────────────── 2. LocalStorage helpers ───────────────────── */
const getList = () => {
  try { return JSON.parse(localStorage.getItem(storageKey)) || []; }
  catch { return []; }
};
const setList = list => {
  localStorage.setItem(storageKey, JSON.stringify(list));
  updateHeaderUI(list);
};

/* ─────────────────────────── 3. Header UI (icono + badge) ─────────────── */
const toggleBtn = (btn, on) => {
  btn.classList.toggle('active', on);
  const ic = btn.querySelector('i');
  if (ic) { ic.classList.toggle('fa-solid', on); ic.classList.toggle('fa-regular', !on); }
};

const updateHeaderUI = list => {
  wishlistIcon?.classList.toggle('fa-solid', list.length);
  wishlistIcon?.classList.toggle('fa-regular', !list.length);
  if (wishlistIcon) wishlistIcon.style.color = list.length ? '#ff4d6d' : '';
  if (wishlistCount) {
    wishlistCount.textContent = list.length;
    wishlistCount.hidden = list.length === 0;
  }
};

/* Marca corazones guardados al cargar */
const hydrate = () => {
  const list = getList();
  list.forEach(id => {
    const btn = document.querySelector(`${selector}[data-product-id="${id}"]`);
    btn && toggleBtn(btn, true);
  });
  updateHeaderUI(list);
};

/* ─────────────────────────── 4. Panel show/hide ───────────────────────── */
const showWishlist = () => {
  wishlistPanel?.classList.add('open');
  overlay?.classList.add('active');
};
const hideWishlist = () => {
  wishlistPanel?.classList.remove('open');
  overlay?.classList.remove('active');
};
overlay?.addEventListener('click', hideWishlist);

/* ─────────────────────────── 5. Corazones catálogo ────────────────────── */
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

  if (backendURL && clienteId !== null) {
    fetch(`${backendURL}${clienteId}/`, {
      method : add ? 'PATCH' : 'DELETE',
      headers: { 'Content-Type':'application/json',
                 ...(csrfToken && { 'X-CSRFToken': csrfToken })},
      body   : JSON.stringify({ producto_id: id })
    }).catch(err => console.error('Wishlist sync', err));
  }
});

/* ─────────────────────────── 6. Placeholder carrito ───────────────────── */
const addToCart = (productoId, talla) => {
  console.log(`addToCart → id=${productoId} talla=${talla}`);
  /* TODO: fetch('/carrito/', { body:{productoId, talla} }) */
};

/* ─────────────────────────── 7. Render panel ──────────────────────────── */
const renderWishlistPanel = async () => {
  wishlistContent.textContent = 'Cargando…';

  const list = getList();
  if (!fetchProductoURL || !list.length) {
    wishlistContent.textContent = 'No tienes productos en tu wishlist.';
    return;
  }

  const frag = document.createDocumentFragment();

  for (const id of list) {
    try {
      console.log(fetchProductoURL)
      const res = await fetch(`${fetchProductoURL}${id}/`);
      if (!res.ok) continue;
      const p = await res.json();    // debe traer p.tallas = ["24","25",…]

      const sizes = Array.isArray(p.tallas) && p.tallas.length
                  ? p.tallas.join(',') : '';

      const item = document.createElement('div');
      item.className = 'wishlist-item';
      item.innerHTML = `
        <img src="${p.imagen}" alt="${p.nombre}">
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
    } catch(e){ console.warn('Producto no cargado', id, e); }
  }
  wishlistContent.innerHTML = '';
  wishlistContent.appendChild(frag);
};

/* ─────────────────────────── 8. Selector de talla ─────────────────────── */
wishlistContent?.addEventListener('click', e => {

  /* click en botón Agregar */
  if (e.target.matches('.btn-carrito-mini')) {
    const btn   = e.target;
    const sizes = btn.dataset.sizes ? btn.dataset.sizes.split(',') : ['Única'];
    const already = btn.parentElement.querySelector('.size-picker');

    /* si ya está abierto → lo cerramos */
    if (already) { already.remove(); return; }

    /* construir selector de tallas */
    const picker = document.createElement('div');
    picker.className = 'size-picker fade-up';
    picker.innerHTML = `
      <p class="size-title">Selecciona tu talla</p>
      <div class="size-options">
        ${sizes.map(s => `<button class="size-option" data-size="${s.trim()}">${s.trim()}</button>`).join('')}
      </div>`;
    btn.parentElement.insertBefore(picker, btn);
    return;
  }

  /* click en una talla */
  if (e.target.matches('.size-option')) {
    const size   = e.target.dataset.size;
    const pid    = e.target.closest('.wishlist-actions')
                           .querySelector('.btn-carrito-mini').dataset.id;
    addToCart(pid, size);
    /* feedback visual */
    e.target.classList.add('chosen');
    setTimeout(() => {
      e.target.closest('.size-picker')?.remove();
    }, 200);
  }
});

/* ─────────────────────────── 9. Bootstrap ─────────────────────────────── */
hydrate();
wishlistBtn?.addEventListener('click', () => { renderWishlistPanel(); showWishlist(); });
closeBtn  ?.addEventListener('click', hideWishlist);
}
