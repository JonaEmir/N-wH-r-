export function setupContactPanel() {
  const btnContacto = document.getElementById('btn-contacto');
  const contactPanel = document.getElementById('contact-panel');
  const closeContactPanel = document.getElementById('close-contact-panel');

  btnContacto.addEventListener('click', () => {
    contactPanel.classList.add('open');
  });

  closeContactPanel.addEventListener('click', () => {
    contactPanel.classList.remove('open');
  });

  document.addEventListener('click', (e) => {
    if (
      contactPanel.classList.contains('open') &&
      !contactPanel.contains(e.target) &&
      e.target !== btnContacto
    ) {
      contactPanel.classList.remove('open');
    }
  });
}
