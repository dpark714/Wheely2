from django.shortcuts import render, redirect
from .form.forms import TripForm, SignupForm

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

import json
import requests
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail

from .models import StationInfo
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse
from .models import AccessibleStation, AllStation,  SearchHistory
# from .models import AccessibilityStation
import logging
from django.views.decorators.csrf import csrf_exempt, csrf_protect

logger = logging.getLogger(__name__)


def index(request):
    return render(request, 'main/index.html')

def map(request):
    context = {}
    context['form'] = TripForm()
    return render(request, 'main/map.html', context)

def user_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('/profile/')
        else:
            return render(request, 'auth/login.html', {'error_message': 'Invalid email or password'})
    return render(request, 'auth/login.html')

def logout_view(request):
    logout(request)
    return redirect('/')

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            # Extract form data
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            # Create and save the user
            user = User.objects.create_user(username=email, email=email, password=password)
            user.first_name = first_name
            user.last_name = last_name
            user.save()

            return redirect('/login/')
    else:
        form = SignupForm()
    return render(request, 'auth/signup.html', {'form': form})

def contact_us(request):
    # if request.method == 'POST':
    #     first_name = request.POST.get('firstName')
    #     last_name = request.POST.get('lastName')
    #     email = request.POST.get('email')
    #     message = request.POST.get('message')

    #     #sending email to admin
    #     subject = 'Contact Us Submission'
    #     message_body = f'Submission: \n\nName: {first_name} {last_name}\nEmail: {email}\nMessage:{message}'
    #     sender_email = email
    #     recipient_email = 'dpark000@citymail.cuny.edu'
    #     send_mail(subject, message_body, sender_email, [recipient_email])

    #     return render(request, 'confirm.html')
    return render(request, 'contact_us.html')

def about_wheely(request):
    return render(request, 'about_wheely.html')

def about_team(request):
    return render(request, 'about_team.html')

@login_required
def profile(request):
    return render(request, 'auth/profile.html')

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import SearchHistory

@login_required
def delete_history(request):
    if request.method == 'POST':
        selected_histories = request.POST.getlist('selected_histories')
        if selected_histories:
            SearchHistory.objects.filter(id__in=selected_histories, user=request.user).delete()
    return redirect('profile') 


def accessible_station_list(request):
    stations = AccessibleStation.objects.all()
    return render(request, 'accessible_station_list.html', {'stations': stations})

def all_station_list(request):
    stations = AllStation.objects.all()
    return render(request, 'all_station_list.html', {'stations': stations})

logger = logging.getLogger(__name__)


@require_http_methods(["POST"])
def station_info(request):
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
            transfer_stations = []
            bus_stations = []

            for route in directions['routes']:
                for leg in route['legs']:
                    for step in leg['steps']:
                        if step['travel_mode'] == 'TRANSIT':
                            transit_details = step['transit_details']
                            departure_stop = transit_details['departure_stop']['name']
                            arrival_stop = transit_details['arrival_stop']['name']
                            vehicle_type = transit_details['line']['vehicle']['type']

                            if vehicle_type == 'SUBWAY':
                                transfer_stations.append(departure_stop)
                                transfer_stations.append(arrival_stop)

                            elif vehicle_type == 'BUS':
                                bus_stations.append(departure_stop)
                                bus_stations.append(arrival_stop)

                                if 'intermediate_stops' in transit_details:
                                    for stop in transit_details['intermediate_stops']:
                                        bus_stations.append(stop['name'])

                            logger.debug(f"Added {vehicle_type} stops: {departure_stop}, {arrival_stop}")

            StationInfo.objects.create(
                start_station=user_origin,
                end_station=user_destination,
                transfer_stations=transfer_stations,
                bus_stations=bus_stations,
            )

            SearchHistory.objects.create(
                user=request.user,
                origin=user_origin,
                destination=user_destination
            )

            # Check accessibility for origin and destination stops of each leg
            legs_accessibility = []
            for route in directions['routes']:
                for leg in route['legs']:
                    leg_info = {
                        'start_station': user_origin,
                        'end_station': user_destination,
                        'steps': []
                    }
                    for step in leg['steps']:
                        if step['travel_mode'] == 'TRANSIT':
                            transit_details = step['transit_details']
                            departure_stop = transit_details['departure_stop']['name']
                            arrival_stop = transit_details['arrival_stop']['name']

                            departure_accessible = AccessibleStation.objects.filter(station_name=departure_stop).exists()
                            arrival_accessible = AccessibleStation.objects.filter(station_name=arrival_stop).exists()
                            
                            leg_info['steps'].append({
                                'departure_stop': departure_stop,
                                'arrival_stop': arrival_stop,
                                'departure_accessible': departure_accessible,
                                'arrival_accessible': arrival_accessible
                            })
                    legs_accessibility.append(leg_info)

            return JsonResponse({
                'status': 'OK',
                'directions': directions,
                'legs_accessibility': legs_accessibility
            })
        else:
            logger.error("Google Maps API error: " + directions['status'])
            return JsonResponse({'status': 'error', 'message': 'Unable to find route'})
    except json.JSONDecodeError as e:
        return JsonResponse({'error': 'Invalid JSON data', 'message': str(e)}, status=400)
    except Exception as e:
        logger.exception("Exception in station_info:")
        return JsonResponse({'status': 'error', 'message': str(e)})

    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)

