from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView,TemplateView
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
        # try:
        cola = Cola.objects.get(id=self.kwargs["pk"])
        cola_ingredients = ColaIngredient.objects.filter(cola=cola)
        context["cola_ingredients"] = cola_ingredients
        # except:
            # context["cola_ingredients"] = {}
        context["ingredients"] = Ingredient.objects.all()
        context["cola_ingredient_form"] = ColaIngredientForm()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = ColaIngredientForm(request.POST)
        def ingr_exists(ingr):
            try:
                cola_ingr = ColaIngredient.objects.get(cola=self.object, ingredient=ingr)
                if cola_ingr:
                    return True
                else:
                    return False
            except:
                return False
        
        if form.is_valid():
            cola_ingr = form.save(commit=False)
            cola_ingr.cola = self.object   # attach cola automatically
            print(f'cola_ingr.ingredient: {cola_ingr.ingredient}')
            if ingr_exists(cola_ingr.ingredient):
                old_cola = ColaIngredient.objects.get(cola=self.object, ingredient=cola_ingr.ingredient)
                old_cola.quantity += cola_ingr.quantity
                old_cola.save()
                return redirect("cola-detail", pk=self.object.pk)
            else:
                cola_ingr.save()
                return redirect("cola-detail", pk=self.object.pk)
        return self.render_to_response(self.get_context_data(form=form))


# class ColaDetail(TemplateView):
#     template_name = "main_app/cola_detail.html"
#     # model = Cola
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         cola = get_object_or_404(Cola, pk=self.kwargs["pk"])
#         try:
#             cola_ingredients = ColaIngredient.objects.get(cola=self.kwargs["pk"])
#             context["cola_ingredients"] = cola_ingredients
#         except:
#             context["cola_ingredients"] = {}
#         context["cola"] = cola
#         context["ingredients"] = Ingredient.objects.all()
#         context["cola_ingredient_form"] = ColaIngredientForm()
#         return context

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

def AddIngrToCola(request, cola_id, ingredient_id):
    cola = Cola.objects.get(id=cola_id)
    ingredient = Ingredient.objects.get(id=ingredient_id)
    cola.add_ingredient(ingredient, 0)
    print('string')
    return redirect('cola-detail', pk=cola_id)

def RemoveIngrFromCola(request, cola_id, ingredient):
    cola = Cola.objects.get(id=cola_id)
    cola.remove_ingredient(ingredient)
    return redirect('cola-detail', cola_id=cola_id)
