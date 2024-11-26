from rest_framework import viewsets
from .models import Cliente, Receta, OrdenTrabajo, Abono, Certificado
from django.views.generic.edit import CreateView

from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin

from typing import Any
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy

from django.views import generic
from django.db.models import QuerySet
from django.db.models import Q

from .forms import RecetaForm 
from .forms import OrdenTrabajoForm 
from .forms import AbonoForm
from .forms import CertificadoForm

from django import forms
from django.views import View

import os
from django.http import FileResponse
from django.conf import settings
from datetime import datetime
from django.db.models import Max




def index(request):
    # Construir la ruta completa del archivo index.html en la raíz
    file_path = os.path.join(settings.BASE_DIR, 'index.html')
    
    # Devolver el archivo como respuesta
    return FileResponse(open(file_path, 'rb'), content_type='text/html')

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
    # 'esAbono',
    # 'esPagoTotal',
    'estadoDelPago',
    'tipoPago',
    'numeroVoucherOrdenTrabajo',
    'observacionOrdenTrabajo',
    'estadoOrdenTrabajo'
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
        'valorAbono',
        'saldo',
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
        
        # if rut_cliente:
        #     try:
        #         cliente = Cliente.objects.get(rutCliente=rut_cliente)
        #         messages.success(request, "Cliente encontrado")
        #     except Cliente.DoesNotExist:
        #         messages.error(request, "Cliente no encontrado")

        # Cargar formulario de ABONO con datos del Cliente y Orden de Trabajo, si existen, se pueden prellenar campos
        # form = AbonoForm(initial={
        #     'numeroAbono': numero_abono,
        #     'idOrdenTrabajo': orden_trabajo.idOrdenTrabajo if orden_trabajo else '',
        #     'rutCliente': cliente.rutCliente if cliente else '',
        #     'valorAbono': '',
        #     'saldo': '',
        #     'tipoPagoAbono': '',
        #     'numeroVoucherAbono': '',
        #     'idAbono': '',
        #     'numeroOrdenTrabajo': orden_trabajo.numeroOrdenTrabajo if orden_trabajo else '',
         
        #     'estadoDelPago': orden_trabajo.estadoDelPago if orden_trabajo else '',
        #     'totalLejos': orden_trabajo.totalLejos if orden_trabajo else '',
        #     'totalCerca': orden_trabajo.totalCerca if orden_trabajo else '',
        #     'totalOrdenTrabajo': orden_trabajo.totalOrdenTrabajo if orden_trabajo else ''
        
        
        
           # Cargar formulario de ABONO con datos del Cliente y Orden de Trabajo, si existen, se pueden prellenar campos
        form = AbonoForm(initial={
            'numeroAbono': numero_abono,
            'idOrdenTrabajo': orden_trabajo.idOrdenTrabajo if orden_trabajo else '',
            # 'rutCliente' : orden_trabajo.idReceta.rutCliente if orden_trabajo else '', #se esta tomando el cliente de la receta, se debe cambiar por el cliente de la orden de trabajo

            'rutCliente': cliente.rutCliente if cliente else '',
            'valorAbono': '',
            'saldo': '',
            'tipoPagoAbono': '',
            'numeroVoucherAbono': ''
        })

        return render(request, self.template_name, {
            'form': form,
            'orden_trabajo': orden_trabajo,
            'cliente': cliente,
            'numeroAbono': numero_abono,
            'idOrdenTrabajo': orden_trabajo.idOrdenTrabajo if orden_trabajo else '',
            'numeroOrdenTrabajo': orden_trabajo.numeroOrdenTrabajo if orden_trabajo else '',
            'estadoDelPago': orden_trabajo.estadoDelPago if orden_trabajo else '',
            'totalLejos': orden_trabajo.totalLejos if orden_trabajo else '',
            'totalCerca': orden_trabajo.totalCerca if orden_trabajo else '',
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
        initial['numeroAbono'] = self.object.numeroAbono  # Valor del modelo
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
class ListarCertificadoView(generic.ListView):
    model = Certificado
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
    
    
class CrearCertificadoView(SuccessMessageMixin, generic.CreateView):
    model = Certificado
    fields = (
        'idAbono',
        'idOrdenTrabajo',
        'rutCliente',  
        'valorAbono',
        'saldo',
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
        
        # if rut_cliente:
        #     try:
        #         cliente = Cliente.objects.get(rutCliente=rut_cliente)
        #         messages.success(request, "Cliente encontrado")
        #     except Cliente.DoesNotExist:
        #         messages.error(request, "Cliente no encontrado")

        # Cargar formulario de ABONO con datos del Cliente y Orden de Trabajo, si existen, se pueden prellenar campos
        # form = AbonoForm(initial={
        #     'numeroAbono': numero_abono,
        #     'idOrdenTrabajo': orden_trabajo.idOrdenTrabajo if orden_trabajo else '',
        #     'rutCliente': cliente.rutCliente if cliente else '',
        #     'valorAbono': '',
        #     'saldo': '',
        #     'tipoPagoAbono': '',
        #     'numeroVoucherAbono': '',
        #     'idAbono': '',
        #     'numeroOrdenTrabajo': orden_trabajo.numeroOrdenTrabajo if orden_trabajo else '',
         
        #     'estadoDelPago': orden_trabajo.estadoDelPago if orden_trabajo else '',
        #     'totalLejos': orden_trabajo.totalLejos if orden_trabajo else '',
        #     'totalCerca': orden_trabajo.totalCerca if orden_trabajo else '',
        #     'totalOrdenTrabajo': orden_trabajo.totalOrdenTrabajo if orden_trabajo else ''
        
        
        
           # Cargar formulario de ABONO con datos del Cliente y Orden de Trabajo, si existen, se pueden prellenar campos
        form = AbonoForm(initial={
            'numeroAbono': numero_abono,
            'idOrdenTrabajo': orden_trabajo.idOrdenTrabajo if orden_trabajo else '',
            # 'rutCliente' : orden_trabajo.idReceta.rutCliente if orden_trabajo else '', #se esta tomando el cliente de la receta, se debe cambiar por el cliente de la orden de trabajo

            'rutCliente': cliente.rutCliente if cliente else '',
            'valorAbono': '',
            'saldo': '',
            'tipoPagoAbono': '',
            'numeroVoucherAbono': ''
        })

        return render(request, self.template_name, {
            'form': form,
            'orden_trabajo': orden_trabajo,
            'cliente': cliente,
            'numeroAbono': numero_abono,
            'idOrdenTrabajo': orden_trabajo.idOrdenTrabajo if orden_trabajo else '',
            'numeroOrdenTrabajo': orden_trabajo.numeroOrdenTrabajo if orden_trabajo else '',
            'estadoDelPago': orden_trabajo.estadoDelPago if orden_trabajo else '',
            'totalLejos': orden_trabajo.totalLejos if orden_trabajo else '',
            'totalCerca': orden_trabajo.totalCerca if orden_trabajo else '',
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
            'totalOrdenTrabajo': orden_trabajo.totalOrdenTrabajo if orden_trabajo else ''
        })    

class EditarCertificadoView(SuccessMessageMixin, generic.UpdateView):
    model = Certificado
    fields = ( 'valorAbono', 
    'tipoPagoAbono', 
    'saldoAnterior',
    'saldo',
    'numeroVoucherAbono',)
    success_url = reverse_lazy('abono_list')
    success_message = "El abono se ha editado exitosamente."
    
def get_initial(self):
        initial = super().get_initial()
        initial['numeroAbono'] = self.object.numeroAbono  # Valor del modelo
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


class EliminarCertificadoView(SuccessMessageMixin, generic.DeleteView):
    model = Certificado
    success_url = reverse_lazy('abono_list')
    success_message = "El abono se ha eliminado exitosamente."

