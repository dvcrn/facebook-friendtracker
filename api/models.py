from django.db import models
from djangotoolbox.fields import DictField, ListField


# Create your models here.
class Person(models.Model):
    facebook_id = models.CharField(max_length=20)
    friends = DictField()
    history = DictField()

    lost_friends = DictField()
    new_friends = DictField()

    access_token = models.TextField(default='')
    access_token_expires_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)