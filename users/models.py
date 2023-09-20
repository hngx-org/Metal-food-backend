from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin,UserManager

# class Organization(models.Model):
#     id = models.BigAutoField(primary_key=True, unique=True)
#     name = models.CharField(max_length=50)
#     lunch_price = models.DecimalField(max_digits=10, decimal_places=2)
#     currency = models.CharField(max_length=3)

#     def __str__(self):
#         return self.name

# class Users(models.Model):
#     """
#      user model
#     """
#     id = models.AutoField(primary_key=True, unique=True)
#     # org_id = models.ForeignKey(Organization, on_delete=models.SET_NULL, null=True)
#     first_name = models.CharField(max_length=100, null=False)
#     # last_name = models.CharField(max_length=100, null=False)
#     # profile_picture = models.ImageField(upload_to='profile_image/')
#     # email = models.EmailField(unique=True)
#     # phone_number = models.CharField(max_length=15)
#     password_hash = models.CharField(max_length=100)
#     # refresh_token = models.CharField(max_length=100)
    # bank_number = models.CharField(max_length=20)
    # bank_code = models.CharField(max_length=30) 
    # bank_name = models.CharField(max_length=30)
#     created_at = models.DateTimeField(auto_now_add=True)
#     isAdmin = models.BooleanField(default=False)
    # lunch_credit_balance = models.IntegerField()
    # updated_at = models.DateTimeField()

    
#     def __str__(self):
#         return self.fir

# class CustomUserManager(UserManager):
#     def _create_user(self, email, password, **extra_fields):
#         if not email:
#             raise ValueError("you have not provided a valid email")
        
#         email = self.normalize_email(email)
#         user = self.model(email= email,  **extra_fields)
#         user.set_password(password)
#         user.save(using = self._db)

#         return user
    
#     def create_user(self, email = None,  password = None , **extra_fields):
#         extra_fields.setdefault('is_staff',False)
#         extra_fields.setdefault('is_superuser',False)

#         return self._create_user(email,password,**extra_fields)
    
#     def create_superuser(self, email = None, password = None , **extra_fields):
#           extra_fields.setdefault('is_staff',True)
#           extra_fields.setdefault('is_superuser',True)

#           return self._create_user(email,password, **extra_fields)

# class Users(AbstractBaseUser,PermissionsMixin):
#     email = models.EmailField(blank = True, default='')
#     username = models.CharField(max_length=255,blank = True,default='', unique=True)
#     first_name = models.CharField(max_length=255,blank = True,default='' )
#     last_name = models.CharField(max_length=255, blank = True, default = '')
#     profile_picture = models.ImageField(upload_to='profile_image/', blank = True, null = True)
#     bank_number = models.CharField(max_length=20, blank = True, null = True)
#     bank_code = models.CharField(max_length=30, blank  = True, null = True) 
#     bank_name = models.CharField(max_length=30, blank = True, null = True)
#     is_active = models.BooleanField(default=True)
#     is_superuser = models.BooleanField(default=False)
#     is_staff = models.BooleanField(default=False)
#     phone_number = models.CharField(max_length=15, blank = True, null = True)
#     lunch_credit_balance = models.IntegerField(blank = True, null = True)

#     created_at = models.DateTimeField(default=timezone.now)
#     last_login = models.DateTimeField(blank = True , null = True)

#     objects = CustomUserManager()

#     USERNAME_FIELD = 'username'
#     EMAIL_FIELD = 'email'
#     REQUIRED_FIELDS = ['email']

#     class Meta :
#         verbose_name = 'User'
#         verbose_name_plural = 'Users'

#     def get_full_name(self):
#         return f'{self.first_name} {self.last_name}'
    

# class Lunches(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     sender_id = models.ForeignKey(Users, on_delete=models.CASCADE, null=False, related_name='lunch_sender')
#     reciever_id = models.ForeignKey(Users, on_delete=models.CASCADE, null=False, related_name='lunch_reciever')
#     quantity = models.IntegerField()
#     redeemed = models.BooleanField(default=False)
#     created_at = models.DateTimeField(auto_now=True)
#     note = models.TextField(null=True)

#     def __str__(self) -> str:
#         return self.id

# class Withdrawals(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     user_id = models.ForeignKey(Users, on_delete=models.CASCADE)
#     status= models.CharField(max_length=30)
#     amount = models.DecimalField(default=0.00, max_digits=10, decimal_places=2)
#     created_at = models.DateTimeField(auto_now=True)

#     def __str__(self) -> str:
#         return self.id

# class OrganizationInvites(models.Model):
#     id = models.ForeignKey(Organization, on_delete=models.CASCADE, primary_key=True)
#     email = models.EmailField(unique=True)
#     token = models.CharField(max_length=100)
#     TTL = models.DateTimeField()

#     def __str__(self) -> str:
#         return self.id

# class OrganizationLunchWallet(models.Model):
#     id= models.BigAutoField(primary_key=True, unique=True)
#     org_id = models.ForeignKey(Organization, on_delete=models.CASCADE)
#     balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

#     def __str__(self) -> str:
#         return self.id