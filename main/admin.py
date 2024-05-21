from django.contrib import admin
<<<<<<< HEAD
from .models import Trip, TripDetail


# Register your models here.

class TripAdmin(admin.ModelAdmin):
    list_display = ('origin', 'destination', 'date_created')
    list_filter = ('date_created',)
    search_fields = ('origin', 'destination')

admin.site.register(Trip)
admin.site.register(TripDetail)
=======
from .models import StationInfo, AccessibleStation, AllStation
# from .models import AccessibilityStation

# Register your models here.

class StationInfoAdmin(admin.ModelAdmin):
    list_display = ['start_station', 'end_station', 'transfer_stations', 'bus_stations']

class AccessibleStationAdmin(admin.ModelAdmin):
    list_display = ('station_name', 'line')
    search_fields = ('station_name', 'line')

class AllStationAdmin(admin.ModelAdmin):
    list_display = ('station_id', 'station_name', 'line')
    search_fields = ('station_name', 'line')

admin.site.register(StationInfo, StationInfoAdmin)
# admin.site.register(AccessibilityStation)
admin.site.register(AllStation, AllStationAdmin)
admin.site.register(AccessibleStation, AccessibleStationAdmin)
>>>>>>> 9a26a7e (Connected backend to frontend)
