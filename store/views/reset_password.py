from django.shortcuts import render, redirect
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.urls import reverse
from django.core.mail import EmailMultiAlternatives  # ✅ mejor que send_mail
from django.conf import settings
from django.template.loader import render_to_string
from store.models import Cliente


def solicitar_reset(request):
    """Muestra el formulario y envía el enlace de recuperación."""
    if request.method == "POST":
        email = (request.POST.get("email") or "").strip().lower()

        # Ajusta el campo si tu modelo usa `email` en lugar de `username`
        cliente = Cliente.objects.filter(username=email).first()
        if not cliente:
            return render(
                request,
                "public/password/recuperar-password.html",
                {"error": "❌ Correo no registrado."}
            )

        # Generar token y enlace seguro
        uidb64 = urlsafe_base64_encode(force_bytes(cliente.pk))
        token  = default_token_generator.make_token(cliente)
        link   = request.build_absolute_uri(
            reverse("cliente_reset_password_confirm",
                    kwargs={"uidb64": uidb64, "token": token})
        )

        context = {
            "nombre": getattr(cliente, "nombre", "Cliente"),
            "link": link,
        }

        # Renderizar versiones TXT y HTML
        text_body = render_to_string(
            "public/emails/reset_password_email.txt", context
        )
        html_body = render_to_string(
            "public/emails/reset_password_email.html", context
        )

        # Construir y enviar el correo
        email_msg = EmailMultiAlternatives(
            subject="Recuperación de contraseña – NöwHėrē",
            body=text_body,
            from_email=f"NöwHėrē <{settings.DEFAULT_FROM_EMAIL}>",
            to=[email],
        )
        email_msg.attach_alternative(html_body, "text/html")
        enviar_correo_async(email_msg)

        return render(request, "public/password/confirmacion-envio-correo.html")

    # GET: mostrar formulario
    return render(request, "public/password/recuperar-password.html")


# 2. Confirmar enlace (muestra formulario si token válido)
def reset_password_confirm(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        cliente = Cliente.objects.get(pk=uid)
    except (Cliente.DoesNotExist, ValueError, TypeError, OverflowError):
        cliente = None

    if cliente and default_token_generator.check_token(cliente, token):
        return render(request, "public/password/recuperar-nuevo-password.html", {
            "uidb64": uidb64,
            "token": token,
        })
    else:
        return render(request, "public/password/recuperar-invalid-token.html")


def reset_password_submit(request, uidb64, token):
    if request.method == "POST":
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            cliente = Cliente.objects.get(pk=uid)
        except (Cliente.DoesNotExist, ValueError, TypeError, OverflowError):
            cliente = None

        if cliente and default_token_generator.check_token(cliente, token):
            pass1 = request.POST.get("password1")
            pass2 = request.POST.get("password2")

            if not pass1 or not pass2:
                return render(request,
                              "public/password/recuperar-nuevo-password.html",
                              {"uidb64": uidb64, "token": token,
                               "error": "Debes escribir la contraseña dos veces."})

            if pass1 != pass2:
                return render(request,
                              "public/password/recuperar-nuevo-password.html",
                              {"uidb64": uidb64, "token": token,
                               "error": "Las contraseñas no coinciden."})

            # ¡Ahora sí!
            cliente.set_password(pass1)   # <-- cifra de forma correcta
            cliente.save()
            return render(request, "public/password/recuperar-exito.html")

    return render(request, "public/password/recuperar-invalid-token.html")

# Al final del archivo reset_password.py (o en otro utils.py si prefieres)
import threading

def enviar_correo_async(email_msg):
    threading.Thread(target=email_msg.send, kwargs={"fail_silently": False}).start()
