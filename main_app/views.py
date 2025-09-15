from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Cola, Ingredient, ColaIngredient
from .forms import ColaIngredientForm, IngredientForm

# Create your views here.


class Home(LoginView):
    template_name = 'home.html'


class ColaIndex(LoginRequiredMixin, ListView):
    model = Cola
    
    def get_queryset(self):
        return Cola.objects.filter(user=self.request.user)


class ColaDetail(LoginRequiredMixin, DetailView):
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


class ColaCreate(LoginRequiredMixin, CreateView):
    model = Cola
    fields = ['name', 'brand', 'image_url', 'fizz_rating']

    def form_valid(self, form):
        # Assign the logged in user (self.request.user)
        form.instance.user = self.request.user  # form.instance is the cat
        # Let the CreateView do its job as usual
        return super().form_valid(form)


class ColaUpdate(LoginRequiredMixin, UpdateView):
    model = Cola
    fields = ['name', 'brand', 'image_url', 'fizz_rating']


class ColaDelete(LoginRequiredMixin, DeleteView):
    model = Cola
    success_url = '/colas/'


class IngrCreate(LoginRequiredMixin, CreateView):
    model = Ingredient


class IngrDelete(LoginRequiredMixin, DeleteView):
    model = Ingredient


class ColaIngredientCreate(LoginRequiredMixin, CreateView):
    model = ColaIngredient
    fields = ["ingredient", "quantity"]
    
# class ColaIngredientDelete(DeleteView):
#     model = ColaIngredient

@login_required
def ColaIngredientDelete(request, cola_id, cola_ingredient_id):
    ColaIngredient.objects.get(id=cola_ingredient_id).delete()
    return redirect('cola-detail', pk=cola_id)

@login_required
def IncrementColaIngredient(request, cola_id, cola_ingredient_id):
    cola_ingredient = ColaIngredient.objects.get(id=cola_ingredient_id)
    cola_ingredient.quantity += 1
    cola_ingredient.save()
    return redirect('cola-detail', pk=cola_id)

@login_required
def DecrementColaIngredient(request, cola_id, cola_ingredient_id):
    cola_ingredient = ColaIngredient.objects.get(id=cola_ingredient_id)
    if cola_ingredient.quantity != 0:
        cola_ingredient.quantity -= 1
        cola_ingredient.save()
    return redirect('cola-detail', pk=cola_id)

def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('cola-index')
        else:
            error_message = 'Invalid sign up - try again'
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'signup.html', context)