from django.db import models

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from django.utils import timezone


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **kwargs):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **kwargs):
        kwargs.setdefault('is_staff', True)
        kwargs.setdefault('is_superuser', True)

        if kwargs.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if kwargs.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **kwargs)


class Organization(models.Model):
    name = models.CharField(max_length=50, unique=True, null=False)    
    lunch_price = models.DecimalField(max_digits=10, decimal_places=2, default=1000.00)
    currency = models.CharField(max_length=3, default='NGN')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    objects = CustomUserManager()

    def __str__(self):
        return self.name


class Users(AbstractBaseUser, PermissionsMixin):
    org = models.ForeignKey(Organization, on_delete=models.CASCADE, null=True)
    full_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True, null=False, blank=False)
    username = models.CharField(unique=True, max_length=100, null=True, blank=True)
    password = models.CharField(max_length=255, null=False, blank=False)
    phone_number = PhoneNumberField(null=True, blank=True, unique=True)
    profile_picture = models.ImageField(upload_to='profile_image/', null=True)
    token = models.CharField(max_length=255, null=True)
    bank_number = models.CharField(max_length=20, null=True)
    bank_code = models.CharField(max_length=30, null=True)
    bank_name = models.CharField(max_length=30, null=True)
    bank_region = models.CharField(max_length=255, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    lunch_credit_balance = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    currency = models.CharField(max_length=255, null=True)
    currency_code = models.CharField(max_length=10, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    otp = models.IntegerField(default=None, null=True, blank=True)

    groups = models.ManyToManyField(
        'auth.Group',
        blank=True,
        related_name='customuser_set'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        blank=True,
        related_name='customuser_set'
    )

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'username', 'password']

    def __str__(self):
        return self.email
    def has_perm(self, perm, obj=None):

        return True
    def has_module_perms(self, app_label):

        return True

class OrganizationInvites(models.Model):
    org_id = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="company")
    email = models.EmailField(unique=True)
    token = models.CharField(max_length=100, blank=False, null=False)
    TTL = models.DateTimeField(default=timezone.now() + timezone.timedelta(hours=24))

    def __str__(self) -> str:
        return str(self.id)

   
class OrganizationLunchWallet(models.Model):
    org_id = models.ForeignKey(Organization, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self) -> str:
        return str(self.id)