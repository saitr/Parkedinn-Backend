# Generated by Django 4.2.2 on 2023-08-23 05:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parking_app', '0007_parkingbilling_delete_billing'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parkingslot',
            name='slot_number',
            field=models.CharField(max_length=10, unique=True),
        ),
    ]
