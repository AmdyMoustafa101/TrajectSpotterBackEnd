# traject/models.py
from djongo import models
from django.db.models import Sum
from datetime import timedelta
from django.utils import timezone

class Trajet(models.Model):
    emplacement_actuel = models.CharField(max_length=255)
    lieu_prise_en_charge = models.CharField(max_length=255)
    lieu_depot = models.CharField(max_length=255)
    cycle_actuel = models.IntegerField()
    distance_parcourue = models.FloatField(default=0)  # Distance parcourue en miles

    def __str__(self):
        return f"Trajet from {self.emplacement_actuel} to {self.lieu_depot}"

class JournalELD(models.Model):
    trajet = models.ForeignKey(Trajet, on_delete=models.CASCADE)
    heure_debut = models.DateTimeField()
    heure_fin = models.DateTimeField(null=True, blank=True)
    duree_pause = models.IntegerField(default=0)
    heures_conduite = models.FloatField(default=0)
    pause_start = models.DateTimeField(null=True, blank=True)  # Ajouter ce champ

    def __str__(self):
        return f"Journal for {self.trajet}"