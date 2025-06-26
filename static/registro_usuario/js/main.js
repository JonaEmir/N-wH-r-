/* -------- Obtener token CSRF desde el input oculto -------- */
function getCSRFToken() {
  // Busca el campo que Django inserta con {% csrf_token %}
  const el = document.querySelector('input[name="csrfmiddlewaretoken"]');
  return el ? el.value : '';
}

/* -------- Esperar al DOM y enganchar el submit -------- */
document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("registroForm");
  if (!form) return;

  form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const email  = form.email.value.trim();
    const email2 = form.email2.value.trim();
    const pwd    = form.pwd.value;

    if (email !== email2) {
      alert("❌ Los correos no coinciden."); return;
    }

    try {
      const res = await fetch("/create-client/", {
        method: "POST",
        credentials: "same-origin",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": getCSRFToken(),      // ✅ ahora siempre tiene valor
        },
        body: JSON.stringify({ username: email, password: pwd }),
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
