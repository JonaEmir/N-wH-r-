/* -------- Obtener token CSRF desde el input oculto -------- */
function getCSRFToken() {
  const el = document.querySelector('input[name="csrfmiddlewaretoken"]');
  return el ? el.value : '';
}

/* -------- Esperar al DOM y enganchar el submit -------- */
document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("registroForm");
  if (!form) return;

  form.addEventListener("submit", async (e) => {
    e.preventDefault();

    // Obtener valores del formulario
    const email     = form.email.value.trim();
    const email2    = form.email2.value.trim();
    const pwd       = form.pwd.value;
    const nombre    = form.nombre.value.trim();
    const telefono  = form.telefono.value.trim();
    const direccion = form.direccion.value.trim();

    // Validaciones obligatorias
    if (!email || !email2 || !pwd) {
      alert("❌ Los campos de correo, confirmación y contraseña son obligatorios.");
      return;
    }

    if (email !== email2) {
      alert("❌ Los correos no coinciden.");
      return;
    }

    // Armar el objeto de datos
    const datos = {
      username: email,
      password: pwd,
      correo: email,
    };

    // Agregar opcionales si están llenos
    if (nombre) datos.nombre = nombre;
    if (telefono) datos.telefono = telefono;
    if (direccion) datos.direccion = direccion;

    try {
      const res = await fetch("/create-client/", {
        method: "POST",
        credentials: "same-origin",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": getCSRFToken(),
        },
        body: JSON.stringify(datos),
      });

      const data = await res.json().catch(() => ({}));

      if (res.ok) {
        alert("✅ Cliente creado con éxito.");
        window.location.href = "/";
      } else {
        alert("❌ Error: " + (data.error || res.status));
      }
    } catch (err) {
      alert("❌ Error inesperado: " + err);
    }
  });
});
