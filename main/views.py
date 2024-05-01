from django.shortcuts import render
from .form.forms import TripForm

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
    return render(request, 'request/contact_us.html')

def news_press(request):
    return render(request, 'news_press.html')

def about_team(request):
    return render(request, 'about_team.html')