# Generated by Django 4.2.1 on 2023-07-07 07:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartproduct',
            name='variation',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
