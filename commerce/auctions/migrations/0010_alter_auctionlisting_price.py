# Generated by Django 4.1.5 on 2023-01-20 10:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0009_bid_alter_auctionlisting_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auctionlisting',
            name='price',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='bid_amount', to='auctions.bid'),
        ),
    ]