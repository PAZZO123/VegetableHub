from django import forms

from .models import Application


class PersonalInfoForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['first_name', 'last_name', 'telephone', 'email', 'location']
        
class FarmInfoForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['gps_coordinates', 'farm_size', 'description', 'growth_stage', 'production','farm_image']