# Generated by Django 4.2.5 on 2023-09-20 10:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_users_bank_code_users_bank_name_users_bank_number_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='organizationinvites',
            name='id',
        ),
        migrations.RemoveField(
            model_name='organizationlunchwallet',
            name='org_id',
        ),
        migrations.RemoveField(
            model_name='withdrawals',
            name='user_id',
        ),
        migrations.DeleteModel(
            name='Lunches',
        ),
        migrations.DeleteModel(
            name='Organization',
        ),
        migrations.DeleteModel(
            name='OrganizationInvites',
        ),
        migrations.DeleteModel(
            name='OrganizationLunchWallet',
        ),
        migrations.DeleteModel(
            name='Withdrawals',
        ),
    ]
