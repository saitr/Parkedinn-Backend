# Generated by Django 4.2.2 on 2023-08-25 07:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('parking_app', '0011_alter_parkingbilling_end_time_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parkingbilling',
            name='parking_slot',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='parking_app.parkingslot', unique=True),
        ),
    ]