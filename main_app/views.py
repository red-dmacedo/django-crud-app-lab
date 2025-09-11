from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Cola

# Create your views here.
def home(request):
    return render(request, 'home.html')

class ColaIndex(ListView):
    model = Cola

class ColaDetail(DetailView):
    model = Cola

class ColaCreate(CreateView):
    model = Cola
    fields = '__all__'

class ColaUpdate(UpdateView):
    model = Cola
    fields = '__all__'

class ColaDelete(DeleteView):
    model = Cola
    success_url = '/colas/'
