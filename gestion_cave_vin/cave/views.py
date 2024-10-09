# cave/views.py

from django.shortcuts import render, redirect, get_object_or_404
from .models import Cave, Bouteille
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm

def accueil(request):
    return render(request, 'cave/accueil.html')

@login_required
def liste_caves(request):
    caves = Cave.objects.filter(user=request.user)
    return render(request, 'cave/liste_caves.html', {'caves': caves})

@login_required
def creer_cave(request):
    if request.method == 'POST':
        nom_cave = request.POST['name']
        Cave.objects.create(user=request.user, name=nom_cave)
        return redirect('liste_caves')
    return render(request, 'cave/creer_cave.html')

@login_required
def liste_bouteilles(request, cave_id):
    cave = get_object_or_404(Cave, id=cave_id, user=request.user)
    bouteilles = Bouteille.objects.filter(etagere__cave=cave, archive=False)
    tri = request.GET.get('tri', None)
    if tri:
        bouteilles = bouteilles.order_by(tri)
    return render(request, 'cave/liste_bouteilles.html', {'bouteilles': bouteilles, 'cave': cave})

@login_required
def ajouter_bouteille(request, cave_id):
    cave = get_object_or_404(Cave, id=cave_id, user=request.user)
    if request.method == 'POST':
        # Logique pour ajouter une nouvelle bouteille
        domaine = request.POST['domaine']
        nom = request.POST['nom']
        type_vin = request.POST['type']
        annee = request.POST['annee']
        region = request.POST['region']
        prix = request.POST['prix']
        Bouteille.objects.create(
            domaine_viticole=domaine,
            nom=nom,
            type=type_vin,
            annee=annee,
            region=region,
            prix=prix,
            etagere=cave.etagere_set.first()
        )
        return redirect('liste_bouteilles', cave_id=cave.id)
    return render(request, 'cave/ajouter_bouteille.html', {'cave': cave})

@login_required
def noter_bouteille(request, bouteille_id):
    bouteille = get_object_or_404(Bouteille, id=bouteille_id)
    if request.method == 'POST':
        nouvelle_note = int(request.POST['note'])
        bouteille.ajouter_note_communautaire(nouvelle_note)
        bouteille.save()
        return redirect('liste_bouteilles', cave_id=bouteille.etagere.cave.id)
    return render(request, 'cave/noter_bouteille.html', {'bouteille': bouteille})

@login_required
def archiver_bouteille(request, bouteille_id):
    bouteille = get_object_or_404(Bouteille, id=bouteille_id)
    bouteille.archive = True
    bouteille.save()
    return redirect('liste_bouteilles', cave_id=bouteille.etagere.cave.id)

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('accueil')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})
