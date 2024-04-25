from django import forms

class TripForm(forms.Form):
    origin = forms.CharField(max_length=100, label='Origin', widget=forms.TextInput(attrs={'placeholder': 'Type your starting location'}))
    destination = forms.CharField(max_length=100, label='Destination', widget=forms.TextInput(attrs={'placeholder': 'Type your destination'}))
