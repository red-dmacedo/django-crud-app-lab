from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('colas/', views.cola_index, name='cola-index'),
    # path('colas/<int:cat_id>/', views.cola_detail, name='cola-detail'),
]
