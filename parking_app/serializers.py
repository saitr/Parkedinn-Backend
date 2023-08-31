from rest_framework import serializers
from .models import *
from django.utils.crypto import get_random_string
from django.conf import settings
from django.core.mail import send_mail,EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'phone_number']

    def create(self, validated_data):
        otp = get_random_string(length=6, allowed_chars='1234567890')
        user = CustomUser.objects.create_user(**validated_data)
        user.otp = otp
        user.save()

        subject = 'Your OTP Code'
        context = {'username': user.username, 'otp': otp}
        html_message = render_to_string('otp.html', context)
        plain_message = strip_tags(html_message)  # Strips HTML tags for the plain text version

        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [validated_data['email']]

        send_mail(subject, plain_message, from_email, recipient_list, html_message=html_message)
        return user

################## SignIn serializer ###############

class SignInSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('emial')

############### Listing of User #####################

class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'

################# Parking Lot Serializer ##############

class ParkingLotSerializer(serializers.ModelSerializer):
    available_slots = serializers.IntegerField(read_only=True)  # Add this field
    
    class Meta:
        model = ParkingLot
        fields = ['id', 'name', 'address', 'description', 'image', 'latitude', 'longitude','available_slots','parking_type']


################ Parking Slot Serializer ###############

class ParkingSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParkingSlot
        fields = '__all__'
        depth = 2



########################## Billing Serializer ######################

from decimal import Decimal

class ParkingBillingSerializer(serializers.ModelSerializer):
    
    total_cost = serializers.SerializerMethodField()
    
    class Meta:
        model = ParkingBilling
        fields = '__all__'
        
    def get_total_cost(self, obj):
        if obj.start_time and obj.end_time:
            elapsed_time = obj.end_time - obj.start_time
            seconds = elapsed_time.seconds + elapsed_time.days * 86400
            minutes = seconds // 60
            total_cost = Decimal(minutes * 0.67)
            return total_cost
        return Decimal(0)



class ParkingBillingDetailSerializer(serializers.ModelSerializer):
    user = UserListSerializer() 
    class Meta:
        model = ParkingBilling
        fields = ['id', 'user', 'vehicle_number', 'start_time', 'end_time', 'total_cost']


class ContactUsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactUs
        fields = ('name','email','phone_number','message')

    def create(self, validated_data):
        contact = ContactUs.objects.create(**validated_data)
        contact.save()
        subject = 'New Form Submission'
        context = {'name':contact.name,'email':contact.email,'phone_number':contact.phone_number,'message':contact.message}
        html_message = render_to_string('Contact.html',context)
        plain_message = strip_tags(html_message)  # Strips HTML tags for the plain text version
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [settings.DEFAULT_FROM_EMAIL]

        send_mail(subject, plain_message, from_email, recipient_list, html_message=html_message)
        return contact

class SubscriberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscribe
        fields = ('id','email')
    
    def create(self, validated_data):
        subscriber = Subscribe.objects.create(**validated_data)
        subscriber.save()


        subject = 'Thanks For Subscribing'
        html_message = render_to_string('subscribing.html')
        plain_message = strip_tags(html_message)  # Strips HTML tags for the plain text version

        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [validated_data['email']]

        send_mail(subject, plain_message, from_email, recipient_list, html_message=html_message)
        return subscriber
    

class FinalBillingSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinalBilling
        fields = '__all__'
        depth= 2


class ParkingRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParkingRate
        fields = ['vehicle_type','parking_lot','upto_1_hr','above_1_hr_upto_5_hr','above_5_hr_and_upto_24_hr','above_1_day_and_upto_3_days','above_3_days_and_upto_7_days','above_1_week_and_upto_2_weeks','above_2_week_and_upto_1_month']
        # depth = 1




################# Admin signup ######################


class AdminSignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'username', 'phone_number', 'password')

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = CustomUser.objects.create_superuser(
            password=password,
            **validated_data,
            is_active=True  # You might want to ensure the user is active as well
        )
        return user


    

