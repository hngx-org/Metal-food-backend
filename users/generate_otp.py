import random
from .models import Users
import os
import smtplib

def generate_otp(user):
    otp = str(random.randint(1000, 9999))
    user.otp = otp
    return otp



def send_email(email):
    user = Users.objects.get(email=email)
    otp = user.otp
    own_email = os.getenv('EMAIL_ADD')
    own_password = os.getenv('EMAIL_PASS')
    email_message = f"Subject:password request\n\nOTP: {otp}: "
    with smtplib.SMTP_SSL("smtp.gmail.com") as connection:
        # connection.starttls()
        connection.login(own_email, own_password)
        connection.sendmail(from_addr='Free Lunch', to_addrs=email, msg=email_message)
