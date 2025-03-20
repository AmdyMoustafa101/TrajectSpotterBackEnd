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
                defaults={'heure_debut': timezone.now()}
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
def start_sleep(request, trajet_id):
    if request.method == 'POST':
        try:
            trajet = Trajet.objects.get(id=trajet_id)
            journal = JournalELD.objects.get(trajet=trajet)
            if not journal.sleep_start:
                journal.sleep_start = timezone.now()
                journal.save()
                return JsonResponse({'message': 'Début de sommeil enregistré'}, status=200)
            else:
                return JsonResponse({'error': 'Sommeil déjà en cours'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Méthode non autorisée'}, status=405)

@csrf_exempt
def end_sleep(request, trajet_id):
    if request.method == 'POST':
        try:
            trajet = Trajet.objects.get(id=trajet_id)
            journal = JournalELD.objects.get(trajet=trajet)
            if journal.sleep_start:
                journal.sleep_end = timezone.now()
                journal.sleep_duration = (journal.sleep_end - journal.sleep_start).total_seconds() / 3600
                journal.save()
                return JsonResponse({'message': 'Fin de sommeil enregistrée'}, status=200)
            else:
                return JsonResponse({'error': 'Aucun sommeil en cours'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Méthode non autorisée'}, status=405)

@csrf_exempt
def start_onduty(request, trajet_id):
    if request.method == 'POST':
        try:
            trajet = Trajet.objects.get(id=trajet_id)
            journal = JournalELD.objects.get(trajet=trajet)
            if not journal.onduty_start:
                journal.onduty_start = timezone.now()
                journal.save()
                return JsonResponse({'message': 'Début de service enregistré'}, status=200)
            else:
                return JsonResponse({'error': 'Service déjà en cours'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Méthode non autorisée'}, status=405)

@csrf_exempt
def end_onduty(request, trajet_id):
    if request.method == 'POST':
        try:
            trajet = Trajet.objects.get(id=trajet_id)
            journal = JournalELD.objects.get(trajet=trajet)
            if journal.onduty_start:
                journal.onduty_end = timezone.now()
                journal.onduty_duration = (journal.onduty_end - journal.onduty_start).total_seconds() / 3600
                journal.save()
                return JsonResponse({'message': 'Fin de service enregistrée'}, status=200)
            else:
                return JsonResponse({'error': 'Aucun service en cours'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Méthode non autorisée'}, status=405)

@csrf_exempt
def start_offduty(request, trajet_id):
    if request.method == 'POST':
        try:
            trajet = Trajet.objects.get(id=trajet_id)
            journal = JournalELD.objects.get(trajet=trajet)
            if not journal.offduty_start:
                journal.offduty_start = timezone.now()
                journal.save()
                return JsonResponse({'message': 'Début de hors service enregistré'}, status=200)
            else:
                return JsonResponse({'error': 'Hors service déjà en cours'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Méthode non autorisée'}, status=405)

@csrf_exempt
def end_offduty(request, trajet_id):
    if request.method == 'POST':
        try:
            trajet = Trajet.objects.get(id=trajet_id)
            journal = JournalELD.objects.get(trajet=trajet)
            if journal.offduty_start:
                journal.offduty_end = timezone.now()
                journal.offduty_duration = (journal.offduty_end - journal.offduty_start).total_seconds() / 3600
                journal.save()
                return JsonResponse({'message': 'Fin de hors service enregistrée'}, status=200)
            else:
                return JsonResponse({'error': 'Aucun hors service en cours'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Méthode non autorisée'}, status=405)


@csrf_exempt
def get_resume(request, trajet_id):
    if request.method == 'GET':
        try:
            trajet = Trajet.objects.get(id=trajet_id)
            journal = JournalELD.objects.get(trajet=trajet)

            # Exemple de données formatées pour le graphique
            data = []

            if journal.offduty_duration > 0:
                data.append({
                    'type': 'off',
                    'start': journal.offduty_start.hour,
                    'duration': journal.offduty_duration
                })

            if journal.sleep_duration > 0:
                data.append({
                    'type': 'sleep',
                    'start': journal.sleep_start.hour,
                    'duration': journal.sleep_duration
                })

            if journal.heures_conduite > 0:
                data.append({
                    'type': 'driving',
                    'start': journal.heure_debut.hour,
                    'duration': journal.heures_conduite
                })

            if journal.onduty_duration > 0:
                data.append({
                    'type': 'on',
                    'start': journal.onduty_start.hour,
                    'duration': journal.onduty_duration
                })

            return JsonResponse(data, safe=False)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Méthode non autorisée'}, status=405)