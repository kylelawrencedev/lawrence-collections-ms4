# Generated by Django 3.2.8 on 2021-10-26 21:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
        ('profiles', '0003_alter_userprofile_wishlists'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='wishlists',
            field=models.ManyToManyField(to='products.Product'),
        ),
    ]
