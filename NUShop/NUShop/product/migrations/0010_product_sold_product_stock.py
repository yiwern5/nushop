# Generated by Django 4.2.1 on 2023-07-17 13:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0009_merge_20230709_1828'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='sold',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='stock',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]