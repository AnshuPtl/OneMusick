# Generated by Django 4.2.1 on 2023-05-05 18:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('onemusic', '0002_remove_user_address'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='product_price',
            field=models.BigIntegerField(),
        ),
        migrations.AlterField(
            model_name='user',
            name='mobile',
            field=models.BigIntegerField(),
        ),
    ]
