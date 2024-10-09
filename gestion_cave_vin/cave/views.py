from django.shortcuts import render, redirect, get_object_or_404
from .models import Cave, Bouteille
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def liste_bouteilles(request, cave_id):
    cave = get_object_or_404(Cave, id=cave_id, user=request.user)
    bouteilles = cave.bouteille_set.filter(archive=False)
    tri = request.GET.get('tri', None)
    if tri:
        bouteilles = bouteilles.order_by(tri)
    return render(request, 'cave/liste_bouteilles.html', {'bouteilles': bouteilles, 'cave': cave})

@login_required
def ajouter_bouteille(request, cave_id):
    cave = get_object_or_404(Cave, id=cave_id, user=request.user)
    if request.method == 'POST':
        # Ajouter une nouvelle bouteille
        bouteille = Bouteille.objects.create(
            etagere=cave.etagere_set.first(),  # ou tout autre logique pour assigner une étagère
            domaine_viticole=request.POST['domaine'],
            nom=request.POST['nom'],
            type=request.POST['type'],
            annee=request.POST['annee'],
            region=request.POST['region'],
            prix=request.POST['prix']
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
