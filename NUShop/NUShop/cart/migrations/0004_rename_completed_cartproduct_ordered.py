# Generated by Django 4.2.1 on 2023-06-06 10:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0003_rename_ordered_cartproduct_completed'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cartproduct',
            old_name='completed',
            new_name='ordered',
        ),
    ]
