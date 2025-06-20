from django.shortcuts import render
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.urls import reverse
from django.core.mail import send_mail
from django.conf import settings
from store.models import Cliente
from django.template.loader import render_to_string

def solicitar_reset(request):
    if request.method == "POST":
        email = request.POST.get("email")
        try:
            cliente = Cliente.objects.get(username=email)
            token = default_token_generator.make_token(cliente)
            uid = urlsafe_base64_encode(force_bytes(cliente.pk))

            # Genera el enlace de recuperación
            link = request.build_absolute_uri(
                reverse('cliente_reset_password_confirm', kwargs={'uidb64': uid, 'token': token})
            )

            # Carga el contenido del email
            mensaje = render_to_string("emails/reset_password_email.html", {
                'nombre': getattr(cliente, 'nombre', 'cliente'),
                'link': link,
            })

            # Envía el correo
            send_mail(
                "Recuperación de contraseña",
                mensaje,
                settings.EMAIL_HOST_USER,
                [cliente.username],
                fail_silently=False,
            )

            return render(request, "public/recuperar_confirmacion.html")
        except Cliente.DoesNotExist:
            return render(request, "public/recuperar-password.html", {"error": "❌ Correo no registrado."})

    # Si es GET, muestra el formulario
    return render(request, "public/recuperar-password.html")
