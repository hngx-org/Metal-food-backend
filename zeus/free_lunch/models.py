from django.db import models

# Create your models here.

class Users(models.Model):
    """
     user model
    """
    id = models.AutoField(primary_key=True, unique=True)
    org_id = models.ForeignKey('Organization', on_delete=models.SET_NULL)
    name = models.CharField(max_length=100)
    profile_picture = models.ImageField(upload_to='profile_image/')
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)
    password = models.CharField(max_length=100)
    refresh_token = models.CharField(max_length=100)
    bank_number = models.CharField(max_length=20)
    bank_code = models.CharField(max_length=30) 
    bank_name = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    isAdmin = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name

class Organization(models.Model):
    id = models.BigAutoField(primary_key=True, unique=True)
    name = models.CharField(max_length=50)
    lunch_price = models.DecimalField(max_digit=10, decimal_places=2)
    currency = models.CharField(max_length=3)

    def __str__(self):
        return self.name
