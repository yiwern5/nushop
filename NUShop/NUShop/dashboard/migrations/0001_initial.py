# Generated by Django 4.2.1 on 2023-06-08 08:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name_plural': 'Categories',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lastname', models.CharField(max_length=255)),
                ('address1', models.TextField(blank=True, null=True)),
                ('address2', models.FloatField()),
                ('blocknumber', models.ImageField(blank=True, null=True, upload_to='product_images')),
                ('zipcode', models.BooleanField(default=False)),
                ('contactnumber', models.TextField(blank=True, null=True)),
                ('email', models.TextField(blank=True, null=True)),
                ('firstname', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='dashboard.category')),
            ],
        ),
    ]