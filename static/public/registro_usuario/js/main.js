function getCSRFToken() {
  const el = document.querySelector('input[name="csrfmiddlewaretoken"]');
  return el ? el.value : '';
}

document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("registroForm");
  if (!form) return;

  form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const email     = form.email.value.trim();
    const email2    = form.email2.value.trim();
    const pwd       = form.pwd.value;
    const nombre    = form.nombre.value.trim();
    const telefono  = form.telefono.value.trim();
    const direccion = form.direccion.value.trim();

    if (!email || !email2 || !pwd) {
      alert("❌ Los campos de correo, confirmación y contraseña son obligatorios.");
      return;
    }

    if (email !== email2) {
      alert("❌ Los correos no coinciden.");
      return;
    }

    const datos = {
      username: email,
      password: pwd,
      correo: email,
    };

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
        // redirige sin alert
        window.location.href = "/";
      } else {
        alert("❌ Error: " + (data.error || res.status));
      }
    } catch (err) {
      alert("❌ Error inesperado: " + err);
    }
  });
});
