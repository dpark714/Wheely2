from django.contrib import admin
from .models import Trip, TripDetail





# Register your models here.

class TripAdmin(admin.ModelAdmin):
    list_display = ('origin', 'destination', 'date_created')
    list_filter = ('date_created',)
    search_fields = ('origin', 'destination')

admin.site.register(Trip)
admin.site.register(TripDetail)