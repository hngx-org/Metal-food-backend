# Generated by Django 4.2.5 on 2023-09-21 14:21

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Lunch',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('quantity', models.IntegerField()),
                ('redeemed', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('note', models.TextField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Withdrawals',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('status', models.CharField(max_length=30)),
                ('amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('created_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
