# Generated by Django 4.2.15 on 2024-12-10 21:02

import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('rutCliente', models.IntegerField(primary_key=True, serialize=False, verbose_name='RUN Cliente')),
                ('dvRutCliente', models.CharField(max_length=1, verbose_name='Digito')),
                ('nombreCliente', models.CharField(max_length=20, verbose_name='Nombre')),
                ('apPaternoCliente', models.CharField(max_length=20, verbose_name='Apellido Paterno')),
                ('apMaternoCliente', models.CharField(blank=True, max_length=20, null=True, verbose_name='Apellido Materno')),
                ('celularCliente', models.IntegerField(blank=True, null=True, verbose_name='Celular')),
                ('telefonoCliente', models.IntegerField(blank=True, null=True, verbose_name='Teléfono')),
                ('emailCliente', models.EmailField(blank=True, max_length=50, null=True, verbose_name='Correo Electrónico')),
                ('direccionCliente', models.CharField(blank=True, max_length=100, null=True, verbose_name='Dirección')),
                ('creacionCliente', models.DateTimeField(auto_now_add=True, verbose_name='Creado el día')),
            ],
        ),
        migrations.CreateModel(
            name='Receta',
            fields=[
                ('idReceta', models.BigAutoField(primary_key=True, serialize=False, verbose_name='ID receta')),
                ('dvRutCliente', models.CharField(blank=True, max_length=1, null=True, verbose_name='Dígito')),
                ('nombreCliente', models.CharField(blank=True, max_length=20, null=True, verbose_name='Nombre')),
                ('apPaternoCliente', models.CharField(blank=True, max_length=20, null=True, verbose_name='Apellido Paterno')),
                ('apMaternoCliente', models.CharField(blank=True, max_length=20, null=True, verbose_name='Apellido Materno')),
                ('celularCliente', models.IntegerField(blank=True, null=True, verbose_name='Celular')),
                ('telefonoCliente', models.IntegerField(blank=True, null=True, verbose_name='Teléfono')),
                ('numeroReceta', models.IntegerField(blank=True, null=True, verbose_name='Número de Receta')),
                ('fechaReceta', models.DateField(blank=True, null=True, verbose_name='Fecha Receta')),
                ('creacionReceta', models.DateTimeField(auto_now_add=True, verbose_name='Creado el día')),
                ('imagenReceta', models.ImageField(blank=True, null=True, upload_to='imagenes/', verbose_name='Imagen')),
                ('lejosOdEsfera', models.CharField(blank=True, max_length=10, null=True, verbose_name='Esfera')),
                ('lejosOdCilindro', models.CharField(blank=True, max_length=10, null=True, verbose_name='Cilindro')),
                ('lejosOdEje', models.CharField(blank=True, max_length=10, null=True, verbose_name='Eje')),
                ('lejosOiEsfera', models.CharField(blank=True, max_length=10, null=True, verbose_name='Esfera')),
                ('lejosOiCilindro', models.CharField(blank=True, max_length=10, null=True, verbose_name='Cilindro')),
                ('lejosOiEje', models.CharField(blank=True, max_length=10, null=True, verbose_name='Eje')),
                ('dpLejos', models.CharField(blank=True, max_length=10, null=True, verbose_name='Distancia Pupilar')),
                ('cercaOdEsfera', models.CharField(blank=True, max_length=10, null=True, verbose_name='Esfera')),
                ('cercaOdCilindro', models.CharField(blank=True, max_length=10, null=True, verbose_name='Cilindro')),
                ('cercaOdEje', models.CharField(blank=True, max_length=10, null=True, verbose_name='Eje')),
                ('cercaOiEsfera', models.CharField(blank=True, max_length=10, null=True, verbose_name='Esfera')),
                ('cercaOiCilindro', models.CharField(blank=True, max_length=10, null=True, verbose_name='Cilindro')),
                ('cercaOiEje', models.CharField(blank=True, max_length=10, null=True, verbose_name='Eje')),
                ('dpCerca', models.CharField(blank=True, max_length=10, null=True, verbose_name='Distancia Pupilar')),
                ('tipoLente', models.CharField(blank=True, max_length=20, null=True, verbose_name='Tipo de Lente')),
                ('institucion', models.CharField(blank=True, max_length=20, null=True, verbose_name='Institución')),
                ('doctorOftalmologo', models.CharField(blank=True, max_length=40, null=True, verbose_name='Médico Oftalmología')),
                ('observacionReceta', models.CharField(blank=True, max_length=300, null=True, verbose_name='Observaciones')),
                ('rutCliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='optica.cliente', verbose_name='RUN Cliente')),
            ],
        ),
        migrations.CreateModel(
            name='OrdenTrabajo',
            fields=[
                ('idOrdenTrabajo', models.BigAutoField(primary_key=True, serialize=False, verbose_name='ID Orden de Trabajo')),
                ('numeroOrdenTrabajo', models.IntegerField(verbose_name='Número de Orden de Trabajo')),
                ('fechaOrdenTrabajo', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Fecha Orden de Trabajo')),
                ('fechaEntregaOrdenTrabajo', models.DateField(blank=True, null=True, verbose_name='Fecha Entrega')),
                ('horaEntregaOrdenTrabajo', models.TimeField(blank=True, null=True, verbose_name='Hora de Entrega')),
                ('laboratorioLejos', models.CharField(blank=True, max_length=30, null=True, verbose_name='Laboratorio')),
                ('gradoLejosOd', models.CharField(blank=True, max_length=10, null=True, verbose_name='Grado')),
                ('gradoLejosOi', models.CharField(blank=True, max_length=10, null=True, verbose_name='Grado')),
                ('prismaLejosOd', models.CharField(blank=True, max_length=10, null=True, verbose_name='Prisma')),
                ('prismaLejosOi', models.CharField(blank=True, max_length=10, null=True, verbose_name='Prisma')),
                ('adicionLejosOd', models.CharField(blank=True, max_length=10, null=True, verbose_name='Adición')),
                ('adicionLejosOi', models.CharField(blank=True, max_length=10, null=True, verbose_name='Adición')),
                ('tipoCristalLejos', models.CharField(blank=True, max_length=25, null=True, verbose_name='Tipo de Cristal')),
                ('colorCristalLejos', models.CharField(blank=True, max_length=20, null=True, verbose_name='Color')),
                ('marcoLejos', models.CharField(blank=True, max_length=25, null=True, verbose_name='Marco')),
                ('valorMarcoLejos', models.IntegerField(blank=True, null=True, verbose_name='Valor Marco')),
                ('valorCristalesLejos', models.IntegerField(blank=True, null=True, verbose_name='Valor Cristal')),
                ('totalLejos', models.IntegerField(blank=True, null=True, verbose_name='Total')),
                ('altura', models.CharField(blank=True, max_length=25, null=True, verbose_name='Altura')),
                ('laboratorioCerca', models.CharField(blank=True, max_length=30, null=True, verbose_name='Laboratotio')),
                ('gradoCercaOd', models.CharField(blank=True, max_length=10, null=True, verbose_name='Grado')),
                ('gradoCercaOi', models.CharField(blank=True, max_length=10, null=True, verbose_name='Grado')),
                ('prismaCercaOd', models.CharField(blank=True, max_length=10, null=True, verbose_name='Prisma')),
                ('prismaCercaOi', models.CharField(blank=True, max_length=10, null=True, verbose_name='Prisma')),
                ('adicionCercaOd', models.CharField(blank=True, max_length=10, null=True, verbose_name='Adición')),
                ('adicionCercaOi', models.CharField(blank=True, max_length=10, null=True, verbose_name='Adición')),
                ('tipoCristalCerca', models.CharField(blank=True, max_length=25, null=True, verbose_name='Tipo de Cristal')),
                ('colorCristalCerca', models.CharField(blank=True, max_length=20, null=True, verbose_name='Color')),
                ('marcoCerca', models.CharField(blank=True, max_length=25, null=True, verbose_name='Marco')),
                ('valorMarcoCerca', models.IntegerField(blank=True, null=True, verbose_name='Valor Marco')),
                ('valorCristalesCerca', models.IntegerField(blank=True, null=True, verbose_name='Valor Cristal')),
                ('totalCerca', models.IntegerField(blank=True, null=True, verbose_name='Total (Cerca)')),
                ('totalOrdenTrabajo', models.IntegerField(blank=True, null=True, verbose_name='Total Orden de Trabajo')),
                ('tipoPago', models.CharField(blank=True, max_length=25, null=True, verbose_name='Tipo de Pago')),
                ('numeroVoucherOrdenTrabajo', models.IntegerField(blank=True, null=True, verbose_name='Número de Voucher')),
                ('observacionOrdenTrabajo', models.CharField(blank=True, max_length=300, null=True, verbose_name='Observaciones')),
                ('estadoDelPago', models.CharField(max_length=20, verbose_name='Estado del Pago')),
                ('estadoOrdenTrabajo', models.CharField(max_length=20, verbose_name='Estado Orden de Trabajo')),
                ('idReceta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='optica.receta', verbose_name='ID Receta')),
            ],
        ),
        migrations.CreateModel(
            name='Certificado',
            fields=[
                ('numeroCertificado', models.AutoField(primary_key=True, serialize=False, verbose_name='ID Certificado')),
                ('fechaCertificado', models.DateTimeField(auto_now_add=True, verbose_name='Fecha Certificado')),
                ('idOrdenTrabajo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='optica.ordentrabajo', verbose_name='ID Orden de Trabajo')),
                ('idReceta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='optica.receta', verbose_name='ID Receta')),
            ],
        ),
        migrations.CreateModel(
            name='Abono',
            fields=[
                ('idAbono', models.AutoField(primary_key=True, serialize=False, verbose_name='ID Abono')),
                ('fechaAbono', models.DateTimeField(auto_now_add=True, verbose_name='Fecha Abono')),
                ('valorAbono', models.IntegerField(verbose_name='Valor Abono')),
                ('saldoAnterior', models.IntegerField(blank=True, null=True, verbose_name='Saldo Anterior')),
                ('saldo', models.IntegerField(blank=True, null=True, verbose_name='Saldo')),
                ('tipoPagoAbono', models.CharField(choices=[('Efectivo', 'Efectivo'), ('Debito', 'Débito'), ('Credito', 'Crédito'), ('Cheque', 'Cheque')], max_length=20, verbose_name='Forma de pago del Abono')),
                ('numeroVoucherAbono', models.IntegerField(blank=True, null=True, verbose_name='Número de Voucher')),
                ('numeroAbono', models.PositiveIntegerField(verbose_name='Abono Número')),
                ('idOrdenTrabajo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='optica.ordentrabajo', verbose_name='ID Orden de Trabajo')),
                ('rutCliente', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='optica.cliente', verbose_name='RUN Cliente')),
            ],
        ),
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('first_name', models.CharField(max_length=30, verbose_name='Nombre')),
                ('ap_paterno', models.CharField(max_length=30, verbose_name='Apellido Paterno')),
                ('ap_materno', models.CharField(max_length=30, verbose_name='Apellido Materno')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='Email')),
                ('rut', models.CharField(max_length=8, verbose_name='RUN')),
                ('dv', models.CharField(max_length=1, verbose_name='DV')),
                ('celular', models.CharField(max_length=9, verbose_name='Celular')),
                ('user_type', models.PositiveSmallIntegerField(choices=[(1, 'Administrador'), (2, 'Atendedor'), (3, 'Técnico')], verbose_name='Tipo de Usuario')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
        ),
    ]
