from django.contrib import admin

from .models import (AI_Harvest_Sorting, Application, Disease_Detection, Farm,
                     Farmer, Harvest, IoT_Monitoring, Register,
                     Smart_Irrigation, Storage, Vegatable_Practice)


@admin.register(Farmer)
class FarmerAdmin(admin.ModelAdmin):
    list_display = ('farmer_id', 'first_name', 'last_name', 'telephone', 'email', 'location','user')

@admin.register(Farm)
class FarmAdmin(admin.ModelAdmin):
    list_display = ('farm_id', 'farm_name', 'latitude','longitude', 'area_size', 'farmer', 'user','Vegetable_type','farm_image')

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('application_id', 'first_name', 'last_name', 'telephone', 'email', 
                    'location', 'latitude','longitude', 'farm_size', 'description', 
                    'growth_stage', 'status', 'production', 'created_at','farm_image','user','Vegetable_type')

@admin.register(Vegatable_Practice)
class CarrotPracticeAdmin(admin.ModelAdmin):
    list_display = ('practice_id', 'stage', 'description', 'media_url','user','Vegetable_type')

@admin.register(Smart_Irrigation)
class SmartIrrigationAdmin(admin.ModelAdmin):
    list_display = ('irrigation_id', 'farm', 'water_usage', 'irrigation_date', 
                    'soil_moisture_level', 'sensor_status')

@admin.register(Disease_Detection)
class DiseaseDetectionAdmin(admin.ModelAdmin):
    list_display = ('detection_id', 'farm_id', 'disease_type', 'detection_date', 
                    'recommendation', 'detection_status')

@admin.register(Harvest)
class HarvestAdmin(admin.ModelAdmin):
    list_display = ('harvest_id', 'farm_id', 'harvest_date', 'quantity', 'quality_rating')

@admin.register(AI_Harvest_Sorting)
class AIHarvestSortingAdmin(admin.ModelAdmin):
    list_display = ('sorting_id', 'harvest', 'quality_score', 'sorted_date', 'selected_for_export')

@admin.register(Storage)
class StorageAdmin(admin.ModelAdmin):
    list_display = ('storage_id', 'location', 'capacity', 'farm_id')

@admin.register(IoT_Monitoring)
class IoTMonitoringAdmin(admin.ModelAdmin):
    list_display = ('monitoring_id', 'storage_id', 'temperature', 'humidity', 'monitoring_date', 'alert_status')

@admin.register(Register)
class RegisterAdmin(admin.ModelAdmin):
    list_display = ('Names', 'email', 'phone', 'password','user')
