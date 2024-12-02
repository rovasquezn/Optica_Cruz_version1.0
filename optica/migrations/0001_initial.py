# Generated by Django 4.2.15 on 2024-12-02 14:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
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
                ('institucion', models.CharField(blank=True, max_length=20, null=True, verbose_name='Institucion')),
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
                ('laboratorioLejos', models.CharField(blank=True, max_length=30, null=True, verbose_name='Laboratorio (Lejos)')),
                ('gradoLejosOd', models.CharField(blank=True, max_length=10, null=True, verbose_name='Grado Lejos OD')),
                ('gradoLejosOi', models.CharField(blank=True, max_length=10, null=True, verbose_name='Grado Lejos OI')),
                ('prismaLejosOd', models.CharField(blank=True, max_length=10, null=True, verbose_name='Prisma Lejos OD')),
                ('prismaLejosOi', models.CharField(blank=True, max_length=10, null=True, verbose_name='Prisma Lejos OI')),
                ('adicionLejosOd', models.CharField(blank=True, max_length=10, null=True, verbose_name='Adición Lejos OD')),
                ('adicionLejosOi', models.CharField(blank=True, max_length=10, null=True, verbose_name='Adición Lejos OI')),
                ('tipoCristalLejos', models.CharField(blank=True, max_length=25, null=True, verbose_name='Tipo de Cristal (Lejos)')),
                ('colorCristalLejos', models.CharField(blank=True, max_length=20, null=True, verbose_name='Color (Lejos)')),
                ('marcoLejos', models.CharField(blank=True, max_length=25, null=True, verbose_name='Marco (Lejos)')),
                ('valorMarcoLejos', models.IntegerField(blank=True, null=True, verbose_name='Valor Marco (Lejos)')),
                ('valorCristalesLejos', models.IntegerField(blank=True, null=True, verbose_name='Valor Cristal (Lejos)')),
                ('totalLejos', models.IntegerField(blank=True, null=True, verbose_name='Total (Lejos)')),
                ('altura', models.CharField(blank=True, max_length=25, null=True, verbose_name='Altura')),
                ('laboratorioCerca', models.CharField(blank=True, max_length=30, null=True, verbose_name='Laboratotio (Cerca)')),
                ('gradoCercaOd', models.CharField(blank=True, max_length=10, null=True, verbose_name='Grado Cerca OD')),
                ('gradoCercaOi', models.CharField(blank=True, max_length=10, null=True, verbose_name='Grado Cerca OI')),
                ('prismaCercaOd', models.CharField(blank=True, max_length=10, null=True, verbose_name='Prisma Cerca OD')),
                ('prismaCercaOi', models.CharField(blank=True, max_length=10, null=True, verbose_name='Prisma Cerca OI')),
                ('adicionCercaOd', models.CharField(blank=True, max_length=10, null=True, verbose_name='Adición Cerca OD')),
                ('adicionCercaOi', models.CharField(blank=True, max_length=10, null=True, verbose_name='Adición Cerca OI')),
                ('tipoCristalCerca', models.CharField(blank=True, max_length=25, null=True, verbose_name='Tipo de Cristal (Cerca)')),
                ('colorCristalCerca', models.CharField(blank=True, max_length=20, null=True, verbose_name='Color (Cerca)')),
                ('marcoCerca', models.CharField(blank=True, max_length=25, null=True, verbose_name='Marco (Cerca)')),
                ('valorMarcoCerca', models.IntegerField(blank=True, null=True, verbose_name='Valor Marco (Cerca)')),
                ('valorCristalesCerca', models.IntegerField(blank=True, null=True, verbose_name='Valor Cristal (Cerca)')),
                ('totalCerca', models.IntegerField(blank=True, null=True, verbose_name='Total (Cerca)')),
                ('totalOrdenTrabajo', models.IntegerField(blank=True, null=True, verbose_name='Total')),
                ('tipoPago', models.CharField(blank=True, max_length=25, null=True, verbose_name='Tipo de Pago')),
                ('numeroVoucherOrdenTrabajo', models.IntegerField(blank=True, null=True, verbose_name='Número de Voucher')),
                ('observacionOrdenTrabajo', models.CharField(blank=True, max_length=300, null=True, verbose_name='Observaciones')),
                ('estadoDelPago', models.CharField(max_length=20, verbose_name='Estado del Pago')),
                ('estadoOrdenTrabajo', models.CharField(max_length=20, verbose_name='Estado Orden de Trabajo')),
                ('idReceta', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='optica.receta', verbose_name='ID Receta')),
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
                ('valorAbono', models.IntegerField(blank=True, null=True, verbose_name='Valor Abono')),
                ('saldoAnterior', models.IntegerField(blank=True, null=True, verbose_name='Saldo Anterior')),
                ('saldo', models.IntegerField(blank=True, null=True, verbose_name='Saldo')),
                ('tipoPagoAbono', models.CharField(blank=True, max_length=10, null=True, verbose_name='Forma de pago')),
                ('numeroVoucherAbono', models.IntegerField(blank=True, null=True, verbose_name='Número de Voucher')),
                ('numeroAbono', models.IntegerField(blank=True, null=True, verbose_name='Abono Número')),
                ('idOrdenTrabajo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='optica.ordentrabajo', verbose_name='ID Orden de Trabajo')),
                ('rutCliente', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='optica.cliente', verbose_name='RUN Cliente')),
            ],
        ),
    ]
