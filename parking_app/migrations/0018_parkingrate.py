# Generated by Django 4.2.4 on 2023-08-30 12:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('parking_app', '0017_parkinglot_parking_type_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ParkingRate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vehicle_type', models.CharField(choices=[('Two Wheeler', 'Two Wheeler'), ('Four Wheeler', 'Four Wheeler'), ('Heavy Vechiles', 'Heavy Vechiles')], max_length=20)),
                ('upto_1_hr', models.IntegerField(verbose_name='Fare Per Hour')),
                ('above_1_hr_upto_5_hr', models.IntegerField(verbose_name='Fare Above 1 hour and upto 5 hours')),
                ('above_5_hr_and_upto_24_hr', models.IntegerField(verbose_name='Fare above 5 day and upto 1 Day')),
                ('above_1_day_and_upto_3_days', models.IntegerField(verbose_name='Fare above 1 day and upto 3 days')),
                ('above_3_days_and_upto_7_days', models.IntegerField(verbose_name='Fare above 3 days and upto 7 days')),
                ('above_1_week_and_upto_2_weeks', models.IntegerField(verbose_name='Fare above 1 weeks and upto 2 weeks')),
                ('above_2_week_and_upto_1_month', models.IntegerField(verbose_name='Fare above 2 weeks and upto 1 month')),
                ('parking_lot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='parking_app.parkinglot')),
            ],
            options={
                'db_table': 'Parking Rates',
            },
        ),
    ]
