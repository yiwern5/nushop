# Generated by Django 4.2.1 on 2024-01-09 16:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0014_rename_type_variation_option'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='variation_bool',
            field=models.BooleanField(default=False),
        ),
    ]
