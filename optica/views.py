import json
from django import forms
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash, get_user_model
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetConfirmView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views import generic, View
from django.views.generic import ListView, TemplateView
from django.views.generic.edit import CreateView
from django.db.models import Q, Max, QuerySet
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.utils import timezone
from django.http import JsonResponse, FileResponse, HttpResponse
from django.core.mail import EmailMessage
from django.template import Context
from django.template.loader import get_template, render_to_string
from xhtml2pdf import pisa
from typing import Any
import os
from datetime import date, datetime, timedelta
import tempfile
# Importaciones de rest_framework
from rest_framework import viewsets

# Importaciones locales
from .forms import (
    CustomUserCreationForm, CustomUserChangeForm, 
    CustomPasswordChangeForm, RecetaForm, OrdenTrabajoForm, 
    UserProfileForm, AbonoForm, CertificadoForm
)
from .models import Cliente, Receta, OrdenTrabajo, CustomUser, Abono, Certificado
from .signals import send_password_reset_success_email, send_user_creation_email
from optica import models
from django.conf import settings
from django.http import JsonResponse

User = get_user_model()


def abono_create(request):
    if request.method == 'POST':
        form = AbonoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('abono_list')  # Redirige a la lista de abonos después de guardar
    else:
        form = AbonoForm()
        # Obtener el saldo del abono anterior si existe
        id_orden_trabajo = request.GET.get('idOrdenTrabajo')
        numero_abono = request.GET.get('numeroAbono')
        saldo_anterior = 0
        if id_orden_trabajo and numero_abono:
            abono_anterior = Abono.objects.filter(idOrdenTrabajo=id_orden_trabajo, numeroAbono=int(numero_abono) - 1).first()
            if abono_anterior:
                saldo_anterior = abono_anterior.saldo

    return render(request, 'abono_form.html', {'form': form, 'saldo_anterior': saldo_anterior})


def editar_orden_trabajo(request, pk):
    orden_trabajo = get_object_or_404(OrdenTrabajo, pk=pk)
    if request.method == "POST":
        form = OrdenTrabajoForm(request.POST, instance=orden_trabajo)
        if form.is_valid():
            form.save()
            return redirect('orden_trabajo_list')
    else:
        form = OrdenTrabajoForm(instance=orden_trabajo)
    return render(request, 'ordenTrabajo_form.html', {'form': form, 'orden_trabajo': orden_trabajo})

def certificado_new(request):
    id_orden_trabajo = request.GET.get('id_orden_trabajo')
    orden_trabajo = None
    if id_orden_trabajo:
        orden_trabajo = get_object_or_404(OrdenTrabajo, idOrdenTrabajo=id_orden_trabajo)
    
    return render(request, 'certificado_form.html', {
        'orden_trabajo': orden_trabajo,
    })

def generar_certificado_pdf(request, id_orden_trabajo):
    # Obtener los datos necesarios de la base de datos
    orden_trabajo = get_object_or_404(OrdenTrabajo, idOrdenTrabajo=id_orden_trabajo)

    
    # Crear el objeto HttpResponse con el encabezado PDF adecuado.
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="certificado_{orden_trabajo.idOrdenTrabajo}.pdf"'
    
    # Obtener la URL completa de la imagen
    logo_url = os.path.join(settings.STATIC_ROOT, 'images/Optica_Cruz_Celeste2.png')
    timbre_firma_url = os.path.join(settings.STATIC_ROOT, 'images/timbre_firma.png')

    # Renderizar la plantilla HTML con los datos
    template_path = 'optica/certificado_pdf.html'
    context = {
        'orden_trabajo': orden_trabajo,
        'logo_url': logo_url,
        'timbre_firma_url': timbre_firma_url
    }
    template = get_template(template_path)
    html = template.render(context)

    # Crear el PDF
    pisa_status = pisa.CreatePDF(html, dest=response)

    # Verificar si hubo errores
    if pisa_status.err:
        return HttpResponse('Hubo un error al generar el PDF', status=400)
    
    return response

def enviar_certificado_pdf(request, id_orden_trabajo):
    # Obtener los datos necesarios de la base de datos
    orden_trabajo = get_object_or_404(OrdenTrabajo, idOrdenTrabajo=id_orden_trabajo)

    # Obtener la URL completa de la imagen
    logo_url = os.path.join(settings.STATIC_ROOT, 'images/Optica_Cruz_Celeste2.png')
    timbre_firma_url = os.path.join(settings.STATIC_ROOT, 'images/timbre_firma.png')

    # Renderizar la plantilla HTML con los datos
    template_path = 'optica/certificado_pdf.html'
    context = {
        'orden_trabajo': orden_trabajo,
        'logo_url': logo_url,
        'timbre_firma_url': timbre_firma_url,
    }
    template = get_template(template_path)
    html = template.render(context)

    # Crear un archivo temporal para el PDF
    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
        pisa_status = pisa.CreatePDF(html, dest=temp_file)
        temp_file_path = temp_file.name

    # Verificar si hubo errores
    if pisa_status.err:
        return JsonResponse({'error': 'Hubo un error al generar el PDF'}, status=400)

    # Obtener el correo del cliente desde el modelo Cliente a través de Receta
    email_cliente = orden_trabajo.idReceta.rutCliente.emailCliente

    # Enviar el PDF por correo electrónico
    email = EmailMessage(
        'Certificado de Óptica Cruz',
        'Adjunto encontrará su certificado.',
        settings.DEFAULT_FROM_EMAIL,
        [email_cliente],  # Usar el correo del cliente
    )
    email.attach_file(temp_file_path)
    email.send()

    # Eliminar el archivo temporal
    os.remove(temp_file_path)

    return JsonResponse({'success': 'El certificado ha sido enviado por correo electrónico.'})


@login_required
def index(request):
    user = request.user
    last_name_parts = user.last_name.split()
    apellido_paterno = last_name_parts[0] if last_name_parts else ''
    nombre_completo = f"{user.first_name} {apellido_paterno}"  # Solo el apellido paterno
    context = {
        'nombre_completo': nombre_completo,
    }
    return render(request, 'optica/index.html', context)

@login_required
def mi_perfil(request):
    user = request.user
    if request.method == 'POST':
        password_form = PasswordChangeForm(user=request.user, data=request.POST)
        if password_form.is_valid():
            user = password_form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Tu contraseña ha sido cambiada con éxito.')
            return redirect('mi_perfil')
        else:
            messages.error(request, 'Por favor, corrige los errores a continuación.')
    else:
        password_form = PasswordChangeForm(user=request.user)
    
    context = {
        'first_name': user.first_name,
        'ap_paterno': user.ap_paterno,
        'ap_materno': user.ap_materno,
        'rut': f"{user.rut}-{user.dv}",
        'email': user.email,
        'celular': user.celular,
        'username': user.username,
        'user_type': user.get_user_type_display(),
        'password_form': password_form,
    }
    return render(request, 'optica/mi_perfil.html', context)

class CustomLoginView(LoginView):
    template_name = 'optica/login.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('index')  # Redirige a la página de inicio si el usuario ya está autenticado
        return super().dispatch(request, *args, **kwargs)

#Restablecer contraseña
class CustomPasswordResetView(PasswordResetView):
    template_name = 'optica/password_reset.html'
    email_template_name = 'optica/password_reset_email.html'
    subject_template_name = 'optica/password_reset_subject.txt'  # Añadir esta línea
    html_email_template_name = 'optica/password_reset_email.html'  # Añadir esta línea
    success_url = reverse_lazy('password_reset_done')

#Envio de mail confirmando restablecimiento de contraseña
class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    success_url = reverse_lazy('password_reset_complete')

    def form_valid(self, form):
        user = form.save()
        send_password_reset_success_email(user)
        return super().form_valid(form)



# Usuarios
class UsuarioListView(LoginRequiredMixin, UserPassesTestMixin, generic.ListView):
    model = CustomUser
    template_name = 'optica/usuario_list.html'
    context_object_name = 'usuarios'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset().order_by('id')  # Ordenar por 'id' o cualquier otro campo relevante
        query = self.request.GET.get('q')
        if query:
            user_type_map = {
                'Administrador': 1,
                'Atendedor': 2,
                'Técnico': 3
            }
            user_type_value = user_type_map.get(query, None)
            if user_type_value is not None:
                queryset = queryset.filter(user_type=user_type_value)
            else:
                queryset = queryset.filter(
                    Q(username__icontains=query) |
                    Q(email__icontains=query) |
                    Q(first_name__icontains=query) |
                    Q(ap_paterno__icontains=query) |
                    Q(ap_materno__icontains=query) |
                    Q(rut__icontains=query)
                )
        return queryset

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.user_type in [1, 2, 3]  # Administrador y Atendedor


class UsuarioCreateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, generic.CreateView):
    model = CustomUser
    form_class = CustomUserCreationForm
    template_name = 'optica/usuario_form.html'
    success_url = reverse_lazy('usuario_list')
    success_message = "Usuario {username} creado con éxito."

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Crear Usuario'
        context['is_edit'] = False
        return context

    def form_valid(self, form):
        form.instance.username = form.cleaned_data['username']
        self.object = form.save()
        password = form.cleaned_data.get('password1')
        send_user_creation_email(self.object, password)
        # Limpiar los mensajes de error antes de agregar el mensaje de éxito
        storage = messages.get_messages(self.request)
        list(storage)  # Consume todos los mensajes para limpiarlos
        return super().form_valid(form)

    def get_success_message(self, cleaned_data):
        return self.success_message.format(username=self.object.username)

    def form_invalid(self, form):
        messages.error(self.request, 'Por favor, corrija los errores en el formulario.')
        return self.render_to_response(self.get_context_data(form=form))

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.user_type == 1  # Solo Administrador
    

class UsuarioUpdateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, generic.UpdateView):
    model = CustomUser
    form_class = CustomUserChangeForm
    template_name = 'optica/usuario_form.html'
    success_url = reverse_lazy('usuario_list')
    success_message = "Usuario {username} actualizado con éxito."

    def get_success_message(self, cleaned_data):
        return self.success_message.format(username=self.object.username)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Editar Usuario'
        context['is_edit'] = True
        return context
    
    def form_valid(self, form):
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Por favor, corrija los errores en el formulario.')
        return self.render_to_response(self.get_context_data(form=form))

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.user_type == 1  # Solo Administrador

class UsuarioDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = CustomUser
    template_name = 'optica/usuario_confirm_delete.html'
    success_url = reverse_lazy('usuario_list')
    success_message = "Usuario borrado con éxito."

    #Nuevo
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)

    
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.user_type == 1  # Solo Administrador
    



# Create your views here.
class ListarClienteView(generic.ListView):
    model = Cliente
    paginate_by = 10
    ordering = ['-creacionCliente']  # Ordena por el campo 'creacionCliente' en orden descendente    
    
    
    def get_queryset(self):
        q = self.request.GET.get('q')

        queryset = super().get_queryset()

        if q:
            queryset = queryset.filter(
                Q(nombreCliente__icontains=q) |
                Q(apPaternoCliente__icontains=q) |
                Q(rutCliente__icontains=q)
            )

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['q'] = self.request.GET.get('q', '')  # Mantener el valor de la búsqueda en el contexto
        return context

class CrearClienteView(SuccessMessageMixin, generic.CreateView):
    model = Cliente
    fields = ('rutCliente', 
    'dvRutCliente', 
    'nombreCliente',
    'apPaternoCliente',
    'apMaternoCliente', 
    'celularCliente',
    'telefonoCliente', 
    'emailCliente',
    'direccionCliente',)
    success_url = reverse_lazy('cliente_list')
    success_message = "El cliente se ha creado exitosamente."


class EditarClienteView(SuccessMessageMixin, generic.UpdateView):
    model = Cliente
    fields = ('nombreCliente',
    'apPaternoCliente',
    'apMaternoCliente', 
    'celularCliente',
    'telefonoCliente', 
    'emailCliente',
    'direccionCliente',)
    success_url = reverse_lazy('cliente_list')
    success_message = "El cliente se ha editado exitosamente."

class EliminarClienteView(SuccessMessageMixin, generic.DeleteView):
    model = Cliente
    success_url = reverse_lazy('cliente_list')
    success_message = "El cliente se ha eliminado exitosamente."


#RECETAS

class ListarRecetaView(generic.ListView):
    model = Receta
    paginate_by = 10
    ordering = ['-creacionReceta']
    
    
    def get_queryset(self) -> QuerySet[Any]: 
        q = self.request.GET.get('q')
        if q:
            return Receta.objects.filter(
                Q(rutCliente__nombreCliente__icontains=q) | 
                Q(rutCliente__apPaternoCliente__icontains=q) | 
                Q(rutCliente__rutCliente__icontains=q)
            )
        return super().get_queryset()

class CrearRecetaView(SuccessMessageMixin, generic.CreateView):
    model = Receta
    fields = ('idReceta',
    'rutCliente',
    'dvRutCliente',
    'nombreCliente',
    'apPaternoCliente',
    'apMaternoCliente',
    'celularCliente',
    'telefonoCliente',
    # 'rutAdministrador', 
    'rutTecnico', 
    'rutAtendedor', 
    'numeroReceta', 
    'fechaReceta', 
    'lejosOdEsfera', 
    'lejosOdCilindro', 
    'lejosOdEje', 
    'lejosOiEsfera', 
    'lejosOiCilindro',
    'lejosOiEje', 
    'dpLejos', 
    'cercaOdEsfera', 
    'cercaOdCilindro', 
    'cercaOdEje', 
    'cercaOiEsfera', 
    'cercaOiCilindro', 
    'cercaOiEje',
    'dpCerca', 
    'tipoLente',
    'institucion',
    'doctorOftalmologo',
    'imagenReceta',
    'observacionReceta',)
    
    
    widgets = {
            'imagenReceta': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
    success_url = reverse_lazy('receta_list')
    success_message = "La receta se ha creado exitosamente."


    template_name = 'optica/receta_form.html'  # Cambia esto al nombre de tu template
    
    def get(self, request):
        cliente = None
        rut_cliente = request.GET.get('rut_cliente')
        
        # Buscar cliente por RUT
        if rut_cliente:
            try:
                cliente = Cliente.objects.get(rutCliente=rut_cliente)
                messages.success(request, "Cliente encontrado")
            except Cliente.DoesNotExist:
                cliente = None
                messages.error(request, "Cliente no encontrado")
        
        # Cargar formulario de receta con datos del Cliente, si existe cliente, se pueden prellenar campos
        form = RecetaForm(initial={
            'rutCliente': cliente.rutCliente if cliente else '',
            'dvRutCliente': cliente.dvRutCliente if cliente else '', 
            'nombreCliente': cliente.nombreCliente if cliente else '',
            'apPaternoCliente': cliente.apPaternoCliente if cliente else '',
            'apMaternoCliente': cliente.apMaternoCliente if cliente else '',
            'celularCliente': cliente.celularCliente if cliente else '',
            'telefonoCliente': cliente.telefonoCliente if cliente else '',
        })
    
        return render(request, self.template_name, {'form': form, 'cliente': cliente})


    def post(self, request):
        form = RecetaForm(request.POST, request.FILES)
        
        if form.is_valid():
            receta = form.save()  # Guardar la receta
            messages.success(request, self.success_message)  # Añadir el mensaje de éxito
            return redirect(self.success_url)  # Redirige a la lista de recetas
        
        return render(request, self.template_name, {'form': form})
    

class EditarRecetaView(SuccessMessageMixin, generic.UpdateView):
    model = Receta
    fields = ('numeroReceta', 
    'fechaReceta', 
    'lejosOdEsfera', 
    'lejosOdCilindro', 
    'lejosOdEje', 
    'lejosOiEsfera', 
    'lejosOiCilindro',
    'lejosOiEje', 
    'dpLejos', 
    'cercaOdEsfera', 
    'cercaOdCilindro', 
    'cercaOdEje', 
    'cercaOiEsfera', 
    'cercaOiCilindro', 
    'cercaOiEje',
    'dpCerca', 
    'tipoLente',
    'institucion',
    'doctorOftalmologo',
    'imagenReceta',
    'observacionReceta'
    )
    success_url = reverse_lazy('receta_list')
    success_message = "La receta se ha editado exitosamente."


class EliminarRecetaView(SuccessMessageMixin, generic.DeleteView):
    model = Receta
    success_url = reverse_lazy('receta_list')
    success_message = "La receta se ha eliminado exitosamente."


#ENVIAR RECETA A CLIENTE POR CORREO ELECTRÓNICO    

def enviar_receta_por_correo(request, id_receta):
    try:
        receta = get_object_or_404(Receta, idReceta=id_receta)
        cliente_email = receta.rutCliente.emailCliente
        cliente_nombre = receta.rutCliente.nombreCliente
        cliente_apellido = receta.rutCliente.apPaternoCliente

        if not cliente_email:
            return JsonResponse({'error': f'El cliente {cliente_nombre} {cliente_apellido} no tiene un correo electrónico registrado.'}, status=400)

        # Renderizar el contenido del correo usando la plantilla
        email_content = render_to_string('optica/receta_copy_email.html', {'receta': receta})

        # Crear el correo electrónico
        email = EmailMessage(
            'Copia de Receta de Óptica Cruz',
            email_content,
            'Óptica Cruz <optica.cruz.sgo@gmail.com>',  # Nombre y correo del remitente
            [cliente_email],
        )

        # Adjuntar la imagen de la receta
        if receta.imagenReceta:
            email.attach_file(receta.imagenReceta.path)

        # Enviar el correo
        email.content_subtype = 'html'  # Para enviar el correo en formato HTML
        email.send()

        return JsonResponse({'success': f'La receta ha sido enviada por correo electrónico a {cliente_nombre} {cliente_apellido} ({cliente_email}).'})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    
    

#ORDEN DE TRABAJO

class ListarOrdenTrabajoView(generic.ListView):
    model = OrdenTrabajo
    paginate_by = 10
    ordering = ['-fechaOrdenTrabajo']
    
    def get_queryset(self) -> QuerySet[Any]:
        q = self.request.GET.get('q')
        if q:
            return OrdenTrabajo.objects.filter(
                Q(idReceta__rutCliente__nombreCliente__icontains=q) | 
                Q(idReceta__rutCliente__apPaternoCliente__icontains=q) | 
                Q(idReceta__rutCliente__rutCliente__icontains=q)
            )
        return super().get_queryset()
 
    
class CrearOrdenTrabajoView(SuccessMessageMixin, generic.CreateView):
    model = OrdenTrabajo
    fields = (
    'idReceta',
    # 'rutAdministrador', 
    'rutTecnico', 
    'rutAtendedor', 
    'idOrdenTrabajo',
    'numeroOrdenTrabajo',
    # 'fechaOrdenTrabajo'
    'fechaEntregaOrdenTrabajo',
    'horaEntregaOrdenTrabajo',
    'laboratorioLejos',
    'gradoLejosOd',
    'gradoLejosOi',
    'prismaLejosOd',
    'prismaLejosOi',
    'adicionLejosOd', 
    'adicionLejosOi',
    'tipoCristalLejos',
    'colorCristalLejos',
    'marcoLejos',
    'valorMarcoLejos', 
    'valorCristalesLejos',
    'totalLejos',
    'altura',
    'laboratorioCerca',
    'gradoCercaOd',
    'gradoCercaOi',
    'prismaCercaOd',
    'prismaCercaOi',
    'adicionCercaOd',
    'adicionCercaOi',
    'tipoCristalCerca',
    'colorCristalCerca',
    'marcoCerca',
    'valorMarcoCerca',
    'valorCristalesCerca', 
    'totalCerca',
    'totalOrdenTrabajo',
    'tipoPago',
    'estadoDelPago',
    'numeroVoucherOrdenTrabajo',
    'observacionOrdenTrabajo',
    'estadoOrdenTrabajo',
    )
    
    success_url = reverse_lazy('ordenTrabajo_list')
    success_message = "La Orden de Trabajo se ha creado exitosamente."
    template_name = 'optica/ordenTrabajo_form.html'  # Cambia esto al nombre de tu template
    

    def generar_numero_orden(self):
        # Lógica para calcular el siguiente número de orden
        ultimo_valor = OrdenTrabajo.objects.aggregate(max_val=Max('numeroOrdenTrabajo'))['max_val']
        return (ultimo_valor + 1) if ultimo_valor and ultimo_valor >= 6000 else 6000

    def get(self, request):
        receta = None
        id_receta = request.GET.get('id_receta')

        if id_receta:
            try:
                receta = Receta.objects.get(idReceta=id_receta)
                messages.success(request, "Receta encontrada") 
            except Receta.DoesNotExist:
                messages.error(request, "Receta no encontrada")

        numero_orden = self.generar_numero_orden()

    
    
        form = OrdenTrabajoForm(initial={  
            'numeroOrdenTrabajo': numero_orden,
            'idReceta': receta.idReceta if receta else '',
                                   
            'rutCliente': receta.rutCliente if receta else '',
            'dvRutCliente': receta.dvRutCliente if receta else '',
            'nombreCliente': receta.nombreCliente if receta else '',
            'apPaternoCliente': receta.apPaternoCliente if receta else '',
            'apMaternoCliente': receta.apMaternoCliente if receta else '',
            'celularCliente': receta.celularCliente if receta else '',
            'telefonoCliente': receta.telefonoCliente if receta else '',
            # # 'rutAdministrador', 
            # # 'rutTecnico', 
            # # 'rutAtendedor', 
            'numeroReceta': receta.numeroReceta if receta else '', 
            'fechaReceta': receta.fechaReceta if receta else '', 
            'lejosOdEsfera': receta.lejosOdEsfera if receta else '', 
            'lejosOdCilindro': receta.lejosOdCilindro if receta else '', 
            'lejosOdEje': receta.lejosOdEje if receta else '', 
            'lejosOiEsfera': receta.lejosOiEsfera if receta else '', 
            'lejosOiCilindro': receta.lejosOiCilindro if receta else '',
            'lejosOiEje': receta.lejosOiEje if receta else '', 
            'dpLejos': receta.dpLejos if receta else '', 
            'cercaOdEsfera': receta.cercaOdEsfera if receta else '', 
            'cercaOdCilindro': receta.cercaOdCilindro if receta else '', 
            'cercaOdEje': receta.cercaOdEje if receta else '', 
            'cercaOiEsfera': receta.cercaOiEsfera if receta else '', 
            'cercaOiCilindro': receta.cercaOiCilindro if receta else '', 
            'cercaOiEje': receta.cercaOiEje if receta else '',
            'dpCerca': receta.dpCerca if receta else '', 
            'tipoLente': receta.tipoLente if receta else '',
            'institucion': receta.institucion if receta else '',
            'doctorOftalmologo': receta.doctorOftalmologo if receta else '',
            'observacionReceta': receta.observacionReceta if receta else '',           
            })
    
        return render(request, self.template_name, {'form': form, 'receta': receta})
    
    def post(self, request):
        form = OrdenTrabajoForm(request.POST)
        receta = None 
        id_receta = request.GET.get('id_receta')  # Captura el `id_receta` del parámetro de consulta

        if id_receta:
            try:
                # Obtén la receta con el `id_receta` proporcionado
                receta = Receta.objects.get(idReceta=id_receta)
                
                if form.is_valid():
                    orden_trabajo = form.save(commit=False)
                    orden_trabajo.idReceta = receta  # Asigna la receta a la orden de trabajo
                    
                    # Manejo de los campos booleanos
                    tipo_pago = request.POST.get('tipoDePago')
                    if tipo_pago == 'esAbono':
                        orden_trabajo.esAbono = True
                        orden_trabajo.esPagoTotal = False
                    elif tipo_pago == 'esPagoTotal':
                        orden_trabajo.esAbono = False
                        orden_trabajo.esPagoTotal = True

                # Manejo del campo estadoDelPago
                estado_del_pago = form.cleaned_data['estadoDelPago']
                orden_trabajo.estadoDelPago = estado_del_pago
                    
                orden_trabajo.save()  # Guarda la orden de trabajo
                    
                messages.success(request, "La Orden de Trabajo se ha creado exitosamente.")
                return redirect(self.success_url)  # Redirige tras guardar
                    
            except Receta.DoesNotExist:
                messages.error(request, "Receta no encontrada.")
        else:
            messages.error(request, "No se proporcionó un ID de receta válido.")
        
        # Si no es válido, muestra el formulario de nuevo con los mensajes de error
        return render(request, self.template_name, {'form': form, 'receta': receta})

 
class EditarOrdenTrabajoView(SuccessMessageMixin, generic.UpdateView):
    model = OrdenTrabajo
    fields = (
    'fechaEntregaOrdenTrabajo',
    'horaEntregaOrdenTrabajo',
    'laboratorioLejos',
    'gradoLejosOd',
    'gradoLejosOi',
    'prismaLejosOd',
    'prismaLejosOi',
    'tipoCristalLejos',
    'colorCristalLejos',
    'adicionLejosOd',
    'adicionLejosOi',
    'marcoLejos',
    'valorMarcoLejos', 
    'valorCristalesLejos',
    'altura',
    'laboratorioCerca',
    'gradoCercaOd',
    'gradoCercaOi',
    'prismaCercaOd',
    'prismaCercaOi',
    'adicionCercaOd',
    'adicionCercaOi',
    'tipoCristalCerca',
    'colorCristalCerca',
    'marcoCerca',
    'valorMarcoCerca',
    'valorCristalesCerca', 
    'estadoDelPago',
    'tipoPago',
    'numeroVoucherOrdenTrabajo',
    'observacionOrdenTrabajo',
    'estadoOrdenTrabajo',
    'totalLejos',
    'totalCerca',
    'totalOrdenTrabajo',
    )
    success_url = reverse_lazy('ordenTrabajo_list')
    success_message = "La Orden de Trabajo se ha editado exitosamente."

def get_initial(self):
        initial = super().get_initial()
        initial['numeroOrdenTrabajo'] = self.object.numeroOrdenTrabajo  # Valor del modelo
        return initial


def editar_orden_trabajo(request, pk):
    orden_trabajo = get_object_or_404(OrdenTrabajo, pk=pk)
    if request.method == "POST":
        form = OrdenTrabajoForm(request.POST, instance=orden_trabajo)
        if form.is_valid():
            form.save()
            return redirect('orden_trabajo_list')
    else:
        form = OrdenTrabajoForm(instance=orden_trabajo)
    return render(request, 'ordenTrabajo_form.html', {'form': form, 'orden_trabajo': orden_trabajo})

def form_valid(self, form):
        # Aquí puedes agregar lógica si necesitas procesar el formulario
        return super().form_valid(form) 
class EliminarOrdenTrabajoView(SuccessMessageMixin, generic.DeleteView):
    model = OrdenTrabajo
    # template_name = 'ordenTrabajo_delete'
    success_url = reverse_lazy('ordenTrabajo_list')
    success_message = "La Orden de Trabajo se ha eliminado exitosamente."


# ABONOS
class ListarAbonoView(generic.ListView):
    model = Abono
    paginate_by = 10
    ordering = ['-fechaAbono']
    
    def get_queryset(self) -> QuerySet[Any]:
        q = self.request.GET.get('q')
        if q:
            return Abono.objects.filter(
                Q(idOrdenTrabajo__idReceta__rutCliente__nombreCliente__icontains=q) | 
                Q(idOrdenTrabajo__idReceta__rutCliente__apPaternoCliente__icontains=q) | 
                Q(idOrdenTrabajo__idReceta__rutCliente__rutCliente__icontains=q)
            )
        return super().get_queryset()
    
    
class CrearAbonoView(SuccessMessageMixin, generic.CreateView):
    model = Abono
    fields = (
        'idAbono',
        'idOrdenTrabajo',
        'rutCliente', 
        'dvRutCliente', 
        'valorAbono',
        'saldo',
        'saldoAnterior',
        'tipoPagoAbono',
        'numeroVoucherAbono',
        'numeroAbono',
    )
    form_class = AbonoForm
    success_url = reverse_lazy('abono_list')
    success_message = "El abono se ha Registrado exitosamente."
    template_name = 'optica/abono_form.html'

    def generar_numero_abono(self, numeroOrdenTrabajo):
        # Lógica para calcular el siguiente número de orden
        ultimo_valor = Abono.objects.filter(idOrdenTrabajo=numeroOrdenTrabajo).aggregate(max_val=Max('numeroAbono'))['max_val']
        return (ultimo_valor + 1) if ultimo_valor else 1
    
    def get(self, request):
        orden_trabajo = None
        cliente = None
        id_orden_trabajo = request.GET.get('id_orden_trabajo')
        # rut_cliente = request.GET.get('rut_cliente') #va a ser usado cuando se haga la relacion entre cliente y orden de trabajo

        if id_orden_trabajo:
            try:
                orden_trabajo = OrdenTrabajo.objects.get(idOrdenTrabajo=id_orden_trabajo)
                
                cliente = orden_trabajo.idReceta.rutCliente #se esta tomando el cliente de la receta, se debe cambiar por el cliente de la orden de trabajo
                # cliente = Cliente.objects.get(rutCliente=rut_cliente) #funcionara cuando se haga la relacion entre cliente y orden de trabajo
                messages.success(request, "Orden de Trabajo encontrada")
            except OrdenTrabajo.DoesNotExist:
                messages.error(request, "Orden de Trabajo no encontrada")

        numero_abono = self.generar_numero_abono(orden_trabajo) if orden_trabajo else 1
        
         # Obtener el último saldo guardado para el idOrdenTrabajo
        ultimo_abono = Abono.objects.filter(idOrdenTrabajo=orden_trabajo).order_by('-numeroAbono').first()
        # saldo_anterior = ultimo_abono.saldo if ultimo_abono else orden_trabajo.totalOrdenTrabajo
        
        
        
           # Cargar formulario de ABONO con datos del Cliente y Orden de Trabajo, si existen, se pueden prellenar campos
        form = AbonoForm(initial={
            'numeroAbono': numero_abono,
            'idOrdenTrabajo': orden_trabajo.idOrdenTrabajo if orden_trabajo else '',
            # 'rutCliente' : orden_trabajo.idReceta.rutCliente if orden_trabajo else '', #se esta tomando el cliente de la receta, se debe cambiar por el cliente de la orden de trabajo
            'rutCliente': cliente.rutCliente if cliente else '',
            'dvRutCliente': cliente.dvRutCliente if cliente else '',
            'totalOrdenTrabajo': orden_trabajo.totalOrdenTrabajo if orden_trabajo else '',
            'valorAbono': '',
            'saldoAnterior': '',
            'saldo': '',
            'tipoPagoAbono': '',
            'numeroVoucherAbono': ''
        })

        return render(request, self.template_name, {
            'form': form,
            'orden_trabajo': orden_trabajo,
            'cliente': cliente,
            'dvRutCliente': cliente.dvRutCliente if cliente else '',
            'numeroAbono': numero_abono,
            'idOrdenTrabajo': orden_trabajo.idOrdenTrabajo if orden_trabajo else '',
            'numeroOrdenTrabajo': orden_trabajo.numeroOrdenTrabajo if orden_trabajo else '',
            'estadoDelPago': orden_trabajo.estadoDelPago if orden_trabajo else '',
            'totalLejos': orden_trabajo.totalLejos if orden_trabajo else '',
            'totalCerca': orden_trabajo.totalCerca if orden_trabajo else '',
            'saldoAnterior': orden_trabajo.totalOrdenTrabajo if orden_trabajo else '',
            'saldo': orden_trabajo.totalOrdenTrabajo if orden_trabajo else '',
            'totalOrdenTrabajo': orden_trabajo.totalOrdenTrabajo if orden_trabajo else ''
        })
        
        
        # return render(request, self.template_name, {'form': form, 'orden_trabajo': orden_trabajo, 'cliente': cliente})

    # def post(self, request):
    #     form = AbonoForm(request.POST)
    #     if form.is_valid():
    #         abono=form.save()
    #         messages.success(request, self.success_message)
    #         return redirect(self.success_url)
    #     return render(request, self.template_name, {'form': form})
    
   
    
    def post(self, request):
        form = AbonoForm(request.POST)
        # cliente = None 
        orden_trabajo = None
        # rut_cliente = request.POST.get('rutCliente')  # Captura el `rut_cliente` del formulario
        id_orden_trabajo = request.POST.get('idOrdenTrabajo')  # Captura el `id_orden_trabajo` del formulario
        
        if id_orden_trabajo:
            try:
                # cliente = Cliente.objects.get(rutCliente=rut_cliente)
                orden_trabajo = OrdenTrabajo.objects.get(idOrdenTrabajo=id_orden_trabajo)
             
                if form.is_valid():
                    abono = form.save(commit=False)
                    # abono.rutCliente = cliente  # Asigna el cliente al abono
                    abono.idOrdenTrabajo = orden_trabajo  # Asigna la orden de trabajo al abono
                    abono.save()  # Guarda el abono
                    messages.success(request, "El abono se ha registrado exitosamente.")
                    return redirect(self.success_url)
            except OrdenTrabajo.DoesNotExist:
                messages.error(request, "Orden de trabajo no encontrada.")
        
        else:
            messages.error(request, "No se proporcionó un ID de orden de trabajo válido.")
        
        return render(request, self.template_name, {
            'form': form,
            'orden_trabajo': orden_trabajo,
            'dvRutCliente': orden_trabajo.idReceta.dvRutCliente if orden_trabajo else '',
            'nombreCliente': orden_trabajo.idReceta.nombreCliente if orden_trabajo else '',
            'apPaternoCliente': orden_trabajo.idReceta.apPaternoCliente if orden_trabajo else '',
            'apMaternoCliente': orden_trabajo.idReceta.apMaternoCliente if orden_trabajo else '',
            'numeroOrdenTrabajo': orden_trabajo.numeroOrdenTrabajo if orden_trabajo else '',
            'estadoDelPago': orden_trabajo.estadoDelPago if orden_trabajo else '',
            'totalLejos': orden_trabajo.totalLejos if orden_trabajo else '',
            'totalCerca': orden_trabajo.totalCerca if orden_trabajo else '',
            # 'saldoAnterior': orden_trabajo.totalOrdenTrabajo if orden_trabajo else '',
            'saldo': orden_trabajo.totalOrdenTrabajo if orden_trabajo else '',
            'totalOrdenTrabajo': orden_trabajo.totalOrdenTrabajo if orden_trabajo else ''
        })    

class EditarAbonoView(SuccessMessageMixin, generic.UpdateView):
    model = Abono
    fields = ( 'valorAbono', 
    'tipoPagoAbono', 
    'saldoAnterior',
    'saldo',
    'numeroVoucherAbono',)
    success_url = reverse_lazy('abono_list')
    success_message = "El abono se ha editado exitosamente."
    
def get_initial(self):
        initial = super().get_initial()
        initial['numeroAbono'] = self.object.numeroOrdenTrabajo.numeroAbono  # Valor del modelo
        return initial
    
    
def editar_abono(request, pk):
    abono = get_object_or_404(Abono, pk=pk)
    if request.method == "POST":
        form = AbonoForm(request.POST, instance=abono)
        if form.is_valid():
            form.save()
            return redirect('abono_list')
    else:
        form = AbonoForm(instance=abono)
    return render(request, 'abono_form.html', {'form': form, 'abono': abono})

def form_valid(self, form):
        # Aquí puedes agregar lógica si necesitas procesar el formulario
        return super().form_valid(form) 


class EliminarAbonoView(SuccessMessageMixin, generic.DeleteView):
    model = Abono
    success_url = reverse_lazy('abono_list')
    success_message = "El abono se ha eliminado exitosamente."



#CERTIFICADOS
    

class CrearCertificadoView(CreateView):
    template_name = 'optica/certificado_form.html'

    def get(self, request, *args, **kwargs):
        orden_trabajo = None
        id_orden_trabajo = request.GET.get('id_orden_trabajo')

        if id_orden_trabajo:
            try:
                orden_trabajo = OrdenTrabajo.objects.get(idOrdenTrabajo=id_orden_trabajo)
                messages.success(request, "Orden de Trabajo encontrada")
            except OrdenTrabajo.DoesNotExist:
                messages.error(request, "Orden de Trabajo no encontrada")

        return render(request, self.template_name, {
            'orden_trabajo': orden_trabajo,
            'numero_orden_trabajo': orden_trabajo.numeroOrdenTrabajo if orden_trabajo else '',
            'idOrdenTrabajo': orden_trabajo.idOrdenTrabajo if orden_trabajo else '',
        })
        
        


class CertificadoPdfView(View):
    def get(self, request, *args, **kwargs):
        template = get_template('optica/certificado_pdf.html')  
        context = {'title': 'Certificado de Óptica Cruz'}
        html = template.render(context)
         # return HttpResponse ('<h1> Certificado </h1>')
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="certificado.pdf"'
        pisaStatus = pisa.CreatePDF(
            html, dest=response)
        if pisaStatus.err:
            return HttpResponse('We had some errors <pre>' + html + '</pre>')
        return response
    
    
    # VISTA DEL DASHBOARD EN index.html
def dashboard(request):
    # Fechas relevantes
    hoy = date.today()
    proximos_3_dias = hoy + timedelta(days=3)

    # Órdenes con diferentes condiciones
    ot_hoy = OrdenTrabajo.objects.filter(
        fechaEntregaOrdenTrabajo=hoy
    ).exclude(estadoOrdenTrabajo__in=["OT ENTREGADA", "OT PARA RETIRO"]).order_by('horaEntregaOrdenTrabajo')

    ot_vencidas = OrdenTrabajo.objects.filter(
        fechaEntregaOrdenTrabajo__lt=hoy
    ).exclude(estadoOrdenTrabajo__in=["OT ENTREGADA", "OT PARA RETIRO"]).order_by('fechaEntregaOrdenTrabajo')

    ot_proximos_dias = OrdenTrabajo.objects.filter(
        fechaEntregaOrdenTrabajo__range=[hoy + timedelta(days=1), proximos_3_dias]
    ).exclude(estadoOrdenTrabajo__in=["OT ENTREGADA", "OT PARA RETIRO"]).order_by('fechaEntregaOrdenTrabajo', 'horaEntregaOrdenTrabajo')

    # KPIs
    total_creadas = OrdenTrabajo.objects.filter(estadoOrdenTrabajo="OT CREADA").count()
    total_en_proceso = OrdenTrabajo.objects.filter(estadoOrdenTrabajo="OT EN PROCESO").count()
    total_listas_para_retiro = OrdenTrabajo.objects.filter(estadoOrdenTrabajo="OT PARA RETIRO").count()
    total_entregadas = OrdenTrabajo.objects.filter(estadoOrdenTrabajo="OT ENTREGADA").count()

    # Contar órdenes pendientes (Atrasadas, Hoy, Próximos 3 Días)
    total_pendientes = ot_vencidas.count() + ot_hoy.count() + ot_proximos_dias.count()

    # Contar órdenes activas (Creadas, En Proceso, Para Retiro)
    total_activas = total_creadas + total_en_proceso + total_listas_para_retiro

    # Órdenes por estado
    ot_creadas = OrdenTrabajo.objects.filter(estadoOrdenTrabajo="OT CREADA").order_by('fechaEntregaOrdenTrabajo')
    ot_en_proceso = OrdenTrabajo.objects.filter(estadoOrdenTrabajo="OT EN PROCESO").order_by('fechaEntregaOrdenTrabajo')
    ot_para_retiro = OrdenTrabajo.objects.filter(estadoOrdenTrabajo="OT PARA RETIRO").order_by('fechaEntregaOrdenTrabajo')
    ot_entregadas = OrdenTrabajo.objects.filter(estadoOrdenTrabajo="OT ENTREGADA").order_by('-fechaEntregaOrdenTrabajo')[:10]  # Últimas 10 entregadas

    # Leer cambios de estado desde el archivo JSON
    file_path = os.path.join(settings.BASE_DIR, 'cambios_estado.json')
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            cambios_estado = json.load(file)
    else:
        cambios_estado = []

    # Añadir cálculo de días transcurridos y fecha de cambio a "OT PARA RETIRO"
    for orden in ot_para_retiro:
        orden.dias_transcurridos = (hoy - orden.fechaEntregaOrdenTrabajo).days
        cambio_estado = next((cambio for cambio in cambios_estado if cambio["idOrdenTrabajo"] == orden.idOrdenTrabajo), None)
        if cambio_estado:
            fecha_cambio = datetime.strptime(cambio_estado["fecha_cambio"], "%Y-%m-%d %H:%M:%S")
            orden.fecha_cambio_estado = fecha_cambio.strftime("%d/%m/%Y")
        else:
            orden.fecha_cambio_estado = None

    # Contexto para renderizado
    context = {
        "total_pendientes": total_pendientes,
        "total_activas": total_activas,
        "total_creadas": total_creadas,
        "total_en_proceso": total_en_proceso,
        "total_listas_para_retiro": total_listas_para_retiro,
        "total_entregadas": total_entregadas,
        "ot_hoy": ot_hoy,
        "ot_vencidas": ot_vencidas,
        "ot_proximos_dias": ot_proximos_dias,
        "ot_creadas": ot_creadas,
        "ot_en_proceso": ot_en_proceso,
        "ot_para_retiro": ot_para_retiro,
        "ot_entregadas": ot_entregadas,
    }

    return render(request, 'optica/index.html', context)