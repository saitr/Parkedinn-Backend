# Generated by Django 4.2.2 on 2023-08-25 07:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('parking_app', '0012_alter_parkingbilling_parking_slot'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parkingbilling',
            name='parking_slot',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='parking_app.parkingslot', unique=True),
        ),
        migrations.AlterField(
            model_name='parkingbilling',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='parkingbilling',
            name='vehicle_number',
            field=models.CharField(max_length=20, null=True),
        ),
    ]