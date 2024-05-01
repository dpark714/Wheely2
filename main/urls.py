from django.urls import path
from .views import *
from . import views
from .views import save_trip_details


urlpatterns = [
    path('', index),
    path('map/', map, name='map'),
    path('login/', login, name='login'),
    path('signup/', signup, name='signup'),
    path('contact_us', contact_us, name='contact_us'),
    path('news_press/', news_press, name='news_press'),
    path('about_team/', about_team, name='about_team'),
    path('save-trip/', views.save_Trip, name='save_Trip'),
    path('save-trip-details/', save_trip_details, name='save_trip_details'),
]