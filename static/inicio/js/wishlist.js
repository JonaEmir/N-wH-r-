export function initWishlist({
  selector        = '.wishlist-btn',
  storageKey      = 'wishlist_ids',
  backendURL      = null,
  csrfToken       = null,
  isAuthenticated = false,
  onRequireLogin  = null
} = {}) {

  const wishlistIcon  = document.querySelector('#btn-wishlist-panel i');
  const wishlistCount = document.querySelector('#btn-wishlist-panel .wishlist-count');

  const getList = () => {
    try { return JSON.parse(localStorage.getItem(storageKey)) || []; }
    catch { return []; }
  };

  const setList = arr => {
    localStorage.setItem(storageKey, JSON.stringify(arr));
    updateHeaderUI(arr); // ← Actualiza ícono y contador
  };

  const toggleBtn = (btn, active) => {
    btn.classList.toggle('active', active);
    const icon = btn.querySelector('i');
    icon.classList.toggle('fa-regular', !active);
    icon.classList.toggle('fa-solid',   active);
  };

  const updateHeaderUI = (list) => {
    if (wishlistIcon) {
      wishlistIcon.classList.toggle('fa-solid', list.length > 0);
      wishlistIcon.classList.toggle('fa-regular', list.length === 0);
      wishlistIcon.style.color = list.length > 0 ? '#ff4d6d' : '';
    }

    if (wishlistCount) {
      const hasItems = list.length > 0;
      wishlistCount.textContent = list.length;

      // Reiniciar animaciones previas
      wishlistCount.classList.remove('animate-in', 'animate-out');

      if (hasItems) {
        wishlistCount.hidden = false;
        void wishlistCount.offsetWidth; // Reinicia animación
        wishlistCount.classList.add('animate-in');
      } else {
        wishlistCount.classList.add('animate-out');
        setTimeout(() => {
          wishlistCount.hidden = true;
        }, 300);
      }
    }
  };

  const hydrate = () => {
    const list = getList();
    list.forEach(id => {
      const btn = document.querySelector(`${selector}[data-product-id="${id}"]`);
      if (btn) toggleBtn(btn, true);
    });
    updateHeaderUI(list);
  };

  const clickHandler = async e => {
    const btn = e.target.closest(selector);
    if (!btn) return;

    if (!isAuthenticated) {
      if (typeof onRequireLogin === 'function') onRequireLogin();
      return;
    }

    const id     = btn.dataset.productId;
    let   list   = getList();
    const active = !btn.classList.contains('active');

    toggleBtn(btn, active);
    btn.classList.add('pop');
    btn.addEventListener('animationend', () => btn.classList.remove('pop'), { once: true });

    if (active) {
      if (!list.includes(id)) list.push(id);
    } else {
      list = list.filter(x => x !== id);
    }
    setList(list);

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
        if (!res.ok) throw new Error('bad response');
      } catch (err) {
        toggleBtn(btn, !active);
        active
          ? setList(list.filter(x => x !== id))
          : setList([...list, id]);
        console.error('Wishlist sync error', err);
        alert('No se pudo actualizar tu wishlist. Intenta de nuevo.');
      }
    }
  };

  hydrate();
  document.body.addEventListener('click', clickHandler);

  return {
    destroy() { document.body.removeEventListener('click', clickHandler); },
    getWishlist: getList,
    setWishlist: setList
  };
}
