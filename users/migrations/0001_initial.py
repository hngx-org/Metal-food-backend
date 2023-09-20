<<<<<<< HEAD
# Generated by Django 4.2.5 on 2023-09-20 22:50
=======
# Generated by Django 4.2.5 on 2023-09-20 23:24
>>>>>>> c1862153d985ee44d31c2ae4c09fefcca1d8ec02

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('lunch_price', models.DecimalField(decimal_places=2, default=1000.0, max_digits=10)),
                ('currency', models.CharField(default='NGN', max_length=3)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='OrganizationLunchWallet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('balance', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('org_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.organization')),
            ],
        ),
        migrations.CreateModel(
            name='OrganizationInvites',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('token', models.CharField(blank=True, max_length=100, null=True)),
                ('TTL', models.DateTimeField(default=datetime.datetime(2023, 9, 21, 23, 24, 54, 416120, tzinfo=datetime.timezone.utc))),
                ('org_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='company', to='users.organization')),
            ],
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('username', models.CharField(max_length=100, unique=True)),
                ('password', models.CharField(max_length=255)),
                ('phone_number', models.CharField(max_length=15)),
                ('profile_picture', models.ImageField(null=True, upload_to='profile_image/')),
                ('refresh_token', models.CharField(max_length=255, null=True)),
                ('bank_number', models.CharField(max_length=20, null=True)),
                ('bank_code', models.CharField(max_length=30, null=True)),
                ('bank_name', models.CharField(max_length=30, null=True)),
                ('bank_region', models.CharField(max_length=255, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('lunch_credit_balance', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('currency', models.CharField(max_length=255, null=True)),
                ('currency_code', models.CharField(max_length=10, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, related_name='customuser_set', to='auth.group')),
                ('org', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.organization')),
                ('user_permissions', models.ManyToManyField(blank=True, related_name='customuser_set', to='auth.permission')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
