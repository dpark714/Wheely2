from django.urls import path
from .views import *
from . import views
from .views import save_trip_details


urlpatterns = [
    path('', index),
    path('map/', map, name='map'),
    path('login/', user_login, name='login'),
    path('logout/', logout_view, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('contact_us/', contact_us, name='contact_us'),
    path('about_wheely/', about_wheely, name='about_wheely'),
    path('profile/', views.profile, name='profile'),
    path('save-trip/', views.save_Trip, name='save_Trip'),
    path('save-trip-details/', save_trip_details, name='save_trip_details'),
]