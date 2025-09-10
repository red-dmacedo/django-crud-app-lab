from django.db import models

# Create your models here.
class Cola(models.Model):
    name = models.CharField(max_length=100)
    brand = models.CharField(max_length=100)
    image_url = models.TextField(max_length=255)
    fizz_rating = models.IntegerField()

    def __str__(self):
        return self.name
