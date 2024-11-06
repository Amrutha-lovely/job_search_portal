from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.views import LoginView as AuthLoginView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Job

# Custom Login View
class LoginView(AuthLoginView):
    template_name = 'jobs/login.html'

    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('available_jobs')  # Redirect to available jobs if login is successful
        else:
            messages.error(request, 'Invalid credentials or not registered. Please register first.')
            return render(request, self.template_name)

# Registration View
class RegisterView(View):
    def get(self, request):
        return render(request, 'jobs/register.html')  # Render the registration form

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        if password == confirm_password:
            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(username=username, password=password)
                user.save()
                login(request, user)  # Log in the user after successful registration
                return redirect('available_jobs')  # Redirect to available jobs after registration
            else:
                messages.error(request, "Username already exists.")
        else:
            messages.error(request, "Passwords do not match.")
        
        return render(request, 'jobs/register.html')  # Reload form if there was an error

class HomeView(View):
    def get(self, request):
        return render(request, 'jobs/home.html')

class AvailableJobsView(View):
    def get(self, request):
        jobs = Job.objects.all()  # Fetch all jobs from the database
        return render(request, 'jobs/available_jobs.html', {'jobs': jobs})

class ApplicationFormView(View):
    def get(self, request, job_id):
        return render(request, 'jobs/application_form.html', {'job_id': job_id})

    def post(self, request, job_id):
        # Handle form submission logic here
        return redirect('thank_you')  # Redirect to a thank you page after submission

class ContactView(View):
    def get(self, request):
        return render(request, 'jobs/contact.html')

class ThankYouView(View):
    def get(self, request):
        return render(request, 'jobs/thank_you.html')

# Logout View
def logout_view(request):
    logout(request)
    return redirect('login')  # Redirect to the login page after logout
