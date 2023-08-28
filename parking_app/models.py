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


# class ParkingSlots(models.Model):
#     class Meta:
#         db_table = 'Parking Slot'
#     slotNo = models.IntegerField('Slot Number',blank=False,null=False)



# class Parking(models.Model):
#     class Meta:
#         db_table = 'Parking Lot'
#     parkingname = models.CharField('Parking Lot Name',max_length=1000,blank=False,null=False)
#     description = models.CharField('Parking Lot Description',max_length=1000,null=False,blank=False)
#     parkingslot = models.ManyToManyField(ParkingSlots,blank=False,null=False)
#     parkingimage1 = CloudinaryField('ParkingImage1',blank=False,null=False)
#     parkingiamge2 = CloudinaryField('ParkingImage2',blank=False,null=False)
#     parkingimage3 = CloudinaryField('ParkingImage3',blank=False,null=False)
#     parkingimage4 = CloudinaryField('ParkingImage4',blank=False,null=False)
#     latitude = models.FloatField('Latitude Cordinates',blank=False,null=False)
#     longitude = models.FloatField('Longitude Cordinates',blank=False,null=False)
#     vehicle_number = models.CharField('Vehicle Number',max_length=15,blank=False,null=False)
#     parkingtime = models.DateField('Parking Date',blank=False,null=False)

#     def __str__(self):
#         return self.parkingname
    

    

class ParkingLot(models.Model):
    class Meta:
        db_table='ParkingLot'
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    description = models.TextField(blank=True,null=True)
    image = CloudinaryField('Parking Image Lot Picture',blank=True, null=True)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return self.name

class ParkingSlot(models.Model):
    class Meta:
        db_table='ParkingSlot'
    parking_lot = models.ForeignKey(ParkingLot, on_delete=models.CASCADE)
    slot_number = models.CharField(max_length=10,unique=True)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.parking_lot.name} -  {self.slot_number}"
    
class ParkingBilling(models.Model):
    class Meta:
        db_table = 'ParkingBilling'
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True)
    parking_slot = models.ForeignKey(ParkingSlot, on_delete=models.CASCADE,null=True)
    vehicle_number = models.CharField(max_length=20,null=True)
    start_time = models.DateTimeField(null=True)
    end_time = models.DateTimeField(null=True)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)


class FinalBilling(models.Model):
    class Meta:
        db_table = 'Final Billing'
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True)
    parking_slot = models.ForeignKey(ParkingSlot, on_delete=models.CASCADE,null=True)
    vehicle_number = models.CharField(max_length=20,null=True)
    start_time = models.DateTimeField(null=True)
    end_time = models.DateTimeField(null=True)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)


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