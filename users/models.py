from django.db import models

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
    profile_picture = models.ImageField(upload_to='profile_image/', null=True)
    email = models.EmailField(unique=True,null=False)
    phone_number = models.CharField(max_length=1, null=False)
    password_hash = models.CharField(max_length=255, null=False)
    refresh_token = models.CharField(max_length=255,null=True)
    bank_number = models.CharField(max_length=20, null=True)
    bank_code = models.CharField(max_length=30, null=True) 
    bank_name = models.CharField(max_length=30, null=True)
    bank_region = models.CharField(max_length=255, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    isAdmin = models.BooleanField(default=False, null=True)
    lunch_credit_balance = models.IntegerField()
    currency = models.CharField(max_length=255)
    currency_code = models.CharField(max_length=10)
    updated_at = models.DateTimeField(auto_now=True)

    
    def __str__(self):
        return self.name


class OrganizationInvites(models.Model):
    id = models.OneToOneField(Organization, on_delete=models.CASCADE, primary_key=True)
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
    