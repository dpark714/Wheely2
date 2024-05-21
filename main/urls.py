from django.urls import path
from .views import *
from . import views
<<<<<<< HEAD
from .views import save_trip_details
=======
from .views import station_info
# from .views import list_accessible_stations
>>>>>>> 9a26a7e (Connected backend to frontend)


urlpatterns = [
    path('', index),
    path('map/', map, name='map'),
    path('login/', user_login, name='login'),
    path('logout/', logout_view, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('contact_us/', contact_us, name='contact_us'),
    path('about_wheely/', about_wheely, name='about_wheely'),
    path('profile/', views.profile, name='profile'),
<<<<<<< HEAD
    path('save-trip/', views.save_Trip, name='save_Trip'),
    path('save-trip-details/', save_trip_details, name='save_trip_details'),
]
=======
    path('delete_history/', views.delete_history, name='delete_history'),
    path('station_info/', station_info, name='station_info'),
    # path('accessible-stations/', list_accessible_stations, name='accessible-stations'),
    path('accessible-stations/', views.accessible_station_list, name='accessible_station_list'),
    path('all-stations/', views.all_station_list, name='all_station_list')
]
>>>>>>> 9a26a7e (Connected backend to frontend)
