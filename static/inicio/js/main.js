import { setupScrollRestoration } from './scroll-behavior.js';
import { setupHeaderScroll } from './header.js';
import { setupBurgerMenu } from './burger-menu.js';
import { setupZoomEffect } from './zoom-effect.js';
import { setupAccordion } from './accordion.js';
import { setupNavigationButtons } from './navigation.js';
import { setupContactPanel } from './contact-panel.js';
import { setupLoginPanel } from './usuario.js';
import { getCSRFToken} from './login.js'
import { setupClientePanel } from './logged.js';
import { initWishlist } from './wishlist.js';



/* —— Lee el flag de sesión que Django dejó en <script id="is-authenticated"> —— */
const isAuthenticated = window.IS_AUTHENTICATED ?? false;


window.addEventListener('load', () => {
  // Espera un frame más para asegurar que se haya renderizado todo
  requestAnimationFrame(() => {
    initWishlist({
      isAuthenticated,
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

