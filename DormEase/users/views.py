from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.views import View
from django.urls import reverse
from django.views.generic import TemplateView

from . import models, forms

# Create your views here.

User = get_user_model()

# RA Dashboard View with check-in functionality
class RADashboardView(LoginRequiredMixin, View):
    def get(self, request):
        residents = models.CustomUser.objects.filter(role='resident')
        rooms = models.Room.objects.all()
        checkin_forms = {resident.id: forms.CheckInForm(instance=resident) for resident in residents}
        return render(request, 'users/dashboard.html', {
            'residents': residents,
            'rooms': rooms,
            'checkin_forms': checkin_forms
        })

    def post(self, request):
        resident_id = request.POST.get('resident_id')
        resident = models.CustomUser.objects.get(id=resident_id)
        form = forms.CheckInForm(request.POST, instance=resident)
        if form.is_valid():
            form.save()
        return redirect('ra-dashboard')

# Resident Dashboard View
class ResidentDashboardView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        if user.role != 'resident':
            return redirect('ra-dashboard')
        room = user.assigned_room
        return render(request, 'users/resident_dashboard.html', {'user': user, 'room': room})


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

# Room Assignment View
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
    redirect_authenticated_user = True

    def get_success_url(self):
        user = self.request.user
        if user.role == 'resident':
            return reverse('resident-dashboard')
        elif user.role == 'ra':
            return reverse('ra-dashboard')
        else:
            return reverse('home')  # fallback in case of undefined role

# Home View
class HomeView(TemplateView):
    template_name = 'users/home.html'

# Password Reset View
class PasswordResetView(TemplateView):
    template_name = 'users/password_reset.html'

