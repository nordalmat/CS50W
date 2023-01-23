from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Brand(models.Model):
    name = models.CharField(max_length=64)
    image_url = models.CharField(max_length=300, default='No image.')

    def __str__(self):
        return self.name


class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='user_bid')
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return str(self.amount)


class AuctionListing(models.Model):
    title = models.CharField(max_length=64)
    price = models.ForeignKey(Bid, on_delete=models.CASCADE, blank=True, null=True, related_name='bid_amount')
    image_url = models.CharField(max_length=300, default='No image.')
    description = models.CharField(max_length=1000, default='No description.')
    created = models.DateField(auto_now_add=True)
    isActive = models.BooleanField(default=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='user')
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, blank=True, null=True, related_name='category')
    watchlist = models.ManyToManyField(User, blank=True, null=True, related_name='itemlist')

    def __str__(self):
        return self.title.title()


class Comment(models.Model):
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, blank=True, null=True, related_name='listing_com')
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='user_com')
    content = models.CharField(max_length=300)
    created = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.author} commented on {self.listing}"
