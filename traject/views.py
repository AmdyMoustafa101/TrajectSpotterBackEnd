# traject/views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Trajet
import json

@csrf_exempt
def create_trajet(request):
    if request.method == 'POST':
        try:
            # Récupérer les données du corps de la requête
            data = json.loads(request.body)
            
            # Valider les données
            if not all(key in data for key in ['emplacement_actuel', 'lieu_prise_en_charge', 'lieu_depot', 'cycle_actuel']):
                return JsonResponse({'error': 'Données manquantes'}, status=400)
            
            # Créer un nouvel objet Trajet
            trajet = Trajet(
                emplacement_actuel=data['emplacement_actuel'],
                lieu_prise_en_charge=data['lieu_prise_en_charge'],
                lieu_depot=data['lieu_depot'],
                cycle_actuel=int(data['cycle_actuel']),  # Convertir en entier
            )
            
            # Sauvegarder l'objet dans la base de données
            trajet.save()
            
            # Retourner une réponse JSON avec l'ID du trajet créé
            return JsonResponse({
                'id': str(trajet.id),  # Convertir ObjectId en chaîne
                'message': 'Trajet créé avec succès',
            }, status=201)
        
        except Exception as e:
            # En cas d'erreur, retourner un message d'erreur
            return JsonResponse({
                'error': str(e),
            }, status=400)
    
    # Si la méthode HTTP n'est pas POST, retourner une erreur
    return JsonResponse({
        'error': 'Méthode non autorisée',
    }, status=405)