# Generated by Django 5.1.6 on 2025-03-15 11:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_loan_devuelto'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='titulo',
            field=models.CharField(max_length=40, unique=True),
        ),
    ]
