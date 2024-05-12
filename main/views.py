from django.shortcuts import render, redirect
from .form.forms import TripForm, SignupForm
from .models import Trip
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import TripDetail
import json
import requests
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.conf import settings

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