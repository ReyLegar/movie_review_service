from django.db import models

class Review(models.Model):
    text = models.TextField()
    rating = models.IntegerField()
    emotion = models.TextField()