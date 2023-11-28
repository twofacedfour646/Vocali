from django.db import models
from django.contrib.auth.models import User
from users.models import Profile

# Create your models here.
class VocalRequest(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_requests")
    receiver = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="received_reqeusts")

    body = models.TextField()
    datePosted = models.DateField()

    def __str__(self) -> str:
        return super().__str__()
