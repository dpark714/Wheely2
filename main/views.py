from django.shortcuts import render, redirect
from .form.forms import TripForm 
from .models import Trip
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import TripDetail
import json
import requests
from django.conf import settings
from .models import TripDetail

# Create your views here.
def index(request):
    return render(request, 'main/index.html')

def map(request):
    context = {}
    context['form'] = TripForm()
    return render(request, 'main/map.html', context)

def login(request):
    return render(request, 'auth/login.html')

def signup(request):
    return render(request, 'auth/signup.html')

def contact_us(request):
    return render(request, 'contact_us.html')

def news_press(request):
    return render(request, 'news_press.html')

def about_team(request):
    return render(request, 'about_team.html')


def save_Trip(request):
    if request.method == 'POST':
        form = TripForm(request.POST)
        if form.is_valid():
            Trip = form.save()
            return redirect('some-success-url')  
    else:
        form = TripForm()

    return render(request, 'your_template_name.html', {'form': form})


@csrf_protect
def save_trip_details(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            user_origin = data.get('origin')
            user_destination = data.get('destination')

            response = requests.get(
                'https://maps.googleapis.com/maps/api/directions/json',
                params={
                    'origin': user_origin,
                    'destination': user_destination,
                    'mode': 'transit', 
                    'key': settings.GOOGLE_MAPS_API_KEY
                }
            )
            directions = response.json()

            if directions['status'] == 'OK':
                for route in directions['routes']:
                    for leg in route['legs']:
                        start_station = leg['start_address']
                        end_station = leg['end_address']

                       
                        for step in leg['steps']:
                            if step['travel_mode'] == 'TRANSIT':
                                transit_details = step['transit_details']
                                departure_stop = transit_details['departure_stop']['name']
                                arrival_stop = transit_details['arrival_stop']['name']


                                StationInfo.objects.create(
                                    start_station=departure_stop,
                                    end_station=arrival_stop
                                )
                
                return JsonResponse({'status': 'success', 'message': 'Station details saved.'})
            else:
                return JsonResponse({'status': 'error', 'message': 'Unable to find route'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)