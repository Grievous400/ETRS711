from django.db import models
from django.contrib.auth.models import AbstractUser

class Utilisateur(AbstractUser):
    telephone = models.CharField(max_length=15, blank=True, null=True)
    adresse = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.username

class Cave(models.Model):
    user = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

class Etagere(models.Model):
    cave = models.ForeignKey(Cave, on_delete=models.CASCADE)
    numero_etagere = models.IntegerField()
    nombre_emplacements = models.IntegerField()
    nombre_bouteilles = models.IntegerField()

class Bouteille(models.Model):
    domaine_viticole = models.CharField(max_length=100)
    nom = models.CharField(max_length=100)
    type = models.CharField(max_length=50)
    annee = models.IntegerField()
    region = models.CharField(max_length=100)
    commentaires = models.TextField(blank=True, null=True)
    note_personnelle = models.IntegerField(blank=True, null=True)
    note_communaute = models.FloatField(blank=True, null=True)
    photo_etiquette = models.ImageField(upload_to='etiquettes/', blank=True, null=True)
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    etagere = models.ForeignKey(Etagere, on_delete=models.CASCADE)
    archive = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.nom} ({self.annee})"

    def ajouter_note_communautaire(self, nouvelle_note):
        if self.note_communaute is None:
            self.note_communaute = nouvelle_note
        else:
            self.note_communaute = (self.note_communaute + nouvelle_note) / 2
