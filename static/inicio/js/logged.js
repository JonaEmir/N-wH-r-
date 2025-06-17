export function setupClientePanel() {
  const userIcon = document.getElementById("btn-user-menu");
  const clientePanel = document.getElementById("cliente-panel");
  const closeClientePanel = document.getElementById("close-cliente-panel");
  const pageOverlay = document.querySelector(".page-overlay");

  if (userIcon && clientePanel && closeClientePanel) {
    userIcon.addEventListener("click", (e) => {
      e.stopPropagation();
      clientePanel.classList.add("open");
      pageOverlay.classList.add("active");
    });

    closeClientePanel.addEventListener("click", () => {
      clientePanel.classList.remove("open");
      pageOverlay.classList.remove("active");
    });

    document.addEventListener("click", (e) => {
      if (!clientePanel.contains(e.target) && !userIcon.contains(e.target)) {
        clientePanel.classList.remove("open");
        pageOverlay.classList.remove("active");
      }
    });

    clientePanel.addEventListener("click", (e) => e.stopPropagation());
  }
}
