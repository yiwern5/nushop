# Generated by Django 4.2.1 on 2024-01-09 16:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authuser', '0011_remove_bank_otp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='role',
            name='name',
            field=models.CharField(default='unverified', max_length=50),
        ),
    ]
