/* -------- token desde el input oculto -------- */
export function getCSRFToken() {
  const input = document.querySelector('#loginForm input[name="csrfmiddlewaretoken"]');
  return input ? input.value : '';
}

/* -------- envío del formulario de login -------- */
document.getElementById("loginForm").addEventListener("submit", async (e) => {
  e.preventDefault();

  const username = document.getElementById("username").value.trim();
  const password = document.getElementById("password").value;
  const errorBox = document.getElementById("login-error");

  if (!username || !password) {
    errorBox.textContent = "⚠️ Por favor, completa todos los campos.";
    return;
  }

  try {
    const res = await fetch("/login-client/", {
      method: "POST",
      credentials: "same-origin",          // envía las cookies (csrftoken y sessionid)
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": getCSRFToken(),     // token correcto
      },
      body: JSON.stringify({ username, password }),
    });

    const data = await res.json().catch(() => ({})); // por si la respuesta no es JSON

    if (res.ok) {
      // 1) Obtener el ID de cliente
      const idRes = await fetch(`/api/cliente_id/${username}/`, {
        credentials: "same-origin"
      });
      if (idRes.ok) {
        const { id } = await idRes.json();
        localStorage.setItem('clienteId', id);
      } else {
        console.warn("No pude recuperar el clienteId");
      }

      // 2) Refrescar para que el resto de scripts vean el ID
      window.location.reload();          // 🔁 recarga la página
    } else {
      errorBox.textContent = `❌ ${data.error || "Error desconocido"}`;
    }
  } catch (err) {
    errorBox.textContent = `❌ Error inesperado: ${err}`;
  }
});
