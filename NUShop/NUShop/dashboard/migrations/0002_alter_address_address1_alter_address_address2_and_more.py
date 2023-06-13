# Generated by Django 4.2.1 on 2023-06-08 08:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='address1',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='address',
            name='address2',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='address',
            name='blocknumber',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='address',
            name='contactnumber',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='address',
            name='email',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='address',
            name='firstname',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='address',
            name='zipcode',
            field=models.IntegerField(),
        ),
        migrations.DeleteModel(
            name='Category',
        ),
    ]