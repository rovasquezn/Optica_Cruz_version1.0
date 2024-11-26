# forms.py
from django import forms
from django.db import models
from .models import Receta, OrdenTrabajo, Abono, Certificado 
from crispy_forms.helper import FormHelper


class RecetaForm(forms.ModelForm):
    class Meta:
        model = Receta  
        fields = '__all__' 
        
    def __init__(self, *args, **kwargs):
        super(RecetaForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-control-sm'
  
        # Hacer los campos readonly
        self.fields['rutCliente'].widget = forms.TextInput()
        self.fields['rutCliente'].widget.attrs['readonly'] = True
        self.fields['dvRutCliente'].widget.attrs['readonly'] = True
        self.fields['nombreCliente'].widget.attrs['readonly'] = True
        self.fields['apPaternoCliente'].widget.attrs['readonly'] = True
        self.fields['apMaternoCliente'].widget.attrs['readonly'] = True
        self.fields['celularCliente'].widget.attrs['readonly'] = True
        self.fields['telefonoCliente'].widget.attrs['readonly'] = True
        
            
            
class OrdenTrabajoForm(forms.ModelForm):
    class Meta:
        model = OrdenTrabajo  
        fields = ['idReceta',
        'idOrdenTrabajo',
        'numeroOrdenTrabajo',
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
        'numeroVoucherOrdenTrabajo',
        'observacionOrdenTrabajo',
        'estadoDelPago',
        'estadoOrdenTrabajo',
        'estadoOrdenTrabajo']
             
    estadoDelPago = forms.ChoiceField(
        choices=[
            ('', 'Elija una opción'),
            ('Pagado', 'Pagado'),
            ('Abono', 'Abono'),
            ('Pago pendiente', 'Pago pendiente')
        ],
        required=True,
        widget=forms.Select(attrs={'class': 'form-select', 'style': 'width: 220px;'})
    )        

    def __init__(self, *args, **kwargs):
        super(OrdenTrabajoForm, self).__init__(*args, **kwargs)
       
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control form-control-sm'    
            field.widget.attrs.update({'class': 'form-control form-control-sm'})  # Clases para diseño 
            
            self.fields['idReceta'].widget = forms.TextInput()
            
       
        # Hacer los campos readonly 
        self.fields['numeroOrdenTrabajo'].widget.attrs['readonly'] = True 
        self.fields['totalLejos'].widget.attrs['readonly'] = True
        self.fields['totalCerca'].widget.attrs['readonly'] = True
        self.fields['totalOrdenTrabajo'].widget.attrs['readonly'] = True

class AbonoForm(forms.ModelForm):
    class Meta:
        model = Abono  
        fields = [ 
            'idAbono', 
            'numeroAbono', 
            'idOrdenTrabajo',
            'rutCliente', 
            'valorAbono', 
            'saldoAnterior', 
            'saldo', 
            'tipoPagoAbono', 
            'numeroVoucherAbono'
        ]
        
    def __init__(self, *args, **kwargs):
        super(AbonoForm, self).__init__(*args, **kwargs)
        # self.helper = FormHelper()
        # self.helper.form_class = 'form-control-sm'

       
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control form-control-sm'    
            field.widget.attrs.update({'class': 'form-control form-control-sm'})  # Clases para diseño 
            
        self.fields['idOrdenTrabajo'].widget = forms.TextInput()
  
            # Hacer los campos readonly
            # self.fields['rutCliente'].widget = forms.TextInput()
        self.fields['saldoAnterior'].widget.attrs['readonly'] = True 
            # self.fields['saldo'].widget.attrs['readonly'] = True
        self.fields['numeroAbono'].widget.attrs['readonly'] = True
            # self.fields['fechaAbono'].widget.attrs['readonly'] = True
           # Asegúrate de que el campo valorAbono sea requerido
        self.fields['valorAbono'].required = True  
        
 
class CertificadoForm(forms.ModelForm):
    class Meta:
        model = Certificado 
        fields = [ 
            'numeroCertificado',
            'idOrdenTrabajo',
            # 'fechaCertificado',
            'idOrdenTrabajo',
            'idReceta'
            
        ]
        
    def __init__(self, *args, **kwargs):
        super(CertificadoForm, self).__init__(*args, **kwargs)
        # self.helper = FormHelper()
        # self.helper.form_class = 'form-control-sm'

       
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control form-control-sm'    
            field.widget.attrs.update({'class': 'form-control form-control-sm'})  # Clases para diseño 
            
        self.fields['idOrdenTrabajo'].widget = forms.TextInput()
  
            # Hacer los campos readonly
            # self.fields['rutCliente'].widget = forms.TextInput()
        #self.fields['saldoAnterior'].widget.attrs['readonly'] = True 
            # self.fields['saldo'].widget.attrs['readonly'] = True
       
       # self.fields['numeroAbono'].widget.attrs['readonly'] = True
            # self.fields['fechaAbono'].widget.attrs['readonly'] = True
           # Asegúrate de que el campo valorAbono sea requerido
        #self.fields['valorAbono'].required = True  
        
 