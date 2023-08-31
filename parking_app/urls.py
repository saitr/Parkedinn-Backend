from django.urls import path

from . import views
from parking_app.rest_views.parkingview import * 

urlpatterns = [
    ####### user routes ##############
    path('signup/',views.SignUp.as_view(),name='signup'),
    path('verify/<str:email>/',views.VerifyOtpView.as_view(), name='VerifyEmail'),
    path('signin/', views.SignInView.as_view(), name='signin'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('user_list/',views.UserList.as_view(),name="userlist"),
    # path('send-otp/', views.SendOTP.as_view(), name='send-otp'),

    ########################## Admin urls ###########################

    path('admin-signup/', views.AdminSignupView.as_view(), name='admin-signup'),

    ################## parking lot urls ############
    path('nearest_parking_lots/', NearbyParkingLots.as_view(), name='nearest_parking_lots'),
    path('parking_lot_create/',ParkingLotCreateView.as_view(),name='create_parking_create'),
    path('parking_lot_list/',ParkingLotList.as_view(),name='parking_lot_list'),
    path('parking-lots/<int:id>/', ParkingLotDetailAPIView.as_view(), name='parking-lot-detail'),
    path('parking-slot-create/',ParkingSlotCreate.as_view(),name="parking-slot-create"),
    path('parking-slots-filter/<int:parking_lot_id>/', ParkingSlotListByParkingLot.as_view(), name='parking-slot-list-by-parking-lot'),
    # path('order-billing/',StartTimerView.as_view(),name='billing'),
    path('start-timer/', StartTimerView.as_view(), name='start-timer'),
    path('stop-timer/<int:pk>/', StopTimerView.as_view(), name='stop-timer'),
    path('parking-slot/<int:parking_slot_id>/billing/', ParkingBillingDetailAPIView.as_view(), name='parking-billing-detail'),
    path('total_bookings/',BillingListView.as_view(),name='billinglist'),
    path('user_billing/',BiilingPerPerson.as_view(),name='user-billing'),
    ################ subscribing and contact us #######################
    path('subscriber/',SubscriberView.as_view(),name='subscriber'),
    path('contactus/',ContactUsView.as_view(),name='contactus'),
    path('parking_rates_all/',ParkingRateCreate.as_view(),name='parking-rates'),
]