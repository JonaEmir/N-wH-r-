document.addEventListener("DOMContentLoaded", () => {

  /* -------- volver -------- */
  const btnVolver = document.getElementById("btn-volver");
  if (btnVolver) {
    btnVolver.addEventListener("click", (e) => {
      if (history.length > 1) {           // mejora UX
        e.preventDefault();
        history.back();
      }
    });
  }

  /* -------- variantes -------- */
  const variantes   = JSON.parse(document.getElementById("variantes-data").textContent);
  const selectTalla = document.getElementById("selector-talla");
  const precioSpan  = document.getElementById("precio-actual");
  const stockMsg    = document.getElementById("info-stock");

  selectTalla.addEventListener("change", () => {
    const talla = selectTalla.value;
    stockMsg.textContent = "";

    if (!talla) return;

    const v = variantes.find(v => v.talla === talla);

    if (!v) {
      stockMsg.textContent = "Talla no disponible";
      return;
    }

    // actualiza precio (si la variante tiene precio diferente)
    precioSpan.textContent = `$${Number(v.precio).toFixed(2)}`;

    // mensaje de stock
    stockMsg.textContent = v.stock > 0
        ? `Stock disponible: ${v.stock}`
        : "Sin stock";

  });

});

// Activar la animación de entrada
document.querySelectorAll(".detalle-section").forEach(sec => {
  sec.classList.add("fade-in");
});
