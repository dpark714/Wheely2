from django.urls import path
from .views import *

urlpatterns = [
    path('', index),
    path('map/', map, name='map'),
    path('login/', login, name='login'),
    path('signup/', signup, name='signup'),
    path('contact_us', contact_us, name='contact_us'),
    path('news_press/', news_press, name='news_press'),
    path('about_team/', about_team, name='about_team')
]