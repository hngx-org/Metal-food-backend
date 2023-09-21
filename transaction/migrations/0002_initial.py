# Generated by Django 4.2.5 on 2023-09-20 23:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('transaction', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='withdrawals',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='lunches',
            name='reciever_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lunch_reciever', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='lunches',
            name='sender_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lunch_sender', to=settings.AUTH_USER_MODEL),
        ),
    ]
