from django.shortcuts import render
from .serializers import *
from rest_framework import generics, status
from .models import *
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth.hashers import check_password
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


# Create your views here.


###### Signup ##############

class SignUp(generics.ListCreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class=SignUpSerializer

############# Verify the otp ##################

class VerifyOtpView(generics.GenericAPIView):

    permission_classes = [AllowAny]
    def post(self, request,email):
        user = CustomUser.objects.filter(email=email).first()
        otp = request.data.get('otp')

        if otp == user.otp:
            user.is_active = True
            refresh = RefreshToken.for_user(user)
            user.jwt_token = RefreshToken.for_user(user)
            
            user.save()

            ############# To send the email after verification #################

            subject = 'Welcome To The Family'
            from_email = settings.DEFAULT_FROM_EMAIL
            context = {'username':user.username,'email':user.email}
            to = [email]
            html_content = render_to_string('thankyouemail.html',context)
            text_content = strip_tags(html_content)
            
            msg = EmailMultiAlternatives(subject,text_content,from_email,to)
            msg.attach_alternative(html_content,'text/html')
            msg.send()

            return Response({'status':200,'refresh': str(refresh), 'access': str(refresh.access_token),'verification':'verified successfully'})
        else:
            return Response({'detail': 'Invalid otp'}, status=status.HTTP_401_UNAUTHORIZED)


################### Logout API ############################

class LogoutView(APIView):

    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)



########################### Signin API ################################### 

from django.contrib.auth import login

class SignInView(generics.CreateAPIView):


    def post(self, request, *args, **kwargs):
        email = request.data.get('email')

        # user = authenticate(email=email, password=password)

        user = CustomUser.objects.filter(email=email).first()

        if user:
            login(request,user)
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token)
            }, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)


# from django.contrib.auth import authenticate, login
# from rest_framework import generics, status
# from rest_framework.response import Response
# from rest_framework_simplejwt.tokens import RefreshToken
# from .models import CustomUser

# class SignInView(generics.CreateAPIView):
#     def post(self, request, *args, **kwargs):
#         email = request.data.get('email')
#         # password = request.data.get('password')  # Assuming you have a password field in the request

#         user = authenticate(email=email)

#         if user is not None:
#             login(request, user)  # Manually log in the user to update last_login
#             refresh = RefreshToken.for_user(user)
#             return Response({
#                 'refresh': str(refresh),
#                 'access': str(refresh.access_token)
#             }, status=status.HTTP_200_OK)
#         else:
#             return Response({'error': 'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)



# Testing process 

class UserList(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserListSerializer
    


# views.py
# import random
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from django.utils import timezone
# import pywhatkit as kit

# class SendOTP(APIView):
#     def post(self, request):
#         # Get the user's WhatsApp number from the request data
#         whatsapp_number = request.data.get('whatsapp_number')

#         # Generate a random OTP
#         otp = ''.join([str(random.randint(0, 9)) for _ in range(6)])

#         # Send the OTP via WhatsApp
#         message = f"Your OTP is: {otp}"
#         kit.sendwhatmsg(whatsapp_number, message, timezone.localtime().hour, timezone.localtime().minute + 1)

#         # Store the OTP in the user's session or database for validation
#         request.session['otp'] = otp

#         return Response({"message": "OTP sent successfully"})


# from django.utils import timezone
# import datetime


# class TimeTest(generics.ListAPIView):
#     queryset = CustomUser.objects.all()
#     serializer_class = UserListSerializer
     
#     print(timezone.now())
#     print(timezone.localtime())
#     print(datetime.datetime.now())




