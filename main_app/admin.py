from django.contrib import admin
from .models import Cola, Ingredient, ColaIngredient

# Register your models here.
admin.site.register(Cola)
admin.site.register(Ingredient)
admin.site.register(ColaIngredient)
