# Generated by Django 4.2.1 on 2023-07-02 09:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0003_rename_product_orderproduct_cart_product_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderproduct',
            name='thumbnail',
            field=models.ImageField(upload_to='orderproduct_images'),
        ),
    ]