from django.db import models


# Create your models here.
class Review(models.Model):
    text = models.TextField()
    rating = models.FloatField()
    status = models.CharField(max_length=20)

    def __str__(self):
        return f"Review: {self.text[:50]} - Rating: {self.rating} - Status: {self.status}"