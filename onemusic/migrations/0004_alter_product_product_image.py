# Generated by Django 4.2.1 on 2023-05-16 07:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('onemusic', '0003_alter_product_product_price_alter_user_mobile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='product_image',
            field=models.ImageField(upload_to='images/'),
        ),
    ]
