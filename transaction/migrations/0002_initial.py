# Generated by Django 4.2.5 on 2023-09-20 12:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('transaction', '0001_initial'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='withdrawals',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.users'),
        ),
        migrations.AddField(
            model_name='lunches',
            name='reciever_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lunch_reciever', to='users.users'),
        ),
        migrations.AddField(
            model_name='lunches',
            name='sender_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lunch_sender', to='users.users'),
        ),
    ]
