# Generated by Django 4.2.1 on 2023-07-06 13:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authuser', '0006_userotp_otp'),
    ]

    operations = [
        migrations.DeleteModel(
            name='UserOTP',
        ),
    ]