from django import forms

class TripForm(forms.Form):
    origin = forms.CharField(max_length=100, label='Origin', widget=forms.TextInput(attrs={'placeholder': 'Type your starting location'}))
    destination = forms.CharField(max_length=100, label='Destination', widget=forms.TextInput(attrs={'placeholder': 'Type your destination'}))

class SignupForm(forms.Form):
    first_name = forms.CharField(label='First Name', max_length=100, required=True)
    last_name = forms.CharField(label='Last Name', max_length=100, required=True)
    email = forms.EmailField(label='Email Address', max_length=100, required=True)
    password = forms.CharField(label='Password', widget=forms.PasswordInput, required=True)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput, required=True)

    def clean(self):
            cleaned_data = super().clean()
            password = cleaned_data.get('password')
            password2 = cleaned_data.get('password2')
            
            if password != password2:
                raise forms.ValidationError("Passwords do not match.")