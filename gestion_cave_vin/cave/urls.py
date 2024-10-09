from django.urls import path
from . import views

urlpatterns = [
    path('', views.accueil, name='accueil'),  # Page d'accueil
    path('caves/', views.liste_caves, name='liste_caves'),
    path('cave/creer/', views.creer_cave, name='creer_cave'),
    path('cave/<int:cave_id>/', views.liste_bouteilles, name='liste_bouteilles'),
    path('cave/<int:cave_id>/ajouter/', views.ajouter_bouteille, name='ajouter_bouteille'),
    path('bouteille/<int:bouteille_id>/noter/', views.noter_bouteille, name='noter_bouteille'),
    path('bouteille/<int:bouteille_id>/archiver/', views.archiver_bouteille, name='archiver_bouteille'),
]