from django.db import models
from .managers import *
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from cloudinary.models import CloudinaryField
from django.utils import timezone
import datetime
# Create your models here.


class CustomUser(AbstractBaseUser, PermissionsMixin):
    
    username = models.CharField(max_length=100,blank=False,null=False)
    email = models.EmailField(blank=False,null=False,unique=True)
    phone_number = models.CharField(unique=True,max_length=15,blank=False,null=False)
    otp = models.CharField(max_length=6,blank=True,null=True)
    jwt_token = models.CharField(max_length=250,unique=True,null=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'phone_number']

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin



class ParkingLot(models.Model):
    class Meta:
        db_table='ParkingLot'
    PARKING_CHOICES = (
        ('INDOOR','Indoor'),
        ('OUTDOOR','Outdoor')
    )
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    description = models.TextField(blank=True,null=True)
    image = CloudinaryField('Parking Image Lot Picture',blank=True, null=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    parking_type = models.CharField('Parking Type',max_length=20,choices=PARKING_CHOICES,blank=False,null=False)

    def __str__(self):
        return self.name
    

# class ParkingRate(models.Model):
#     class Meta:
#         db_table = 'Parking Rates'
#     VEHICLE_CHOICES = (
#         ('Two Wheeler', 'Two Wheeler'),
#         ('Four Wheeler', 'Four Wheeler'),
#         ('Heavy Vehicle', 'Heavy Vehicle')
#     )
#     vehicle_type = models.CharField(max_length=20, choices=VEHICLE_CHOICES)
#     parking_lot = models.ForeignKey(ParkingLot, on_delete=models.CASCADE)
#     # Cost for different time intervals
#     less_than_hour = models.DecimalField(max_digits=6, decimal_places=2)  # 1 hr
#     after_one_hour = models.DecimalField(max_digits=6, decimal_places=2)  # 1-5 hrs
#     after_one_day = models.DecimalField(max_digits=6, decimal_places=2)  # 5-24 hrs
#     after_one_week = models.DecimalField(max_digits=6, decimal_places=2)  # 1 day
#     # rate_1_week = models.DecimalField(max_digits=6, decimal_places=2)  # 1 week
    
#     def __str__(self):
#         return f" The rates at  {self.parking_lot} are as Rupees  {self.less_than_hour} for below 1hr and  {self.after_one_hour} after 1hr  and Rupees {self.after_one_day} per 1hour after day and for a week it is rupees {self.after_one_week} per hour"

class ParkingRate(models.Model):
    class Meta:
        db_table = 'Parking Rates'
    VEHICLE_CHOICES = (
        ('Two Wheeler','Two Wheeler'),
        ('Four Wheeler','Four Wheeler'),
        ('Heavy Vechiles','Heavy Vechiles')
    )
    vehicle_type = models.CharField(max_length=20, choices=VEHICLE_CHOICES)
    parking_lot = models.ForeignKey(ParkingLot, on_delete=models.CASCADE)
    # Cost for different time intervals
    upto_1_hr = models.IntegerField('Fare Per Hour')  
    above_1_hr_upto_5_hr = models.IntegerField("Fare Above 1 hour and upto 5 hours") 
    above_5_hr_and_upto_24_hr = models.IntegerField("Fare above 5 day and upto 1 Day")  
    above_1_day_and_upto_3_days = models.IntegerField("Fare above 1 day and upto 3 days")
    above_3_days_and_upto_7_days = models.IntegerField("Fare above 3 days and upto 7 days")
    above_1_week_and_upto_2_weeks = models.IntegerField("Fare above 1 weeks and upto 2 weeks")
    above_2_week_and_upto_1_month = models.IntegerField("Fare above 2 weeks and upto 1 month")
    # rate_1_week = models.DecimalField(max_digits=6, decimal_places=2)
    
    def __str__(self):
        return f" The rates at  {self.parking_lot} are rupees for upto 1 hour {self.upto_1_hr} and above 1 and b/w 5 hours {self.above_1_hr_upto_5_hr}"

class ParkingSlot(models.Model):
    class Meta:
        db_table='ParkingSlot'
    VEHICLE_CHOICES = (
        ('Two Wheeler','Two Wheeler'),
        ('Four Wheeler','Four Wheeler'),
        ('Heavy Vechiles','Heavy Vechiles')
    )
    parking_lot = models.ForeignKey(ParkingLot, on_delete=models.CASCADE)
    slot_number = models.CharField(max_length=10,unique=True)
    is_available = models.BooleanField(default=True)
    parking_slot_type = models.CharField('Parking Slot Type',max_length=30,choices=VEHICLE_CHOICES)
    def __str__(self):
        return f"{self.parking_lot.name} -  {self.slot_number}"
    
class ParkingBilling(models.Model):
    class Meta:
        db_table = 'ParkingBilling'
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True)
    parking_slot = models.ForeignKey(ParkingSlot, on_delete=models.CASCADE,null=True)
    vehicle_number = models.CharField(max_length=20,null=True)
    start_time = models.DateTimeField(null=True,default=timezone.now)
    end_time = models.DateTimeField(null=True,default=timezone.now)
    elapsed_time = models.CharField(null=True,blank=True,max_length=20)
    total_cost = models.DecimalField(max_digits=10, decimal_places=3)

    def formatted_start_time(self):
        return self.start_time.strftime('%Y-%m-%d %I:%M %p')
    def formatted_end_time(self):
        return self.end_time.strftime('%Y-%m-%d %I:%M %p')
    
class FinalBilling(models.Model):
    class Meta:
        db_table = 'Final Billing'
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True)
    parking_slot = models.ForeignKey(ParkingSlot, on_delete=models.CASCADE,null=True)
    vehicle_number = models.CharField(max_length=20,null=True)
    start_time = models.DateTimeField(null=True,default=timezone.now)
    end_time = models.DateTimeField(null=True,default=timezone.now)
    elapsed_time = models.CharField(null=True,blank=True,max_length=20)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)

    def formatted_start_time(self):
        return self.start_time.strftime('%Y-%m-%d %I:%M %p')
    def formatted_end_time(self):
        return self.end_time.strftime('%Y-%m-%d %I:%M %p')
    
class ContactUs(models.Model):
    class Meta:
        db_table = 'Contact Us'
    name = models.CharField('Enter name',max_length=50,null=False,blank=False)
    email = models.EmailField('Email',null=False,blank=False)
    phone_number = models.IntegerField('Phone Number',null=False,blank=False)
    message = models.CharField('Message',null=False,blank=False,max_length=1000)

class Subscribe(models.Model):
    class Meta:
        db_table = 'Subscriber'
    email = models.EmailField('Subscriber Email',unique=True,null=False,blank=False)
