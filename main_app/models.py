from django.db import models
from django.urls import reverse
from django.contrib.postgres.fields import ArrayField

# Create your models here.


class Ingredient(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("ingredient-detail", kwargs={"pk": self.id})


class Cola(models.Model):
    name = models.CharField(max_length=100)
    brand = models.CharField(max_length=100)
    image_url = models.TextField(max_length=255, blank=True)
    fizz_rating = models.IntegerField()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("cola-detail", kwargs={"pk": self.id})

    def add_ingredient(self, ingredient, quantity):
        item, created = ColaIngredient.objects.get_or_create(
            cola=self,
            ingredient=ingredient,
            defaults={'quantity': quantity}
        )
        if not created:
            item.quantity += quantity
            item.save()
        return item

    def remove_ingredient(self, ingredient):
        ColaIngredient.objects.filter(
            cola=self,
            ingredient=ingredient
        ).delete()


# I asked chatGPT: Write a django model where the property is an array of objects with foreign keys and quantity
# It responded: In Django, you don’t store arrays of objects directly (like in MongoDB). Instead, you use a related model with ForeignKey or ManyToManyField through a "join model."
# I believe this is the join model that will give me the functionality I wanted.
class ColaIngredient(models.Model):
    cola = models.ForeignKey(
        Cola,
        related_name="ingredients",
        on_delete=models.CASCADE
    )
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.PositiveBigIntegerField(default=0)

    class Meta:
        # Prevent duplicate product entries
        unique_together = ("cola", "ingredient")

    def __str__(self):
        return f"{self.ingredient.name} x{self.quantity}"
