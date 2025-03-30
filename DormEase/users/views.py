from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.views import View
from django.urls import reverse_lazy
from django.views.generic import TemplateView

from . import models, forms

# Create your views here.

User = get_user_model()

# Resident Assistant Dashboard View
class RADashboardView(LoginRequiredMixin, View):
    def get(self, request):
        residents = models.CustomUser.objects.filter(role='resident')
        rooms = models.Room.objects.all()
        return render(request, 'users/dashboard.html', {'residents': residents, 'rooms': rooms})


# Resident Registration View
class ResidentRegistrationView(View):

    def get(self, request):
        form = forms.ResidentRegistrationForm()
        return render(request, 'users/register.html', {'form': form})
    
    def post(self, request):
        form = forms.ResidentRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.role = 'resident'
            user.save()

            messages.success(request, 'Registration successful! Please log in.')
            return redirect('login')
        return render(request, 'users/register.html', {'form': form})

# Room Assignment API View
class RoomAssignmentView(View):

    def get(self, request):
        residents = models.CustomUser.objects.filter(role='resident', assigned_room=None)
        rooms = models.Room.objects.all()
        return render(request, 'users/assign_room.html', {'residents': residents, 'rooms': rooms})

    def post(self, request):
        resident_id = request.POST.get('resident_id')
        room_id = request.POST.get('room_id')
        resident = models.CustomUser.objects.get(id=resident_id)
        room = models.Room.objects.get(id=room_id)
        
        if not room.is_full():
            room.occupants.add(resident)
            return redirect('ra-dashboard')
        return render(request, 'users/assign_room.html', {'error': 'Room is full'})

# Login View
class CustomLoginView(LoginView):
    template_name = 'users/login.html'
    redirect_authenticated_user = True  # Redirect users if they are already logged in
    next_page = reverse_lazy('ra-dashboard')  # Redirect to the dashboard after login'

class HomeView(TemplateView):
    template_name = 'users/home.html'