# Generated by Django 4.1.5 on 2023-01-22 16:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0010_alter_auctionlisting_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='brand',
            name='image_url',
            field=models.CharField(default='No image.', max_length=300),
        ),
        migrations.AlterField(
            model_name='auctionlisting',
            name='image_url',
            field=models.CharField(default='No image.', max_length=300),
        ),
    ]
