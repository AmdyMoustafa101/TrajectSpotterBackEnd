from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Trip, ELDLog
from django.utils import timezone
import json

@csrf_exempt
def create_trip(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            trip = Trip(
                current_location=data['current_location'],
                pickup_location=data['pickup_location'],
                dropoff_location=data['dropoff_location'],
                current_cycle=int(data['current_cycle']),
            )
            trip.save()
            return JsonResponse({'id': str(trip.id), 'message': 'Trip created successfully'}, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def start_trip(request, trip_id):
    if request.method == 'POST':
        try:
            trip = Trip.objects.get(id=trip_id)
            log, created = ELDLog.objects.get_or_create(
                trip=trip,
                defaults={'start_time': timezone.now()}
            )
            if not created and not log.start_time:
                log.start_time = timezone.now()
                log.save()
            return JsonResponse({'message': 'Start time recorded'}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def end_trip(request, trip_id):
    if request.method == 'POST':
        try:
            trip = Trip.objects.get(id=trip_id)
            log = ELDLog.objects.get(trip=trip)
            log.end_time = timezone.now()
            log.driving_hours = (log.end_time - log.start_time).total_seconds() / 3600
            log.save()
            return JsonResponse({'message': 'End time recorded'}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def start_sleep(request, trip_id):
    if request.method == 'POST':
        try:
            trip = Trip.objects.get(id=trip_id)
            log = ELDLog.objects.get(trip=trip)
            if not log.sleep_start:
                log.sleep_start = timezone.now()
                log.save()
                return JsonResponse({'message': 'Sleep start recorded'}, status=200)
            else:
                return JsonResponse({'error': 'Sleep already in progress'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def end_sleep(request, trip_id):
    if request.method == 'POST':
        try:
            trip = Trip.objects.get(id=trip_id)
            log = ELDLog.objects.get(trip=trip)
            if log.sleep_start:
                log.sleep_end = timezone.now()
                log.sleep_duration = (log.sleep_end - log.sleep_start).total_seconds() / 3600
                log.save()
                return JsonResponse({'message': 'Sleep end recorded'}, status=200)
            else:
                return JsonResponse({'error': 'No sleep in progress'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def start_onduty(request, trip_id):
    if request.method == 'POST':
        try:
            trip = Trip.objects.get(id=trip_id)
            log = ELDLog.objects.get(trip=trip)
            if not log.onduty_start:
                log.onduty_start = timezone.now()
                log.save()
                return JsonResponse({'message': 'On-duty start recorded'}, status=200)
            else:
                return JsonResponse({'error': 'On-duty already in progress'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def end_onduty(request, trip_id):
    if request.method == 'POST':
        try:
            trip = Trip.objects.get(id=trip_id)
            log = ELDLog.objects.get(trip=trip)
            if log.onduty_start:
                log.onduty_end = timezone.now()
                log.onduty_duration = (log.onduty_end - log.onduty_start).total_seconds() / 3600
                log.save()
                return JsonResponse({'message': 'On-duty end recorded'}, status=200)
            else:
                return JsonResponse({'error': 'No on-duty in progress'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def start_offduty(request, trip_id):
    if request.method == 'POST':
        try:
            trip = Trip.objects.get(id=trip_id)
            log = ELDLog.objects.get(trip=trip)
            if not log.offduty_start:
                log.offduty_start = timezone.now()
                log.save()
                return JsonResponse({'message': 'Off-duty start recorded'}, status=200)
            else:
                return JsonResponse({'error': 'Off-duty already in progress'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def end_offduty(request, trip_id):
    if request.method == 'POST':
        try:
            trip = Trip.objects.get(id=trip_id)
            log = ELDLog.objects.get(trip=trip)
            if log.offduty_start:
                log.offduty_end = timezone.now()
                log.offduty_duration = (log.offduty_end - log.offduty_start).total_seconds() / 3600
                log.save()
                return JsonResponse({'message': 'Off-duty end recorded'}, status=200)
            else:
                return JsonResponse({'error': 'No off-duty in progress'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def get_resume(request, trip_id):
    if request.method == 'GET':
        try:
            trip = Trip.objects.get(id=trip_id)
            log = ELDLog.objects.get(trip=trip)

            # Example of formatted data for the chart
            data = []

            if log.offduty_duration > 0:
                data.append({
                    'type': 'off',
                    'start': log.offduty_start.hour,
                    'duration': log.offduty_duration
                })

            if log.sleep_duration > 0:
                data.append({
                    'type': 'sleep',
                    'start': log.sleep_start.hour,
                    'duration': log.sleep_duration
                })

            if log.driving_hours > 0:
                data.append({
                    'type': 'driving',
                    'start': log.start_time.hour,
                    'duration': log.driving_hours
                })

            if log.onduty_duration > 0:
                data.append({
                    'type': 'on',
                    'start': log.onduty_start.hour,
                    'duration': log.onduty_duration
                })

            return JsonResponse(data, safe=False)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Method not allowed'}, status=405)