from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.utils.timezone import now
from Webapp.models import Application, Farm, Farmer

from .forms import FarmInfoForm, PersonalInfoForm
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
                gps_coordinates=application.gps_coordinates or "Not Provided",
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
    applications = Application.objects.filter(status="Processed")  # Adjust filter as needed
    context = {
        "applications": applications
    }
 
    return render(request,'Webapp/home.html',context)
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
                return redirect('user')  # Redirect to user dashboard or another page
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

def userPage(request):
    return render(request,'Webapp/userdashboard.html')

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

 