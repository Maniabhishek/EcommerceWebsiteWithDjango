# Generated by Django 3.1 on 2020-12-05 11:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_item_descrption'),
    ]

    operations = [
        migrations.RenameField(
            model_name='item',
            old_name='descrption',
            new_name='description',
        ),
    ]
