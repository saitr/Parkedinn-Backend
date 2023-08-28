from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import make_password


# class CustomUserManager(BaseUserManager):
#     def create_user(self, username, email, phone_number):
#         if not username or not email or not phone_number:
#             raise ValueError("Username, email, and phone number must be set")
        
#         user = self.model(username=username, email=self.normalize_email(email), phone_number=phone_number)
#         user.save(using=self._db)
#         return user

#     def create_superuser(self, username, email, phone_number, password=None, **extra_fields):
#         extra_fields.setdefault('is_staff', True)
#         extra_fields.setdefault('is_superuser', True)
#         extra_fields.setdefault('is_active', True)

#         if extra_fields.get('is_staff') is not True:
#             raise ValueError('Superuser must have is_staff=True.')
#         if extra_fields.get('is_superuser') is not True:
#             raise ValueError('Superuser must have is_superuser=True.')

#         if password:
#             user = self.create_user(username, email, phone_number, password=password, **extra_fields)
#             user.is_admin = True
#             user.save(using=self._db)
#             return user
#         else:
#             raise ValueError("Superuser must have a password")


class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, phone_number, password=None, **extra_fields):
        if not username or not email or not phone_number:
            raise ValueError("Username, email, and phone number must be set")
        
        user = self.model(username=username, email=self.normalize_email(email), phone_number=phone_number, **extra_fields)
        if password:
            user.set_password(password)  # Set the password
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, phone_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_admin',True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        user = self.create_user(username, email, phone_number, password=password, **extra_fields)
        return user
