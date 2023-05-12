from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, email_or_phone, password=None, **extra_fields):
        if not email_or_phone:
            raise ValueError('The Email or Phone field must be set')
        email_or_phone = self.normalize_email(email_or_phone)
        user = self.model(email_or_phone=email_or_phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email_or_phone, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email_or_phone, password, **extra_fields)


GENDER_CHOICE = [
    ("M", "Male"),
    ("F", "Female"),
    ("O", "Other"),
]
class CustomUser(AbstractUser):
    full_name = models.CharField(max_length=255)
    email_or_phone = models.CharField(max_length=255, unique=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICE)
    country = models.CharField(max_length=120)
    online_status = models.BooleanField(default=False)
    is_profileComplete = models.BooleanField(default=False)
    connected_with = models.CharField(max_length=255, default="")
    interests = models.TextField() #This will be CSV kind of data

    # Disable All unnecessary Fields
    username = None
    first_name = None
    last_name = None
    email = None

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email_or_phone'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email_or_phone
    def has_perm(self, *args, **kwargs) -> bool:
        return True
    def has_module_perms(self, *args, **kwargs) -> bool:
        return True
