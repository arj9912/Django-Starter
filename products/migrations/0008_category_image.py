# Generated by Django 5.0.2 on 2024-02-26 16:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0007_order_orderitem'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='image',
            field=models.ImageField(default=1, upload_to='images/category'),
            preserve_default=False,
        ),
    ]