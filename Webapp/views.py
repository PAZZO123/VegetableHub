from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.models import User
from django.db import transaction
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.timezone import now
from Webapp.models import Application, Farm, Farmer

from .forms import (FarmerUpdateForm, FarmInfoForm, FarmUpdateForm,
                    PersonalInfoForm, UserUpdateForm)
from .models import Application, Register


def process_approved_applications(request):
    approved_applications = Application.objects.filter(status="Approved")

    for application in approved_applications:
        with transaction.atomic():
            farmer = Farmer.objects.create(
                first_name=application.first_name,
                last_name=application.last_name,
                telephone=application.telephone,
                email=application.email,
                location=application.location,
                user=application.user,
            )

            farm = Farm.objects.create(
                farm_name=f"{farmer.first_name}'s Farm",
                latitude=application.latitude or "Not Provided",
                longitude=application.longitude or "Not Provided",
                area_size=application.farm_size,
                farmer=farmer,
                user=application.user,
            )
            farm.save()
            application.status = "Processed"
            application.save()

    return HttpResponse("Approved applications have been processed into Farmers and Farms.")

def application_personal(request):
    if request.method == 'POST':
        form = PersonalInfoForm(request.POST)
        if form.is_valid():
            # Save personal info in the session temporarily
            request.session['app-person'] = form.cleaned_data
            return redirect('app-farm')  # Redirect to the next step
    else:
        form = PersonalInfoForm()
    return render(request, 'Webapp/application_personal.html', {'form': form})

def application_farm(request):
    if request.method == 'POST':
        form = FarmInfoForm(request.POST)
        if form.is_valid():
            personal_info = request.session.get('app-person', {})
            if not personal_info:
                return redirect('app-person')  # Go back if session data is missing

            # Combine the data from both steps
            combined_data = {**personal_info, **form.cleaned_data}
            Application.objects.create(**combined_data)  # Save to the database

            # Clear the session data after saving
            del request.session['app-person']
            return redirect('app-success')  # Redirect to a success page
    else:
        form = FarmInfoForm()
    return render(request, 'Webapp/application_farm.html', {'form': form})


def home(request):
    query = request.GET.get('query', '')  # Get the search query from the request
    if query:
        # Filter applications based on location (case-insensitive)
        applications = Application.objects.filter(location__icontains=query, status="Processed")
    else:
        # Default to showing the first 6 processed applications
        applications = Application.objects.filter(status="Processed")[:6]

    context = {
        "applications": applications,  # Pass applications to the template
        "query": query  # Pass the search query to keep it in the search box
    }
    
    return render(request, 'Webapp/home.html', context)

def contact(request):
    return render(request,'Webapp/contact.html',{})
def about(request):
    return render(request,'Webapp/about.html',{})
def loginUser(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        
        try:
            # Get the user based on the email
            user = Register.objects.get(email=email)
            
            # Check if the password matches
            if check_password(password, user.password):
                return redirect('user',pk=user.pk)  # Redirect to user dashboard or another page
            else:
                messages.error(request, "Invalid email or password.")  # Add error message
        except Register.DoesNotExist:
            messages.error(request, "Invalid email or password.")  # Add error message

    return render(request, 'Webapp/user_login.html')

def loginAdmin(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        # Authenticate the user
        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)  # Log the user in
            # Check if the user is a superuser and redirect accordingly
            if user.is_superuser:
                return redirect('admins')  # Replace 'admins' with your admin dashboard URL name
            else:
                return redirect('login-user')  # Replace 'login-user' with your farmer dashboard URL name
        else:
            return render(request, 'Webapp/admin_login.html', {'error': 'Invalid email or password'})

    return render(request, 'Webapp/admin_login.html')

def userPage(request,pk):
    users=Register.objects.all()
    user = get_object_or_404(Register, pk=pk)
    
 
     # Filter farmers whose email matches the logged-in user's email
    farmers = Farmer.objects.filter(email=user.email)

    # Filter farms associated with these farmers
    farms = Farm.objects.filter(farmer__email=user.email)
    context={'user':user,
             'farmers':farmers,
             'farms':farms,
             'now': now(),
             'users':users}
    return render(request,'Webapp/userdashboard.html',context)

def application_success(request):
    return render(request, 'Webapp/application_success.html', {'message': "Your application has been submitted successfully!"})

def adminDashboard(request):
    applications = Application.objects.filter(status="Pending")  # Adjust filter as needed
    context = {
        "applications": applications
    }

    return render(request, 'Webapp/admin_dashboard.html', context)

def update_status(request, application_id, status):
    try:
        application = Application.objects.get(application_id=application_id)

    except Application.DoesNotExist:
        return redirect('home')  # You can modify 'home' to any other page, such as an error page
    
    # Check if the status is valid
    if status in ['Approved', 'Rejected']:
        # Update the application status
        application.status = status
        application.save()  # Save the changes to the database

    return render(request, 'Webapp/admin_dashboard.html') 
def adminAdd(request):
    applications = Application.objects.filter(status="Pending")  # Adjust filter as needed
    context = {
        "applications": applications
    }

    return render(request, 'Webapp/admin_add.html', context)

def adminHistory(request):
    applications = Application.objects.all()  
    pending_count = Application.objects.filter(status='Pending').count()
    approved_count = Application.objects.filter(status='Processed').count()
    rejected_count = Application.objects.filter(status='Rejected').count()
    context = {
        "applications": applications,
        'pending_count': pending_count,
        'approved_count': approved_count,
        'rejected_count': rejected_count,
    }

    return render(request, 'Webapp/admin_history.html', context)

def adminView(request):
    applications = Application.objects.filter(status="Processed") 
    users=Register.objects.all()# Adjust filter as needed
    context = {
        "applications": applications,
        'users':users
        
    }

    return render(request, 'Webapp/admin_view_users.html', context)

def adminRequest(request):
    applications = Application.objects.filter(status="Pending")  # Adjust filter as needed
    context = {
        "applications": applications
    }

    return render(request, 'Webapp/membership_requests.html', context)



def deletem(request,pk):
    users=Register.objects.get(id=pk)
    
    if request.user !=users.user:
        return HttpResponse('You are not allowed Here!!')
    if request.method=='POST':
        users.delete()
        return redirect('home')
    return render(request, 'Webapp/delete.html',{'obj':users})


def register_user(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        # Validate passwords
        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('register_user')

        try:
            # Save the new user
            user = Register(
                Names=name,
                email=email,
                phone=phone,
                password=password , # This will be hashed in the model's save method
                user=request.user
            )
            user.save()
            messages.success(request, "User registered successfully!")
            return redirect('register_user')
        except Exception as e:
            messages.error(request, f"An error occurred: {e}")
            return redirect('register_user')

    return render(request, "Webapp/admin_add.html")
def adminProfile(request):
    users = User.objects.all()
    return render(request, 'Webapp/admin_profile.html',{'users': users,'now': now()} )


def fetch_users(request):
    # Fetch all users with the required fields
    users = User.objects.all()
    return render(request, 'Webapp/admin_profile.html', {'users': users})

def Help(request,pk):
    users=Register.objects.all()
    user = get_object_or_404(Register, pk=pk)
    
 
     # Filter farmers whose email matches the logged-in user's email
    farmers = Farmer.objects.filter(email=user.email)

    # Filter farms associated with these farmers
    farms = Farm.objects.filter(farmer__email=user.email)
    context={'user':user,
             'farmers':farmers,
             'farms':farms,
             'now': now(),
             'users':users}
    return render(request ,'Webapp/help_line.html',context )


def ChangePassowrd(request, pk):
    # Fetch the user and related data
    user = get_object_or_404(Register, pk=pk)
    farmers = Farmer.objects.filter(email=user.email)
    farms = Farm.objects.filter(farmer__email=user.email)
    users = Register.objects.all()

    context = {
        'user': user,
        'farmers': farmers,
        'farms': farms,
        'now': now(),
        'users': users,
    }

    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        # Check if the current password is correct
        if not check_password(current_password, user.password):
            messages.error(request, "Current password is incorrect.")
            return render(request, 'Webapp/change_password.html', context)

        # Check if the new password matches the confirmation
        if new_password != confirm_password:
            messages.error(request, "New password and confirmation do not match.")
            return render(request, 'Webapp/change_password.html', context)

        # Update the user's password
        user.password = make_password(new_password)
        user.save()
        messages.success(request, "Password changed successfully!")
        return render(request, 'Webapp/change_password.html', context)

    # Render the form for GET requests
    return render(request, 'Webapp/change_password.html', context)


def ViewUserprofile(request, pk):
    # Fetch the user from the Register model
    user = get_object_or_404(Register, pk=pk)

    # Get all users, farmers, and farms associated with the current user
    users = Register.objects.all()
    farmers = Farmer.objects.filter(email=user.email)
    farms = Farm.objects.filter(farmer__email=user.email)

    if request.method == 'POST':
        # Create forms for Register, Farmer, and Farm models
        user_form = UserUpdateForm(request.POST, instance=user)
        farmer_forms = [FarmerUpdateForm(request.POST, instance=farmer) for farmer in farmers]
        farm_forms = [FarmUpdateForm(request.POST, instance=farm) for farm in farms]

        # Validate all forms
        if (
            user_form.is_valid() and
            all(farmer_form.is_valid() for farmer_form in farmer_forms) and
            all(farm_form.is_valid() for farm_form in farm_forms)
        ):
            # Save updated user info
            user_form.save()

            # Update all farmers with the same email as the user
            for farmer_form in farmer_forms:
                farmer_form.save()

            # Update all farms associated with the farmers
            for farm_form in farm_forms:
                farm_form.save()

            # Show a success message and redirect to the profile page
            messages.success(request, "Profile updated successfully.")
            return redirect('user', pk=user.pk)
        else:
            # Show an error message if any of the forms are invalid
            messages.error(request, "Failed to update profile. Please check your input.")

    else:
        # Initialize forms with current user, farmer, and farm data
        user_form = UserUpdateForm(instance=user)
        farmer_forms = [FarmerUpdateForm(instance=farmer) for farmer in farmers]
        farm_forms = [FarmUpdateForm(instance=farm) for farm in farms]

    # Pass forms and other context data to the template
    context = {
        'user': user,
        'users': users,
        'farmers': farmers,
        'farms': farms,
        'now': now(),
        'user_form': user_form,
        'farmer_forms': farmer_forms,
        'farm_forms': farm_forms,
    }

    return render(request, 'Webapp/user_profile.html', context)


@login_required(login_url='login-user')
def ContactFarmer(request,pk):
    applications = Application.objects.filter(status="Processed",pk=pk) # Adjust filter as needed
    context = {
        "applications": applications
    }
   
    return render(request ,'Webapp/contact_farmer.html',context )

 
 
 
 
 

