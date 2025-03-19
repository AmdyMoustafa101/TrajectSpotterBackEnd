# traject/models.py
from djongo import models

class Trajet(models.Model):
    emplacement_actuel = models.CharField(max_length=255)
    lieu_prise_en_charge = models.CharField(max_length=255)
    lieu_depot = models.CharField(max_length=255)
    cycle_actuel = models.IntegerField()

    def __str__(self):
        return f"Trajet from {self.emplacement_actuel} to {self.lieu_depot}"

class JournalELD(models.Model):
    trajet = models.ForeignKey(Trajet, on_delete=models.CASCADE)
    heure_debut = models.DateTimeField()
    heure_fin = models.DateTimeField()
    duree_pause = models.IntegerField()

    def __str__(self):
        return f"Journal for {self.trajet}"