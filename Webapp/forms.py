from django import forms

from .models import Application,Farm,Farmer,Register


class PersonalInfoForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['first_name', 'last_name', 'telephone', 'email', 'location']
        
class FarmInfoForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['latitude', 'longitude','farm_size', 'description', 'growth_stage', 'production','farm_image']
        
class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = Register
        fields = ["Names", "email", "phone"]

class FarmerUpdateForm(forms.ModelForm):
    class Meta:
        model = Farmer
        fields = ["location","email"]

class FarmUpdateForm(forms.ModelForm):
    class Meta:
        model = Farm
        fields = ["Vegetable_type", "area_size"]        