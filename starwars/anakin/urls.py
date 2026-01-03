from django.urls import path
from . import  views

urlpatterns = [
    path('', views.anakin_view, name='home'),
    path('anakin/', views.anakin_view, name='anakin'),
    path('api/starwars/', views.starwars_api, name='starwars_api'),
    path('people/', views.people_list, name='people_list'),
    path('people/<int:pk>/', views.people_detail, name='people_detail'),
    path('films/', views.films_api, name='films_api'),
    path('films/<int:pk>/', views.films_detail, name='films_detail'),
    path('films/', views.films_list, name='fimls_list'),
    ] 