# Generated by Django 3.1 on 2020-12-03 14:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='category',
            field=models.CharField(choices=[('p', 'primary'), ('s', 'seceondary'), ('d', 'danger')], default='S', max_length=1),
            preserve_default=False,
        ),
    ]
