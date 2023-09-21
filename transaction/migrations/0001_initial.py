# Generated by Django 4.2.4 on 2023-09-20 11:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Withdrawals',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('status', models.CharField(max_length=30)),
                ('amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.users')),
            ],
        ),
        migrations.CreateModel(
            name='Lunches',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('quantity', models.IntegerField()),
                ('redeemed', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('note', models.TextField(null=True)),
                ('reciever_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lunch_reciever', to='users.users')),
                ('sender_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lunch_sender', to='users.users')),
            ],
        ),
    ]
