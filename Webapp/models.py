from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.core.validators import EmailValidator, RegexValidator
from django.db import models


class Farmer(models.Model):
    farmer_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    telephone = models.CharField(max_length=13)
    email = models.CharField(max_length=50)
    location = models.CharField(max_length=255)
    user=models.ForeignKey(User, on_delete=models.CASCADE, related_name='farmers')
    Vegetable_type=models.CharField(max_length=20, default='Carrot')
    def __str__(self):
            return f"{self.first_name} {self.last_name} ({self.email})" 



class Farm(models.Model):
    farm_id = models.AutoField(primary_key=True)
    farm_name = models.CharField(max_length=255)
    latitude = models.FloatField(default=-1.9441)  # Default to Kigali latitude
    longitude = models.FloatField(default=30.0619)  # Default to Kigali longitude
    area_size = models.FloatField()
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE, related_name='farms')
    user=models.ForeignKey(User, on_delete=models.CASCADE, related_name='farm')
    Vegetable_type=models.CharField(max_length=20, default='Carrot')
    farm_image=models.ImageField(null=True,default="th1.jpeg")
    def __str__(self):
        return f"{self.farm_name} {self.area_size} - {self.Vegetable_type} (Lat: {self.latitude}, Long: {self.longitude})"

from django.contrib.auth.models import User
from django.core.validators import EmailValidator, RegexValidator
from django.db import models


class Application(models.Model):
    application_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    telephone = models.CharField(
        max_length=15, 
        validators=[RegexValidator(r'^\+?\d{10,15}$', message="Enter a valid phone number.")]
    )
    email = models.EmailField(validators=[EmailValidator()])
    location = models.CharField(max_length=255)
    latitude = models.FloatField(default=-1.9441)  # Default to Kigali latitude
    longitude = models.FloatField(default=30.0619)  # Default to Kigali longitude
    farm_size = models.FloatField()
    description = models.TextField()
    growth_stage = models.CharField(max_length=30)
    status = models.CharField(max_length=20, default='Pending')
    production = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically set on creation
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True,default="Mbabazi")
    Vegetable_type = models.CharField(max_length=20, default='Carrot')
    farm_image = models.ImageField(null=True, default="th1.jpeg")

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.status}"


    



class Vegatable_Practice(models.Model):
    practice_id = models.AutoField(primary_key=True)
    stage = models.CharField(max_length=100)
    description = models.TextField()
    media_url = models.URLField(blank=True, null=True)
    Vegetable_type=models.CharField(max_length=20, default='Carrot')
    user=models.ForeignKey(User, on_delete=models.CASCADE, related_name='carrot', default=1)



class Smart_Irrigation(models.Model):
    irrigation_id = models.AutoField(primary_key=True)
    farm = models.ForeignKey('Farm', on_delete=models.CASCADE, related_name='irrigations')
    water_usage = models.FloatField()
    irrigation_date = models.DateField()
    soil_moisture_level = models.FloatField()
    sensor_status = models.CharField(max_length=50)
    Vegetable_type=models.CharField(max_length=20, default='Carrot')




class Disease_Detection(models.Model):
    detection_id = models.AutoField(primary_key=True)
    farm_id = models.ForeignKey('Farm', on_delete=models.CASCADE, related_name='detections')
    disease_type = models.CharField(max_length=100)
    detection_date = models.DateField()
    recommendation = models.TextField()
    detection_status = models.CharField(max_length=50)
    Vegetable_type=models.CharField(max_length=20, default='Carrot')



class Harvest(models.Model):
    harvest_id = models.AutoField(primary_key=True)
    farm_id = models.ForeignKey('Farm', on_delete=models.CASCADE, related_name='harvests')
    harvest_date = models.DateField()
    quantity = models.FloatField()
    quality_rating = models.IntegerField()
    Vegetable_type=models.CharField(max_length=20, default='Carrot')




class AI_Harvest_Sorting(models.Model):
    sorting_id = models.AutoField(primary_key=True)
    harvest = models.ForeignKey('Harvest', on_delete=models.CASCADE, related_name='sortings')
    quality_score = models.FloatField()
    sorted_date = models.DateField()
    selected_for_export = models.BooleanField(default=False)
    Vegetable_type=models.CharField(max_length=20, default='Carrot')



class Storage(models.Model):
    storage_id = models.AutoField(primary_key=True)
    location = models.CharField(max_length=255)
    capacity = models.FloatField()
    farm_id = models.ForeignKey('Farm', on_delete=models.CASCADE, related_name='storages')
    Vegetable_type=models.CharField(max_length=20, default='Carrot')




class IoT_Monitoring(models.Model):
    monitoring_id = models.AutoField(primary_key=True)
    storage_id = models.ForeignKey('Storage', on_delete=models.CASCADE, related_name='monitorings')
    temperature = models.FloatField()
    humidity = models.FloatField()
    monitoring_date = models.DateField()
    alert_status = models.CharField(max_length=50)
    Vegetable_type=models.CharField(max_length=20, default='Carrot')
    
    
class Register(models.Model):
     user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
     Names=models.CharField(max_length=255)
     email=models.EmailField(validators=[EmailValidator()])
     phone = models.CharField(
        max_length=15, 
        validators=[RegexValidator(r'^\+?\d{10,15}$', message="Enter a valid phone number.")]
       )
     password = models.CharField(max_length=128)  # Store hashed password
def save(self, *args, **kwargs):
    # Hash only if the password is not already hashed
    if not self.password.startswith('pbkdf2_'):
        self.password = make_password(self.password)
    super().save(*args, **kwargs)

    

# class Vegetable(models.Model):
#      vegetable_id= models.AutoField(primary_key=True)
#      Vegetable_type=models.CharField(max_length=20, default='Carrot')