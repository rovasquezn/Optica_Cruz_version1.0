# forms.py
from django import forms
from django.db import models
from .models import Abono, Certificado, Receta, OrdenTrabajo, CustomUser
from crispy_forms.helper import FormHelper
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from .models import CustomUser, Cliente, Receta, OrdenTrabajo, Abono
from django.contrib.auth import get_user_model

User = get_user_model()

class AdminCustomUserChangeForm(UserChangeForm):
    password = forms.CharField(label='Contraseña', widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    class Meta:
        model = CustomUser
        fields = ['first_name', 'ap_paterno', 'ap_materno', 'email', 'rut', 'dv', 'celular', 'user_type', 'is_active', 'username', 'password']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].widget.attrs['readonly'] = True
        self.fields['password'].widget = forms.TextInput(attrs={'readonly': 'readonly'})
        self.fields['password'].help_text = (
            "Las contraseñas no se almacenan en texto claro, por lo que no hay forma de ver la contraseña de este usuario, "
            "pero puede cambiar la contraseña usando <a href='../password/'>este formulario</a>."
        )

class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(label='Nombre', widget=forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}))
    ap_paterno = forms.CharField(label='Apellido Paterno', widget=forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}))
    ap_materno = forms.CharField(label='Apellido Materno', widget=forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}))
    rut = forms.CharField(label='RUN', widget=forms.TextInput(attrs={'class': 'form-control', 'required': 'required', 'pattern': '\d{7,8}', 'title': 'El RUT debe tener entre 7 y 8 dígitos.', 'maxlength': '8'}), initial='')
    dv = forms.CharField(label='DV', widget=forms.TextInput(attrs={'class': 'form-control', 'required': 'required', 'pattern': '[0-9Kk]', 'maxlength': '1', 'title': 'El DV debe ser un número o la letra K.'}), initial='')
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-control', 'required': 'required'}))
    celular = forms.CharField(label='Celular', widget=forms.TextInput(attrs={'class': 'form-control', 'required': 'required', 'pattern': '\d{9}', 'maxlength': '9', 'title': 'El celular debe tener 9 dígitos.'}), initial='')
    user_type = forms.ChoiceField(label='Tipo de Usuario', choices=[('', '---'), (1, 'Administrador'), (2, 'Atendedor'), (3, 'Técnico')], widget=forms.Select(attrs={'class': 'form-control', 'required': 'required'}))
    username = forms.CharField(label='Nombre de Usuario', widget=forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}))
    password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput(attrs={'class': 'form-control', 'required': 'required', 'minlength': '8', 'title': 'La contraseña debe tener al menos 8 caracteres.'}))
    password2 = forms.CharField(label='Confirmar Contraseña', widget=forms.PasswordInput(attrs={'class': 'form-control', 'required': 'required', 'minlength': '8', 'title': 'Las contraseñas deben coincidir.'}))
    is_active = forms.ChoiceField(
        label='Estado',
        choices=[(True, 'Activo'), (False, 'Inactivo')],
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True
    )
    
    class Meta:
        model = CustomUser
        fields = ['first_name', 'ap_paterno', 'ap_materno', 'rut', 'dv', 'email', 'celular', 'user_type', 'username', 'password1', 'password2', 'is_active']

    def clean(self):
        cleaned_data = super().clean()
        rut = cleaned_data.get("rut")
        dv = cleaned_data.get("dv")
        email = cleaned_data.get("email")
        username = cleaned_data.get("username")
        

        # Validar RUT y DV juntos
        if CustomUser.objects.filter(rut=rut, dv=dv).exists():
            self.add_error('rut', "Ya existe Usuario con este RUN y DV.")
            

        # # Validar Email
        # if CustomUser.objects.filter(email=email).exists():
        #     raise forms.ValidationError("El correo electrónico ya existe en el sistema.")

        return cleaned_data

    def clean_username(self):
        first_name = self.cleaned_data.get('first_name', '').lower()
        ap_paterno = self.cleaned_data.get('ap_paterno', '').lower()
        username = f"{first_name[0]}.{ap_paterno}"
        return username

class CustomUserChangeForm(UserChangeForm):
    first_name = forms.CharField(label='Nombre', widget=forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}))
    ap_paterno = forms.CharField(label='Apellido Paterno', widget=forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}))
    ap_materno = forms.CharField(label='Apellido Materno', widget=forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-control', 'required': 'required'}))
    rut = forms.CharField(label='RUT', widget=forms.TextInput(attrs={'class': 'form-control', 'required': 'required', 'pattern': '\d{7,8}', 'title': 'El RUT debe tener entre 7 y 8 dígitos.'}))
    dv = forms.CharField(label='DV', widget=forms.TextInput(attrs={'class': 'form-control', 'required': 'required', 'pattern': '[0-9Kk]', 'maxlength': '1', 'title': 'El DV debe ser un número o la letra K.'}))
    celular = forms.CharField(label='Celular', widget=forms.TextInput(attrs={'class': 'form-control', 'required': 'required', 'pattern': '\d{9}', 'maxlength': '9', 'title': 'El celular debe tener 9 dígitos.'}))
    user_type = forms.ChoiceField(label='Tipo de Usuario', choices=[(1, 'Administrador'), (2, 'Atendedor'), (3, 'Técnico')], widget=forms.Select(attrs={'class': 'form-control', 'required': 'required'}))
    is_active = forms.ChoiceField(
        label='Estado',
        choices=[(True, 'Activo'), (False, 'Inactivo')],
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True
    )
    username = forms.CharField(label='Nombre de Usuario', widget=forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}))
    
    class Meta:
        model = CustomUser
        fields = ['first_name', 'ap_paterno', 'ap_materno', 'email', 'rut', 'dv', 'celular', 'user_type', 'is_active', 'username']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'password' in self.fields:
            del self.fields['password']
        if 'password1' in self.fields:
            del self.fields['password1']
        if 'password2' in self.fields:
            del self.fields['password2']

class CustomPasswordChangeForm(PasswordChangeForm):
    class Meta:
        model = User
        fields = ('old_password', 'new_password1', 'new_password2')

# Mi Perfil
class UserProfileForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('first_name', 'ap_paterno', 'ap_materno', 'rut', 'dv', 'email', 'celular', 'username', 'user_type')
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'ap_paterno': forms.TextInput(attrs={'class': 'form-control'}),
            'ap_materno': forms.TextInput(attrs={'class': 'form-control'}),
            'rut': forms.TextInput(attrs={'class': 'form-control'}),
            'dv': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'celular': forms.TextInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'user_type': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'first_name': 'Nombre',
            'ap_paterno': 'Apellido Paterno',
            'ap_materno': 'Apellido Materno',
            'rut': 'RUT',
            'dv': 'DV',
            'email': 'Correo Electrónico',
            'celular': 'Celular',
            'username': 'Nombre de Usuario',
            'user_type': 'Tipo de Usuario',
        }

    class Meta:
        model = CustomUser
        fields = ['username']



class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['rutCliente', 'dvRutCliente', 'nombreCliente', 'apPaternoCliente', 'apMaternoCliente', 'celularCliente', 'telefonoCliente', 'emailCliente', 'direccionCliente']
     
    def __init__(self, *args, **kwargs):
        super(ClienteForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-control form-control-sm'
        self.fields['dvRutCliente'].widget.attrs['readonly'] = True
        

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
        fields = ['idOrdenTrabajo', 'numeroAbono', 'rutCliente', 'valorAbono', 'saldo', 'tipoPagoAbono', 'numeroVoucherAbono']
        widgets = {
            'saldo': forms.TextInput(attrs={'readonly': 'readonly'}),
        }

    # def clean_valorAbono(self):
    #     valorAbono = self.cleaned_data.get('valorAbono')
    #     idOrdenTrabajo = self.cleaned_data.get('idOrdenTrabajo')
    #     if valorAbono < 1:
    #         raise forms.ValidationError('El valor del abono no puede ser menor a 1.')
    #     if valorAbono > idOrdenTrabajo.totalOrdenTrabajo:
    #         raise forms.ValidationError('El valor del abono no puede ser mayor al total de la orden de trabajo.')
    #     return valorAbono
    
    def clean_valorAbono(self):
        valorAbono = self.cleaned_data.get('valorAbono')
        idOrdenTrabajo = self.cleaned_data.get('idOrdenTrabajo')
        if idOrdenTrabajo is None:
            raise forms.ValidationError('La orden de trabajo no puede ser nula.')
        if valorAbono < 1:
            raise forms.ValidationError('El valor del abono no puede ser menor a 1.')
        if self.instance.numeroAbono == 1 and valorAbono > idOrdenTrabajo.totalOrdenTrabajo:
            raise forms.ValidationError('El valor del abono no puede ser mayor al total de la orden de trabajo.')
        elif self.instance.numeroAbono > 1:
            abono_anterior = Abono.objects.filter(idOrdenTrabajo=idOrdenTrabajo, numeroAbono=self.instance.numeroAbono - 1).first()
            if abono_anterior and valorAbono > abono_anterior.saldo:
                raise forms.ValidationError('El valor del abono no puede ser mayor al saldo del abono anterior.')
        return valorAbono
        
 
class CertificadoForm(forms.ModelForm):
    class Meta:
        model = Certificado 
        fields = [ 
            'numeroCertificado',
            'idOrdenTrabajo',
            'idReceta',
          
            
        ]
        
    def __init__(self, *args, **kwargs):
        super(CertificadoForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-control-sm'

       
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control form-control-sm'    
            field.widget.attrs.update({'class': 'form-control form-control-sm'})  # Clases para diseño 
            
        self.fields['idOrdenTrabajo'].widget = forms.TextInput()
        # self.fields['numeroOrdenTrabajo'].widget.attrs['readonly'] = True 
            # Hacer los campos readonly
            # self.fields['rutCliente'].widget = forms.TextInput()
        # self.fields['numeroCertificado'].widget.attrs['readonly'] = True
