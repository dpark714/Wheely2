from django.contrib import admin
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