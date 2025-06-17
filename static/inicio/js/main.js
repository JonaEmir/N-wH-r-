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

