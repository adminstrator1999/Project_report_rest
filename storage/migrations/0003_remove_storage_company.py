# Generated by Django 3.1 on 2020-09-06 08:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('storage', '0002_storage_company'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='storage',
            name='company',
        ),
    ]
