# Generated by Django 4.2.15 on 2024-12-02 17:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('optica', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='abono',
            old_name='formaPagoAbono',
            new_name='tipoPagoAbono',
        ),
        migrations.RemoveField(
            model_name='certificado',
            name='idCertificado',
        ),
        migrations.RemoveField(
            model_name='certificado',
            name='rutCliente',
        ),
        migrations.AddField(
            model_name='abono',
            name='saldoAnterior',
            field=models.IntegerField(blank=True, null=True, verbose_name='Saldo Anterior'),
        ),
        migrations.AddField(
            model_name='certificado',
            name='numeroCertificado',
            field=models.AutoField(default=0, primary_key=True, serialize=False, verbose_name='ID Certificado'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='ordentrabajo',
            name='estadoDelPago',
            field=models.CharField(default='Pendiente', max_length=20, verbose_name='Estado del Pago'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='ordentrabajo',
            name='estadoOrdenTrabajo',
            field=models.CharField(default='Ingresada', max_length=20, verbose_name='Estado Orden de Trabajo'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='abono',
            name='idAbono',
            field=models.AutoField(primary_key=True, serialize=False, verbose_name='ID Abono'),
        ),
        migrations.AlterField(
            model_name='abono',
            name='rutCliente',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='optica.cliente', verbose_name='RUN Cliente'),
        ),
    ]
