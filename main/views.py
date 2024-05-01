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


@csrf_exempt
def save_trip_details(request):
        if request.method == 'POST':
            user_origin = request.POST.get('origin')
            user_destination = request.POST.get('destination')

           
            response = requests.get(
                'https://maps.googleapis.com/maps/api/directions/json',
                params={
                    'origin': user_origin,
                    'destination': user_destination,
                    'key': settings.GOOGLE_MAPS_API_KEY
                }
            )
            directions = response.json()


            if directions['status'] == 'OK':
                real_origin = directions['routes'][0]['legs'][0]['start_address']
                real_destination = directions['routes'][0]['legs'][0]['end_address']

               
                TripDetail.objects.create(
                    origin=real_origin,
                    destination=real_destination
                )
                return JsonResponse({'status': 'success', 'origin': real_origin, 'destination': real_destination})
            else:
                return JsonResponse({'status': 'error', 'message': 'Unable to find route'})

        return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)