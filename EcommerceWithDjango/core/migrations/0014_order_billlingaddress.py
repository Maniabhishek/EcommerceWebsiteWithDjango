# Generated by Django 3.1 on 2020-12-22 15:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_billingaddress'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='billlingAddress',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.billingaddress'),
        ),
    ]
