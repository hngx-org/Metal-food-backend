from django.db import models

# Create your models here.

class Organization(models.Model):
    id = models.BigAutoField(primary_key=True, unique=True)
    name = models.CharField(max_length=50)
    lunch_price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3)

    def __str__(self):
        return self.name

class Users(models.Model):
    """
     user model
    """
    id = models.AutoField(primary_key=True, unique=True)
    org_id = models.ForeignKey(Organization, on_delete=models.SET_NULL)
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


class Lunches(models.Model):
    id = models.BigAutoField(primary_key=True)
    sender_id = models.ForeignKey(Users, on_delete=models.CASCADE, null=False, related_name='lunch_sender')
    reciever_id = models.ForeignKey(Users, on_delete=models.CASCADE, null=False, related_name='lunch_reciever')
    quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now=True)
    note = models.TextField(null=True)

    def __str__(self) -> str:
        return self.id

class Withdrawals(models.Model):
    id = models.BigAutoField(primary_key=True)
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE)
    status= models.CharField(max_length=30)
    amount = models.DecimalField()
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.id

class OrganizationInvites(models.Model):
    id = models.BigAutoField(primary_key=True)
    email = models.EmailField(unique=True)
    token = models.CharField(max_length=100)
    TTL = models.DateTimeField()
