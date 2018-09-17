from django.db import models


class Clover(models.Model):
    access_token = models.CharField(max_length=200)
    achieved = models.DateTimeField(auto_now_add=True)
