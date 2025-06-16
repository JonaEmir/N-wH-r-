/* ----------- util: leer cookie csrf ----------- */
export function getCSRFToken() {
  const match = document.cookie.match(/csrftoken=([^;]+)/);
  return match ? match[1] : '';
}

/* ----------- envío del login ----------- */
document.getElementById("loginForm").addEventListener("submit", async function (e) {
  e.preventDefault();

  const username = document.getElementById("username").value.trim();
  const password = document.getElementById("password").value;

  const res = await fetch("/login-client", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": getCSRFToken()   // 💡 token seguro
    },
    body: JSON.stringify({ username, password })
  });

  const data = await res.json();

  if (res.ok) {
    alert("✅ Bienvenido/a " + username);
    document.getElementById("login-panel").classList.remove("active");
    // aquí podrías recargar la página o actualizar el UI para mostrar “Mi cuenta”
  } else {
    alert("❌ " + data.error);
  }
});