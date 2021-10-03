from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    pass

    def __str__(self):
        return self.username

    

class auction_listing(models.Model):
    Title=models.CharField(max_length=100)
    Description=models.CharField(max_length=1000,null=True,default="")
    date_time=models.DateTimeField(auto_now_add = True)
    Url=models.URLField(blank=True)
    Tag=models.CharField(max_length=50)
    author=models.ForeignKey(User,on_delete=models.CASCADE,related_name="auction")
    starting_bid=models.DecimalField(max_digits=10,decimal_places=2)
    active=models.BooleanField(default=True)




    def __str__(self):
        return self.Title


class  bids(models.Model):
    date_time=models.DateTimeField(auto_now_add = True)
    listing=models.ForeignKey(auction_listing,on_delete=models.CASCADE,related_name="bids")
    amount=models.DecimalField(max_digits=10,decimal_places=2)
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="user")

    def __str__(self):
        return self.amount


class comments(models.Model):
    comment=models.CharField(max_length=1000)
    author=models.ForeignKey(User,on_delete=models.CASCADE,related_name="author")
    listing=models.ForeignKey(auction_listing,on_delete=models.CASCADE,related_name="comment")
    date_time=models.DateTimeField(auto_now_add = True)



    def __str__(self):
        return self.comment


