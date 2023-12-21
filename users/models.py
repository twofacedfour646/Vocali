from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    avatar = models.TextField()
    bio = models.TextField()
    banner = models.TextField()

    isCreator = models.BooleanField()
    activated = models.BooleanField()

    earnings = models.FloatField()
    price = models.FloatField()


class Review(models.Model):
    body = models.TextField()

    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_reviews")
    receiver = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="received_reviews")

    rating = models.IntegerField()
    datePosted = models.DateField(null=True)
