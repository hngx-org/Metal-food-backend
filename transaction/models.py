from django.db import models
from users.models import Users

# Create your models here.


class Lunches(models.Model):
    id = models.BigAutoField(primary_key=True)
    sender_id = models.ForeignKey(
        Users, on_delete=models.CASCADE, null=False, related_name='lunch_sender')
    reciever_id = models.ForeignKey(
        Users, on_delete=models.CASCADE, null=False, related_name='lunch_reciever')
    quantity = models.IntegerField()
    redeemed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)
    note = models.TextField(null=True)

    def __str__(self) -> str:
        return self.id


class Withdrawals(models.Model):
    id = models.BigAutoField(primary_key=True)
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE)
    status = models.CharField(max_length=30)
    amount = models.DecimalField(default=0.00, max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f'{self.id}'
