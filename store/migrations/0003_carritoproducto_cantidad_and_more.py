# Generated by Django 5.2.2 on 2025-06-27 01:37

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_alter_cliente_correo_alter_cliente_nombre'),
    ]

    operations = [
        migrations.AddField(
            model_name='carritoproducto',
            name='cantidad',
            field=models.PositiveIntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='carritoproducto',
            name='carrito',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='store.carrito'),
        ),
    ]
