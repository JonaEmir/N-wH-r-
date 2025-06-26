import { setupScrollRestoration } from './scroll-behavior.js';
import { setupHeaderScroll } from './header.js';
import { setupBurgerMenu } from './burger-menu.js';
import { setupZoomEffect } from './zoom-effect.js';
import { setupAccordion } from './accordion.js';
import { setupNavigationButtons } from './navigation.js';
import { setupContactPanel } from './contact-panel.js';
import { setupLoginPanel } from './usuario.js';
import { getCSRFToken } from './login.js';
import { setupClientePanel } from './logged.js';
import { initWishlist } from './wishlist.js';

/* —— Lee datos inyectados desde Django —— */
const isAuthenticated = window.IS_AUTHENTICATED ?? false;
const clienteId = window.CLIENTE_ID ?? null;
const csrfToken = window.CSRF_TOKEN ?? null;

window.addEventListener('load', () => {
  requestAnimationFrame(() => {
    initWishlist({
      isAuthenticated,
      clienteId,
      csrfToken,
      backendURL: '/wishlist/',         // PATCH/DELETE: /api/wishlist/<clienteId>/
      fetchProductoURL: '/wishlist/',  // GET: /api/productos/<id>/
      onRequireLogin: () => {
        const loginPanel = document.querySelector('#login-panel');
        const overlay = document.querySelector('.page-overlay');

        if (!loginPanel || !overlay) {
          console.warn('🔴 No se encontró el panel de login o el overlay');
          return;
        }

        loginPanel.classList.add('open');
        overlay.classList.add('active');
      }
    });
  });
});

// main.js (o el módulo que corresponda)
const wishlist = initWishlist({
  selector: '.wishlist-btn',
  clienteId: window.USER_ID ?? null,
  isAuthenticated: !!window.USER_ID,
  /* otros parámetros … */
});

async function handleLogout() {
  await fetch('/logout/', { method: 'POST' });
  wishlist.clearWishlist();      // ← vacía los corazones de la sesión actual
  window.location.reload();      // si refrescas la página tras logout
}


setupScrollRestoration();
setupHeaderScroll();
setupBurgerMenu();
setupZoomEffect();
setupAccordion();
setupNavigationButtons();
setupContactPanel();
setupLoginPanel();
setupClientePanel();
getCSRFToken();
