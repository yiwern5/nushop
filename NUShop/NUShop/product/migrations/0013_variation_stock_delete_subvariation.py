# Generated by Django 4.2.1 on 2023-12-27 14:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0012_merge_20230721_0031'),
    ]

    operations = [
        migrations.AddField(
            model_name='variation',
            name='stock',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.DeleteModel(
            name='Subvariation',
        ),
    ]
