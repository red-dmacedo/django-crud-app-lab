from django.shortcuts import render
from .models import Cola

# Create your views here.
def home(request):
    return render(request, 'home.html')

def cola_index(request):
    cola = Cola.objects.all()
    # return render(<req>, <view>, <Object>)
    return render(request, 'cola/index.html', {'cola': cola})

def cola_detail(request, cola_id):
    cola = Cola.objects.get(id=cola_id)
    return render(request, 'cola/detail.html', {'cola': cola})
