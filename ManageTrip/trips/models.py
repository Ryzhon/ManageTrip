import uuid as uuid_lib

from django.conf import settings
from django.db import models
from django.db.models.fields.related import OneToOneField

from core.models import TimeStampedModel
from users.models import CustomUser



class Trip(TimeStampedModel):
    uuid = models.UUIDField(default=uuid_lib.uuid4, editable=False)
    content = models.CharField(max_length=240)
    slug = models.SlugField(max_length=255, unique=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="trips"
    )
    def __str__(self):
        return self.content




class Todo(TimeStampedModel):
    uuid = models.UUIDField(db_index=True, default=uuid_lib.uuid4, editable=False)
    body = models.TextField()
    trip = models.ForeignKey(
        Trip, on_delete=models.CASCADE, related_name="todo"
    )
    From = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="From",default="",primary_key=False)
    To = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="to", db_index=False)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="author")
    voters = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="votes")
    charge = models.IntegerField()




    def __str__(self):
        return self.author.username



# class CalcUser(TimeStampedModel):
#     From = OneToOneField(CustomUser,on_delete=models.CASCADE, related_name="From")
#     To = OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="To")
#     charge = models.IntegerField()

