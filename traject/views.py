# traject/views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Trajet, JournalELD
from django.utils import timezone
import json

@csrf_exempt
def create_trajet(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            trajet = Trajet(
                emplacement_actuel=data['emplacement_actuel'],
                lieu_prise_en_charge=data['lieu_prise_en_charge'],
                lieu_depot=data['lieu_depot'],
                cycle_actuel=int(data['cycle_actuel']),
            )
            trajet.save()
            return JsonResponse({'id': str(trajet.id), 'message': 'Trajet créé avec succès'}, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Méthode non autorisée'}, status=405)

@csrf_exempt
def start_trajet(request, trajet_id):
    if request.method == 'POST':
        try:
            trajet = Trajet.objects.get(id=trajet_id)
            journal, created = JournalELD.objects.get_or_create(
                trajet=trajet,
                defaults={'heure_debut': timezone.now()}  # Définir heure_debut lors de la création
            )
            if not created and not journal.heure_debut:
                journal.heure_debut = timezone.now()
                journal.save()
            return JsonResponse({'message': 'Heure de début enregistrée'}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Méthode non autorisée'}, status=405)
@csrf_exempt
def end_trajet(request, trajet_id):
    if request.method == 'POST':
        try:
            trajet = Trajet.objects.get(id=trajet_id)
            journal = JournalELD.objects.get(trajet=trajet)
            journal.heure_fin = timezone.now()
            journal.heures_conduite = (journal.heure_fin - journal.heure_debut).total_seconds() / 3600
            journal.save()
            return JsonResponse({'message': 'Heure de fin enregistrée'}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Méthode non autorisée'}, status=405)

@csrf_exempt
def pause_trajet(request, trajet_id):
    if request.method == 'POST':
        try:
            trajet = Trajet.objects.get(id=trajet_id)
            journal = JournalELD.objects.get(trajet=trajet)
            if not journal.pause_start:  # Assurez-vous que pause_start est défini dans votre modèle
                journal.pause_start = timezone.now()
                journal.save()
                return JsonResponse({'message': 'Pause démarrée'}, status=200)
            else:
                return JsonResponse({'error': 'Pause déjà en cours'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Méthode non autorisée'}, status=405)
@csrf_exempt
def resume_trajet(request, trajet_id):
    if request.method == 'POST':
        try:
            trajet = Trajet.objects.get(id=trajet_id)
            journal = JournalELD.objects.get(trajet=trajet)
            if journal.pause_start:  # Assurez-vous que pause_start est défini dans votre modèle
                pause_end = timezone.now()
                pause_duration = (pause_end - journal.pause_start).total_seconds() / 3600
                journal.duree_pause += pause_duration
                journal.pause_start = None  # Réinitialiser pause_start
                journal.save()
                return JsonResponse({'message': 'Pause terminée'}, status=200)
            else:
                return JsonResponse({'error': 'Aucune pause en cours'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Méthode non autorisée'}, status=405)