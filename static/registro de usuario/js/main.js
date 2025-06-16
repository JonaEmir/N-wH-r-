document.getElementById("registroForm").addEventListener("submit", async function(e) {
  e.preventDefault();

  const email = document.getElementById("email").value;
  const email2 = document.getElementById("email2").value;
  const password = document.getElementById("pwd").value;


  if (email !== email2) {
    alert("❌ Los correos no coinciden.");
    return;
  }

  const data = {
    username: email,
    password: password
  };

  try {
    const response = await fetch("/create-client", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(data)
    });

    const result = await response.json();

    if (response.ok) {
      alert("✅ Cliente creado con éxito.");
      window.location.href = "/"; // redirige a home o login
    } else {
      alert("❌ Error: " + result.error);
    }
  } catch (err) {
    alert("❌ Error inesperado: " + err);
  }
});

