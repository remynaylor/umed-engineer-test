# Generated by Django 4.1.4 on 2023-01-15 17:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0004_patientdocument'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patientdocument',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]