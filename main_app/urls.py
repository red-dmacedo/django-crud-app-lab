from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('colas/', views.ColaIndex.as_view(), name='cola-index'),
    path('colas/create/', views.ColaCreate.as_view(), name='cola-create'),
    path('colas/<int:pk>/', views.ColaDetail.as_view(), name='cola-detail'),
    path('colas/<int:pk>/update/', views.ColaUpdate.as_view(), name='cola-update'),
    path('colas/<int:pk>/delete/', views.ColaDelete.as_view(), name='cola-delete'),
    path(
        'colas/<int:cola_id>/cola-ingredients/<int:cola_ingredient_id>/increment/',
        views.IncrementColaIngredient,
        name='cola-ingredient-increment'
    ),
    path(
        'colas/<int:cola_id>/cola-ingredients/<int:cola_ingredient_id>/decrement/',
        views.DecrementColaIngredient,
        name='cola-ingredient-decrement'
    ),
    path(
        'colas/<int:cola_id>/cola-ingredients/<int:cola_ingredient_id>/delete/',
        views.ColaIngredientDelete,
        name='cola-ingredient-delete'
    ),
    path('accounts/signup/', views.signup, name='signup'),
]
