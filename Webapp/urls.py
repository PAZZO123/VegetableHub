from django.urls import path

from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('map/',views.map,name='map'),
    path('about/',views.about,name='about'),
     path('login-user/',views.loginUser,name='login-user'),
     path('login-admin/',views.loginAdmin,name='login-admin'),
     path('app-person/',views.application_personal,name='app-person'),
     path('app-farm/',views.application_farm,name='app-farm'),
     path('user/<str:pk>/',views.userPage,name='user'),
     path('app-success/',views.application_success,name='app-success'),
     path('admins/',views.adminDashboard,name='admins'),
     path('update-status/<int:application_id>/<str:status>/', views.update_status, name='update_status'),
     path('approve/', views.process_approved_applications, name='approve'),
     path('add-user/', views.adminAdd , name='add-user'),
     path('view-user/', views.adminView , name='view-user'),
     path('view-history/', views.adminHistory , name='view-history'),
     path('view-member/', views.adminRequest , name='view-member'),
     path('delete/<int:pk>/', views.deletem, name='delete'),
     path('register_user/', views.register_user, name='register_user'),
     path('add-profile/', views.adminProfile, name='add-profile'),
     path('fetch-admin/', views.fetch_users, name='fetch-admin'),
     path('help/<int:pk>/', views.Help, name='help'),
     path('changep/<int:pk>/', views.ChangePassowrd, name='changep'),
     path('view_profile/<int:pk>/', views.ViewUserprofile, name='view_profile'),
     path('contactf/<int:pk>/', views.ContactFarmer, name='contactf'),
     

]