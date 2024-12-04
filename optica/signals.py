from django.conf import settings
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .models import OrdenTrabajo
#from .models import Administrador, Atendedor, Tecnico

User = get_user_model()

# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created and not instance.is_superuser:
#         if instance.user_type == 1:
#             Administrador.objects.create(user=instance)
#         elif instance.user_type == 2:
#             Atendedor.objects.create(user=instance)
#         elif instance.user_type == 3:
#             Tecnico.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if not instance.is_superuser:
        if instance.user_type == 1 and hasattr(instance, 'administrador'):
            instance.administrador.save()
        elif instance.user_type == 2 and hasattr(instance, 'atendedor'):
            instance.atendedor.save()
        elif instance.user_type == 3 and hasattr(instance, 'tecnico'):
            instance.tecnico.save()

def send_password_reset_success_email(user):
    subject = 'Contraseña restablecida con éxito'
    logo_url = f"{settings.SITE_URL}{settings.STATIC_URL}images/Optica Cruz-Calada.jpg"
    html_message = render_to_string('optica/password_reset_success_email.html', {'user': user, 'logo_url': logo_url})
    plain_message = strip_tags(html_message)
    from_email = settings.DEFAULT_FROM_EMAIL
    to = user.email

    send_mail(subject, plain_message, from_email, [to], html_message=html_message)

def send_user_creation_email(user, password):
    subject = 'Cuenta creada con éxito'
    logo_url = f"{settings.SITE_URL}{settings.STATIC_URL}images/Optica Cruz-Calada.jpg"
    site_url = settings.SITE_URL
    html_message = render_to_string('optica/user_creation_email.html', {
        'user': user,
        'password': password,
        'logo_url': logo_url,
        'site_url': site_url
    })
    plain_message = strip_tags(html_message)
    from_email = settings.DEFAULT_FROM_EMAIL
    to = user.email

    send_mail(subject, plain_message, from_email, [to], html_message=html_message)


#Email Ordden de Trabajo creada
@receiver(pre_save, sender=OrdenTrabajo)
def pre_save_orden_trabajo(sender, instance, **kwargs):
    if instance.pk:
        instance._old_instance = OrdenTrabajo.objects.get(pk=instance.pk)
    else:
        instance._old_instance = None

@receiver(post_save, sender=OrdenTrabajo)
def enviar_correo_orden_trabajo(sender, instance, created, **kwargs):
    if created:
        send_order_creation_email(instance)
    else:
        if instance._old_instance:
            changes = []
            if instance.estadoOrdenTrabajo != instance._old_instance.estadoOrdenTrabajo:
                changes.append("estado")
            if instance.fechaEntregaOrdenTrabajo != instance._old_instance.fechaEntregaOrdenTrabajo:
                changes.append("fecha")
            if instance.horaEntregaOrdenTrabajo != instance._old_instance.horaEntregaOrdenTrabajo:
                changes.append("hora")
            
            if changes:
                send_order_status_update_email(instance, changes)

def send_order_creation_email(orden_trabajo):
    subject = 'Nueva Orden de Trabajo Creada'
    html_message = render_to_string('optica/ordenTrabajo_creation_email.html', {'orden_trabajo': orden_trabajo})
    plain_message = strip_tags(html_message)
    from_email = settings.DEFAULT_FROM_EMAIL
    to = orden_trabajo.idReceta.rutCliente.emailCliente if orden_trabajo.idReceta and orden_trabajo.idReceta.rutCliente else None

    if to:
        send_mail(subject, plain_message, from_email, [to], html_message=html_message)

def send_order_status_update_email(orden_trabajo, changes):
    subject = 'Actualización de Estado de Orden de Trabajo'
    context = {
        'orden_trabajo': orden_trabajo,
        'changes': changes
    }
    html_message = render_to_string('optica/ordenTrabajo_status_update_email.html', context)
    plain_message = strip_tags(html_message)
    from_email = settings.DEFAULT_FROM_EMAIL
    to = orden_trabajo.idReceta.rutCliente.emailCliente if orden_trabajo.idReceta and orden_trabajo.idReceta.rutCliente else None

    if to:
        send_mail(subject, plain_message, from_email, [to], html_message=html_message)