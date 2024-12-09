import os
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from itertools import cycle
from django.core.exceptions import ValidationError

# Función para calcular el dígito verificador
def calcular_dv(rut):
    rut = str(rut)
    reversed_digits = map(int, reversed(rut))
    factors = cycle(range(2, 8))
    s = sum(d * f for d, f in zip(reversed_digits, factors))
    mod = (-s) % 11
    return 'K' if mod == 10 else str(mod)

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('El email debe ser proporcionado')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('El superusuario debe tener is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('El superusuario debe tener is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractUser):
    first_name = models.CharField(max_length=30, verbose_name="Nombre")
    ap_paterno = models.CharField(max_length=30, verbose_name="Apellido Paterno")
    ap_materno = models.CharField(max_length=30, verbose_name="Apellido Materno")
    email = models.EmailField(unique=True, verbose_name="Email")
    rut = models.CharField(max_length=8, verbose_name="RUN")
    dv = models.CharField(max_length=1, verbose_name="DV")
    celular = models.CharField(max_length=9, verbose_name="Celular")
    user_type = models.PositiveSmallIntegerField(choices=[(1, 'Administrador'), (2, 'Atendedor'), (3, 'Técnico')], verbose_name="Tipo de Usuario")

    def __str__(self):
        return self.username

    objects = CustomUserManager()


#CLIENTE
class Cliente(models.Model):
    rutCliente = models.IntegerField(primary_key=True, verbose_name="RUN Cliente") 
    dvRutCliente = models.CharField(max_length=1, verbose_name="Digito")
    nombreCliente = models.CharField(max_length=20, verbose_name="Nombre")
    apPaternoCliente = models.CharField(max_length=20, verbose_name="Apellido Paterno")
    apMaternoCliente = models.CharField(max_length=20, null=True, blank=True, verbose_name="Apellido Materno")
    celularCliente = models.IntegerField(null=True, blank=True, verbose_name="Celular")
    telefonoCliente = models.IntegerField(null=True, blank=True, verbose_name="Teléfono")
    emailCliente = models.EmailField(max_length=50, null=True, blank=True, verbose_name="Correo Electrónico")
    direccionCliente = models.CharField(max_length=100, null=True, blank=True, verbose_name="Dirección")
    creacionCliente = models.DateTimeField(auto_now_add=True, verbose_name="Creado el día")

    def save(self, *args, **kwargs):
        if not self.dvRutCliente:
            self.dvRutCliente = calcular_dv(self.rutCliente)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.rutCliente}"
    
class Receta(models.Model):
    idReceta = models.BigAutoField(primary_key=True, verbose_name="ID receta")
    rutCliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, verbose_name="RUN Cliente")

    dvRutCliente = models.CharField(max_length=1, null=True, blank=True, verbose_name="Dígito")
    nombreCliente = models.CharField(max_length=20, null=True, blank=True, verbose_name="Nombre")
    apPaternoCliente = models.CharField(max_length=20, null=True, blank=True, verbose_name="Apellido Paterno")
    apMaternoCliente = models.CharField(max_length=20, null=True, blank=True, verbose_name="Apellido Materno")
    celularCliente = models.IntegerField(null=True, blank=True, verbose_name="Celular")
    telefonoCliente = models.IntegerField(null=True, blank=True, verbose_name="Teléfono")
    

    numeroReceta = models.IntegerField(null=True, blank=True, verbose_name="Número de Receta")
    fechaReceta = models.DateField(null=True, blank=True, verbose_name="Fecha Receta") 
    creacionReceta = models.DateTimeField(auto_now_add=True, verbose_name="Creado el día")
    imagenReceta = models.ImageField(upload_to='imagenes/', null=True, blank=True, verbose_name="Imagen")
    
    lejosOdEsfera = models.CharField(max_length=10, null=True, blank=True, verbose_name="Esfera")
    lejosOdCilindro = models.CharField(max_length=10, null=True, blank=True, verbose_name="Cilindro")
    lejosOdEje = models.CharField(max_length=10, null=True, blank=True, verbose_name="Eje")
    
    lejosOiEsfera = models.CharField(max_length=10, null=True, blank=True, verbose_name="Esfera")
    lejosOiCilindro = models.CharField(max_length=10, null=True, blank=True, verbose_name="Cilindro")
    lejosOiEje = models.CharField(max_length=10, null=True, blank=True, verbose_name="Eje")
    
    dpLejos = models.CharField(max_length=10, null=True, blank=True, verbose_name="Distancia Pupilar")

    cercaOdEsfera = models.CharField(max_length=10, null=True, blank=True, verbose_name="Esfera")
    cercaOdCilindro = models.CharField(max_length=10, null=True, blank=True, verbose_name="Cilindro")
    cercaOdEje = models.CharField(max_length=10, null=True, blank=True, verbose_name="Eje")

    cercaOiEsfera = models.CharField(max_length=10, null=True, blank=True, verbose_name="Esfera")
    cercaOiCilindro = models.CharField(max_length=10, null=True, blank=True, verbose_name="Cilindro")
    cercaOiEje = models.CharField(max_length=10, null=True, blank=True, verbose_name="Eje")

    dpCerca = models.CharField(max_length=10, null=True, blank=True, verbose_name="Distancia Pupilar")
   
    tipoLente = models.CharField(max_length=20, null=True, blank=True, verbose_name="Tipo de Lente")
    institucion = models.CharField(max_length=20, null=True, blank=True, verbose_name="Institución")
    doctorOftalmologo = models.CharField(max_length=40, null=True, blank=True, verbose_name="Médico Oftalmología")
    observacionReceta = models.CharField(max_length=300, null=True, blank=True, verbose_name="Observaciones")

    def __str__(self):
        return f"{self.idReceta}"
    
    def save(self, *args, **kwargs):
        # Verifica si ya hay una imagen antes de guardar la nueva
        try:
            this = Receta.objects.get(idReceta=self.idReceta)
            if this.imagenReceta != self.imagenReceta and this.imagenReceta:
                # Si la imagen ha cambiado, eliminar la anterior
                if os.path.isfile(this.imagenReceta.path):
                    os.remove(this.imagenReceta.path)
        except Receta.DoesNotExist:
            pass  # El objeto no existe aún (primera vez que se guarda)
        
        # Guarda normalmente después de eliminar la imagen anterior
        super().save(*args, **kwargs)
    
    
    def delete(self, using=None, keep_parents=False):
    # Borra la imagen asociada si existe
        if self.imagenReceta:
            self.imagenReceta.storage.delete(self.imagenReceta.name)

    # Llamar al método delete del modelo base pasando los argumentos correctos
        super().delete(using=using, keep_parents=keep_parents)
    
    def delete_receta(self, idReceta):
        Receta.objects.filter(idReceta=idReceta).delete()
    
    

class OrdenTrabajo(models.Model): 
    idReceta = models.ForeignKey(Receta, null=True, blank=True, on_delete=models.CASCADE, verbose_name="ID Receta")
    # rutCliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, verbose_name="RUN Cliente") 
    idOrdenTrabajo = models.BigAutoField(primary_key=True, verbose_name="ID Orden de Trabajo")
    numeroOrdenTrabajo = models.IntegerField(verbose_name="Número de Orden de Trabajo") 
    fechaOrdenTrabajo = models.DateTimeField(auto_now_add=True, null=True, blank=True, verbose_name="Fecha Orden de Trabajo")
    fechaEntregaOrdenTrabajo = models.DateField(null=True, blank=True, verbose_name="Fecha Entrega") 
    horaEntregaOrdenTrabajo = models.TimeField(null=True, blank=True, verbose_name="Hora de Entrega")
    laboratorioLejos = models.CharField(max_length=30, null=True, blank=True, verbose_name="Laboratorio")
    gradoLejosOd = models.CharField(max_length=10, null=True, blank=True, verbose_name="Grado")
    gradoLejosOi = models.CharField(max_length=10, null=True, blank=True, verbose_name="Grado")
    prismaLejosOd = models.CharField(max_length=10, null=True, blank=True, verbose_name="Prisma")
    prismaLejosOi = models.CharField(max_length=10, null=True, blank=True, verbose_name="Prisma")
    adicionLejosOd = models.CharField(max_length=10, null=True, blank=True, verbose_name="Adición")
    adicionLejosOi = models.CharField(max_length=10, null=True, blank=True, verbose_name="Adición")    
    tipoCristalLejos = models.CharField(max_length=25, null=True, blank=True, verbose_name="Tipo de Cristal")
    colorCristalLejos = models.CharField(max_length=20, null=True, blank=True, verbose_name="Color")
    marcoLejos = models.CharField(max_length=25, null=True, blank=True, verbose_name="Marco")
    valorMarcoLejos = models.IntegerField(null=True, blank=True, verbose_name="Valor Marco") 
    valorCristalesLejos = models.IntegerField(null=True, blank=True, verbose_name="Valor Cristal") 
    totalLejos = models.IntegerField(null=True, blank=True, verbose_name="Total") 
    altura = models.CharField(max_length=25, null=True, blank=True, verbose_name="Altura")
    laboratorioCerca = models.CharField(max_length=30, null=True, blank=True, verbose_name="Laboratotio")
    gradoCercaOd = models.CharField(max_length=10, null=True, blank=True, verbose_name="Grado")
    gradoCercaOi = models.CharField(max_length=10, null=True, blank=True, verbose_name="Grado")
    prismaCercaOd = models.CharField(max_length=10, null=True, blank=True, verbose_name="Prisma")
    prismaCercaOi = models.CharField(max_length=10, null=True, blank=True, verbose_name="Prisma")
    adicionCercaOd = models.CharField(max_length=10, null=True, blank=True, verbose_name="Adición")
    adicionCercaOi = models.CharField(max_length=10, null=True, blank=True, verbose_name="Adición")
    tipoCristalCerca = models.CharField(max_length=25, null=True, blank=True, verbose_name="Tipo de Cristal")
    colorCristalCerca = models.CharField(max_length=20, null=True, blank=True, verbose_name="Color")
    marcoCerca = models.CharField(max_length=25, null=True, blank=True, verbose_name="Marco")
    valorMarcoCerca = models.IntegerField(null=True, blank=True, verbose_name="Valor Marco") 
    valorCristalesCerca = models.IntegerField(null=True, blank=True, verbose_name="Valor Cristal") 
    totalCerca = models.IntegerField(null=True, blank=True, verbose_name="Total (Cerca)")     
    totalOrdenTrabajo = models.IntegerField(null=True, blank=True, verbose_name="Total Orden de Trabajo") 
    tipoPago = models.CharField(max_length=25, null=True, blank=True, verbose_name="Tipo de Pago") 
    numeroVoucherOrdenTrabajo = models.IntegerField(null=True, blank=True, verbose_name="Número de Voucher")
    observacionOrdenTrabajo = models.CharField(max_length=300, null=True, blank=True, verbose_name="Observaciones")
    estadoDelPago = models.CharField(max_length=20, verbose_name="Estado del Pago")
    estadoOrdenTrabajo = models.CharField(max_length=20, verbose_name="Estado Orden de Trabajo")

    # Otros campos existentes...

    def __str__(self):
        return f"{self.idOrdenTrabajo}"
    
    def save(self, *args, **kwargs):
 
        if not self.numeroOrdenTrabajo:
            ultimo_valor = OrdenTrabajo.objects.aggregate(max_val=models.Max('numeroOrdenTrabajo'))['max_val']
            self.numeroOrdenTrabajo = (ultimo_valor + 1) if ultimo_valor and ultimo_valor >= 60000 else 60000
        super().save(*args, **kwargs)

    
    
    def delete_orden_trabajo(self, idOrdenTrabajo):
        OrdenTrabajo.objects.filter(idOrdenTrabajo=idOrdenTrabajo).delete()
    # def delete(self, using=None, keep_parents=False):
    # Borra la imagen asociada si existe
        # if self.imagenReceta:
        #     self.imagenReceta.storage.delete(self.imagenReceta.name)

    # Llamar al método delete del modelo base pasando los argumentos correctos
        # super().delete(using=using, keep_parents=keep_parents)
        
        
        
        

class Abono(models.Model): 
    idAbono = models.AutoField(primary_key=True, verbose_name="ID Abono")
    idOrdenTrabajo = models.ForeignKey(OrdenTrabajo, on_delete=models.CASCADE, verbose_name="ID Orden de Trabajo")
    rutCliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, null=True, blank=True, verbose_name="RUN Cliente") 
    fechaAbono = models.DateTimeField(auto_now_add=True, verbose_name="Fecha Abono")
    valorAbono = models.IntegerField(verbose_name="Valor Abono")
    saldoAnterior = models.IntegerField(null=True, blank=True, verbose_name="Saldo Anterior")
    saldo = models.IntegerField(null=True, blank=True, verbose_name="Saldo")
    tipoPagoAbono = models.CharField(max_length=20, choices=[('Efectivo', 'Efectivo'), ('Debito', 'Débito'), ('Credito', 'Crédito'), ('Cheque', 'Cheque')], verbose_name="Forma de pago del Abono")
    numeroVoucherAbono = models.IntegerField(null=True, blank=True, verbose_name="Número de Voucher")
    numeroAbono = models.PositiveIntegerField(verbose_name="Abono Número")
    
    # def clean(self):
    #     # Validar que valorAbono no sea mayor a totalOrdenTrabajo y no sea menor a 1
    #     if self.valorAbono < 1:
    #         raise ValidationError({'valorAbono': 'El valor del abono no puede ser menor a 1.'})
    #     if self.valorAbono > self.idOrdenTrabajo.totalOrdenTrabajo:
    #         raise ValidationError({'valorAbono': 'El valor del abono no puede ser mayor al total de la orden de trabajo.'})

    # def save(self, *args, **kwargs):
    #     self.full_clean()  # Llama a full_clean para ejecutar las validaciones
    #     # Calcular el saldo
    #     if self.numeroAbono == 1:
    #         self.saldo = self.idOrdenTrabajo.totalOrdenTrabajo - self.valorAbono
    #     else:
    #         abono_anterior = Abono.objects.filter(idOrdenTrabajo=self.idOrdenTrabajo, numeroAbono=self.numeroAbono - 1).first()
    #         if abono_anterior:
    #             self.saldo = abono_anterior.saldo - self.valorAbono
    #         else:
    #             raise ValidationError({'numeroAbono': 'No se encontró el abono anterior.'})
    #     super().save(*args, **kwargs)

    def clean(self):
        # Validar que valorAbono no sea mayor a totalOrdenTrabajo y no sea menor a 1
        if self.valorAbono < 1:
            raise ValidationError({'valorAbono': 'El valor del abono no puede ser menor a 1.'})
        if self.numeroAbono == 1 and self.valorAbono > self.idOrdenTrabajo.totalOrdenTrabajo:
            raise ValidationError({'valorAbono': 'El valor del abono no puede ser mayor al total de la orden de trabajo.'})
        elif self.numeroAbono > 1:
            abono_anterior = Abono.objects.filter(idOrdenTrabajo=self.idOrdenTrabajo, numeroAbono=self.numeroAbono - 1).first()
            if abono_anterior and self.valorAbono > abono_anterior.saldo:
                raise ValidationError({'valorAbono': 'El valor del abono no puede ser mayor al saldo del abono anterior.'})

    def save(self, *args, **kwargs):
        self.full_clean()  # Llama a full_clean para ejecutar las validaciones
        # Calcular el saldo
        if self.numeroAbono == 1:
            self.saldo = self.idOrdenTrabajo.totalOrdenTrabajo - self.valorAbono
        else:
            abono_anterior = Abono.objects.filter(idOrdenTrabajo=self.idOrdenTrabajo, numeroAbono=self.numeroAbono - 1).first()
            if abono_anterior:
                self.saldo = abono_anterior.saldo - self.valorAbono
            else:
                raise ValidationError({'numeroAbono': 'No se encontró el abono anterior.'})
        super().save(*args, **kwargs)
    def __str__(self):
        return f"Abono {self.numeroAbono} - Orden {self.idOrdenTrabajo.numeroOrdenTrabajo}"
    
    def delete_abono(self, idabono):
        Abono.objects.filter(idAbono=idabono).delete()

class Certificado(models.Model): 
    numeroCertificado = models.AutoField(primary_key=True, verbose_name="ID Certificado")
    idOrdenTrabajo = models.ForeignKey(OrdenTrabajo, on_delete=models.CASCADE, verbose_name="ID Orden de Trabajo") 
    idReceta = models.ForeignKey(Receta, on_delete=models.CASCADE, verbose_name="ID Receta") 
    fechaCertificado = models.DateTimeField(auto_now_add=True, verbose_name="Fecha Certificado")
    

    def __str__(self):
        return f"{self.numeroCertificado}"
        
    
    def delete_certificado(self, numeroCertificado):
        Certificado.objects.filter(numeroCertificado=numeroCertificado).delete()