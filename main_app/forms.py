from django import forms
from .models import ColaIngredient, Ingredient


class ColaIngredientForm(forms.ModelForm):
    class Meta:
        model = ColaIngredient
        fields = ['ingredient', 'quantity']
        widgets = {
            'quantity': forms.NumberInput
        }


class IngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = '__all__'
        widgets = {
            'name': forms.TextInput
        }
