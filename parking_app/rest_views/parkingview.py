from geopy.distance import geodesic
from rest_framework.views import APIView
from rest_framework.response import Response
from parking_app.models import *
from parking_app.serializers import ParkingLotSerializer, ParkingSlotSerializer,ParkingBillingSerializer, ParkingBillingDetailSerializer,ContactUsSerializer,SubscriberSerializer,FinalBillingSerializer,ParkingRateSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser,AllowAny
from rest_framework import generics
import requests



# class NearbyParkingLots(APIView):
    
#     permission_classes = [IsAuthenticated]
#     authentication_classes = [JWTAuthentication]

#     def get(self, request):
#         lon = request.query_params.get('longitude')
#         lat = request.query_params.get('latitude')

#         if lon is None or lat is None:
#             return Response({"error": "Latitude and longitude are required"}, status=400)

#         try:
#             user_lon = float(lon)
#             user_lat = float(lat)
#         except ValueError:
#             return Response({"error": "Invalid coordinates"}, status=400)

#         user_coords = (user_lat, user_lon)
        
#         parking_lots = ParkingLot.objects.all()
#         parking_lots_data = []
        
#         for parking_lot in parking_lots:
#             parking_coords = (parking_lot.latitude, parking_lot.longitude)
#             distance = geodesic(user_coords, parking_coords).kilometers
#             parking_lot_data = {
#                 "parking_lot": parking_lot,
#                 "distance_km": distance
#             }
#             parking_lots_data.append(parking_lot_data)

#         sorted_parking_lots = sorted(parking_lots_data, key=lambda x: x["distance_km"])
#         print(sorted_parking_lots)
#         serializer = ParkingLotSerializer([p["parking_lot"] for p in sorted_parking_lots], many=True)
#         return Response(serializer.data)

############# Parking Lot Creation Api ##################

class ParkingLotCreateView(APIView):
    permission_classes = [IsAdminUser]
    
    def post(self, request, format=None):
        serializer = ParkingLotSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



############### Parking Lot List ########################
from django.db.models import Count

class ParkingLotList(generics.ListAPIView):
    queryset = ParkingLot.objects.annotate(available_slots=Count('parkingslot', filter=models.Q(parkingslot__is_available=True))).order_by('id')
    serializer_class = ParkingLotSerializer
    
    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        data = response.data
        # print('parking lot',data)
        for item in data:
            item['available_slots'] = item.pop('available_slots')
        return Response(data)


################## Nearby parking lots filtering using geodesic didn't give results gave wrong results ######################

# class NearbyParkingLots(APIView):
#     def get(self, request):
#         user_latitude = float(request.query_params.get('latitude'))
#         user_longitude = float(request.query_params.get('longitude'))
#         radius = 10  # in kilometers
        
#         nearby_lots = []

#         all_lots = ParkingLot.objects.all()
#         for lot in all_lots:
#             lot_coords = (lot.latitude, lot.longitude)
#             user_coords = (user_latitude, user_longitude)
#             distance = geodesic(user_coords, lot_coords).kilometers
#             print(distance)
#             if distance <= radius:
#                 nearby_lots.append(lot)

#         serializer = ParkingLotSerializer(nearby_lots, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)



class NearbyParkingLots(APIView):
    def get(self, request):
        user_latitude = float(request.query_params.get('latitude'))
        user_longitude = float(request.query_params.get('longitude'))
        radius = 3.0  # in kilometers
        
        nearby_lots = []

        all_lots = ParkingLot.objects.all()

        for lot in all_lots:
            lot_latitude = lot.latitude
            lot_longitude = lot.longitude

            # Make request to Google Maps Distance Matrix API
            response = requests.get(
                f"https://maps.googleapis.com/maps/api/distancematrix/json",
                params={
                    "origins": f"{user_latitude},{user_longitude}",
                    "destinations": f"{lot_latitude},{lot_longitude}",
                    "key": "AIzaSyAwlaOn54SWFxclJZ7dBJ9sNFutLYcOwxA"
                }
            )
            data = response.json()

            # Extract distance in meters
            distance_in_meters = data["rows"][0]["elements"][0]["distance"]["value"]
            print(distance_in_meters)
            if distance_in_meters <= radius * 1000:  # Convert radius to meters
                nearby_lots.append(lot)
            
        serializer = ParkingLotSerializer(nearby_lots, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

################################### Parking Lots with 10kms to 50 kms radius #########################




################################## Search the parking lots by name of the parking lots and output should be more
    
############# Single parking lot details  ####################

class ParkingLotDetailAPIView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    queryset = ParkingLot.objects.annotate(available_slots=Count('parkingslot', filter=models.Q(parkingslot__is_available=True))).order_by('id')
    serializer_class = ParkingLotSerializer
    lookup_field = 'id'


############## ParkingSlot creation api ###########################

class ParkingSlotCreate(generics.ListCreateAPIView):
    permission_classes = [IsAdminUser]
    queryset = ParkingSlot.objects.all()
    serializer_class = ParkingSlotSerializer
    

class ParkingSlotListByParkingLot(generics.ListAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = ParkingSlotSerializer

    def get_queryset(self):
        # Retrieve the parking lot ID from the URL parameters
        parking_lot_id = self.kwargs['parking_lot_id']

        # Filter parking slots based on the associated parking lot
        queryset = ParkingSlot.objects.filter(parking_lot_id=parking_lot_id)

        return queryset


################## Parking Time API ###############################


# class ParkingTimerView(generics.UpdateAPIView):
#     queryset = ParkingSlot.objects.all()
#     serializer_class = ParkingBillingSerializer

#     def update(self, request, *args, **kwargs):
#         instance = self.get_object()
#         serializer = self.get_serializer(instance, data=request.data)
#         serializer.is_valid(raise_exception=True)

#         # Calculate the total cost based on timer and rate
#         start_time = serializer.validated_data['start_time']
#         end_time = serializer.validated_data['end_time']
#         minutes_parked = (end_time - start_time).total_seconds() / 60
#         cost_per_minute = 0.67  # Set your cost per minute here
#         total_cost = round(minutes_parked * cost_per_minute, 2)

#         serializer.save(total_cost=total_cost)
        
#         ParkingBilling.objects.create(
#             parking_slot=instance,
#             car_number=serializer.validated_data['car_number'],
#             start_time=start_time,
#             end_time=end_time,
#             total_cost=total_cost
#         )

#         return Response(serializer.data, status=status.HTTP_200_OK)
    




################### Start time API ######################

# class StartTimerView(generics.CreateAPIView):
#     serializer_class = ParkingBillingSerializer
#     permission_classes = [IsAdminUser]
#     def perform_create(self, serializer):
#         print("User:", self.request.user)  # Debug: Print the user object
        
#         user = self.request.user
#         if user.is_authenticated:
#             print("User is authenticated.")
#         else:
#             print("User is not authenticated.")
        
#         vehicle_number = self.request.data.get('vehicle_number')
#         parking_slot = self.request.data.get('parking_slot')
#         start_time = timezone.now()
#         end_time = None
#         total_cost = 0.0

#         serializer.save(
#             user=user,
#             parking_slot_id=parking_slot,
#             vehicle_number=vehicle_number,
#             start_time=start_time,
#             end_time=end_time,
#             total_cost=total_cost
#         )

class StartTimerView(generics.CreateAPIView):
    serializer_class = ParkingBillingSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        user_id = request.data.get('user')
        
        try:
            user = CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            return Response({'error': 'Invalid user ID'}, status=status.HTTP_400_BAD_REQUEST)
        
        vehicle_number = request.data.get('vehicle_number')
        parking_slot_id = request.data.get('parking_slot')  # Rename to parking_slot_id for clarity
        start_time = timezone.now()
        end_time = None
        total_cost = 0.0

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(
            user=user,
            parking_slot_id=parking_slot_id,
            vehicle_number=vehicle_number,
            start_time=start_time,
            end_time=end_time,
            total_cost=total_cost
        )
        
        # Update the is_available field of the corresponding ParkingSlot
        try:
            parking_slot = ParkingSlot.objects.get(id=parking_slot_id)
            parking_slot.is_available = False
            parking_slot.save()
        except ParkingSlot.DoesNotExist:
            pass  # Handle this case as needed
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)

#################### End time API #########################

# This code calculates the elapsed time in seconds and then converts it to minutes. The rest of the calculation remains the same. Remember to adapt the imports and model names according to your project structure.



# class StopTimerView(generics.UpdateAPIView):
#     queryset = ParkingBilling.objects.all()
#     serializer_class = ParkingBillingSerializer
#     lookup_field = 'pk'
    
#     def perform_update(self, serializer):
#         instance = serializer.instance
#         if instance.end_time:
#             return Response({'error': 'Timer has already been stopped'}, status=status.HTTP_400_BAD_REQUEST)

#         instance.end_time = timezone.now()

#         # Calculate elapsed time in minutes
#         start_time = instance.start_time
#         end_time = instance.end_time
#         elapsed_time_seconds = (end_time - start_time).total_seconds()
#         elapsed_time_minutes = elapsed_time_seconds / 60.0  # Time in minutes

#         per_minute_rate = 0.67  # 0.67 paise per minute
#         total_cost = elapsed_time_minutes * per_minute_rate

#         instance.total_cost = total_cost
#         instance.save(update_fields=['end_time', 'total_cost'])

#         try:
#             # Create a record in FinalBilling table
#             final_billing_data = {
#                 'user': instance.user,
#                 'parking_slot': instance.parking_slot,
#                 'vehicle_number': instance.vehicle_number,
#                 'start_time': instance.start_time,
#                 'end_time': instance.end_time,
#                 'total_cost': instance.total_cost
#             }
#             FinalBilling.objects.create(**final_billing_data)
#         except Exception as e:
#             return Response({'error': f'Failed to create FinalBilling record: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#         # Update the is_available field of the corresponding ParkingSlot to True
#         try:
#             parking_slot = instance.parking_slot
#             parking_slot.is_available = True
#             parking_slot.save()
#         except Exception as e:
#             return Response({'error': f'Failed to update ParkingSlot is_available field: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#         # Delete the record from ParkingBilling table
#         try:
#             instance.delete()
#         except Exception as e:
#             return Response({'error': f'Failed to delete ParkingBilling record: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#         return Response({'message': 'Timer stopped successfully, record moved to FinalBilling table, and deleted from ParkingBilling table'}, status=status.HTTP_200_OK)

from decimal import Decimal

# class StopTimerView(generics.UpdateAPIView):
#     queryset = ParkingBilling.objects.all()
#     serializer_class = ParkingBillingSerializer
#     lookup_field = 'pk'
    
#     def perform_update(self, serializer):
#         instance = serializer.instance
#         if instance.end_time:
#             return Response({'error': 'Timer has already been stopped'}, status=status.HTTP_400_BAD_REQUEST)

#         instance.end_time = timezone.now()
#         instance.save(update_fields=['end_time'])

#         # Calculate elapsed time in minutes
#         start_time = instance.start_time
#         end_time = instance.end_time
#         elapsed_time_seconds = (end_time - start_time).total_seconds()
#         elapsed_time_minutes = elapsed_time_seconds / 60.0  # Time in minutes

#         # Get the corresponding ParkingRate based on the vehicle type and parking lot from ParkingSlot
#         try:
#             parking_rate = ParkingRate.objects.get(vehicle_type=instance.parking_slot.parking_slot_type, parking_lot=instance.parking_slot.parking_lot)
#             print('parking_rate',parking_rate)
#         except ParkingRate.DoesNotExist:
#             return Response({'error': 'Parking rate not found'}, status=status.HTTP_400_BAD_REQUEST)

#         # Choose the appropriate rates based on the vehicle type
#         less_than_hour_rate = parking_rate.less_than_hour
#         after_one_hour_rate = parking_rate.after_one_hour
#         after_one_day_rate = parking_rate.after_one_day
#         after_one_week_rate = parking_rate.after_one_week

#         # Calculate fare based on the rates
#         total_fare = 0.0

#         # if elapsed_time_minutes < 60:
#         #     total_fare = elapsed_time_minutes * less_than_hour_rate
#         # elif elapsed_time_minutes >= 60 and elapsed_time_minutes < 24 * 60:
#         #     total_fare = elapsed_time_minutes * after_one_hour_rate
#         # elif elapsed_time_minutes >= 24 * 60 and elapsed_time_minutes < 7 * 24 * 60:
#         #     total_fare = elapsed_time_minutes * after_one_day_rate
#         # else:
#         #     total_fare = elapsed_time_minutes * after_one_week_rate

#         if elapsed_time_minutes < 60:
#             total_fare = Decimal(elapsed_time_minutes) * less_than_hour_rate
#         elif elapsed_time_minutes >= 60 and elapsed_time_minutes < 24 * 60:
#             total_fare = Decimal(elapsed_time_minutes / 60) * after_one_hour_rate
#         elif elapsed_time_minutes >= 24 * 60 and elapsed_time_minutes < 7 * 24 * 60:
#             total_fare = Decimal(elapsed_time_minutes / 60) * after_one_day_rate
#         else:
#             total_fare = Decimal(elapsed_time_minutes / 60) * after_one_week_rate
        
#         print("this is the time used here in the parking lot",elapsed_time_minutes)
#         print('total_cost of the parking',total_fare)
        
#         instance.total_cost = total_fare
#         instance.save(update_fields=['total_cost'])
        
#         try:
#             # Create a record in FinalBilling table
#             final_billing_data = {
#                 'user': instance.user,
#                 'parking_slot': instance.parking_slot,
#                 'vehicle_number': instance.vehicle_number,
#                 'start_time': instance.start_time,
#                 'end_time': instance.end_time,
#                 'total_cost': instance.total_cost
#             }
#             final_billing = FinalBilling.objects.create(**final_billing_data)
#             print(f"FinalBilling record created: {final_billing}")
#         except Exception as e:
#             return Response({'error': f'Failed to create FinalBilling record: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#         try:
#             # Update the is_available field of the corresponding ParkingSlot to True
#             parking_slot = instance.parking_slot
#             parking_slot.is_available = True
#             parking_slot.save()
#             print(f"ParkingSlot availability updated: {parking_slot}")
#         except Exception as e:
#             return Response({'error': f'Failed to update ParkingSlot is_available field: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#         try:
#             # Delete the record from ParkingBilling table
#             instance.delete()
#             print("ParkingBilling record deleted")
#         except Exception as e:
#             return Response({'error': f'Failed to delete ParkingBilling record: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#         return Response({'message': 'Timer stopped successfully, record moved to FinalBilling table, and deleted from ParkingBilling table'}, status=status.HTTP_200_OK)


class StopTimerView(generics.UpdateAPIView):
    queryset = ParkingBilling.objects.all()
    serializer_class = ParkingBillingSerializer
    lookup_field = 'pk'
    
    def perform_update(self, serializer):
        instance = serializer.instance
        if instance.end_time:
            return Response({'error': 'Timer has already been stopped'}, status=status.HTTP_400_BAD_REQUEST)

        instance.end_time = timezone.now()
        instance.save(update_fields=['end_time'])

        # Calculate elapsed time in minutes
        start_time = instance.start_time
        end_time = instance.end_time
        elapsed_time_seconds = (end_time - start_time).total_seconds()
        elapsed_time_minutes = elapsed_time_seconds / 60.0  # Time in minutes

        # Get the corresponding ParkingRate based on the vehicle type and parking lot from ParkingSlot
        try:
            parking_rate = ParkingRate.objects.get(vehicle_type=instance.parking_slot.parking_slot_type, parking_lot=instance.parking_slot.parking_lot)
            print('parking_rate',parking_rate)
        except ParkingRate.DoesNotExist:
            return Response({'error': 'Parking rate not found'}, status=status.HTTP_400_BAD_REQUEST)

        # Choose the appropriate rates based on the vehicle type
        if elapsed_time_minutes < 60:
            total_fare = parking_rate.upto_1_hr
        elif elapsed_time_minutes < 5 * 60:
            total_fare = parking_rate.above_1_hr_upto_5_hr
        elif elapsed_time_minutes < 24 * 60:
            total_fare = parking_rate.above_5_hr_and_upto_24_hr
        elif elapsed_time_minutes < 3 * 24 * 60:
            total_fare = parking_rate.above_1_day_and_upto_3_days
        elif elapsed_time_minutes < 7 * 24 * 60:
            total_fare = parking_rate.above_3_days_and_upto_7_days
        elif elapsed_time_minutes < 14 * 24 * 60:
            total_fare = parking_rate.above_1_week_and_upto_2_weeks
        else:
            total_fare = parking_rate.above_2_week_and_upto_1_month
        
        print("this is the time used here in the parking lot",elapsed_time_minutes)
        print('total_cost of the parking',total_fare)
        
        instance.total_cost = Decimal(total_fare)
        instance.save(update_fields=['total_cost'])
        
        try:
            # Create a record in FinalBilling table
            final_billing_data = {
                'user': instance.user,
                'parking_slot': instance.parking_slot,
                'vehicle_number': instance.vehicle_number,
                'start_time': instance.start_time,
                'end_time': instance.end_time,
                # 'elapsed_time': instance.elapsed_time_minutes,
                'total_cost': instance.total_cost
            }
            final_billing = FinalBilling.objects.create(**final_billing_data)
            print(f"FinalBilling record created: {final_billing}")
        except Exception as e:
            return Response({'error': f'Failed to create FinalBilling record: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        try:
            # Update the is_available field of the corresponding ParkingSlot to True
            parking_slot = instance.parking_slot
            parking_slot.is_available = True
            parking_slot.save()
            print(f"ParkingSlot availability updated: {parking_slot}")
        except Exception as e:
            return Response({'error': f'Failed to update ParkingSlot is_available field: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        try:
            # Delete the record from ParkingBilling table
            instance.delete()
            print("ParkingBilling record deleted")
        except Exception as e:
            return Response({'error': f'Failed to delete ParkingBilling record: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({'message': 'Timer stopped successfully, record moved to FinalBilling table, and deleted from ParkingBilling table'}, status=status.HTTP_200_OK)




############################## Parking Billing State ################################


# class ParkBillingState(generics.ListAPIView):
#     # permission_classes = [AllowAny]
#     queryset = ParkingSlot.objects.all()
#     serializer_class = ParkingBillingSerializer


class ParkingBillingDetailAPIView(generics.RetrieveAPIView):
    queryset = ParkingBilling.objects.all()
    serializer_class = ParkingBillingDetailSerializer
    lookup_field = 'parking_slot_id'  # Use the correct lookup field here

    def get_object(self):
        parking_slot_id = self.kwargs.get(self.lookup_field)
        try:
            parking_billing = ParkingBilling.objects.get(parking_slot__id=parking_slot_id)
            return parking_billing
        except ParkingBilling.DoesNotExist:
            return Response({'detail': 'ParkingBilling not found for the specified ParkingSlot ID'},
                            status=404)
        

class ContactUsView(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    queryset = ContactUs.objects.all()
    serializer_class = ContactUsSerializer


class SubscriberView(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    queryset = Subscribe.objects.all()
    serializer_class = SubscriberSerializer



class BillingListView(generics.ListAPIView):
    permission_classes = [IsAdminUser]
    authentication_classes = [JWTAuthentication]
    queryset = FinalBilling.objects.all()
    serializer_class = FinalBillingSerializer

class BiilingPerPerson(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    serializer_class = FinalBillingSerializer 

    def get_queryset(self):
        # Get the authenticated user
        user = self.request.user

        # Filter the billings where the user is responsible
        queryset = FinalBilling.objects.filter(user=user)
        
        return queryset



class ParkingRateCreate(generics.ListCreateAPIView):
    permission_classes = [IsAdminUser]
    queryset = ParkingRate.objects.all()
    serializer_class = ParkingRateSerializer