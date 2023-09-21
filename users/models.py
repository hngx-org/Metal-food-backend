from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, AbstractUser
from django.db import models
from django.utils import timezone


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **kwargs):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **kwargs)
        # user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **kwargs):
        kwargs.setdefault('is_staff', True)
        kwargs.setdefault('is_superuser', False)

        if kwargs.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if kwargs.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **kwargs)

class Organization(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=50, unique=True, null=False)
    email = models.EmailField(unique=True, null=False, blank=False)
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
    org = models.ForeignKey(Organization, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True, null=False, blank=False)
    username = models.CharField(unique=True, max_length=100, null=False, blank=False)
    password = models.CharField(max_length=255, null=False, blank=False)
    phone_number = models.CharField(max_length=15)
    profile_picture = models.ImageField(upload_to='profile_image/', null=True)
    refresh_token = models.CharField(max_length=255, null=True)
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
    REQUIRED_FIELDS = []

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
    
    # def is_expired(self):
    #     """Checks if the invite token has expired"""
    #     return self.TTL < timezone.now()
    
    # def get_remaining_time(self):
    #     """Get the remaining time until expiration."""
    #     if not self.is_expired():
    #         remaining_time = self.TTL - timezone.now()
    #         return remaining_time.total_seconds()
    #     return None

class OrganizationLunchWallet(models.Model):
    org_id = models.ForeignKey(Organization, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self) -> str:
        return str(self.id)


# Create your models here.
class Organization(models.Model):
    id = models.BigAutoField(primary_key=True, unique=True)
    name = models.CharField(max_length=255)
    lunch_price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3)

    def __str__(self):
        return self.name

class Users(models.Model):
    """
     user model
    """
    id = models.AutoField(primary_key=True, unique=True)
    org_id = models.ForeignKey(Organization, on_delete=models.SET_NULL, null=True)
    first_name = models.CharField(max_length=255, null=False)
    last_name = models.CharField(max_length=255, null=False)
    profile_picture = models.ImageField(upload_to='profile_image/')
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)
    password_hash = models.CharField(max_length=255)
    refresh_token = models.CharField(max_length=255)
    bank_number = models.CharField(max_length=20)
    bank_code = models.CharField(max_length=30) 
    bank_name = models.CharField(max_length=30)
    bank_region = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    isAdmin = models.BooleanField(default=False)
    lunch_credit_balance = models.IntegerField()
    currency = models.CharField(max_length=255)
    currency_code = models.CharField(max_length=10)
    updated_at = models.DateTimeField()

    
    def __str__(self):
        return self.name


class OrganizationInvites(models.Model):
    id = models.ForeignKey(Organization, on_delete=models.CASCADE, primary_key=True)
    email = models.EmailField(unique=True)
    token = models.CharField(max_length=100)
    TTL = models.DateTimeField()

    def __str__(self) -> str:
        return self.id

class OrganizationLunchWallet(models.Model):
    id= models.BigAutoField(primary_key=True, unique=True)
    org_id = models.ForeignKey(Organization, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self) -> str:
        return self.id
    
