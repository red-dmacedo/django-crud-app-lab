from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
# from django.urls import reverse
from .models import Cola, Ingredient, ColaIngredient
from .forms import ColaIngredientForm, IngredientForm

# Create your views here.


def home(request):
    return render(request, 'home.html')


class ColaIndex(ListView):
    model = Cola


class ColaDetail(DetailView):
    model = Cola
    template_name = "main_app/cola_detail.html"
    context_object_name = "cola"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cola = Cola.objects.get(id=self.kwargs["pk"])
        cola_ingredients = ColaIngredient.objects.filter(cola=cola)
        context["cola_ingredients"] = cola_ingredients
        context["ingredients"] = Ingredient.objects.all()
        context["cola_ingredient_form"] = ColaIngredientForm()
        context["ingredient_form"] = IngredientForm()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        if "attach_ingredient" in request.POST:
            form = ColaIngredientForm(request.POST)

            def ingr_exists(ingr):
                try:
                    cola_ingr = ColaIngredient.objects.get(
                        cola=self.object, ingredient=ingr)
                    if cola_ingr:
                        return True
                    else:
                        return False
                except:
                    return False

            if form.is_valid():
                cola_ingr = form.save(commit=False)
                cola_ingr.cola = self.object   # attach cola automatically
                if ingr_exists(cola_ingr.ingredient):
                    old_cola = ColaIngredient.objects.get(
                        cola=self.object, ingredient=cola_ingr.ingredient)
                    old_cola.quantity += cola_ingr.quantity
                    old_cola.save()
                    return redirect("cola-detail", pk=self.object.pk)
                else:
                    cola_ingr.save()
                    return redirect("cola-detail", pk=self.object.pk)
            return self.render_to_response(self.get_context_data(cola_ingredient_form=form))
        elif "create_ingredient" in request.POST:
            form = IngredientForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect("cola-detail", pk=self.object.pk)
            return self.render_to_response(self.get_context_data(ingredient_form=form))
        return self.render_to_response(self.get_context_data())


class ColaCreate(CreateView):
    model = Cola
    fields = '__all__'


class ColaUpdate(UpdateView):
    model = Cola
    fields = '__all__'


class ColaDelete(DeleteView):
    model = Cola
    success_url = '/colas/'


class IngrCreate(CreateView):
    model = Ingredient


class IngrDelete(DeleteView):
    model = Ingredient


class ColaIngredientCreate(CreateView):
    model = ColaIngredient
    fields = ["ingredient", "quantity"]
