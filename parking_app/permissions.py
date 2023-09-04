from rest_framework.permissions import BasePermission, IsAdminUser

class CanCreateParkingLot(BasePermission):
    def has_permission(self, request, view):
        # Allow parking lot creation for users with is_staff=True or IsAdminUser
        return request.user.is_staff or IsAdminUser().has_permission(request, view)
