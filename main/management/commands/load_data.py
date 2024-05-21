import pandas as pd
from django.core.management.base import BaseCommand
from main.models import AccessibleStation, AllStation
# from main.models import AccessibilityStation
from django.conf import settings

class Command(BaseCommand):
    help = 'Loads data from an Excel file into the AccessibilityStation model'

    def handle(self, *args, **options):
        self.load_accessible_stations()
        self.load_all_stations()


    def load_accessible_stations(self):
        excel_path =  settings.BASE_DIR / 'main/static/excel/Accessible_MTA_Stations.xlsx'
        data = pd.read_excel(excel_path)

        for _, row in data.iterrows():
            AccessibleStation.objects.create(
                station_name=row['Station'],
                line=row['Lines'],
        )
        self.stdout.write(self.style.SUCCESS(f'Successfully added {row["Station"]}'))

    def load_all_stations(self):
        csv_path =  settings.BASE_DIR / 'main/static/excel/All Station.csv'
        data = pd.read_csv(csv_path)

        for _, row in data.iterrows():
            AllStation.objects.create(
                station_id=row['Station ID'],
                station_name=row['Station'],
                line=row['Lines'],
            )
            self.stdout.write(self.style.SUCCESS(f'Successfully added {row["Station"]}'))