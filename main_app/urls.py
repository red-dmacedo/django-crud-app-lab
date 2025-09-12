from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    # path('colas/', views.cola_index, name='cola-index'),
    path('colas/', views.ColaIndex.as_view(), name='cola-index'),
    path('colas/create/', views.ColaCreate.as_view(), name='cola-create'),
    path('colas/<int:pk>/', views.ColaDetail.as_view(), name='cola-detail'),
    path('colas/<int:pk>/update/', views.ColaUpdate.as_view(), name='cola-update'),
    path('colas/<int:pk>/delete/', views.ColaDelete.as_view(), name='cola-delete'),
    path(
        'colas/<int:cola_id>/add-ingredient/<int:ingredient_id>/',
        views.ColaIngredientCreate.as_view(),
        name='add-ingredient'
    ),
    path(
        'colas/<int:cola_id>/remove-ingredient/<int:ingredient_id>/',
        views.RemoveIngrFromCola,
        name='remove-ingredient'
    ),
]
