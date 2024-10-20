from django.db import models

class Cliente(models.Model):
    rutCliente = models.IntegerField(primary_key=True) #este campo rutCliente necesito que sea clave primaria de la tabla Cliente
    dvRutCliente = models.CharField(max_length=1)
    nombreCliente = models.CharField(max_length=20)
    apPaternoCliente = models.CharField(max_length=20)
    apMaternoCliente = models.CharField(max_length=20, null=True, blank=True)
    celularCliente = models.IntegerField(null=True, blank=True)
    telefonoCliente = models.IntegerField(null=True, blank=True)
    emailCliente = models.EmailField(max_length=50, null=True, blank=True)  
    direccionCliente = models.CharField(max_length=100, null=True, blank=True)
    creacionCliente = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombreCliente} {self.apPaternoCliente} {self.apMaternoCliente} {self.rutCliente}"

class Atendedor(models.Model): 
    rutAtendedor = models.IntegerField(primary_key=True) #este campo rutAtendedor necesito que sea clave primaria de la tabla Atendedor
    dvRutAtendedor = models.CharField(max_length=1)
    nombreAtendedor = models.CharField(max_length=20)
    apPaternoAtendedor = models.CharField(max_length=20)
    apMaternoAtendedor = models.CharField(max_length=20)
    celularAtendedor = models.IntegerField(null=True, blank=True)
    emailAtendedor = models.EmailField(max_length=30, null=True, blank=True)  
    nombreUsuarioAtendedor = models.CharField(max_length=15) #Nombre de usuario
    claveAtendedor = models.CharField(max_length=15) #Clave

    def __str__(self):
        return f"{self.nombreAtendedor} {self.apPaternoAtendedor} {self.apMaternoAtendedor}"

class Tecnico(models.Model): 
    rutTecnico = models.IntegerField(primary_key=True) #este campo rutTecnico necesito que sea clave primaria de la tabla Tecnico
    dvRutTecnico = models.CharField(max_length=1)
    nombreTecnico = models.CharField(max_length=20)
    apPaternoTecnico = models.CharField(max_length=20)
    apMaternoTecnico = models.CharField(max_length=20)
    celularTecnico = models.IntegerField(null=True, blank=True)
    emailTecnico = models.EmailField(max_length=30, null=True, blank=True)  
    nombreUsuarioTecnico = models.CharField(max_length=15) #Nombre de usuario
    claveTecnico = models.CharField(max_length=15) #Clave

    def __str__(self):
        return f"{self.nombreTecnico} {self.apPaternoTecnico} {self.apMaternoTecnico}"


class Receta(models.Model):
    idReceta = models.BigAutoField(primary_key=True)
    rutCliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)#este campo rutCliente necesito que en mi tabla Receta sea clave foranea del campo rutCliente de tabla Cliente
    numeroReceta = models.IntegerField(null=True, blank=True)
    fechaReceta = models.DateField(null=True, blank=True) 
    creacionReceta = models.DateTimeField(auto_now_add=True)
    lejosOd = models.CharField(max_length=10, null=True, blank=True)
    lejosOi = models.CharField(max_length=10, null=True, blank=True)
    cercaOd = models.CharField(max_length=10, null=True, blank=True)
    cercaOi = models.CharField(max_length=10, null=True, blank=True)
    dpCerca = models.CharField(max_length=10, null=True, blank=True)
    dpLejos = models.CharField(max_length=10, null=True, blank=True)
    tipoLente = models.CharField(max_length=20, null=True, blank=True)
    institucion = models.CharField(max_length=20, null=True, blank=True)
    doctorOftalmologo = models.CharField(max_length=40, null=True, blank=True)
    linkFotoReceta = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return f"{self.creacionReceta}"
    
class Abono(models.Model): 
    idAbono = models.AutoField(primary_key=True, default=1)
    rutCliente = models.ForeignKey(Cliente, on_delete=models.CASCADE) #este campo rutCliente necesito que en mi tabla Certificado sea clave foranea del campo rutCliente de tabla Cliente
    fechaAbono = models.DateTimeField(auto_now_add=True)
    valorAbono = models.IntegerField(null=True, blank=True)
    formaPagoAbono = models.CharField(max_length=10, null=True, blank=True)
    numeroVoucherAbono = models.IntegerField(null=True, blank=True)
    numeroAbono = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.fechaAbono} {self.valorAbono}"


class OrdenTrabajo(models.Model): 
    idOrdenTrabajo = models.BigAutoField(primary_key=True)
    rutCliente = models.ForeignKey(Cliente, on_delete=models.CASCADE) #este campo rutCliente necesito que en mi tabla OrdenTrabajo sea clave foranea del campo rutCliente de tabla Cliente
    rutAtendedor = models.ForeignKey(Atendedor, on_delete=models.CASCADE) #este campo rutAtendedor necesito que en mi tabla OrdenTrabajo sea clave foranea del campo rutAtendedor de tabla Atendedor
    idReceta = models.ForeignKey(Receta, on_delete=models.CASCADE) #este campo idReceta necesito que en mi tabla OrdenTrabajo sea clave foranea del campo idReceta de tabla Receta
    idAbono = models.ForeignKey(Abono, on_delete=models.CASCADE) #este campo idAbono necesito que en mi tabla OrdenTrabajo sea clave foranea del campo idAbono de tabla Abono
    fechaOrdenTrabajo = models.DateTimeField(auto_now_add=True)
    valorOrdenTrabajo = models.IntegerField(null=True, blank=True) 
    fechaEntregaOrdenTrabajo = models.DateField(null=True, blank=True) 
    horaEntregaOrdenTrabajo = models.TimeField(null=True, blank=True)
    lejosDp = models.CharField(max_length=10, null=True, blank=True)
    laboratorioLejos = models.CharField(max_length=30, null=True, blank=True)
    cilLejosOd = models.CharField(max_length=10, null=True, blank=True)
    cilLejosOi = models.CharField(max_length=10, null=True, blank=True)
    gradoLejosOd = models.CharField(max_length=10, null=True, blank=True)
    gradoLejosOi = models.CharField(max_length=10, null=True, blank=True)
    prismaLejosOd = models.CharField(max_length=10, null=True, blank=True)
    prismaLejosOi = models.CharField(max_length=10, null=True, blank=True)
    tipoCristalLejos = models.CharField(max_length=25, null=True, blank=True)
    colorLejos = models.CharField(max_length=20, null=True, blank=True)
    marco = models.CharField(max_length=25, null=True, blank=True)
    altura = models.CharField(max_length=25, null=True, blank=True)
    laboratorioCerca = models.CharField(max_length=30, null=True, blank=True)
    cilCercaOd = models.CharField(max_length=10, null=True, blank=True)
    cilCercaOi = models.CharField(max_length=10, null=True, blank=True)
    gradoCercaOd = models.CharField(max_length=10, null=True, blank=True)
    gradoCercaOi = models.CharField(max_length=10, null=True, blank=True)
    prismaCercaOd = models.CharField(max_length=10, null=True, blank=True)
    prismaCercaOi = models.CharField(max_length=10, null=True, blank=True)
    tipoCristalCerca = models.CharField(max_length=25, null=True, blank=True)
    colorCerca = models.CharField(max_length=20, null=True, blank=True)
    numeroVoucherOrdenTrabajo = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.rutCliente} {self.fechaOrdenTrabajo} {self.valorOrdenTrabajo}"


class Certificado(models.Model): 
    idCertificado = models.AutoField(primary_key=True, default=1)
    idOrdenTrabajo = models.ForeignKey(OrdenTrabajo, on_delete=models.CASCADE) #este campo idOrdenTrabajo necesito que en mi tabla Certificado sea clave foranea del campo idOrdenTrabajo de la tabla OrdenTrabajo
    rutCliente = models.ForeignKey(Cliente, on_delete=models.CASCADE) #este campo rutCliente necesito que en mi tabla Certificado sea clave foranea del campo rutCliente de tabla Cliente
    idReceta = models.ForeignKey(Receta, on_delete=models.CASCADE) #este campo idReceta necesito que en mi tabla OrdenTrabajo sea clave foranea del campo idReceta de tabla Receta
    fechaCertificado = models.DateTimeField(auto_now_add=True)
    valorMarcoLejos = models.IntegerField(null=True, blank=True) 
    valorCristalesLejos = models.IntegerField(null=True, blank=True) 
    valorMarcoCerca = models.IntegerField(null=True, blank=True) 
    valorCristalesCerca = models.IntegerField(null=True, blank=True) 
    totalCerca = models.IntegerField(null=True, blank=True) 
    totalLejos = models.IntegerField(null=True, blank=True) 
    
    def __str__(self):
        return f"{self.rutCliente} {self.fechaCertificado}"
    
    
class Administrador(models.Model): 
    rutAdministrador = models.IntegerField(primary_key=True) #este campo rutAdministrador necesito que sea clave primaria de la tabla Administrador
    dvRutAdministrador = models.CharField(max_length=1)
    nombreAdministrador = models.CharField(max_length=20)
    apPaternoAdministrador = models.CharField(max_length=20)
    apMaternoAdministrador = models.CharField(max_length=20)
    celularAdministrador = models.IntegerField(null=True, blank=True)
    emailAdministrador = models.EmailField(max_length=50, null=True, blank=True)   
    nombreUsuarioAdministrador = models.CharField(max_length=20) #Nombre de usuario
    claveAdministrador = models.CharField(max_length=20) #Clave

    def __str__(self):
        return f"{self.nombreAdministrador} {self.apPaternoAdministrador} {self.apMaternoAdministrador}"