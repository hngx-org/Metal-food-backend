# Generated by Django 4.2.5 on 2023-09-20 14:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_rename_org_id_users_org_users_username_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='currency',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='users',
            name='currency_code',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='users',
            name='lunch_credit_balance',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
    ]
